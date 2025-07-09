import typing

from pydantic import RootModel

from .models import FMPCryptocurrencyListItem
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def cryptocurrency_list(
    apikey: str,
) -> RootModel[typing.List[FMPCryptocurrencyListItem]]:
    """
    Query FMP /cryptocurrency-list endpoint.

    :param apikey: Your API key.
    :return: List of all cryptocurrencies.
    """
    path = "cryptocurrency-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)
