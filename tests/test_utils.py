from utils import md5hash_to_md5sum


def test_md5hash_to_md5sum(md5hash):
    assert (
        md5hash_to_md5sum(md5hash) == "d1ad7875be9ee3c6fde3b6f9efdf3c6b67fad78ebd7f6dbc"
    )
