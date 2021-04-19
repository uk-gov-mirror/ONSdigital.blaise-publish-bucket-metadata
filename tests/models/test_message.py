import json

import pytest

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


def test_file_extension(file):
    assert file.extension() == ".zip"


def test_file_filename(file):
    assert file.filename() == "dd_file.zip"


@pytest.mark.parametrize(
    "file_name,file_type", [("dd_file.zip", "dd"), ("mi_file.zip", "mi")]
)
def test_file_file_type(file, file_name, file_type):
    file.name = f"{file_name}:my-bucket-name"
    assert file.type() == file_type


def test_file_survey_name(file):
    file.name = "dd_opn2101a.zip:my-bucket-name"
    assert file.survey_name() == "OPN"


def test_file_insrument_name(file):
    file.name = "dd_opn2101a.zip:my-bucket-name"
    assert file.instrument_name() == "OPN2101A"
