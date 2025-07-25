import typing

from pydantic import RootModel

from .models import FMPPoliticalTrade
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def senate_latest(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get latest Senate trading disclosures.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).

    Returns
    -------
    list
        List of latest Senate trading disclosures.
    """
    path = "senate-latest"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def house_latest(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get latest House trading disclosures.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).

    Returns
    -------
    list
        List of latest House trading disclosures.
    """
    path = "house-latest"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def senate_trades(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get all Senate trades.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Stock symbol to search for.

    Returns
    -------
    list
        List of all Senate trades.
    """
    path = "senate-trades"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


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
    path = "senate-trades-by-name"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def house_trades(apikey: str, symbol: str) -> RootModel[typing.List[FMPPoliticalTrade]]:
    """
    Get all House trades.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Stock symbol to search for.

    Returns
    -------
    list
        List of all House trades.
    """
    path = "house-trades"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


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
    path = "house-trades-by-name"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


# Create class-like wrappers for backwards compatibility with tests
class SenateFunctions:
    """Wrapper class to provide dot notation access to senate functions."""

    @staticmethod
    def senate_latest(*args, **kwargs):
        return senate_latest(*args, **kwargs)

    @staticmethod
    def senate_trades(*args, **kwargs):
        return senate_trades(*args, **kwargs)

    @staticmethod
    def senate_trades_by_name(*args, **kwargs):
        return senate_trades_by_name(*args, **kwargs)

    @staticmethod
    def house_latest(*args, **kwargs):
        return house_latest(*args, **kwargs)

    @staticmethod
    def house_trades(*args, **kwargs):
        return house_trades(*args, **kwargs)

    @staticmethod
    def house_trades_by_name(*args, **kwargs):
        return house_trades_by_name(*args, **kwargs)


class HouseFunctions:
    """Wrapper class to provide dot notation access to house functions."""

    @staticmethod
    def house_latest(*args, **kwargs):
        return house_latest(*args, **kwargs)

    @staticmethod
    def house_trades(*args, **kwargs):
        return house_trades(*args, **kwargs)

    @staticmethod
    def house_trades_by_name(*args, **kwargs):
        return house_trades_by_name(*args, **kwargs)


# Create instances for backwards compatibility
senate = SenateFunctions()
house = HouseFunctions()
