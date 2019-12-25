import sys
import os
import inspect
import datetime as dt

# def addSecs(tm, secs):
#     fulldate = dt.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
#     fulldate = fulldate + dt.timedelta(seconds=secs)
#     return fulldate.time()

# args = sys.argv

# if len(args) < 3:
#     print("Not enough arguments")
#     exit()

# seconds = int(args[2])
# in_path = os.path.realpath(args[1])
# out_path = os.path.realpath(in_path[:-4] + ' shift' + in_path[-4:])
# tformat = "%H:%M:%S,%f"

# with open(in_path, 'r') as input_file, open(out_path, 'w') as output_file:
#     for line in input_file:
#         if '-->' in line:
#             for time in line.split(' --> '):
#                 milli = time[:-3]
#                 time = addSecs(dt.datetime.strptime(time, tformat), seconds).strftime(tformat) + str(milli)
#             output_file.write(line)
#         else:
#             output_file.write(line)
for x in range(1000):
    a = int(x / 60)
    b = x % 60
    print(a, b)