from pydantic import BaseModel, Field
from attr import frozen
from typing import Literal
from enum import IntEnum

class ZarrVersions(IntEnum):
    v1 = 1
    v2 = 2
    v3 = 3

class ZarrLink(BaseModel):
    href: str
    rel: Literal['root', 'parent', 'self', 'array', 'group']

class ZarrJSON(BaseModel):
    """Used to verify that the input is a valid Zarr JSON"""
    attributes: dict
    zarr_format: ZarrVersions

    # what are the different node_types
    node_type: str
    links: list[ZarrLink]


class ZarrTraverser:

    def __init__(self, zarr_json: ZarrJSON):
        if not isinstance(zarr_json, ZarrJSON):
            raise ValueError('zarr_json must be a ZarrJSON object')
        self.attributes = zarr_json.attributes


