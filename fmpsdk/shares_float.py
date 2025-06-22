import typing

from pydantic import RootModel

from .models import FMPAllShareFloat, FMPShareFloat
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def shares_float(apikey: str, symbol: str) -> RootModel[typing.List[FMPShareFloat]]:
    """
    Query FMP /shares-float endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :return: List of shares float data.
    """
    path = f"shares-float/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def shares_float_all(apikey: str) -> RootModel[typing.List[FMPAllShareFloat]]:
    """
    Query FMP /shares-float-all endpoint.
    :param apikey: Your API key.
    :return: List of shares float data for all companies.
    """
    path = "shares-float-all"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)
