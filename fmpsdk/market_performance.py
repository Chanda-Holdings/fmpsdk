import typing

from pydantic import RootModel

from .models import (
    FMPHistoricalIndustryPE,
    FMPHistoricalIndustryPerformance,
    FMPHistoricalSectorPE,
    FMPHistoricalSectorPerformance,
    FMPIndustryPerformanceSnapshot,
    FMPIndustryPESnapshot,
    FMPMarketMover,
    FMPSectorPerformanceSnapshot,
    FMPSectorPESnapshot,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def sector_performance_snapshot(
    apikey: str,
) -> RootModel[typing.List[FMPSectorPerformanceSnapshot]]:
    """
    Get sector performance snapshot using the /stable/sector-performance-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of sector performance data.
    """
    path = "sector-performance-snapshot"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def industry_performance_snapshot(
    apikey: str,
) -> RootModel[typing.List[FMPIndustryPerformanceSnapshot]]:
    """
    Get industry performance snapshot using the /stable/industry-performance-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of industry performance data.
    """
    path = "industry-performance-snapshot"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def historical_sector_performance(
    apikey: str, sector: str
) -> RootModel[typing.List[FMPHistoricalSectorPerformance]]:
    """
    Get historical sector performance using the /stable/historical-sector-performance endpoint.

    Parameters:
        apikey (str): Your API key.
        sector (str): Sector name.
    Returns:
        List of historical sector performance data.
    """
    path = "historical-sector-performance"
    query_vars = {"apikey": apikey, "sector": sector}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def historical_industry_performance(
    apikey: str, industry: str
) -> RootModel[typing.List[FMPHistoricalIndustryPerformance]]:
    """
    Get historical industry performance using the /stable/historical-industry-performance endpoint.

    Parameters:
        apikey (str): Your API key.
        industry (str): Industry name.
    Returns:
        List of historical industry performance data.
    """
    path = "historical-industry-performance"
    query_vars = {"apikey": apikey, "industry": industry}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def sector_pe_snapshot(
    apikey: str,
) -> RootModel[typing.List[FMPSectorPESnapshot]]:
    """
    Get sector PE snapshot using the /stable/sector-pe-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of sector PE data.
    """
    path = "sector-pe-snapshot"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def industry_pe_snapshot(
    apikey: str,
) -> RootModel[typing.List[FMPIndustryPESnapshot]]:
    """
    Get industry PE snapshot using the /stable/industry-pe-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of industry PE data.
    """
    path = "industry-pe-snapshot"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def historical_sector_pe(
    apikey: str, sector: str
) -> RootModel[typing.List[FMPHistoricalSectorPE]]:
    """
    Get historical sector PE using the /stable/historical-sector-pe endpoint.

    Parameters:
        apikey (str): Your API key.
        sector (str): Sector name.
    Returns:
        List of historical sector PE data.
    """
    path = "historical-sector-pe"
    query_vars = {"apikey": apikey, "sector": sector}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def historical_industry_pe(
    apikey: str, industry: str
) -> RootModel[typing.List[FMPHistoricalIndustryPE]]:
    """
    Get historical industry PE using the /stable/historical-industry-pe endpoint.

    Parameters:
        apikey (str): Your API key.
        industry (str): Industry name.
    Returns:
        List of historical industry PE data.
    """
    path = "historical-industry-pe"
    query_vars = {"apikey": apikey, "industry": industry}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def biggest_gainers(
    apikey: str,
) -> RootModel[typing.List[FMPMarketMover]]:
    """
    Get biggest stock gainers using the /stable/biggest-gainers endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of biggest stock gainers.
    """
    path = "biggest-gainers"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def biggest_losers(
    apikey: str,
) -> RootModel[typing.List[FMPMarketMover]]:
    """
    Get biggest stock losers using the /stable/biggest-losers endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of biggest stock losers.
    """
    path = "biggest-losers"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def most_active_stocks(
    apikey: str,
) -> RootModel[typing.List[FMPMarketMover]]:
    """
    Get most active stocks using the /stable/most-actives endpoint.

    Parameters:
        apikey (str): Your API key.
    Returns:
        List of most active stocks.
    """
    path = "most-actives"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)
