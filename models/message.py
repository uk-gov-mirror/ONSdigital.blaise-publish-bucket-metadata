import json
import pathlib
from dataclasses import asdict, dataclass
from typing import List

from utils import md5hash_to_md5sum


@dataclass
class File:
    name: str
    sizeBytes: str
    md5sum: str
    relativePath: str = ".\\"

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
        parsed_prefix = file_prefix.split("_")[1:]
        instrument_name = [
            instrument_name_part
            for instrument_name_part in parsed_prefix
            if not instrument_name_part.isnumeric()
        ]
        return "_".join(instrument_name).upper()

    def is_lms(self):
        return self.survey_name().startswith("LM")

    def is_opn(self):
        return self.survey_name() == "OPN"

    @classmethod
    def from_event(cls, event):
        return cls(
            name=f"{event['name']}:{event['bucket']}",
            sizeBytes=event["size"],
            md5sum=md5hash_to_md5sum(event["md5Hash"]),
        )


@dataclass
class Message:
    files: List[File]
    sourceName: str
    manifestCreated: str
    fullSizeMegabytes: str
    version: int = 3
    schemaVersion: int = 1
    description: str = ""
    dataset: str = ""
    sensitivity: str = "High"
    iterationL1: str = ""
    iterationL2: str = ""
    iterationL3: str = ""
    iterationL4: str = ""

    def json(self):
        return json.dumps(asdict(self))

    def first_file(self):
        return self.files[0]

    def management_information(self, config):
        self.description = (
            "Management Information files uploaded to GCP bucket from Blaise5"
        )
        self.dataset = "blaise_mi"
        self.iterationL1 = config.on_prem_subfolder
        return self

    def data_delivery_opn(self, config):
        file = self.first_file()
        survey_name = file.survey_name()
        self.description = (
            f"Data Delivery files for {survey_name} uploaded to GCP bucket from Blaise5"
        )
        self.dataset = "blaise_dde"
        self.iterationL1 = "SYSTEMS"
        self.iterationL2 = config.on_prem_subfolder
        self.iterationL3 = survey_name
        self.iterationL4 = file.instrument_name()
        return self

    def data_delivery_lms(self, config):
        file = self.first_file()
        survey_name = file.survey_name()
        environment = config.env
        self.description = (
            f"Data Delivery files for {survey_name} uploaded to GCP bucket from Blaise5"
        )
        self.dataset = "blaise_dde"
        self.iterationL1 = "LMS_Master"
        self.iterationL2 = "CLOUD"
        self.iterationL3 = environment
        self.iterationL4 = file.instrument_name()
        return self
