import base64
import binascii


def md5hash_to_md5sum(md5hash):
    decode_hash = base64.b64decode(md5hash)
    encoded_hash = binascii.hexlify(decode_hash)
    return str(encoded_hash, "utf-8")


class InvalidFileExtension(Exception):
    pass


class InvalidFileType(Exception):
    pass
