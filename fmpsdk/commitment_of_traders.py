import typing

from pydantic import RootModel

from .models import (
    FMPCommitmentOfTradersAnalysis,
    FMPCommitmentOfTradersReport,
    FMPSymbolAndNameList,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def commitment_of_traders_report(
    apikey: str, symbol: str = None, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPCommitmentOfTradersReport]]:
    """
    Get Commitment of Traders report for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str, optional
        The ticker symbol (e.g., 'ES').
    from_date : str, optional
        Start date (YYYY-MM-DD)
    to_date : str, optional
        End date (YYYY-MM-DD)

    Returns
    -------
    FmpCommitmentOfTradersReportResponse
        Commitment of Traders report data as a Pydantic model.
    """
    path = "commitment-of-traders-report"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)


@parse_response
def commitment_of_traders_report_analysis(
    apikey: str, symbol: str = None, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPCommitmentOfTradersAnalysis]]:
    """
    Get Commitment of Traders report analysis for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str, optional
        The ticker symbol (e.g., 'ES').
    from_date : str, optional
        Start date (YYYY-MM-DD)
    to_date : str, optional
        End date (YYYY-MM-DD)

    Returns
    -------
    FmpCommitmentOfTradersAnalysisResponse
        Commitment of Traders report analysis data as a Pydantic model.
    """
    path = "commitment-of-traders-analysis"
    query_vars = {"apikey": apikey}
    if symbol:
        query_vars["symbol"] = symbol
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)


@parse_response
def commitment_of_traders_report_list(
    apikey: str,
) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Get a list of available Commitment of Traders reports.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCommitmentOfTradersListResponse
        List of available Commitment of Traders reports as a Pydantic model.
    """
    path = "commitment-of-traders-list"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
