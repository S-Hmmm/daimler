import datetime
import time


a = datetime.date.today().timetuple()
b = time.mktime(a)

c = datetime.datetime.fromtimestamp(b)
print(c)
print(datetime.datetime.strftime(c, '%Y-%m-%dT%H:%M:%SZ'))
