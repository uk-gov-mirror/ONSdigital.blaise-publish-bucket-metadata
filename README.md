Publish a files metadata onto PubSub queue when a file is uploaded to GCP bucket

gcloud functions deploy helloGET \
--source https://source.developers.google.com/projects/$PROJECT_ID/repos/hello-world/moveable-aliases/master/paths/gcf_hello_world \
--trigger-http \
--runtime=python37;