import pytest
import json
import sys
from pathlib import Path
from traverzarr.schema import (
    ZarrLink,
    ZarrJSON,
)

TEST_DATA = Path(__file__).parent / 'test_data'


@pytest.fixture
def zarr_json() -> dict:
    return json.loads((TEST_DATA / 'zarr.json').read_text())


def test_schema(zarr_json: dict) -> None:
    zarr = ZarrJSON(**zarr_json)
    assert zarr.attributes == zarr_json['attributes']
    assert zarr.zarr_format == zarr_json['zarr_format']
    assert zarr.node_type == zarr_json['node_type']
    assert zarr.links == [ZarrLink(**link) for link in zarr_json['links']]

