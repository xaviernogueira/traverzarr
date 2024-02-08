from typing import Literal, Optional, get_args
from .schema import ZarrGroupJSON

SearchTypes = Literal['contains', 'startswith', 'endswith', 'regex']
SearchAlgos = Literal['depth_first', 'breadth_first']

def search_zarr_group(
    zarr_group: ZarrGroupJSON, 
    pattern: str,
    how: Optional[SearchTypes],
    algo: Optional[SearchAlgos],
) -> ZarrGroupJSON:
    """Searches for string patterns in sub-group href.

    Args:
        zarr_group: The ZarrGroupJSON object to search.
        pattern: The string pattern to search for.
        how: The search algorithm to use.
        algo: The search algorithm to use.

    Returns:
        The ZarrGroupJSON object that contains the pattern.
    """
    if not isinstance(zarr_group, ZarrGroupJSON):
        raise ValueError('zarr_group must be a ZarrGroupJSON object')
    if not isinstance(pattern, str):
        raise ValueError('pattern must be a string')
    if how not in get_args(SearchTypes):
        raise ValueError(f'how must be one of {SearchTypes}')
    if algo not in get_args(SearchAlgos):
        raise ValueError(f'algo must be one of {SearchAlgos}')

    return ZarrGroupJSON

