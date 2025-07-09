import typing

from pydantic import RootModel

from .models import FMPForexPair
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def forex_list(apikey: str) -> RootModel[typing.List[FMPForexPair]]:
    """
    Query FMP /forex-list/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "forex-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
