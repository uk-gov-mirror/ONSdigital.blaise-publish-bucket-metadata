import json, os
from main import createMsg
with open(os.getcwd() + "\data-sent-by-gcp-to-storage-func.json") as json_file:
    data = json.load(json_file)

dest = {}

metaTemplate = os.getcwd() + "\mi-meta-template.json"
dest["metaTemplate"] = f"{metaTemplate}"
dest["iterationL2"] = f"{data['name'][:3]}"
dest["iterationL3"] = f"{data['name'][3:7]}"
dest["iterationL4"] = f"{data['name'][7:8]}"    

x = createMsg(data,dest)       
print(json.dumps(x, indent=3))
