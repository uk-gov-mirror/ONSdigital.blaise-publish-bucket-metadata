import pytest


@pytest.fixture
def dd_event():
    return {
        "name": "dd_OPN2102R_0103202021_16428.zip",
        "bucket": "ons-blaise-v2-nifi",
        "md5Hash": "0a14db6e48b947b57988a2f61469f228",
        "size": 20,
        "timeCreated": "0103202021_16428",
    }


@pytest.fixture
def mi_event():
    return {
        "name": "mi_foobar.zip",
        "bucket": "ons-blaise-v2-nifi",
        "md5Hash": "0a14db6e48b947b57988a2f61469f228",
        "size": 20,
        "timeCreated": "0103202021_16428",
    }
