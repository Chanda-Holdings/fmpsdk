import typing

from pydantic import RootModel

from .models import FMPNewsArticle, FMPPriceTargetNews, FMPStockGradeNews
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def news_stock_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
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
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def company_press_releases_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Query FMP /news/press-releases/ API.

    :param apikey: Your API key.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "news/press-releases-latest"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def news_general_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
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
        Page number.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    list
        List of latest general news.
    """
    path = "news/general-latest"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)


@parse_response
def news_crypto_latest(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
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
    page : int
        Page number.
    limit : int
        Number of rows to return.

    Returns
    -------
    list
        List of latest crypto news.
    """
    path = "news/crypto-latest"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path, query_vars)


@parse_response
def news_forex(
    apikey: str,
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
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
    page : int
        Page number.
    limit : int
        Number of rows to return.

    Returns
    -------
    list
        List of latest forex news.
    """
    path = "news/forex-latest"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path, query_vars)


@parse_response
def price_target_news(
    apikey: str, symbol: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPPriceTargetNews]]:
    """
    Get price target news using the /stable/price-target-news endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target news for.
        page (int, optional): Page number for pagination.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with price target news.
    """
    path = "price-target-news"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)


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


@parse_response
def news_stock(
    apikey: str,
    symbols: typing.List[str],
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Query FMP /news/stock-latest/ API.

    :param apikey: Your API key.
    :param symbols: List of stock symbols (e.g., ['AAPL', 'GOOGL']).
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    symbols_str = ",".join(symbols)
    path = "news/stock"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def company_press_releases(
    apikey: str,
    symbols: typing.List[str],
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Query FMP /news/press-releases/ API.

    :param apikey: Your API key.
    :param symbols: List of stock symbols to get press releases for.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    symbols_str = ",".join(symbols)
    path = "news/press-releases"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def news_crypto(
    apikey: str,
    symbols: typing.List[str],
    from_date: str = None,
    to_date: str = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPNewsArticle]]:
    """
    Get latest crypto news.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : typing.List[str]
        List of crypto symbols (e.g., ['BTC', 'ETH']).
    from_date : str, optional
        The starting time for the API ("yyyy-mm-dd").
    to_date : str, optional
        The ending time for the API ("yyyy-mm-dd").
    page : int
        Page number.
    limit : int
        Number of rows to return.

    Returns
    -------
    list
        List of latest crypto news.
    """
    symbols_str = ",".join(symbols)
    path = "news/crypto"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path, query_vars)


@parse_response
def stock_grade_news(
    apikey: str, symbol: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPStockGradeNews]]:
    """
    Get stock grade news using the /stable/grades-news endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get stock grade news for.
        page (int, optional): Page number for pagination.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with stock grade news.
    """
    path = "grades-news"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def stock_grade_latest_news(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPStockGradeNews]]:
    """
    Get latest stock grade news using the /stable/grades-latest-news endpoint.

    Parameters:
        apikey (str): Your API key.
        page (int, optional): Page number for pagination.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with latest stock grade news.
    """
    path = "grades-latest-news"
    query_vars = {"apikey": apikey}
    if limit:
        query_vars["limit"] = str(limit)
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)
