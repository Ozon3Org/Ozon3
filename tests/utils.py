from urllib.parse import urlsplit, urlunsplit, urlencode
import vcr
from decouple import config
from ozon3 import Ozon3


# Filter out token in response headers
def before_record_response(response):
    loc_lst = response["headers"].get("Location")

    if loc_lst is not None:
        split = urlsplit(loc_lst[0])
        new_loc = urlunsplit(
            (
                split.scheme,
                split.netloc,
                split.path,
                urlencode(dict(token="DUMMY_TOKEN")),
                None,
            )
        )
        response["headers"]["Location"] = [new_loc]

    return response


# VCR arguments
vcr_kwargs = {
    # Filter out token query in URI
    "filter_query_parameters": [("token", "DUMMY_TOKEN")],
    "before_record_response": before_record_response,
    "decode_compressed_response": True,
}

# Prepare a global Ozon3 object
WAQI_TOKEN = config("WAQI_TOKEN", default="DUMMY_TOKEN")
with vcr.use_cassette("tests/cassettes/ozon3_init.yaml", **vcr_kwargs):
    api = Ozon3(WAQI_TOKEN)  # type: ignore
