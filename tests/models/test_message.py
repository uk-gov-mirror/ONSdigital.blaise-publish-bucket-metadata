import json

from models.message import File, Message


def test_message_json():
    file = File(name="a_file", sizeBytes="20", md5sum="dasdasd", relativePath="./")
    message = Message(
        files=[file],
        sourceName="blaise",
        description="blaise test",
        dataset="blaise dataset",
        manifestCreated="my_date",
        fullSizeMegabytes="1",
    )
    assert json.loads(message.json()) == {
        "version": 3,
        "schemaVersion": 1,
        "files": [
            {
                "sizeBytes": "20",
                "name": "a_file",
                "md5sum": "dasdasd",
                "relativePath": "./",
            }
        ],
        "sensitivity": "High",
        "sourceName": "blaise",
        "description": "blaise test",
        "dataset": "blaise dataset",
        "iterationL1": "",
        "iterationL2": "",
        "iterationL3": "",
        "iterationL4": "",
        "manifestCreated": "my_date",
        "fullSizeMegabytes": "1",
    }
