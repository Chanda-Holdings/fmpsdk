import typing

from pydantic import RootModel

from .models import FMPPressRelease
from .settings import DEFAULT_LIMIT
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def company_news(
    apikey: str,
    symbols: typing.Union[str, typing.List] = "",
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /news/stock/ API.

    :param apikey: Your API key.
    :param symbols: List of ticker symbols.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "news/stock"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if symbols:
        if type(symbols) is list:
            symbols = ",".join(symbols)
        query_vars["symbols"] = symbols
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def company_news_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /news/stock-latest/ API.

    :param apikey: Your API key.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "news/stock-latest"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def company_press_releases(
    apikey: str,
    symbols: typing.Union[str, typing.List] = "",
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /news/press-releases/ API.

    :param apikey: Your API key.
    :param symbols: List of ticker symbols.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "news/press-releases"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if symbols:
        if type(symbols) is list:
            symbols = ",".join(symbols)
        query_vars["symbols"] = symbols
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def company_press_releases_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /news/press-releases-latest/ API.

    :param apikey: Your API key.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "news/press-releases-latest"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def news_general_latest(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest general news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest general news.
    """
    path = "/news/general-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_press_releases_latest(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest press releases news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest press releases news.
    """
    path = "/news/press-releases-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_stock_latest(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest stock news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest stock news.
    """
    path = "/news/stock-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_crypto_latest(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest crypto news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest crypto news.
    """
    path = "/news/crypto-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_forex_latest(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest forex news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of latest forex news.
    """
    path = "/news/forex-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_press_releases(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get press releases news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of press releases news.
    """
    path = "/news/press-releases"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def news_forex(apikey: str) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get forex news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of forex news.
    """
    path = "/news/forex"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)
