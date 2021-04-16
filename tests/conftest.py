import pytest

from models.message import File


@pytest.fixture
def md5hash():
    return "0a14db6e48b947b57988a2f61469f228"


@pytest.fixture
def dd_event(md5hash):
    return {
        "name": "dd_OPN2102R_0103202021_16428.zip",
        "bucket": "ons-blaise-v2-nifi",
        "md5Hash": md5hash,
        "size": "20",
        "timeCreated": "0103202021_16428",
    }


@pytest.fixture
def mi_event(md5hash):
    return {
        "name": "mi_foobar.zip",
        "bucket": "ons-blaise-v2-nifi",
        "md5Hash": md5hash,
        "size": "20",
        "timeCreated": "0103202021_16428",
    }


@pytest.fixture
def file():
    return File(
        name="dd_file.zip:my-bucket-name",
        sizeBytes="20",
        md5sum="dasdasd",
        relativePath="./",
    )
