from urllib3 import disable_warnings

from road_segment_ticket import RoadSegmentTicket


class OneStop(RoadSegmentTicket):

    def create_and_release(self, rt_info):
        self.create_ticket(rt_info)
        self.request_validate_ticket()
        self.approve_all_vl_tk()
        self.validate_ticket()
        self.release_ticket()


if __name__ == '__main__':
    disable_warnings()
    tk_info = {
        "streetName": "10003",
        "country": "CHN",
        "junctionStart": "1",
        "junctionEnd": "2",
        "description": "3",
        "mapVersion": "HDMap-NDS-2.5.4-China-Daimler;97",
        "clearanceStates": {"v1": "CLEARANCE"},  # NON_CLEARANCE, ACTIVATION
        "links": [{"id": 1, "enabled": True}],  # 10001942 编译失败
        "startTime": "2022-01-07T00:00:00.000Z"
    }
    OneStop().create_and_release(tk_info)
