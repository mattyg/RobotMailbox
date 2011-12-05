#!/usr/bin/python
import validictory
import json

dataf = open('/home/matt/Brandeis/Email2.0/event/config.json')
schemaf = open('/home/matt/Brandeis/Email2.0/config-schema.json')

data = json.load(dataf)
schema = json.load(schemaf)

print data
print "\n\n\n"
print schema

validictory.validate(data,schema)
