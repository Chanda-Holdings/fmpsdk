import typing

from pydantic import RootModel

from .models import *
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def commitment_of_traders_report(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPCommitmentOfTradersReport]]:
    """
    Get Commitment of Traders report for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
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
    path = "/commitment-of-traders-report/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path, query_vars)


@parse_response
def commitment_of_traders_report_analysis(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPCommitmentOfTradersAnalysis]]:
    """
    Get Commitment of Traders report analysis for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'ES').

    Returns
    -------
    FmpCommitmentOfTradersAnalysisResponse
        Commitment of Traders report analysis data as a Pydantic model.
    """
    path = "/commitment-of-traders-analysis/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


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
    path = "/commitment-of-traders-list"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def crowdfunding_offerings_latest(
    apikey: str,
) -> RootModel[typing.List[FMPCrowdfundingCampaign]]:
    """
    Get latest crowdfunding offerings.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        Latest crowdfunding offerings as a Pydantic model.
    """
    path = "/crowdfunding-offerings-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def crowdfunding_offerings_search(
    apikey: str, query: str
) -> RootModel[typing.List[FMPCrowdfundingSearch]]:
    """
    Search crowdfunding offerings by query string.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    query : str
        Search query string.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        Crowdfunding offerings matching the query as a Pydantic model.
    """
    path = "/crowdfunding-offerings-search/{query}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def crowdfunding_offerings(
    apikey: str,
) -> RootModel[typing.List[FMPCrowdfundingCampaign]]:
    """
    Get all crowdfunding offerings.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        All crowdfunding offerings as a Pydantic model.
    """
    path = "/crowdfunding-offerings"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def fundraising_latest(
    apikey: str,
) -> RootModel[typing.List[FMPEquityOffering]]:
    """
    Get latest fundraising data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpFundraisingResponse
        Latest fundraising data as a Pydantic model.
    """
    path = "/fundraising-latest"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def fundraising_search(
    apikey: str, query: str
) -> RootModel[typing.List[FMPEquityOfferingSearch]]:
    """
    Search fundraising data by query string.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    query : str
        Search query string.

    Returns
    -------
    FmpFundraisingResponse
        Fundraising data matching the query as a Pydantic model.
    """
    path = "/fundraising-search/{query}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def fundraising(
    apikey: str,
) -> RootModel[typing.List[FMPEquityOffering]]:
    """
    Get all fundraising data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpFundraisingResponse
        All fundraising data as a Pydantic model.
    """
    path = "/fundraising"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)
