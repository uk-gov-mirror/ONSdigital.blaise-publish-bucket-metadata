import base64

import pytest


@pytest.fixture
def trigger_data():
    return {
        "name": "test_name.foo",
        "bucket": "test-bucket",
        "size": 230,
        "md5Hash": base64.b64encode(b"test-md5hash"),
        "timeCreated": "test-time",
    }


@pytest.fixture
def trigger_zip(trigger_data):
    trigger_data["name"] = "test_name.zip"
    return trigger_data


@pytest.fixture
def trigger_no_extension(trigger_data):
    trigger_data["name"] = "test_name"
    return trigger_data


@pytest.fixture
def trigger_dd(trigger_data):
    trigger_data["name"] = "dd_test.zip"
    return trigger_data


@pytest.fixture
def trigger_mi(trigger_data):
    trigger_data["name"] = "mi_test.zip"
    return trigger_data
