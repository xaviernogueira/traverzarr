import pytest
import json
import traverzarr
from pathlib import Path

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

