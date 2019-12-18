import json
import os

from main import *

datafile = "data-sent-by-gcp-to-storage-func.json"

with open(os.path.join(os.getcwd(), datafile)) as json_file:
    data = json.load(json_file)

print(json.dumps(createMsg(data), indent=3))
