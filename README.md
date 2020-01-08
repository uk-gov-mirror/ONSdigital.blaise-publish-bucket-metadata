## Publish a files metadata onto PubSub queue when a file is uploaded to GCP bucket. **[LU-4496](https://collaborate2.ons.gov.uk/jira/browse/LU-4496)**

The following filetypes are created or updated on a specified bucket, the message (below) is published to the Pub/Sub queue with file meta data injected for file types :
- *.sps
- *.asc
- *.rmk  
- *.csv (for MI)

This is based on dde/mi-meta-template.json where 'Files', 'iterationL2-4', 'manifestCreated' and 'fullSizeMegabytes' meta data substituted.

```json
{
    "version": 1,
    "files": [{  // the following 4 items Updated by GCP storage trigger function pubFileMetaData
            "sizeBytes": "17",
            "name": "test.csv:blaise-dev-258914-results",  // NOTE bucket name is appended to filename i.e. filename:bucketname
            "md5sum": "testmd5sumdfer34==",
            "relativePath": ".\\"
        }], 
    "sensitivity": "High",
    "sourceName": "gcp_blaise",
    "description": "Creation of Blaise Manifest for DDE files sent to GCP bucket",
    "iterationL1": "ldata12",
                "iterationL2": "opn", // Updated by GCP storage trigger function pubFileMetaData - first 3 letters of filename
                "iterationL3": "1911", // Updated by GCP storage trigger function pubFileMetaData - chars 4-8 of filename
                "iterationL4": "a", // Updated by GCP storage trigger function pubFileMetaData - 9 char of filename
    "dataset": "blaise_dde",
    "schemaVersion": 1,
    "manifestCreated": "",
    "fullSizeMegabytes": ""
}
```

## To deploy the function run the following from the GCP console

```
gcloud functions deploy pubFileMetaData \
  --source https://source.developers.google.com/projects/blaise-dev-258914/repos/github_onsdigital_blaise-gcp-publish-bucket-metadata \
  --runtime python37 \
  --trigger-resource blaise-dev-258914-results \
  --trigger-event google.storage.object.finalize \
  --set-env-vars ON-PREM-SUBFOLDER=BL5,PROJECT_ID=blaise-dev-258914,TOPIC_NAME=blaise-dev-258914-export-topic \
  --region=europe-west2
```

```
Deploying function (may take a while - up to 2 minutes)...done.
availableMemoryMb: 256
entryPoint: pubFileMetaData
environmentVariables:
  PROJECT_ID: blaise-dev-258914
  TOPIC_NAME: blaise-dev-258914-export-topic
eventTrigger:
  eventType: google.storage.object.finalize
  failurePolicy: {}
  resource: projects/_/buckets/blaise-dev-258914-results
  service: storage.googleapis.com
labels:
  deployment-tool: cli-gcloud
name: projects/blaise-dev-258914/locations/europe-west2/functions/pubFileMetaData
runtime: python37
serviceAccountEmail: blaise-dev-258914@appspot.gserviceaccount.com
sourceRepository:
  deployedUrl: https://source.developers.google.com/projects/blaise-dev-258914/repos/github_onsdigital_blaise-gcp-publish-bucket-metadata/revisions/a508a7800f7cf7d1e83f312b0f9e13ff12c7c5a0/paths/
  url: https://source.developers.google.com/projects/blaise-dev-258914/repos/github_onsdigital_blaise-gcp-publish-bucket-metadata/moveable-aliases/master/paths/
status: ACTIVE
timeout: 60s
updateTime: '2019-12-09T14:47:24Z'
versionId: '1'
```
