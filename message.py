import json
from dataclasses import asdict, dataclass
from typing import List


@dataclass
class File:
    name: str
    sizeBytes: str
    md5sum: str
    relativePath: str


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
