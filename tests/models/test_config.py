import os
from unittest import mock

from models.config import Config


def test_config():
    config = Config(
        on_prem_subfolder="OPN", project_id="foobar", topic_name="barfoo", env="test"
    )
    assert config.on_prem_subfolder == "OPN"
    assert config.project_id == "foobar"
    assert config.topic_name == "barfoo"
    assert config.env == "test"


@mock.patch.dict(
    os.environ,
    {
        "PROJECT_ID": "test_project_id",
        "ENV": "test",
        "TOPIC_NAME": "nifi-notify",
        "ON-PREM-SUBFOLDER": "DEV",
    },
)
def test_config_from_env():
    config = Config.from_env()
    assert config.on_prem_subfolder == "DEV"
    assert config.project_id == "test_project_id"
    assert config.topic_name == "nifi-notify"
    assert config.env == "test"
