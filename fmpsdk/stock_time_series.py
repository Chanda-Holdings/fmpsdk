import logging
import typing

from pydantic import RootModel

from .general import __quotes
from .models import *
from .url_methods import __return_json_stable
from .utils import parse_response


@parse_response
def quote_short(apikey: str, symbol: str) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Query FMP /quote-short/ API.

    :param apikey: Your API key
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    path = "quote-short/{symbol}"
    query_vars = {
        "apikey": apikey,
    }
    return __return_json_stable(path, query_vars)


@parse_response
def exchange_realtime(
    apikey: str, exchange: str
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Query FMP /quotes/ API.

    :param apikey: Your API key
    :param exchange: Exchange symbol.
    :return: A list of dictionaries.
    """
    return __quotes(apikey=apikey, value=exchange)


@parse_response
def historical_stock_dividend(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDividend]]:
    """
    Query FMP /historical-price-full/stock_divident/ API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    path = "historical-price-full/stock_dividend/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_stock_split(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPStockSplit]]:
    """
    Query FMP /historical-price-full/stock_divident/ API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    path = "historical-price-full/stock_split/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_survivorship_bias_free_eod(
    apikey: str, symbol: str, date: str
) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Query FMP /historical-price-full/<ticker>/<date> API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param date: str YYYY-MM-DD
    :return: A list of dictionaries.
    """
    path = "historical-price-full/{symbol}/{date}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def live_full_price(apikey: str, symbol: str) -> typing.Optional[typing.Dict]:
    """
    Query FMP /live-full-price/ API.

    Get real-time bid/ask prices, volume, and last trade price for a stock.

    https://site.financialmodelingprep.com/developer/docs#live-full-price

    Endpoint:
        https://financialmodelingprep.com/api/v3/live-full-price/{symbol}

    :param apikey: Your API key.
    :param symbol: Company ticker symbol.
    :return: A dictionary containing real-time price data with fields:
             - symbol: The stock symbol
             - ask: The current ask price
             - askSize: The size of the ask order
             - bid: The current bid price
             - bidSize: The size of the bid order
             - price: The last trade price
             - volume: The trading volume
             - timestamp: The timestamp of the data
    """
    if not symbol:
        logging.warning("No symbol provided for live full price request.")
        return None

    path = "live-full-price/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_price_eod_light(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointLight]]:
    """
    Query FMP /historical-price-eod/light endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: FmpHistoricalPriceEodLightResponse.
    """
    path = "historical-price-eod/light/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_price_eod_full(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/full endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: FmpHistoricalPriceEodFullResponse.
    """
    path = "historical-price-eod/full/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_price_eod_non_split_adjusted(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/non-split-adjusted endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of historical EOD prices (non-split-adjusted).
    """
    path = "historical-price-eod/non-split-adjusted/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_price_eod_dividend_adjusted(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalDataPointFull]]:
    """
    Query FMP /historical-price-eod/dividend-adjusted endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of historical EOD prices (dividend-adjusted).
    """
    path = "historical-price-eod/dividend-adjusted/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


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
    path = "/historical-chart/{interval}/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_chart_1min(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/1min endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 1min historical chart data.
    """
    path = "historical-chart/1min/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_chart_5min(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/5min endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 5min historical chart data.
    """
    path = "historical-chart/5min/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_chart_15min(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/15min endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 15min historical chart data.
    """
    path = "historical-chart/15min/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_chart_30min(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/30min endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 30min historical chart data.
    """
    path = "historical-chart/30min/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_chart_1hour(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/1hour endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 1hour historical chart data.
    """
    path = "historical-chart/1hour/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_chart_4hour(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPIntradayDataPoint]]:
    """
    Query FMP /historical-chart/4hour endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :param from_date: Optional start date (YYYY-MM-DD).
    :param to_date: Optional end date (YYYY-MM-DD).
    :return: List of 4hour historical chart data.
    """
    path = "historical-chart/4hour/{symbol}"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


# All function return types should be updated to match ENDPOINT_MODEL_MAP from model_registry.py
