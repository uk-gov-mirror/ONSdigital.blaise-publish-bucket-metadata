# blaise-publish-bucket-metadata

Cloud function to create and publish metadata to a pub/sub topic about a zip file uploaded to a bucket.

Zip files uploaded to said bucket must be prefixed with "mi_" for Management Information or "dd_" for Data Delivery and be unique via a timestamp. Exampe:

`mi_opn2001a_01012020_1200.zip`

Appropriate zip file metadata messages are published to a Pub/Sub topic for MiNiFi to consume and transfer the zip files on-premises via NiFi.

##Local Setup

Clone the project locally:

```
git clone https://github.com/ONSdigital/blaise-publish-bucket-metadata.git
```

Create a virtual environment:

On MacOS
```
{drive}:\{workspace}> python3 -m venv venv  
{drive}:\{workspace}> source venv/bin/activate (this will run a .bat file)
```
On Windows
```
{drive}:\{workspace}> python -m venv venv  
{drive}:\{workspace}> venv\Scripts\activate (this will run a .bat file)
```

Install poetry:
```
pip install poetry
```

Run poetry install
```
poetry install
```

###Troubleshooting

To give you the path to python for your virtual env run:
```
echo "$(poetry env info | grep Path | awk '{print $2}')/bin/python"
```

