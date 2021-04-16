# blaise-publish-bucket-metadata

Cloud function to create and publish metadata to a pub/sub topic about a zip file uploaded to a bucket.

Zip files uploaded to said bucket must be prefixed with "mi_" for Management Information or "dd_" for Data Delivery and be unique via a timestamp. Exampe:

`mi_opn2001a_01012020_1200.zip`

Appropriate zip file metadata messages are published to a Pub/Sub topic for MiNiFi to consume and transfer the zip files on-premises via NiFi.

## Testing

To run formatting, linting and testing run:

```sh
poetry install
make format lint test
```

If you just want to run the tests:

```sh
poetry install
make test
```

## Configuring your IDE

You will probably need to configure the python interpreter in your IDE to use your virtual env, the easiest way to get
the python path is to run:

```sh
echo "$(poetry env info | grep Path | awk '{print $2}')/bin/python"
```
