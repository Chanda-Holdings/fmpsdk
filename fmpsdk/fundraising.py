import typing

from pydantic import RootModel

from .models import (
    FMPCrowdfundingCampaign,
    FMPCrowdfundingSearch,
    FMPEquityOffering,
    FMPEquityOfferingSearch,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def crowdfunding_offerings_latest(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPCrowdfundingCampaign]]:
    """
    Get latest crowdfunding offerings.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        Latest crowdfunding offerings as a Pydantic model.
    """
    path = "crowdfunding-offerings-latest"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def crowdfunding_offerings_search(
    apikey: str, name: str
) -> RootModel[typing.List[FMPCrowdfundingSearch]]:
    """
    Search crowdfunding offerings by company name, campaign name, or platform.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Search name string.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        Crowdfunding offerings matching the query as a Pydantic model.
    """
    path = "crowdfunding-offerings-search"
    query_vars = {"apikey": apikey, "name": name}

    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def crowdfunding_offerings(
    apikey: str, cik: str
) -> RootModel[typing.List[FMPCrowdfundingCampaign]]:
    """
    Get all crowdfunding offerings for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Central Index Key (CIK) of the company.

    Returns
    -------
    FmpCrowdfundingOfferingsResponse
        All crowdfunding offerings as a Pydantic model.
    """
    path = "crowdfunding-offerings"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def fundraising_latest(
    apikey: str, cik: str = None, page: int = None, limit: int = None
) -> RootModel[typing.List[FMPEquityOffering]]:
    """
    Get latest fundraising data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str, optional
        Central Index Key (CIK) of the company.
    page : int, optional
        Page number for pagination.
    limit : int, optional
        Number of results per page.

    Returns
    -------
    FmpFundraisingResponse
        Latest fundraising data as a Pydantic model.
    """
    path = "fundraising-latest"
    query_vars = {"apikey": apikey}
    if cik:
        query_vars["cik"] = cik
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)

    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def fundraising_search(
    apikey: str, name: str
) -> RootModel[typing.List[FMPEquityOfferingSearch]]:
    """
    Search fundraising data by company name or campaign name.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Search name string.

    Returns
    -------
    FmpFundraisingResponse
        Fundraising data matching the query as a Pydantic model.
    """
    path = "fundraising-search"
    query_vars = {"apikey": apikey, "name": name}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def fundraising(apikey: str, cik: str) -> RootModel[typing.List[FMPEquityOffering]]:
    """
    Get all fundraising data.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Central Index Key (CIK) of the company.

    Returns
    -------
    FmpFundraisingResponse
        All fundraising data as a Pydantic model.
    """
    path = "fundraising"
    query_vars = {"apikey": apikey, "cik": cik}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
