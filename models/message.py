import json
import pathlib
from dataclasses import asdict, dataclass
from typing import List


@dataclass
class File:
    name: str
    sizeBytes: str
    md5sum: str
    relativePath: str

    def extension(self):
        return pathlib.Path(self.filename()).suffix

    def filename(self):
        return self.name.split(":")[0]

    def type(self):
        return self.name.split("_")[0]

    def survey_name(self):
        return self.filename().split("_")[1][0:3].upper()

    def instrument_name(self):
        file_prefix = pathlib.Path(self.filename()).stem
        return file_prefix.split("_")[1].upper()


@dataclass
class Message:
    files: List[File]
    sourceName: str
    description: str
    dataset: str
    manifestCreated: str
    fullSizeMegabytes: str
    version: int = 3
    schemaVersion: int = 1
    sensitivity: str = "High"
    iterationL1: str = ""
    iterationL2: str = ""
    iterationL3: str = ""
    iterationL4: str = ""

    def json(self):
        return json.dumps(asdict(self))

    def management_information(self, config):
        self.description = (
            "Management Information files uploaded to GCP bucket from Blaise5"
        )
        self.dataset = "blaise_mi"
        self.iterationL1 = config.on_prem_subfolder
        return self

    def data_delivery_opn(self, config, event):
        self.description = "Data Delivery files uploaded to GCP bucket from Blaise5"
        self.dataset = "blaise_dde"
        self.iterationL1 = "SYSTEMS"
        self.iterationL2 = config.on_prem_subfolder
        self.iterationL3 = event["name"][3:6].upper()
        self.iterationL4 = event["name"][3:11].upper()
        return self
