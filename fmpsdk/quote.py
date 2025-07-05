import typing

from pydantic import RootModel

from .models import (
    FMPAftermarketQuote,
    FMPAftermarketTrade,
    FMPQuoteFull,
    FMPQuoteShort,
    FMPStockPriceChange,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def quote(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get quote for a given symbol. Can be used for stocks, ETFs, indices, commodities, and forex pairs.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol (e.g., 'GCUSD', 'AAPL', 'EURUSD', 'BTCUSD').
    Returns
    -------
    list
        List of quote data.
    """
    path = "quote"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def quote_short(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get short quote for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol (e.g., 'GCUSD', 'AAPL', 'EURUSD', 'BTCUSD').
    Returns
    -------
    list
        List of short quote data.
    """
    path = "quote-short"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def aftermarket_trade(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPAftermarketTrade]]:
    """
    Get aftermarket trade data for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol (e.g., 'GCUSD', 'AAPL', 'EURUSD', 'BTCUSD').
    Returns
    -------
    list
        List of aftermarket trade data.
    """
    path = "aftermarket-trade"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def aftermarket_quote(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPAftermarketQuote]]:
    """
    Get aftermarket quote for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol (e.g., 'GCUSD', 'AAPL', 'EURUSD', 'BTCUSD').
    Returns
    -------
    list
        List of aftermarket quote data.
    """
    path = "aftermarket-quote"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def stock_price_change(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPStockPriceChange]]:
    """
    Get stock price change for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Symbol (e.g., 'AAPL').

    Returns
    -------
    list
        List of stock price change data.
    """
    path = "stock-price-change"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path, query_vars)


@parse_response
def stock_batch_quote(
    apikey: str,
    symbols: typing.List[str],
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of symbols (e.g., ['AAPL', 'GOOGL']).

    Returns
    -------
    list
        List of batch quote data.
    """
    path = "batch-quote"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path, query_vars)


@parse_response
def batch_quote_short(
    apikey: str,
    symbols: typing.List[str],
) -> RootModel[typing.List[FMPQuoteShort]]:
    """
    Get batch short quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of symbols (e.g., ['AAPL', 'GOOGL']).

    Returns
    -------
    list
        List of batch short quote data.
    """
    path = "batch-quote-short"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path, query_vars)


@parse_response
def batch_aftermarket_trade(
    apikey: str,
    symbols: typing.List[str],
) -> RootModel[typing.List[FMPAftermarketTrade]]:
    """
    Get batch aftermarket trade for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of symbols (e.g., ['AAPL', 'GOOGL']).

    Returns
    -------
    list
        List of batch aftermarket trade data.
    """
    path = "batch-aftermarket-trade"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path, query_vars)


@parse_response
def batch_aftermarket_quote(
    apikey: str,
    symbols: typing.List[str],
) -> RootModel[typing.List[FMPAftermarketQuote]]:
    """
    Get batch aftermarket quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of symbols (e.g., ['AAPL', 'GOOGL']).

    Returns
    -------
    list
        List of batch aftermarket quote data.
    """
    path = "batch-aftermarket-quote"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path, query_vars)


@parse_response
def batch_exchange_quote(
    apikey: str,
    symbols: typing.List[str],
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch exchange quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of symbols (e.g., ['AAPL', 'GOOGL']).

    Returns
    -------
    list
        List of batch exchange quote data.
    """
    path = "batch-exchange-quote"
    query_vars = {"apikey": apikey, "symbols": ",".join(symbols)}
    return __return_json(path, query_vars)


@parse_response
def batch_mutual_fund_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch mutual fund quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-mutualfund-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)


@parse_response
def batch_etf_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch ETF quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-etf-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)


@parse_response
def batch_commodity_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch commodity quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-commodity-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)


@parse_response
def batch_crypto_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch cryptocurrency quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-crypto-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)


@parse_response
def batch_forex_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch forex quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-forex-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)


@parse_response
def batch_index_quote(
    apikey: str, short: bool = None
) -> RootModel[typing.List[FMPQuoteFull]]:
    """
    Get batch index quote for multiple symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    short : bool, optional
        If True, returns short quotes. Default is None (returns full quotes).
    """
    path = "batch-index-quotes"
    query_vars = {"apikey": apikey}
    if short is not None:
        query_vars["short"] = str(short).lower()
    return __return_json(path, query_vars)
