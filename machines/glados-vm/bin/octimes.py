#!/usr/bin/python
import sys
import math

""" To generate the input file
cat OC_cme | grep "ExecutionReport |" OC_cme.log | grep -v EXEC_TYPE_PENDING | sed -n 's/.*exec_type=\([A-Z_]*\).*time_sent=\([0-9]*\).*received_from_exchange=\([0-9]*\).*order_received_oc=\([0-9]*\).*time_sent_exchange=\([0-9]*\).*/\1,\2,\3/p' | python octimes.py

# the columns are: exec_type,order_received_time,time_sent_exchange
"""

outtotal = 0
outcount = 0
intotal = 0
incount = 0
outbound = []
inbound = []
for line in sys.stdin:
    parts = line.split(",")
    t = int(parts[4]) - int(parts[3])
    if t > 0 and t < 1000000:
        outbound.append(t)
        outtotal = outtotal + t
        outcount = outcount + 1
    t = int(parts[1]) - int(parts[2])
    if t > 0 and t < 1000000:
        inbound.append(t)
        intotal = intotal + t
        incount = incount + 1

#######  Process outbound
outbound.sort();
outbound = outbound[1:-1]
if outcount%2 == 0:
    median = (outbound[outcount/2] + outbound[outcount/2 + 1])/2
else:
    median = outbound[outcount/2]

avg = outtotal/outcount

outtotal = 0
outcount = 0

for d in outbound:
    outtotal = outtotal + (d-avg)**2
    outcount = outcount + 1

stddev = math.sqrt(outtotal/outcount)
print "Outbound"
print "samples: {0}".format(outcount)
print "median: {0}".format(median)
print "avg: {0}uS".format(avg)
print "min: {0}".format(outbound[0])
print "max: {0}".format(outbound[-1])
print "stddev: {0}".format(stddev)

#######  Process inbound
inbound.sort();
inbound = inbound[1:-1]
if incount%2 == 0:
    median = (inbound[incount/2] + inbound[incount/2 + 1])/2
else:
    median = inbound[incount/2]

avg = intotal/incount

intotal = 0
incount = 0

for d in inbound:
    intotal = intotal + (d-avg)**2
    incount = incount + 1

stddev = math.sqrt(intotal/incount)
print
print "Inbound"
print "samples: {0}".format(incount)
print "median: {0}".format(median)
print "avg: {0}uS".format(avg)
print "min: {0}".format(inbound[0])
print "max: {0}".format(inbound[-1])
print "stddev: {0}".format(stddev)
