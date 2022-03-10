import datetime
import json
import logging

from pyspark import SparkContext as sc
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

logger = logging.getLogger(__name__)


@udf(returnType=StringType())
def get_date(timestamp):
    return datetime.date.today().fromtimestamp(float(timestamp)).strftime('%Y-%m-%d')


INPUT_CONNECT_STRING = "spark.eventhub.input.connection.string"
INCIDENTS_CHECKPOINT_LOCATION = "spark.checkpoint.location.incidents"

STORAGE_ACCOUNT = "spark.storage.account.name"
STORAGE_ACCOUNT_KEY = "spark.storage.account.key"

INCIDENTS_SAVE_PATH = "spark.incidents.save.path"


def run():
    spark = SparkSession.builder.appName('adas_incidents').getOrCreate()
    spark.conf.set('spark.sql.streaming.fileSink.log.cleanupDelay', '60000')
    conf = spark.sparkContext.getConf()

    input_connect_string = conf.get(INPUT_CONNECT_STRING)
    storage_account_name = conf.get(STORAGE_ACCOUNT)
    storage_account_key = conf.get(STORAGE_ACCOUNT_KEY)
    incidents_checkpoint_location = conf.get(INCIDENTS_CHECKPOINT_LOCATION)
    incidents_save_path = conf.get(INCIDENTS_SAVE_PATH)

    config = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(input_connect_string)

    starting_event_position = {
        "offset": '-1',
        "seqNo": -1,  # not in use
        "enqueuedTime": None,  # not in use
        "isInclusive": True
    }

    eh_conf = {
        'eventhubs.connectionString': config,
        "eventhubs.startingPosition": json.dumps(starting_event_position)
    }

    schema = StructType([StructField("vin", StringType(), False),
                         StructField("eventclass", StringType(), False),
                         StructField("eventtype", StringType(), False),
                         StructField("eventts", LongType(), False),
                         StructField("eventversion", IntegerType(), False),
                         StructField("eventobject", StructType(
                             [StructField("sensordata", BinaryType(), False),
                              StructField("baumuster", StringType(), False)]
                         ), False)])

    # load data from eventhub
    df = (
        spark.readStream.format("eventhubs")
        .options(**eh_conf)
        .load()
        .selectExpr('cast(Body as string) as message')
        .select(from_json('message', schema=schema).alias('body'))
        .select('body.*')
        .withColumn('date', get_date(col('eventts')))
        .withColumn('year', year('date'))
        .withColumn('month', month('date'))
        .withColumn('day', dayofmonth('date'))
        # .withColumn('event_type', col('eventtype'))
    )

    # conf of save data
    save_conf = spark.sparkContext._jsc.hadoopConfiguration()
    save_conf.set("fs.wasbs.impl", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
    save_conf.set("mapreduce.output.fileoutputformat.outputdir", "/tmp")
    spark.conf.set("fs.azure.account.key.%s.blob.core.windows.net" % storage_account_name, storage_account_key)

    # incidents data save
    incidents_df = df.filter(df.eventtype == "incidents").drop('date')
    incidents = (
        incidents_df.coalesce(1).writeStream
        .partitionBy('year', 'month', 'day')
        .format('parquet')
        .option('maxRecordsPerFile', 1)
        .option('failOnDataLoss', False)
        .option('checkpointLocation', incidents_checkpoint_location)
        .option('path', incidents_save_path)
        .start()
    )

    incidents.awaitTermination()


if __name__ == '__main__':
    run()
