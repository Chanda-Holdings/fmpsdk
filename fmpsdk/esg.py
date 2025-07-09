import typing

from pydantic import RootModel

from .models import (
    FMPESGBenchmark,
    FMPESGFiling,
    FMPESGRating,
)
from .url_methods import (
    __return_json,
)
from .utils import parse_response


@parse_response
def esg_disclosures(apikey: str, symbol: str) -> RootModel[typing.List[FMPESGFiling]]:
    """
    Get ESG disclosures for a given symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of ESG disclosures.
    """
    path = "esg-disclosures"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def esg_ratings(apikey: str, symbol: str) -> RootModel[typing.List[FMPESGRating]]:
    """
    Get ESG ratings for a given symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of ESG ratings.
    """
    path = "esg-ratings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def esg_benchmark(
    apikey: str, year: str = None
) -> RootModel[typing.List[FMPESGBenchmark]]:
    """
    Get ESG benchmark data for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str, optional
        The year for which to retrieve ESG benchmark data (e.g., '2023').

    Returns
    -------
    list
        List of ESG benchmark data.
    """
    path = "esg-benchmark"
    query_vars = {"apikey": apikey}
    if year:
        query_vars["year"] = year
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
