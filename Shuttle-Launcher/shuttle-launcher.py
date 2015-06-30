#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, sys, json, os

shuttle_config = os.path.expanduser("~")+"/.shuttle.json"

host_query = "{query}"

pattern = re.compile(host_query, flags=re.IGNORECASE)

found_flag = 0

def listHosts(hosts, current_host = None):
    for host in hosts:
        if (not host.has_key(u'cmd')):
            for key in host:
                host_name = current_host + ' - ' + key if current_host else key
                listHosts(host[key], host_name)
        else:
            host_name = current_host + ' - ' + host['name']
            if pattern.search(host_name):
                global found_flag
                found_flag += 1
                print "  <item uid=\""+ host_name +"\" arg=\""+host['cmd']+"\" >"
                print "    <title>"+ host_name  +"</title>"
                print "    <subtitle>"+host['cmd']+"</subtitle>"
                print "    <icon>icon.png</icon>"
                print "  </item>"
    

shuttle_file = file(shuttle_config)

try:
    json_string = json.dumps(json.load(shuttle_file))
    host_list = json.loads(json_string)

    print "<?xml version=\"1.0\"?>\n<items>"
    listHosts(host_list['hosts'])

    if (found_flag == 0):
        print "  <item uid=\"Not Found\" arg=\"\" >"
        print "    <title>No Match!</title>"
        print "    <subtitle>Cannot find "+host_name+"</subtitle>"
        print "    <icon>icon.png</icon>"
        print "  </item>"
    print "</items>"
    
except Exception,e:
    shuttle_file.close()
    print e
    sys.exit(1)

