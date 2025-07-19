import typing

from pydantic import RootModel

from .models import (
    FMPForm13FDate,
    FMPForm13FExtract,
    FMPForm13FFiling,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def institutional_ownership_latest(
    apikey: str,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPForm13FFiling]]:
    """
    Get latest institutional ownership filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int
        Page number for pagination.
    limit : int
        Number of results per page.
    Returns
    -------
    list
        List of latest institutional ownership filings.
    """
    path = "institutional-ownership/latest"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_extract(
    apikey: str,
    cik: str,
    year: int,
    quarter: int,
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional investor.
    year : int
        Year of the filing.
    quarter : int
        Quarter of the filing (1, 2, 3, or 4).
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/extract"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_dates(
    apikey: str, cik: str
) -> RootModel[typing.List[FMPForm13FDate]]:
    """
    Get available institutional ownership dates for a CIK.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional investor.
    Returns
    -------
    list
        List of available institutional ownership dates.
    """
    path = "institutional-ownership/dates"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_extract_analytics_by_holder(
    apikey: str,
    symbol: str,
    year: int,
    quarter: int,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol of the company.
    year : int
        Year of the filing.
    quarter : int
        Quarter of the filing (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page. Default is 100.
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/extract-analytics/holder"
    query_vars = {"apikey": apikey, "symbol": symbol, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_holder_performance_summary(
    apikey: str, cik: str, page: int = None
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional investor.
    page : int, optional
        Page number for pagination.
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/holder-performance-summary"
    query_vars = {"apikey": apikey, "cik": cik}
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_holder_industry_breakdown(
    apikey: str, cik: str, year: int, quarter: int
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional investor.
    year : int
        Year of the filing.
    quarter : int
        Quarter of the filing (1, 2, 3, or 4).
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/holder-industry-breakdown"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_positions_summary(
    apikey: str, symbol: str, year: int, quarter: int
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol of the institutional investor.
    year : int
        Year of the filing.
    quarter : int
        Quarter of the filing (1, 2, 3, or 4).
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/symbol-positions-summary"
    query_vars = {"apikey": apikey, "symbol": symbol, "year": year, "quarter": quarter}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def institutional_ownership_industry_summary(
    apikey: str, year: int, quarter: int
) -> RootModel[typing.List[FMPForm13FExtract]]:
    """
    Extract detailed data from Form 13F filings.
    Parameters
    ----------
    apikey : str
        Your FMP API key
    year : int
        Year of the filing.
    quarter : int
        Quarter of the filing (1, 2, 3, or 4).
    Returns
    -------
    list
        Extracted data from Form 13F filings.
    """
    path = "institutional-ownership/industry-summary"
    query_vars = {"apikey": apikey, "year": year, "quarter": quarter}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
