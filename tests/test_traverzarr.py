import pytest
import json
import sys
from pathlib import Path
from traverzarr.schema import (
    ZarrLink,
    ZarrGroupJSON,
    ZarrArrayJSON,
    read_zarr_group_json, 
)

TEST_DATA = Path(__file__).parent / "test_data"


@pytest.fixture
def zarr_json() -> dict:
    return json.loads((TEST_DATA / "zarr.json").read_text())


def test_group_schema(zarr_json: dict) -> None:
    zarr = read_zarr_group_json(TEST_DATA / "zarr.json")
    assert zarr.attributes == zarr_json["attributes"]
    assert zarr.zarr_format == zarr_json["zarr_format"]
    assert zarr.node_type == zarr_json["node_type"]
    assert zarr.links == [ZarrLink(**link) for link in zarr_json["links"]]
    
    assert isinstance(zarr.href, Path)
    assert bool(zarr.href)
    
    # the root and parent aren't in our test dir
    with pytest.raises(ValueError):
        zarr.root

    with pytest.raises(ValueError):
        zarr.parent

    groups_list = list(zarr.groups)
    assert len(groups_list) == 1
    assert isinstance(groups_list[0], ZarrGroupJSON)

    arrays_list = list(zarr.arrays)
    assert len(arrays_list) == 1
    assert isinstance(arrays_list[0], ZarrArrayJSON)

