import typing

from pydantic import RootModel

from .models import (
    FMPEconomicCalendarEvent,
    FMPEconomicIndicator,
    FMPMarketRiskPremium,
    FMPTreasuryRates,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def treasury_rates(
    apikey: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPTreasuryRates]]:
    """
    Get US Treasury rates.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    list
        List of US Treasury rates.
    """
    path = "treasury-rates"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def economic_indicators(
    apikey: str, name: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPEconomicIndicator]]:
    """
    Get economic indicators.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Name of the economic indicator (e.g., GDP, RETAIL SALES, CPI).
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    list
        List of economic indicators.
    """
    path = "economic-indicators"
    query_vars = {"apikey": apikey, "name": name}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def economic_calendar(
    apikey: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPEconomicCalendarEvent]]:
    """
    Get economic calendar events.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    list
        List of economic calendar events.
    """
    path = "economic-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def market_risk_premium(apikey: str) -> RootModel[typing.List[FMPMarketRiskPremium]]:
    """
    Get market risk premium.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of market risk premium.
    """
    path = "market-risk-premium"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
