def encrypt_file(filename):
    import os
    import gnupg

    gpghome = os.path.join(os.getcwd(), 'gpghome')
    if(os.path.exists(gpghome)):
        os.system('rm -rf ' + gpghome)
        os.system('mkdir ' + gpghome)

    # os.system('mkdir '+ gpghome)
    print(gpghome)
    gpg = gnupg.GPG(gnupghome=gpghome)
    pubkey = open('key.gpg').read()
    import_result = gpg.import_keys(pubkey)

    print(import_result.results)
    uid = "blaise5-gcp-gpg-key (key to be used for blaise5 content) <nic.hayes@ons.statistics.gov.uk>"
    with open(filename, 'rb') as f:
        status = gpg.encrypt_file(f, recipients=[uid], sign=None,armor=True, output=filename, always_trust=True)
    print ('jc ok: ', status.ok)
    print ('jc status: ', status.status)
    print ('jc stderr: ', status.stderr)
    

def createMsg(data, dest):
    import json

    print(dest["metaTemplate"])
    with open(dest["metaTemplate"]) as json_file:
        msg = json.load(json_file)

    files = {}
    filename = data['name'] + ":" + data['bucket']
    sizeBytes = data['size']
    md5hash = data['md5Hash']
    manifestCreated = data['timeCreated']
    fullSizeMegabytes = "{:.6f}".format(int(data['size'])/1000000)
    files["sizeBytes"] = sizeBytes
    files["name"] = filename
    files["md5hash"] = md5hash
    files["relativePath"] = ".\\"
    msg['files'].append(files)
    msg["manifestCreated"] = manifestCreated
    msg["fullSizeMegabytes"] = fullSizeMegabytes
    return msg


def pubFileMetaData(data, context):
    import os
    import json
    from google.cloud import pubsub_v1
    project_id = os.environ['PROJECT_ID']
    project_id = "blaise-dev-258914"
    if(project_id):
        encrypt_file(data['name'])
        dest = {}
        topic_name = os.environ['TOPIC_NAME']
        topic_name = "blaise-dev-258914-export-topic"
        fileExtn = data['name'].split(".")[1].lower()
        runPubSub = False
        if (fileExtn == "csv"):
            runPubSub = True
            metaTemplate = os.path.join(os.getcwd(), "mi-meta-template.json")
            dest["metaTemplate"] = metaTemplate
            dest["iterationL2"] = ''
            dest["iterationL3"] = ''
            dest["iterationL4"] = ''

        elif fileExtn == "asc" or fileExtn == "rmk" or fileExtn == "sps":
            runPubSub = True
            metaTemplate = os.path.join(os.getcwd(), "dde-meta-template.json")
            # File needs to be in the format of opn1911a.sps
            dest["metaTemplate"] = metaTemplate
            dest["iterationL2"] = data['name'][:3]
            dest["iterationL3"] = data['name'][3:7]
            dest["iterationL4"] = data['name'][7:8]
        else:
            runPubSub = False
            print("Filetype {} not found for DDE or MI".format(fileExtn))

        if (runPubSub):
            client = pubsub_v1.PublisherClient()
            topic_path = client.topic_path(project_id, topic_name)
            msg = createMsg(data, dest)
            print(msg)
            msgbytes = bytes(json.dumps(msg), encoding='utf-8')
            client.publish(topic_path, data=msgbytes)
