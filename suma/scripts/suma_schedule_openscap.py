#!/usr/bin/python

import xmlrpclib

client = xmlrpclib.Server('https://suma3.suse.ar/rpc/api')
key = client.auth.login('admin', 'password')

list = client.system.listSystems(key)
for system in list:
    print "Scheduling scan for: %d" % system.get("id")
    client.system.scap.scheduleXccdfScan(key, system.get("id"),
        '/usr/share/openscap/scap-xccdf.xml',
        '--profile Default')
