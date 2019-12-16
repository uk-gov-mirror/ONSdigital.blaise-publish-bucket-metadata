import json
import os

from main import *
datafile = "data-sent-by-gcp-to-storage-func.json"

with open(os.path.join(os.getcwd(), datafile)) as json_file:
    data = json.load(json_file)

dest = {}

metaTemplate = os.path.join(os.getcwd(), "dde-meta-template.json")
dest["metaTemplate"] = metaTemplate
dest["iterationL2"] = data['name'][:3]
dest["iterationL3"] = data['name'][3:7]
dest["iterationL4"] = data['name'][7:8]
print(json.dumps(createMsg(data, dest), indent=3))

testFile = 'out.txt'
open(testFile, 'w').write('Jc in Blaise5.')
encrypt_file(testFile)