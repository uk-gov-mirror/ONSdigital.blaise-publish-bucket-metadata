Publish a files metadata onto PubSub queue when a file is uploaded to GCP bucket.

From GCP console, deploy function with the following
gcloud functions deploy pubFileMetaData --runtime python37 --trigger-resource dde_bucket --trigger-event google.storage.object.finalize --set-env-vars PROJECT_ID=blaise-dev-258914