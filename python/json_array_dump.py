#!/usr/bin/env python
#
# json array dump
#
# Description:
#   Takes a file with a single JSON array object and writes it out to a file with each array element on its own line
#   Useful for things that read in 'messages' one line at a time and parses them as a single item
#
import json, sys

tmp_file = sys.argv[1]
out_file = sys.argv[2]
print tmp_file

with open(str(tmp_file),'r') as data_file:    
    data = json.load(data_file)

with open(str(out_file),'w') as output_file:
    for k in data["objects"]:
        output_file.write(json.dumps(k))
        output_file.write('\n')
        output_file.flush()


