#!/usr/bin/evn python
# encoding: utf-8
#

__author__ = "Sergey Polzunov"

import twitter
import re
import urllib
from datetime import datetime
import gviz_api

from django.shortcuts import render_to_response
from django.http import HttpResponse


import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

tapi = twitter.Api()
nums_pattern = r'\s[\d]+[.,]?[\d]+\s'

def __merge(lst, res=[]):
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res



def data(request):
    username = request.GET.get("name", None)
    mark = request.GET.get("mark", None)
    
    howmuch = int(request.GET.get("howmuch", 300))
    
    if not username or not mark:
        log.error("No user name or no mark specified")
        return HttpResponse(status=400)
        
    log.debug("Requesting %d statuses for '%s' with mark '%s'" % (howmuch, username, mark))

    statuses = tapi.GetUserTimeline(username, count=howmuch)

    values = {}

    for s in statuses:
        if mark in s.text:
            print s.created_at_in_seconds, s.text
            values[s.created_at_in_seconds] = [float(value) for value in re.findall(nums_pattern, s.text)][0]

    description = {"date": ("datetime", "Date"),
                   "value": ("number", mark + " values")}
        
    data = []
    
    for d, value in values.items():
        #for v in value:
        data.append({"date" : datetime.fromtimestamp(d), "value" : value})
        
                   
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    
    responce_data = data_table.ToJSonResponse(columns_order=("date", "value"), order_by="date")
                                      
    ret = HttpResponse(responce_data, mimetype="text/plain")
    return ret
    

def index(request):
    name = request.GET.get("name", "Bad_Bam")
    mark = request.GET.get("mark", "#nikeplus")
    howmuch = request.GET.get("howmuch", 500)
    
    return render_to_response("main.html", {
        "query" : urllib.urlencode({"name" : name, "mark" : mark, "howmuch" : howmuch}),
        "name" : name,
        "mark" : mark
    })
    