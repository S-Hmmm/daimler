from urllib3 import disable_warnings
import time
import datetime

from road_segment_ticket import RoadSegmentTicket


class OneStop(RoadSegmentTicket):
    def __init__(self, tk=None):
        super().__init__(tk_id=tk)

    def create_and_release(self, rt_info):
        self.create_ticket(rt_info)
        self.request_validate_ticket()
        self.approve_all_vl_tk()
        self.validate_ticket()
        self.release_ticket()


if __name__ == '__main__':
    disable_warnings()
    start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', datetime.date.today().timetuple())

    link_ls = [10006568]
    for link in link_ls:
        tk_info = {
            "streetName": str(link),
            "country": "CHN",
            "junctionStart": "1",
            "junctionEnd": "2",
            "description": "3",
            "mapVersion": "HDMap-NDS-2.5.4-China-Daimler;97",
            "clearanceStates": {"v1": "CLEARANCE"},  # NON_CLEARANCE, ACTIVATION
            "links": [{"id": link, "enabled": True}],  # 10001942 10001665 编译失败
            "startTime": start_time
        }
        OneStop().create_and_release(tk_info)
