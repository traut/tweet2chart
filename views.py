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
nums_pattern = r'\s[\d]+[.,]?[\d]*\s'

def __merge(lst, res=[]):
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res



def data(request):
    username = request.GET.get("user", None)
    mark = request.GET.get("mark", None)
    
    howmuch = int(request.GET.get("howmuch", 300))
    
    if not username or not mark:
        log.error("No user name or no mark specified")
        return HttpResponse(status=400)
        
    log.debug("Requesting %d statuses for '%s' with mark '%s'" % (howmuch, username, mark))

    statuses = tapi.GetUserTimeline(username, count=howmuch)

    values = {}
    messages = {}

    for s in statuses:
        if mark in s.text:
            results = [float(value.replace(",",".")) for value in re.findall(nums_pattern, s.text, re.UNICODE | re.M | re.I | re.S)]
            if results:
                values[s.created_at_in_seconds] = results[0]
                messages[s.created_at_in_seconds] = s.text

    log.info("%d statuses found" % len(values))

    description = {"date": ("datetime", "Date"),
                   "value": ("number", mark + " values"),
                   "message" : ("string", "Tweets")}
        
    data = []
    
    for d, value in values.items():
        #for v in value:
        data.append({"date" : datetime.fromtimestamp(d), "value" : value, "message" : messages[d]})
        
                   
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    
    responce_data = data_table.ToJSonResponse(columns_order=("date", "value", "message"), order_by="date")
                                      
    ret = HttpResponse(responce_data, mimetype="text/plain")
    return ret
    
def index(request):
    return render_to_response("main.html")
    

def search(request, user=None, mark="#chartit", howmuch=500):
    
    try:
        howmuch = int(howmuch)
    except ValueError:
        log.info("Unappropriate value in howmuch: %s" % howmuch)
        howmuch = 500
        
    if not mark:
        mark = "#chartit"
        
    log.info("%s %s %d" % (user, mark, howmuch))
    
    query = "%s %s" % (user, mark)
    
    return render_to_response("main.html", {
        "query" : urllib.urlencode({"user" : user, "mark" : mark.encode("utf-8"), "howmuch" : howmuch}),
        "user" : user,
        "mark" : mark,
        "marksearch" : urllib.urlencode({"q" : query.encode("utf-8")})
    })
    