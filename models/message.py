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
