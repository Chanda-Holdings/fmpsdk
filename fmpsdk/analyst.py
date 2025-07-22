import typing

from pydantic import RootModel

from .models import (
    FMPAnalystEstimates,
    FMPHistoricalRating,
    FMPHistoricalRatingV3,
    FMPHistoricalStockGrade,
    FMPPriceTargetConsensus,
    FMPPriceTargetSummary,
    FMPRatingSnapshot,
    FMPStockGrade,
    FMPStockGradeSummary,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def analyst_estimates(
    apikey: str, symbol: str, period: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPAnalystEstimates]]:
    """
    Get analyst estimates using the /stable/analyst-estimates endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get analyst estimates for.
        period (str): The period for estimates ('annual' or 'quarter').
        page (int, optional): Page number for pagination.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with analyst estimates.
    """
    path = "analyst-estimates"
    query_vars = {"apikey": apikey, "symbol": symbol, "period": period}
    if limit:
        query_vars["limit"] = str(limit)
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ratings_snapshot(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPRatingSnapshot]]:
    """
    Get ratings snapshot using the /stable/ratings-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get ratings for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with ratings snapshot.
    """
    path = "ratings-snapshot"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ratings_historical(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPHistoricalRating]]:
    """
    Get historical ratings using the /stable/ratings-historical endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get historical ratings for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with historical ratings.
    """
    path = "ratings-historical"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def ratings_historical_v3(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPHistoricalRatingV3]]:
    """
    Get historical ratings using the /v3/historical-rating endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get historical ratings for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with historical ratings.
    """
    path = f"historical-rating/{symbol}"
    query_vars = {"apikey": apikey}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars, version="v3")  # type: ignore[no-any-return]


@parse_response
def price_target_summary(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPPriceTargetSummary]]:
    """
    Get price target summary using the /stable/price-target-summary endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target summary for.
    Returns:
        List of dictionaries with price target summary.
    """
    path = "price-target-summary"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def price_target_consensus(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPPriceTargetConsensus]]:
    """
    Get price target consensus using the /stable/price-target-consensus endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target consensus for.
    Returns:
        List of dictionaries with price target consensus.
    """
    path = "price-target-consensus"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def stock_grades(apikey: str, symbol: str) -> RootModel[typing.List[FMPStockGrade]]:
    """
    Get stock grades using the /stable/grades endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get stock grades for.
    Returns:
        List of dictionaries with stock grades.
    """
    path = "grades"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_stock_grades(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPHistoricalStockGrade]]:
    """
    Get historical stock grades using the /stable/grades-historical endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get historical stock grades for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with historical stock grades.
    """
    path = "grades-historical"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def stock_grades_summary(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPStockGradeSummary]]:
    """
    Get stock grades summary using the /stable/grades-consensus endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get stock grades summary for.
    Returns:
        List of dictionaries with stock grades summary.
    """
    path = "grades-consensus"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
