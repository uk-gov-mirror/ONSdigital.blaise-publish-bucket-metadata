Publish a files metadata onto PubSub queue when a file is uploaded to GCP bucket

gcloud functions deploy pubFileMetaData --runtime python37 --trigger-resource dde_bucket --trigger-event google.storage.object.finalize