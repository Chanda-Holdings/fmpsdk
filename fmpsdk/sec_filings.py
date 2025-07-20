import typing
from typing import Any

from pydantic import RootModel

from .models import (
    FMPCompanyProfile,
    FMPCompanySECFilings,
    FMPIndustryClassification,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def sec_filings_8k(
    apikey: str, from_date: str, to_date: str, page: int = None, limit: int = None
) -> RootModel[typing.List[Any]]:
    """
    Get SEC 8-K filings for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str
        Start date for the filings (format: 'YYYY-MM-DD').
    to_date : str
        End date for the filings (format: 'YYYY-MM-DD').
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).
    Returns
    -------
    list
        List of SEC 8-K filings.
    """
    path = "sec-filings-8k"
    query_vars = {"apikey": apikey, "from": from_date, "to": to_date}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_financials(
    apikey: str, from_date: str, to_date: str, page: int = None, limit: int = None
) -> RootModel[typing.List[Any]]:
    """
    Get SEC financial filings for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str
        Start date for the filings (format: 'YYYY-MM-DD').
    to_date : str
        End date for the filings (format: 'YYYY-MM-DD').
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).
    Returns
    -------
    list
        List of SEC financial filings.
    """
    path = "sec-filings-financials"
    query_vars = {"apikey": apikey, "from": from_date, "to": to_date}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_search_form_type(
    apikey: str,
    form_type: str,
    from_date: str,
    to_date: str,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[Any]]:
    """
    Search SEC filings by form type.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    form_type : str
        SEC form type (e.g., '10-K').
    from_date : str
        Start date for the filings (format: 'YYYY-MM-DD').
    to_date : str
        End date for the filings (format: 'YYYY-MM-DD').
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).
    Returns
    -------
    list
        List of SEC filings for the form type.
    """
    path = "sec-filings-search/form-type"
    query_vars = {
        "apikey": apikey,
        "from": from_date,
        "to": to_date,
        "formType": form_type,
    }
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_search_symbol(
    apikey: str,
    symbol: str,
    from_date: str,
    to_date: str,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[Any]]:
    """
    Search SEC filings by symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    from_date : str
        Start date for the filings (format: 'YYYY-MM-DD').
    to_date : str
        End date for the filings (format: 'YYYY-MM-DD').
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).

    Returns
    -------
    list
        List of SEC filings for the symbol.
    """
    path = "sec-filings-search/symbol"
    query_vars = {
        "apikey": apikey,
        "symbol": symbol,
        "from": from_date,
        "to": to_date,
    }
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_search_cik(
    apikey: str,
    cik: str,
    from_date: str,
    to_date: str,
    page: int = None,
    limit: int = None,
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Search SEC filings by company CIK.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Company CIK.
    from_date : str
        Start date for the filings (format: 'YYYY-MM-DD').
    to_date : str
        End date for the filings (format: 'YYYY-MM-DD').
    page : int, optional
        Page number for pagination (default is None).
    limit : int, optional
        Number of results per page (default is None).

    Returns
    -------
    list
        List of SEC filings for the company CIK.
    """
    path = "sec-filings-search/cik"
    query_vars = {
        "apikey": apikey,
        "cik": cik,
        "from": from_date,
        "to": to_date,
    }
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_company_search_name(
    apikey: str, company: str
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Search SEC filings by company name.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    company : str, optional
        Company name.

    Returns
    -------
    list
        List of SEC filings for the company name.
    """
    path = "sec-filings-company-search/name"
    query_vars = {"apikey": apikey, "company": company}

    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_filings_company_search_symbol(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPCompanySECFilings]]:
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
    path = "sec-filings-company-search/symbol"
    query_vars = {"apikey": apikey, "symbol": symbol}

    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


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
    path = "sec-filings-company-search/cik"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def sec_profile(
    apikey: str, symbol: str, cik_A: str = None
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Get SEC profile for a given symbol or CIK.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    cik : str, optional
        Central Index Key (CIK).
    Returns
    -------
    list
        SEC profile data.
    """
    path = "sec-profile"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if cik_A:
        query_vars["cik-A"] = cik_A
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def industry_classification_list(
    apikey: str, industry_title: str = None, sic_code: str = None
) -> RootModel[typing.List[FMPIndustryClassification]]:
    """
    Get a list of industry classifications.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    industry_title : str, optional
        Industry title to filter by.
    sic_code : str, optional
        SIC code to filter by.

    Returns
    -------
    list
        List of industry classifications.
    """
    path = "standard-industrial-classification-list"
    query_vars = {"apikey": apikey}
    if industry_title:
        query_vars["industry_title"] = industry_title
    if sic_code:
        query_vars["sic_code"] = sic_code
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def industry_classification_search(
    apikey: str,
    symbol: str = None,
    cik: str = None,
    sicCode: str = None,
) -> RootModel[typing.List[FMPIndustryClassification]]:
    """
    Search industry classification by symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str, optional
        Ticker symbol (e.g., 'AAPL').
    cik : str, optional
        Central Index Key (CIK).
    sicCode : str, optional
        SIC code.

    Returns
    -------
    list
        List of industry classifications for the symbol.
    """
    path = "industry-classification-search"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if cik:
        query_vars["cik"] = cik
    if sicCode:
        query_vars["sicCode"] = sicCode
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def industry_classification_all(
    apikey: str, page: str = None, limit: str = None
) -> RootModel[typing.List[FMPIndustryClassification]]:
    """
    Get all industry classifications.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : str, optional
        Page number for pagination.
    limit : str, optional
        Number of results per page.

    Returns
    -------
    list
        List of industry classifications.
    """
    path = "all-industry-classification"
    query_vars = {"apikey": apikey}
    if page:
        query_vars["page"] = str(page)
    if limit:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
