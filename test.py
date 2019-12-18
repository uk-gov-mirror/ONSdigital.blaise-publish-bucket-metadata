import json
import os

from main import *

datafile = "test-data-from-gcp.json"

with open(os.path.join(os.getcwd(), datafile)) as json_file:
    data = json.load(json_file)

print(json.dumps(createMsg(data), indent=3))
