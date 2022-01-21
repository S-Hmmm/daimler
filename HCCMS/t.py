import datetime
import time

# import six

a = datetime.date.today().timetuple()
b = time.mktime(a)

c = datetime.datetime.fromtimestamp(b)
print(c)
print(datetime.datetime.strftime(c, '%Y-%m-%dT%H:%M:%S.%fZ'))
print(time.strftime('%Y-%m-%dT%H:%M:%S.000Z', a))
print(datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S.000Z'))