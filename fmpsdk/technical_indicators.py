import typing

from pydantic import RootModel

from .models import FMPTechnicalIndicator
from .url_methods import (
    __return_json
)
from .utils import parse_response


@parse_response
def technical_indicators(
    apikey: str,
    symbol: str,
    indicator: str,
    periodLength: int,
    timeframe: str,
    from_date: str = None,
    to_date: str = None
) -> RootModel[typing.List[FMPTechnicalIndicator]]:
    """
    Query FMP /technical_indicator/ API.

    :param apikey: Your API key
    :param symbol: Company ticker
    :param indicator: Type of technical indicator (e.g., "sma", "ema", etc.)
    :param periodLength: Number of periods for the indicator
    :param timeframe: Timeframe for the indicator (e.g., "1min", "daily", "weekly", etc.)
    :param from_date: Start date for the data (optional)
    :param to_date: End date for the data (optional)
    :return: A list of technical indicators
    """
    valid_indicators = ["sma", "ema", "wma", "dema", "tema", "rsi", "standarddeviation", "williams", "adx"]
    if indicator not in valid_indicators:
        raise ValueError(f"Invalid indicator type. Valid types are: {', '.join(valid_indicators)}")
    
    path = f"technical_indicators/{indicator}"
    query_vars = {
        "apikey": apikey,
        "symbol": symbol,
        "periodLength": periodLength,
        "timeframe": timeframe,
    }
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    
    return __return_json(path=path, query_vars=query_vars)

