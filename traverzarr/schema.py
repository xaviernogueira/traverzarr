import json
from pydantic import BaseModel
from typing import Literal, Iterable
from enum import IntEnum
from pathlib import Path


class ZarrVersions(IntEnum):
    v1 = 1
    v2 = 2
    v3 = 3


class ZarrLink(BaseModel):
    href: str
    rel: Literal["root", "parent", "self", "array", "group"]


class ZarrGroupJSON(BaseModel):
    """Used to verify that the input is a valid Zarr JSON"""

    attributes: dict
    zarr_format: ZarrVersions
    parent_dir: Path
    node_type: Literal["group"]
    links: list[ZarrLink]

    @property
    def groups(self) -> Iterable["ZarrGroupJSON"]:
        for group in filter(lambda x: x.rel == "group", self.links):
            link_href = self.parent_dir / Path(group.href)
            if not link_href.exists():
                raise ValueError(f"Group link does not exist: {link_href}")
            yield read_zarr_group_json(link_href)

    @property
    def arrays(self) -> Iterable["ZarrArrayJSON"]:
        if self.node_type == "array":
            raise ValueError("Zarr arrays cannot contain sub-arrays!")
        for array in filter(lambda x: x.rel == "array", self.links):
            link_href = self.parent_dir / Path(array.href)
            if not link_href.exists():
                raise ValueError(f"Array link does not exist: {link_href}")
            yield read_zarr_array_json(link_href)

    @property
    def href(self) -> Path:
        for link in self.links:
            if link.rel == "self":
                return self.parent_dir / Path(link.href)
        raise ValueError("No self link found")

    @property
    def root(self) -> "ZarrGroupJSON":
        for link in self.links:
            if link.rel == "root":
                link_href = self.parent_dir / Path(link.href)
                if not link_href.exists():
                    raise ValueError(f"Root link does not exist: {link_href}")
                return read_zarr_group_json(link_href)
        raise ValueError("No root link found")

    @property
    def parent(self) -> "ZarrGroupJSON":
        for link in self.links:
            if link.rel == "parent":
                link_href = self.parent_dir / Path(link.href)
                if not link_href.exists():
                    raise ValueError(f"Parent link does not exist: {link_href}")
                return read_zarr_group_json(link_href)
        raise ValueError("No parent link found")


class ZarrArrayJSON(ZarrGroupJSON):
    node_type: Literal["array"]
    shape: list[int]
    data_type: str
    chunk_grid: dict
    chunk_key_encoding: dict
    fill_value: int | float | str | None
    codecs: list[dict]
    attributes: dict


def read_zarr_group_json(file_path: Path) -> ZarrGroupJSON:
    parent_dir = file_path.parent
    zarr_json = json.loads(file_path.read_text())
    return ZarrGroupJSON(**zarr_json, parent_dir=parent_dir)


def read_zarr_array_json(file_path: Path) -> ZarrArrayJSON:
    parent_dir = file_path.parent
    zarr_json = json.loads(file_path.read_text())
    return ZarrArrayJSON(**zarr_json, parent_dir=parent_dir)
