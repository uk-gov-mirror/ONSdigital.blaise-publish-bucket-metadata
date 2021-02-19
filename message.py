import base64
import binascii
from dataclasses import asdict, dataclass, field
from typing import List


@dataclass
class NiFiMessage:
    version: int = 3
    schemaVersion: int = 1
    files: List[dict] = field(default_factory=list)
    sensitivity: str = "High"
    sourceName: str = ""
    description: str = ""
    dataset: str = ""
    iterationL1: str = ""
    iterationL2: str = ""
    iterationL3: str = ""
    iterationL4: str = ""
    manifestCreated: str = ""
    fullSizeMegabytes: str = ""

    @classmethod
    def MI(cls, on_prem_sub_folder):
        msg = cls()
        msg.description = (
            "Management Information files uploaded to GCP bucket from Blaise5"
        )
        msg.dataset = "blaise_mi"
        msg.iterationL1 = on_prem_sub_folder
        return msg

    @classmethod
    def DD(cls, on_prem_sub_folder, name):
        msg = cls()
        msg.description = "Data Delivery files uploaded to GCP bucket from Blaise5"
        msg.dataset = "blaise_dde"
        msg.iterationL1 = "SYSTEMS"
        msg.iterationL2 = on_prem_sub_folder
        msg.iterationL3 = name[3:6].upper()
        msg.iterationL4 = name[3:11].upper()
        return msg


@dataclass
class NiFiFile:
    name: str
    sizeBytes: int
    md5sum: str
    relativePath: str = ".\\"


class NiFiMessageProcessor:
    def __init__(self, env, on_prem_sub_folder):
        self.env = env
        self.on_prem_sub_folder = on_prem_sub_folder

    def create(self, triggerData):
        name = triggerData["name"]
        file_extension = self.file_extension(name)
        file_type = self.file_type(name)

        if file_extension == "zip" and file_type == "mi":
            msg = NiFiMessage.MI(self.on_prem_sub_folder)
        elif file_extension == "zip" and file_type == "dd":
            msg = NiFiMessage.DD(self.on_prem_sub_folder, name)
        else:
            print(
                f"File extension {file_extension} not found or "
                + f"file type {file_type} is invalid"
            )
            return None

        msg.sourceName = f"gcp_blaise_{self.env}"

        file = NiFiFile(
            name=f"{name}:{triggerData['bucket']}",
            sizeBytes=triggerData["size"],
            md5sum=self._md5sum(triggerData["md5Hash"]),
        )
        msg.files.append(file)
        print(file)

        msg.manifestCreated = triggerData["timeCreated"]
        msg.fullSizeMegabytes = "{:.6f}".format(int(triggerData["size"]) / 1000000)
        print(f"Message created {msg}")
        return asdict(msg)

    def file_extension(_self, filename):
        return filename.split(".")[-1].lower()

    def file_type(_self, filename):
        return filename.split("_")[0].lower()

    # Note GCP uses md5hash - however, MiNiFi needs it to be md5sum
    def _md5sum(_self, md5Hash):
        decodedhash = base64.b64decode(md5Hash)
        return binascii.hexlify(decodedhash).decode("utf-8")
