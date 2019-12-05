import json
from main import *
with open("c:\gcp\pubMeta\data-sent-by-gcp-to-storage-func.json") as json_file:
    datatest = json.load(json_file)

pubFileMetaData(datatest)          
           