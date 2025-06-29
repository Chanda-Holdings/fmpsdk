import typing

from pydantic import RootModel

from .models import FMPNewsArticle
from .settings import DEFAULT_LIMIT
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def company_news(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPNewsArticle]]:
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

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def company_press_releases(
    apikey: str,
    symbols: typing.Union[str, typing.List] = "",
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPNewsArticle]]:
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

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def news_general(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Get latest general news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        The starting time for the API ("yyyy-mm-dd").
    to_date : str, optional
        The ending time for the API ("yyyy-mm-dd").
    page : int, optional
        Page number (default is 0).
    limit : int, optional
        Number of rows to return (default is DEFAULT_LIMIT).

    Returns
    -------
    list
        List of latest general news.
    """
    path = "/news/general-latest"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "page": page,
        "from": from_date,
        "to": to_date,
    }
    return __return_json(path, query_vars)


@parse_response
def news_crypto(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Get latest crypto news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        The starting time for the API ("yyyy-mm-dd").
    to_date : str, optional
        The ending time for the API ("yyyy-mm-dd").
    page : int, optional
        Page number (default is 0).
    limit : int, optional
        Number of rows to return (default is DEFAULT_LIMIT).

    Returns
    -------
    list
        List of latest crypto news.
    """
    path = "/news/crypto-latest"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "page": page,
        "from": from_date,
        "to": to_date,
    }
    return __return_json(path, query_vars)


@parse_response
def news_forex(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Get latest forex news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        The starting time for the API ("yyyy-mm-dd").
    to_date : str, optional
        The ending time for the API ("yyyy-mm-dd").
    page : int, optional
        Page number (default is 0).
    limit : int, optional
        Number of rows to return (default is DEFAULT_LIMIT).

    Returns
    -------
    list
        List of latest forex news.
    """
    path = "/news/forex-latest"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "page": page,
        "from": from_date,
        "to": to_date,
    }
    return __return_json(path, query_vars)


@parse_response
def price_target_latest_news(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Get latest price target news using the /stable/price-target-latest-news endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get latest price target news for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with latest price target news.
    """
    path = "price-target-latest-news"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)
