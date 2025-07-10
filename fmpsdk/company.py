import typing

from pydantic import RootModel

from .models import (
    FMPCompanyNote,
    FMPCompanyProfile,
    FMPDelistedCompany,
    FMPEmployeeCount,
    FMPExecutiveCompensation,
    FMPExecutiveProfile,
    FMPHistoricalEmployeeCount,
    FMPMarketCap,
    FMPMergerAcquisition,
    FMPShareFloat,
    FMPStockPeer,
)
from .url_methods import (
    __return_json,
)
from .utils import parse_response


@parse_response
def company_profile(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Retrieve the company profile for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpCompanyNameSearchResponse
        Company profile data as a Pydantic model.
    """
    path = "profile"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def company_profile_cik(
    apikey: str, cik: str
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Retrieve the company profile by Central Index Key (CIK).

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Central Index Key (CIK).

    Returns
    -------
    FmpCikSearchResponse
        Company profile data as a Pydantic model.
    """
    path = "profile-cik"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def company_notes(apikey: str, symbol: str) -> RootModel[typing.List[FMPCompanyNote]]:
    """
    Query FMP /company-notes endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :return: List of company notes.
    """
    path = "company-notes"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def stock_peers(apikey: str, symbol: str) -> RootModel[typing.List[FMPStockPeer]]:
    """
    Retrieve peer companies for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of peer companies as a Pydantic model.
    """
    path = "stock-peers"
    query_vars = {"symbol": symbol, "apikey": apikey}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def delisted_companies(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPDelistedCompany]]:
    """
    Retrieve a list of delisted companies.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results to return.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of delisted companies as a Pydantic model.
    """
    path = "delisted-companies"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def employee_count(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPEmployeeCount]]:
    """
    Retrieve employee count for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        The maximum number of results to return.

    Returns
    -------
    FmpFinancialEstimatesResponse
        Employee count data as a Pydantic model.
    """
    path = "employee-count"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_employee_count(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPHistoricalEmployeeCount]]:
    """
    Retrieve historical employee count for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        The maximum number of results to return.

    Returns
    -------
    FmpFinancialEstimatesResponse
        Historical employee count data as a Pydantic model.
    """
    path = "historical-employee-count"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def market_capitalization(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPMarketCap]]:
    """
    Retrieve the market capitalization for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpMarketCapitalizationResponse
        List of market capitalization data as a Pydantic model.
    """
    path = "market-capitalization"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def market_capitalization_batch(
    apikey: str, symbols: typing.List[str]
) -> RootModel[typing.List[FMPMarketCap]]:
    """
    Query FMP /market-capitalization-batch endpoint.
    :param apikey: Your API key.
    :param symbols: List of ticker symbols.
    :return: List of market capitalization data for the batch.
    """
    path = "market-capitalization-batch"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_market_capitalization(
    apikey: str,
    symbol: str,
    limit: int = None,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPMarketCap]]:
    """
    Retrieve historical market capitalization for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        Number of rows to return.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    FmpMarketCapitalizationResponse
        List of historical market capitalization data as a Pydantic model.
    """
    path = "historical-market-capitalization"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    if from_date is not None:
        query_vars["from"] = from_date
    if to_date is not None:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def shares_float(apikey: str, symbol: str) -> RootModel[typing.List[FMPShareFloat]]:
    """
    Query FMP /shares-float endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :return: List of shares float data.
    """
    path = "shares-float"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def shares_float_all(
    apikey: str, limit: int = None, page: int = None
) -> RootModel[typing.List[FMPShareFloat]]:
    """
    Query FMP /shares-float-all endpoint.
    :param apikey: Your API key.
    :param limit: Optional limit on the number of results.
    :param page: Optional page number for pagination.
    :return: List of shares float data for all companies.
    """
    path = "shares-float-all"
    query_vars = {"apikey": apikey}
    if limit is not None:
        query_vars["limit"] = str(limit)
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def mergers_acquisitions(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPMergerAcquisition]]:
    """
    Retrieve a list of mergers and acquisitions.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results to return.

    Returns
    -------
    FmpMergersAcquisitionsResponse
        List of mergers and acquisitions as a Pydantic model.
    """
    path = "mergers-acquisitions-latest"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def mergers_acquisitions_search(
    apikey: str, name: str
) -> RootModel[typing.List[FMPMergerAcquisition]]:
    """
    Retrieve a list of mergers and acquisitions.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        The name of the company or acquisition to search for.

    Returns
    -------
    FmpMergersAcquisitionsResponse
        List of mergers and acquisitions as a Pydantic model.
    """
    path = "mergers-acquisitions-latest"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def key_executives(
    apikey: str, symbol: str, active: bool = None
) -> RootModel[typing.List[FMPExecutiveProfile]]:
    """
    Retrieve key executives for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    active : bool, optional
        Filter for active executives only.

    Returns
    -------
    FMPExecutiveProfile
        List of key executives as a Pydantic model.
    """
    path = "key-executives"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if active is not None:
        query_vars["active"] = str(active)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def key_executives_compensation(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPExecutiveCompensation]]:
    """
    Retrieve key executives compensation for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FMPExecutiveCompensation
        List of key executives as a Pydantic model.
    """
    path = "governance-executive-compensation"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def executive_compensation_benchmark(
    apikey: str, year: str = None
) -> RootModel[typing.List[FMPExecutiveCompensation]]:
    """
    Retrieve key executives compensation for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str, optional
        The year for the compensation data (e.g., '2020').

    Returns
    -------
    FMPExecutiveCompensation
        List of key executives as a Pydantic model.
    """
    path = "executive-compensation-benchmark"
    query_vars = {"apikey": apikey}
    if year is not None:
        query_vars["year"] = year
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
