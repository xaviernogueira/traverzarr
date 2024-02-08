import pytest
import traverzarr

@pytest.fixture
def zarr_group(test_json_path) -> None:
    return traverzarr.read_zarr_group_json(test_json_path)
 
def test_import() -> None:
    assert traverzarr.search.search_zarr_group
    assert traverzarr.search_zarr_group

