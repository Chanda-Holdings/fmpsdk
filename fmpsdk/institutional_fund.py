import typing

from pydantic import RootModel

from .models import *
from .settings import DEFAULT_LIMIT, SEC_RSS_FEEDS_FILENAME
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def sec_rss_feeds(
    apikey: str,
    limit: int = DEFAULT_LIMIT,
    filename: str = SEC_RSS_FEEDS_FILENAME,
) -> typing.Union[typing.List[typing.Dict], None]:
    """
    Query FMP /rss_feed/ API.

    :param apikey: Your API key.
    :param limit: Number of rows to return.
    :param filename: Name of saved file.
    :return: A list of dictionaries.
    """
    path = "rss_feed"
    query_vars = {"apikey": apikey}
    query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def institutional_ownership_latest(
    apikey: str,
    page: int = 0,
    limit: int = 100,
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
    path = "/stable/institutional-ownership/latest"
    query_vars = {"apikey": apikey, "page": page, "limit": limit}
    return __return_json_stable(path, query_vars)


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
    path = "/stable/institutional-ownership/extract"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    return __return_json_stable(path, query_vars)


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
    path = "/institutional-ownership/dates"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holder_industry_breakdown(
    apikey: str, cik: str, year: int, quarter: int
) -> RootModel[typing.List[FMPHolderIndustryBreakdown]]:
    """
    Get institutional ownership holder industry breakdown for a CIK, year, and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    Returns
    -------
    list
        List of holder industry breakdown data.
    """
    path = "/institutional-ownership/holder-industry-breakdown"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_industry_summary(
    apikey: str, year: int, quarter: int
) -> RootModel[typing.List[FMPIndustryPerformanceSummary]]:
    """
    Get institutional ownership industry summary for a year and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    Returns
    -------
    list
        List of industry summary data.
    """
    path = "/institutional-ownership/industry-summary"
    query_vars = {"apikey": apikey, "year": year, "quarter": quarter}
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holdings_portfolio_changes(
    apikey: str, cik: str, year: int, quarter: int, page: int = None, limit: int = None
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership holdings portfolio changes for a CIK, year, and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of portfolio changes data.
    """
    path = "/institutional-ownership/holdings-portfolio-changes"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holdings_new_positions(
    apikey: str, cik: str, year: int, quarter: int, page: int = None, limit: int = None
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership holdings new positions for a CIK, year, and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of new positions data.
    """
    path = "/institutional-ownership/holdings-new-positions"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holdings_summary(
    apikey: str, cik: str, year: int, quarter: int, page: int = None, limit: int = None
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership holdings summary for a CIK, year, and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of holdings summary data.
    """
    path = "/institutional-ownership/holdings-summary"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holdings_overview(
    apikey: str, cik: str, year: int, quarter: int, page: int = None, limit: int = None
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership holdings overview for a CIK, year, and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of holdings overview data.
    """
    path = "/institutional-ownership/holdings-overview"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_holdings_sold_out_positions(
    apikey: str,
    cik: str,
    year: int,
    quarter: int,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership holdings sold out positions for a CIK, year,
    and quarter.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        CIK of the institutional holder.
    year : int
        Year of the filing period.
    quarter : int
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of sold out positions data.
    """
    path = "/institutional-ownership/holdings-sold-out-positions"
    query_vars = {"apikey": apikey, "cik": cik, "year": year, "quarter": quarter}
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def institutional_ownership_by_symbol(
    apikey: str,
    symbol: str,
    year: int = None,
    quarter: int = None,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[typing.Dict]]:
    """
    Get institutional ownership by symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Stock symbol.
    year : int, optional
        Year of the filing period.
    quarter : int, optional
        Quarter of the filing period (1, 2, 3, or 4).
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.
    Returns
    -------
    list
        List of institutional ownership data for the symbol.
    """
    path = "/institutional-ownership/by-symbol"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if year is not None:
        query_vars["year"] = year
    if quarter is not None:
        query_vars["quarter"] = quarter
    if page is not None:
        query_vars["page"] = page
    if limit is not None:
        query_vars["limit"] = limit
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_8k(apikey: str, symbol: str) -> RootModel[typing.List[Any]]:
    """
    Get SEC 8-K filings for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    Returns
    -------
    list
        List of SEC 8-K filings.
    """
    path = "/sec-filings-8k/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_financials(apikey: str, symbol: str) -> RootModel[typing.List[Any]]:
    """
    Get SEC financial filings for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    Returns
    -------
    list
        List of SEC financial filings.
    """
    path = "/sec-filings-financials/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_search_form_type(
    apikey: str, form_type: str
) -> RootModel[typing.List[Any]]:
    """
    Search SEC filings by form type.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    form_type : str
        SEC form type (e.g., '10-K').
    Returns
    -------
    list
        List of SEC filings for the form type.
    """
    path = "/sec-filings-search/form-type/{form_type}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_search_symbol(apikey: str, symbol: str) -> RootModel[typing.List[Any]]:
    """
    Search SEC filings by symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    Returns
    -------
    list
        List of SEC filings for the symbol.
    """
    path = "/sec-filings-search/symbol/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_company_search_name(
    apikey: str, name: str
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Search SEC filings by company name.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Company name.
    Returns
    -------
    list
        List of SEC filings for the company name.
    """
    path = "/sec-filings-company-search/name/{name}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_company_search_symbol(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Search SEC filings by company symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    Returns
    -------
    list
        List of SEC filings for the company symbol.
    """
    path = "/sec-filings-company-search/symbol/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_filings_company_search_cik(
    apikey: str, cik: str
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Search SEC filings by company CIK.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Company CIK.
    Returns
    -------
    list
        List of SEC filings for the company CIK.
    """
    path = "/sec-filings-company-search/cik/{cik}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def sec_profile(
    apikey: str, symbol: str = None, cik: str = None
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Get SEC profile for a given symbol or CIK.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str, optional
        Ticker symbol (e.g., 'AAPL').
    cik : str, optional
        Central Index Key (CIK).
    Returns
    -------
    list
        SEC profile data.
    """
    path = "/sec-profile/{symbol}" if symbol else "/sec-profile"
    query_vars = {"apikey": apikey}
    if cik:
        query_vars["cik"] = cik
    return __return_json_stable(path, query_vars)
