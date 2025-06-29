import typing

from pydantic import RootModel

from .models import FMPTechnicalIndicator
from .url_methods import (
    __return_json,
    __validate_statistics_type,
)
from .utils import parse_response


@parse_response
def technical_indicators(
    apikey: str,
    symbol: str,
    period: int = 10,
    statistics_type: str = "SMA",
    time_delta: str = "daily",
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Query FMP /technical_indicator/ API.

    :param apikey: Your API key
    :param symbol: Company ticker
    :param period: I don't know.  10 is my only example.
    :param statistics_type: Not sure what this is.
    :param time_delta: 'daily' or intraday: '1min' - '4hour'
    :return:
    """
    path = f"technical_indicator/{time_delta}/{symbol}"
    query_vars = {
        "apikey": apikey,
        "period": period,
        "type": __validate_statistics_type(statistics_type),
    }
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def technical_indicators_sma(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get SMA technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of SMA technical indicator data.
    """
    path = f"/technical-indicators/sma/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_ema(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get EMA technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of EMA technical indicator data.
    """
    path = f"/technical-indicators/ema/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_dema(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get DEMA technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of DEMA technical indicator data.
    """
    path = f"/technical-indicators/dema/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_rsi(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get RSI technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of RSI technical indicator data.
    """
    path = f"/technical-indicators/rsi/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_standarddeviation(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get Standard Deviation technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of Standard Deviation technical indicator data.
    """
    path = f"/technical-indicators/standarddeviation/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_williams(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get Williams %R technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of Williams %R technical indicator data.
    """
    path = f"/technical-indicators/williams/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)


@parse_response
def technical_indicators_adx(
    apikey: str,
    symbol: str,
    interval: str,
    time_period: int,
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Get ADX technical indicator for a symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Ticker symbol (e.g., 'AAPL').
    interval : str
        Interval (e.g., 'daily').
    time_period : int
        Time period for the indicator.
    Returns
    -------
    list
        List of ADX technical indicator data.
    """
    path = f"/technical-indicators/adx/{symbol}"
    query_vars = {"apikey": apikey, "interval": interval, "time_period": time_period}
    return __return_json(path, query_vars)
