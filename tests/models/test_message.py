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
    "file_name,file_type",
    [("dd_file.zip", "dd"), ("mi_file.zip", "mi")],
)
def test_file_file_type(file, file_name, file_type):
    file.name = f"{file_name}:my-bucket-name"
    assert file.type() == file_type


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("dd_opn2101a.zip", "OPN"),
        ("dd_lms2102_a1.zip", "LMS"),
        ("dd_lms2102_bk1.zip", "LMS"),
    ],
)
def test_file_survey_name(file, file_name, expected):
    file.name = f"{file_name}:my-bucket-name"
    assert file.survey_name() == expected


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("dd_opn2101a.zip", "OPN2101A"),
        ("dd_lms2102_a1.zip", "LMS2102_A1"),
        ("dd_lms2102_bk1.zip", "LMS2102_BK1"),
    ],
)
def test_file_instrument_name(file, file_name, expected):
    file.name = f"{file_name}:my-bucket-name"
    assert file.instrument_name() == expected


def test_file_from_event(dd_event):
    file = File.from_event(dd_event)
    assert file.name == "dd_OPN2102R_0103202021_16428.zip:ons-blaise-v2-nifi"
    assert file.sizeBytes == "20"
    assert file.md5sum == "d1ad7875be9ee3c6fde3b6f9efdf3c6b67fad78ebd7f6dbc"
    assert file.relativePath == ".\\"
