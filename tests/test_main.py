import json
import os
from unittest import mock

import blaise_dds
from google.cloud.pubsub_v1 import PublisherClient

from main import publishMsg


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
    mock_pubsub.assert_called_once_with(
        "projects/test_project_id/topics/nifi-notify",
        data=json.dumps(
            {
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
        ).encode("utf-8"),
    )


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
    mock_pubsub.assert_called_once_with(
        "projects/test_project_id/topics/nifi-notify",
        data=json.dumps(
            {
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
        ).encode("utf-8"),
    )


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
        + "Configuration: File name: dd_OPN2102R_0103202021_16428.zip\n"
        + "Configuration: Bucket Name: ons-blaise-v2-nifi\n"
        + "Configuration: ON-PREM-SUBFOLDER: None\n"
        + "project_id not set, publish failed\n"
    )
