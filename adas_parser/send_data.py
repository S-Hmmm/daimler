import json
import os
import re
from datetime import datetime as dt
import datetime
import logging

from pyspark import SparkContext as sc
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, input_file_name, col
from pyspark.sql.types import *
from fap5decoder import decode_r4r_incidents

logger = logging.getLogger(__name__)


@udf(returnType=StringType())
def parse_data(event_type, sensor_data, abs_path):
    file_path = _get_path(abs_path)
    send_data = {'eventtype': 'adas',
                 'url': file_path,
                 'positionlist': [
                     {
                         'positionAltitude': 0.0,
                         'positionLong': 0.0,
                         'positionLat': 0.0,
                     }
                 ]
                 }
    # histograms数据没有经纬度，不需要解析
    if event_type == 'incidents':
        try:
            send_data['positionlist'] = _get_incidents_gps_ls(bytes(sensor_data))
        except Exception as e:
            logger.error(e)
            pass

    send_data = json.dumps(send_data)
    return send_data


def _get_incidents_gps_ls(byte_data):
    decode_incidents = decode_r4r_incidents(byte_data, dt.now())
    gps_list = []
    if decode_incidents.get('decoding_exceptions'):
        return gps_list

    for incident in decode_incidents['incidents']:
        gps = {
            'positionAltitude': 0.0,
            'positionLong': incident.get('gps_raw_position').get('longitude'),
            'positionLat': incident.get('gps_raw_position').get('latitude'),
        }
        gps_list.append(gps)

    return gps_list


def _get_path(abs_path):
    try:
        pattern = '/FAP5.+parquet$'
        file_path = re.search(pattern, abs_path).group()

        return file_path
    except Exception as e:
        logger.error(e)
        return


OUTPUT_CONNECT_STRING = "spark.eventhub.output.connection.string"
OUTPUT_CHECKPOINT_LOCATION = "spark.checkpoint.location.output"

STORAGE_ACCOUNT = "spark.storage.account.name"
STORAGE_ACCOUNT_KEY = "spark.storage.account.key"
INCIDENTS_SAVE_PATH = "spark.incidents.save.path"


def run():
    spark = SparkSession.builder.getOrCreate()
    spark.conf.set('spark.sql.streaming.fileSink.log.cleanupDelay', '60000')
    conf = spark.sparkContext.getConf()
    output_checkpoint_location = conf.get(OUTPUT_CHECKPOINT_LOCATION)
    output_connect_string = conf.get(OUTPUT_CONNECT_STRING)
    incidents_path = conf.get(INCIDENTS_SAVE_PATH)

    # load data from storage
    p_schema = StructType([
        StructField("eventtype", StringType(), False),
        StructField("eventobject", StructType(
            [StructField("sensordata", BinaryType(), False),
             StructField("baumuster", StringType(), False)]
        ), False)])
    date = datetime.date.today()
    df = (
        spark.readStream.format("parquet")
        .schema(p_schema)
        .option('failOnDataLoss', 'false')
        .option('path', '%s/year=%s/month=%s/day=%s' % (incidents_path, date.year, date.month, date.day-1))
        .load()
        .withColumn('abs_path', input_file_name())
    )

    # send data to eventhub
    target_config = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(output_connect_string)
    target = {
        'eventhubs.connectionString': target_config,
    }

    result = (df.filter("abs_path is not null and abs_path != ''")
              .withColumn('body', parse_data(col('eventtype'),
                                             col('eventobject.sensordata'),
                                             col('abs_path'))))
    ds = (
        result.select('body')
        .writeStream.format("eventhubs")
        .trigger(once=True)
        .options(**target)
        .option('checkpointLocation', output_checkpoint_location)
        .start()
    )

    ds.awaitTermination()


if __name__ == '__main__':
    run()
