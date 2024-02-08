import pytest
import json
from pathlib import Path
import traverzarr

TEST_DATA = Path(__file__).parent / "test_data"


@pytest.fixture
def test_json_path() -> Path:
    return TEST_DATA / "zarr.json"


@pytest.fixture
def zarr_json_dict(test_json_path) -> dict:
    return json.loads((test_json_path).read_text())


def test_imports() -> None:
    assert traverzarr.read_zarr_group_json
    assert traverzarr.read_zarr_array_json
    assert traverzarr.schema.ZarrGroupJSON
    assert traverzarr.schema.ZarrArrayJSON
    assert traverzarr.schema.ZarrLink


def test_group_schema(zarr_json_dict: dict) -> None:
    zarr = traverzarr.read_zarr_group_json(TEST_DATA / "zarr.json")
    assert zarr.attributes == zarr_json_dict["attributes"]
    assert zarr.zarr_format == zarr_json_dict["zarr_format"]
    assert zarr.node_type == zarr_json_dict["node_type"]
    assert all([isinstance(link, traverzarr.schema.ZarrLink) for link in zarr.links])

    assert isinstance(zarr.href, Path)
    assert bool(zarr.href)

    # the root and parent aren't in our test dir
    with pytest.raises(ValueError):
        zarr.root

    with pytest.raises(ValueError):
        zarr.parent

    groups_list = list(zarr.groups)
    assert len(groups_list) == 1
    assert isinstance(groups_list[0], traverzarr.schema.ZarrGroupJSON)

    arrays_list = list(zarr.arrays)
    assert len(arrays_list) == 1
    assert isinstance(arrays_list[0], traverzarr.schema.ZarrArrayJSON)
