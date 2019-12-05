Publish a files metadata onto PubSub queue when a file is uploaded to GCP bucket.

For Data Delievery Exchange (DDE), a dde-meta-template.json message is published to the Pub/Sub queue with file meta data injected for file types *.sps, *.asc and *.rmk
For MI, an mi-meta-template.json message is published to the Pub/Sub queue with file metadata injected for file type *.csv

To deploy the function run the following from the GCP console

gcloud functions deploy pubFileMetaData --source https://source.developers.google.com/projects/${PROJECT_ID}/repos/github_onsdigital_blaise-gcp-publish-bucket-metadata --runtime python37 --trigger-resource dde_bucket --trigger-event google.storage.object.finalize --set-env-vars PROJECT_ID=${PROJECT_ID}
