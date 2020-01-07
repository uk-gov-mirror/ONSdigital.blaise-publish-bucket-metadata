import json
import os

from main import createMsg

datafile = "test-data-from-gcp.json"

with open(os.path.join(os.getcwd(), datafile)) as json_file:
    data = json.load(json_file)

msg = createMsg(data)

#print(msg)

msgbytes = bytes(json.dumps(msg), encoding='utf-8')

# print(str(msgbytes))
print(json.dumps(msg, indent=3))
