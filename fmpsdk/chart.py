import typing

from pydantic import RootModel

from .models import (
    FMPHistoricalDataPointFull,
    FMPHistoricalDataPointLight,
    FMPIntradayDataPoint,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def historical_price_eod_light(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointLight]]:
    """
    Query FMP /historical-price-eod/light endpoint. Supports stocks, crypto, forex, and indices.
    :param apikey: Your API key.
    :param symbol: Ticker symbol (e.g., 'AAPL', 'BTCUSD', 'EURUSD').
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: FmpHistoricalPriceEodLightResponse.
    """
    path = f"historical-price-eod/light"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_price_eod(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/full endpoint. Supports stocks, crypto, forex, and indices.
    :param apikey: Your API key.
    :param symbol: Ticker symbol (e.g., 'AAPL', 'BTCUSD', 'EURUSD').
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: FmpHistoricalPriceEodFullResponse.
    """
    path = f"historical-price-eod/full"
    query_vars = {"apikey": apikey, "symbol": symbol}

    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_price_eod_non_split_adjusted(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/non-split-adjusted endpoint.
    :param apikey: Your API key.
    :param symbol: Stock ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of historical EOD prices (non-split-adjusted).
    """
    path = f"historical-price-eod/non-split-adjusted"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_price_eod_dividend_adjusted(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/dividend-adjusted endpoint.
    :param apikey: Your API key.
    :param symbol: Stock ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of historical EOD prices (dividend-adjusted).
    """
    path = f"historical-price-eod/dividend-adjusted"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def historical_chart(
    symbol: str, interval: str, apikey: str
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Get historical intraday chart data for a symbol at a specified interval.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    interval : str
        Interval for the chart. One of: '1min', '5min', '15min', '30min', '1hour', '4hour'.
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of historical intraday chart data.
    """
    valid_intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour"]
    if interval not in valid_intervals:
        raise ValueError(
            f"Invalid interval: {interval}. Must be one of {valid_intervals}."
        )
    path = f"historical-chart/{interval}"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
