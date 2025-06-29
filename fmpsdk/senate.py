import typing

from pydantic import RootModel

from .models import FMPPoliticalTrade
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def senate_latest(
    apikey: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get latest Senate trading disclosures.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest Senate trading disclosures.
    """
    path = "/senate-latest"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def house_latest(
    apikey: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get latest House trading disclosures.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest House trading disclosures.
    """
    path = "/house-latest"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def senate_trades(
    apikey: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get all Senate trades.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of all Senate trades.
    """
    path = "/senate-trades"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def senate_trades_by_name(
    apikey: str,
    name: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get Senate trades by name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Name of the Senator.

    Returns
    -------
    list
        List of Senate trades for the given name.
    """
    path = f"/senate-trades-by-name/{name}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def house_trades(
    apikey: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get all House trades.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of all House trades.
    """
    path = "/house-trades"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def house_trades_by_name(
    apikey: str,
    name: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get House trades by name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Name of the House member.

    Returns
    -------
    list
        List of House trades for the given name.
    """
    path = f"/house-trades-by-name/{name}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def senate_trades_by_symbol(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get Senate trades by symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Stock symbol to search for.

    Returns
    -------
    list
        List of Senate trades for the given symbol.
    """
    path = f"/senate-trades-by-symbol/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def house_trades_by_symbol(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get House trades by symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Stock symbol to search for.

    Returns
    -------
    list
        List of House trades for the given symbol.
    """
    path = f"/house-trades-by-symbol/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
