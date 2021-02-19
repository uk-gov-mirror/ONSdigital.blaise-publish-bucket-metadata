import pytest

from message import NiFiMessageProcessor


class TestNiFiMessageProcessor:
    nifi_message_processor = NiFiMessageProcessor("test", "test_on_prem_subfolder")

    def test_create_not_zip(self, trigger_data):
        assert self.nifi_message_processor.create(trigger_data) is None

    def test_create_no_extension(self, trigger_no_extension):
        assert self.nifi_message_processor.create(trigger_no_extension) is None

    def test_create_not_mi_or_dd(self, trigger_zip):
        assert self.nifi_message_processor.create(trigger_zip) is None

    def test_create_mi(self, trigger_mi):
        assert self.nifi_message_processor.create(trigger_mi) == {
            "version": 3,
            "schemaVersion": 1,
            "files": [
                {
                    "sizeBytes": 230,
                    "name": "mi_test.zip:test-bucket",
                    "md5sum": "746573742d6d643568617368",
                    "relativePath": ".\\",
                }
            ],
            "sensitivity": "High",
            "sourceName": "gcp_blaise_test",
            "description": "Management Information files uploaded to GCP bucket "
            + "from Blaise5",
            "dataset": "blaise_mi",
            "iterationL1": "test_on_prem_subfolder",
            "iterationL2": "",
            "iterationL3": "",
            "iterationL4": "",
            "manifestCreated": "test-time",
            "fullSizeMegabytes": "0.000230",
        }

    def test_create_dd(self, trigger_dd):
        assert self.nifi_message_processor.create(trigger_dd) == {
            "version": 3,
            "schemaVersion": 1,
            "files": [
                {
                    "sizeBytes": 230,
                    "name": "dd_test.zip:test-bucket",
                    "md5sum": "746573742d6d643568617368",
                    "relativePath": ".\\",
                }
            ],
            "sensitivity": "High",
            "sourceName": "gcp_blaise_test",
            "description": "Data Delivery files uploaded to GCP bucket from Blaise5",
            "dataset": "blaise_dde",
            "iterationL1": "SYSTEMS",
            "iterationL2": "test_on_prem_subfolder",
            "iterationL3": "TES",
            "iterationL4": "TEST.ZIP",
            "manifestCreated": "test-time",
            "fullSizeMegabytes": "0.000230",
        }

    @pytest.mark.parametrize(
        "file,extension",
        [
            ("test.zip", "zip"),
            ("test.foo", "foo"),
            ("test.zip.foo", "foo"),
            ("test.foo.zip", "zip"),
            ("test", "test"),
        ],
    )
    def test_file_extension(self, file, extension):
        assert self.nifi_message_processor.file_extension(file) == extension

    @pytest.mark.parametrize(
        "file,type",
        [
            ("dd_test.zip", "dd"),
            ("mi_test.foo", "mi"),
            ("test.zip.foo", "test.zip.foo"),
            ("test_foo.foo.zip", "test"),
            ("foo_test", "foo"),
        ],
    )
    def test_file_type(self, file, type):
        assert self.nifi_message_processor.file_type(file) == type
