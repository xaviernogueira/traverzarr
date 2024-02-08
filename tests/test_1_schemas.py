import pytest
from pathlib import Path
import traverzarr



def test_group_schema(test_json_path, zarr_json_dict: dict) -> None:
    zarr = traverzarr.read_zarr_group_json(test_json_path)
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
