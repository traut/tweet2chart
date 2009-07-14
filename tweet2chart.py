#!/usr/bin/evn python
# encoding: utf-8
#

import twitter
from GChartWrapper import *
from GChartWrapper.encoding import *
import re
from datetime import date

api = twitter.Api()
mark = "#nikeplus"

username = "Bad_Bam"

pattern = r'\s[\d]+[.,]?[\d]+\s'


statuses = api.GetUserTimeline(username, count=300)

values = {}

def merge(lst, res=[]):
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res

for s in statuses:
    if mark in s.text:
        print s.created_at_in_seconds, s.text
        #values[date.fromtimestamp(s.created_at_in_seconds)] = [int(value) for value in re.findall(pattern, s.text)]
        values[s.created_at_in_seconds] = [float(value) for value in re.findall(pattern, s.text)][0]

        

values.keys().sort()
vals = merge(values.values())

keys = values.keys()
keys.sort()
keys = [key for key in keys if values[key]]

print "keys", keys
print "values", vals



# encoder = Encoder(encoding="extended", scale=0.5)
# encoded_data = encoder.encode([values[k] for k in keys])

G = Line(merge([values[k] for k in keys]), encoding='text')
G.size(600,300)
G.axes('xy')
G.axes.label(0, *keys)
G.axes.label(1, max(vals))
G.legend(username)

print G