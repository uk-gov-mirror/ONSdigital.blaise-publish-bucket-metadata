def pubFileMetaData(data, context):
    import json
    import os
    
    from google.cloud import pubsub_v1
    project_id = os.environ['PROJECT_ID']
    if(project_id): 

        topic_name = "blaise-dev-258914-export-topic"
        fileExtn = data['name'].split(".")[1].lower()
        runPubSub = False
        if (fileExtn == "csv"):
            runPubSub = True
            metaTemplate = "mi-meta-template.json"
            iterationL2 = ""
            iterationL3 = ""
            iterationL4 = ""
        elif fileExtn == "asc" or fileExtn == "rmk" or fileExtn == "sps":
            runPubSub = True
            # File needs to be in the format of opn1911a.sps
            iterationL2 = data['name'][:3]
            iterationL3 = data['name'][3:7]
            iterationL4 = data['name'][7:8]
            metaTemplate = "dde-meta-template.json"
        else:
            runPubSub = False
            print("Error: Filetype {} not found for DDE or MI".format(fileExtn))

        if (runPubSub):
            client = pubsub_v1.PublisherClient()
            topic_path = client.topic_path(project_id, topic_name)

            with open(metaTemplate) as json_file:
                msg = json.load(json_file)

            files = {}
            filename = data['name'] + ":" + data['bucket']
            sizeBytes = data['size']
            md5hash = data['md5Hash']
            manifestCreated = data['timeCreated']
            fullSizeMegabytes = "{:.6f}".format(int(data['size'])/1000000)
            files["sizeBytes"] = f"{sizeBytes}"
            files["name"] = f"{filename}"
            files["md5hash"] = f"{md5hash}"
            files["relativePath"] = ".\\"
            msg['files'].append(files)
            msg["iterationL2"] = f"{iterationL2}"
            msg["iterationL3"] = f"{iterationL3}"
            msg["iterationL4"] = f"{iterationL4}"
            msg["manifestCreated"] = f"{manifestCreated}"
            msg["fullSizeMegabytes"] = f"{fullSizeMegabytes}"

            msgbytes = bytes(json.dumps(msg), encoding='utf-8')
            client.publish(topic_path, data=msgbytes)
            print (json.dumps(msg, sort_keys=True, indent=3))
