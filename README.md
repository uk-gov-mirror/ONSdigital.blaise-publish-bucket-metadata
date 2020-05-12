# blaise-publish-bucket-metadata

Cloud function to create and publish metadata to a pub/sub topic about a zip file uploaded to a bucket.

Zip files uploaded to said bucket must be prefixed with "mi_" for Management Information or "dd_" for Data Delivery and be unique via a timestamp. Exampe:

  mi_opn2001a_01012020_1200.zip

Appropriate zip file metadata messages are published to a Pub/Sub topic for MiNiFi to consume and transfer the zip files on-premises.