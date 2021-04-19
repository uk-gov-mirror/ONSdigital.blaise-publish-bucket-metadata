import json
import os
from unittest import mock

import blaise_dds
import pytest
from google.cloud.pubsub_v1 import PublisherClient

from main import publishMsg, size_in_megabytes


@mock.patch.dict(
    os.environ,
    {
        "PROJECT_ID": "test_project_id",
        "ENV": "test",
        "TOPIC_NAME": "nifi-notify",
        "ON-PREM-SUBFOLDER": "DEV",
    },
)
@mock.patch.object(blaise_dds.Client, "update_state")
@mock.patch.object(PublisherClient, "publish")
def test_publishMsg_dd(mock_pubsub, mock_update_state, dd_event):
    publishMsg(dd_event, None)
    assert mock_update_state.call_count == 2
    assert mock_update_state.call_args_list[0] == mock.call(
        dd_event["name"],
        "in_nifi_bucket",
    )
    assert mock_update_state.call_args_list[1] == mock.call(
        dd_event["name"],
        "nifi_notified",
    )
    assert len(mock_pubsub.call_args_list) == 1
    assert (
        mock_pubsub.call_args_list[0][0][0]
        == "projects/test_project_id/topics/nifi-notify"
    )
    pubsub_message = mock_pubsub.call_args_list[0][1]["data"]
    assert json.loads(pubsub_message) == {
        "version": 3,
        "schemaVersion": 1,
        "files": [
            {
                "sizeBytes": "20",
                "name": "dd_OPN2102R_0103202021_16428.zip:ons-blaise-v2-nifi",
                "md5sum": "d1ad7875be9ee3c6fde3b6f9efdf3c6b67fad78ebd7f6dbc",
                "relativePath": ".\\",
            }
        ],
        "sensitivity": "High",
        "sourceName": "gcp_blaise_test",
        "description": "Data Delivery files uploaded to GCP bucket from Blaise5",
        "dataset": "blaise_dde",
        "iterationL1": "SYSTEMS",
        "iterationL2": "DEV",
        "iterationL3": "OPN",
        "iterationL4": "OPN2102R",
        "manifestCreated": "0103202021_16428",
        "fullSizeMegabytes": "0.000020",
    }


@mock.patch.dict(
    os.environ,
    {
        "PROJECT_ID": "test_project_id",
        "ENV": "test",
        "TOPIC_NAME": "nifi-notify",
        "ON-PREM-SUBFOLDER": "DEV",
    },
)
@mock.patch.object(blaise_dds.Client, "update_state")
@mock.patch.object(PublisherClient, "publish")
def test_publishMsg_mi(mock_pubsub, mock_update_state, mi_event):
    publishMsg(mi_event, None)
    assert mock_update_state.call_count == 2
    assert mock_update_state.call_args_list[0] == mock.call(
        mi_event["name"],
        "in_nifi_bucket",
    )
    assert mock_update_state.call_args_list[1] == mock.call(
        mi_event["name"],
        "nifi_notified",
    )

    assert (
        mock_pubsub.call_args_list[0][0][0]
        == "projects/test_project_id/topics/nifi-notify"
    )
    pubsub_message = mock_pubsub.call_args_list[0][1]["data"]
    assert json.loads(pubsub_message) == {
        "version": 3,
        "schemaVersion": 1,
        "files": [
            {
                "sizeBytes": "20",
                "name": "mi_foobar.zip:ons-blaise-v2-nifi",
                "md5sum": "d1ad7875be9ee3c6fde3b6f9efdf3c6b67fad78ebd7f6dbc",
                "relativePath": ".\\",
            }
        ],
        "sensitivity": "High",
        "sourceName": "gcp_blaise_test",
        "description": "Management Information files uploaded to GCP bucket from Blaise5",
        "dataset": "blaise_mi",
        "iterationL1": "DEV",
        "iterationL2": "",
        "iterationL3": "",
        "iterationL4": "",
        "manifestCreated": "0103202021_16428",
        "fullSizeMegabytes": "0.000020",
    }


@mock.patch.dict(
    os.environ,
    {"PROJECT_ID": "test_project_id", "ENV": "test", "TOPIC_NAME": "nifi-notify"},
)
@mock.patch.object(blaise_dds.Client, "update_state")
@mock.patch.object(PublisherClient, "publish")
def test_publishMsg_error(mock_pubsub, mock_update_state, dd_event):
    mock_pubsub.side_effect = Exception(
        "Explosions occured when sending message to pubsub"
    )
    publishMsg(dd_event, None)
    assert mock_update_state.call_count == 2
    assert mock_update_state.call_args_list[0] == mock.call(
        dd_event["name"],
        "in_nifi_bucket",
    )
    assert mock_update_state.call_args_list[1] == mock.call(
        dd_event["name"],
        "errored",
        "Exception('Explosions occured when sending message to pubsub')",
    )


@mock.patch.dict(
    os.environ,
    {"TOPIC_NAME": "nifi-notify"},
)
@mock.patch.object(blaise_dds.Client, "update_state")
def test_project_id_not_set(mock_update_state, dd_event, capsys):
    publishMsg(dd_event, None)
    assert mock_update_state.call_count == 1
    assert mock_update_state.call_args_list[0] == mock.call(
        dd_event["name"],
        "in_nifi_bucket",
    )
    captured = capsys.readouterr()
    assert captured.out == (
        "Configuration: Project ID: None\n"
        + "Configuration: Topic Name: nifi-notify\n"
        + "Configuration: ON-PREM-SUBFOLDER: None\n"
        + "Configuration: Env: None\n"
        + "Configuration: File name: dd_OPN2102R_0103202021_16428.zip\n"
        + "Configuration: Bucket Name: ons-blaise-v2-nifi\n"
        + "project_id not set, publish failed\n"
    )


@pytest.mark.parametrize(
    "size_in_bytes,size_in_megs",
    [
        ("20", "0.000020"),
        ("320", "0.000320"),
        ("4783", "0.004783"),
        ("12004783", "12.004783"),
        ("3475231", "3.475231"),
    ],
)
def test_size_in_megabytes(size_in_bytes, size_in_megs):
    assert size_in_megabytes(size_in_bytes) == size_in_megs
