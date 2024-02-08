import pytest
import traverzarr


@pytest.fixture
def zarr_group(test_json_path) -> traverzarr.schema.ZarrGroupJSON:
    return traverzarr.read_zarr_group_json(test_json_path)


def test_import() -> None:
    assert traverzarr.search.search_zarr_group
    assert traverzarr.search_zarr_group


def test_bad_inputs(zarr_group) -> None:
    with pytest.raises(ValueError):
        traverzarr.search_zarr_group("not_an_obj", "foo")

    with pytest.raises(ValueError):
        traverzarr.search_zarr_group(zarr_group, 109832)

    with pytest.raises(ValueError):
        traverzarr.search_zarr_group(zarr_group, "")

    with pytest.raises(ValueError):
        traverzarr.search_zarr_group(zarr_group, "foo", "bar")

    with pytest.raises(ValueError):
        traverzarr.search_zarr_group(zarr_group, "foo", "bar", "baz")
