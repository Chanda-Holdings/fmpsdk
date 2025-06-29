import logging
import typing

from pydantic import RootModel

from .models import (
    FMPBulkBalanceSheetGrowth,
    FMPBulkBalanceSheetStatement,
    FMPBulkCashFlowGrowth,
    FMPBulkCashFlowStatement,
    FMPBulkDCF,
    FMPBulkEarningsSurprise,
    FMPBulkEOD,
    FMPBulkETFHolder,
    FMPBulkIncomeStatement,
    FMPBulkIncomeStatementGrowth,
    FMPBulkPriceTargetSummary,
    FMPBulkRating,
    FMPBulkStockPeers,
    FMPBulkUpgradeDowngradeConsensus,
    FMPCompanyProfile,
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPKeyMetrics,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def bulk_profiles(apikey: str, part: str) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    It contains all profiles from our API in one CSV file

    Endpoint:
        https://site.financialmodelingprep.com/developer/docs/bulk-profiles

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    part : str
        Part identifier for the bulk download.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of company profiles as Pydantic models.
    """
    path = "profile-bulk"
    query_vars = {"apikey": apikey, "part": part}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def scores_bulk(
    apikey: str, symbols: typing.List[str]
) -> RootModel[typing.List[FMPFinancialScores]]:
    """
    Get financial scores and metrics for multiple symbols in a single request.

    Endpoint:
        https://financialmodelingprep.com/stable/scores-bulk

    Parameters
    ----------
    apikey : str
        Your API key.
    symbols : list of str
        List of stock symbols to get scores for.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of financial scores and metrics as Pydantic models.
    """
    if not symbols:
        logging.warning("No symbols provided for scores bulk request.")
        return []

    path = "scores-bulk"
    query_vars = {"apikey": apikey, "symbol": ",".join(symbols)}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def upgrades_downgrades_consensus_bulk(
    apikey: str,
    limit: typing.Optional[int] = None,
    download: bool = False,
) -> RootModel[typing.List[FMPBulkUpgradeDowngradeConsensus]]:
    """
    Get bulk data for upgrades and downgrades consensus.

    Endpoint:
        https://financialmodelingprep.com/stable/upgrades-downgrades-consensus-bulk

    Parameters
    ----------
    apikey : str
        Your API key.
    limit : int, optional
        Number of rows to return.
    download : bool, optional
        If True, returns data in CSV format.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of upgrades/downgrades consensus data as Pydantic models.
    """
    path = "upgrades-downgrades-consensus-bulk"
    query_vars = {"apikey": apikey}

    if limit is not None:
        query_vars["limit"] = str(limit)

    if download:
        query_vars["datatype"] = "csv"

    return __return_json(path=path, query_vars=query_vars)


@parse_response
def profile_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Get bulk company profiles for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols (e.g., ['AAPL', 'MSFT']).
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of company profiles as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/profile-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def rating_bulk(apikey: str, symbols: list) -> RootModel[typing.List[FMPBulkRating]]:
    """
    Get bulk ratings for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of ratings as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/rating-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def dcf_bulk(apikey: str, symbols: list) -> RootModel[typing.List[FMPBulkDCF]]:
    """
    Get bulk discounted cash flow data for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of discounted cash flow data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/dcf-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def price_target_summary_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkPriceTargetSummary]]:
    """
    Get bulk price target summary for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of price target summaries as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/price-target-summary-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def etf_holder_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkETFHolder]]:
    """
    Get bulk ETF holders for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ETF ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of ETF holders as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/etf-holder-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def key_metrics_ttm_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPKeyMetrics]]:
    """
    Get bulk key metrics TTM for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of key metrics TTM data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/key-metrics-ttm-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def ratios_ttm_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPFinancialRatios]]:
    """
    Get bulk ratios TTM for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of ratios TTM data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/ratios-ttm-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def peers_bulk(apikey: str, symbols: list) -> RootModel[typing.List[FMPBulkStockPeers]]:
    """
    Get bulk peers for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of peers data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/peers-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def earnings_surprises_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkEarningsSurprise]]:
    """
    Get bulk earnings surprises for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of earnings surprises data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/earnings-surprises-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def income_statement_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkIncomeStatement]]:
    """
    Get bulk income statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of income statements as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/income-statement-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def income_statement_growth_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkIncomeStatementGrowth]]:
    """
    Get bulk income statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of income statement growth data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/income-statement-growth-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def balance_sheet_statement_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkBalanceSheetStatement]]:
    """
    Get bulk balance sheet statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of balance sheet statements as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/balance-sheet-statement-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def balance_sheet_statement_growth_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkBalanceSheetGrowth]]:
    """
    Get bulk balance sheet statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of balance sheet statement growth data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/balance-sheet-statement-growth-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def cash_flow_statement_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkCashFlowStatement]]:
    """
    Get bulk cash flow statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of cash flow statements as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/cash-flow-statement-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def cash_flow_statement_growth_bulk(
    apikey: str, symbols: list
) -> RootModel[typing.List[FMPBulkCashFlowGrowth]]:
    """
    Get bulk cash flow statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of cash flow statement growth data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/cash-flow-statement-growth-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def eod_bulk(apikey: str, symbols: list) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Get bulk end-of-day (EOD) data for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbols : list
        List of ticker symbols.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of EOD data as Pydantic models.
    """
    symbols_str = ",".join(symbols)
    path = f"/eod-bulk/{symbols_str}"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)
