import typing

from pydantic import RootModel

from .models import FMPCommodity
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def commodity_list(apikey: str) -> RootModel[typing.List[FMPCommodity]]:
    """
    Query FMP /commodity-list endpoint.

    :param apikey: Your API key.
    :return: List of commodities.
    """
    path = "commodities-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
