import logging
import typing

from pydantic import RootModel

from .models import (
    FMPBalanceSheetGrowth,
    FMPBalanceSheetStatement,
    FMPBulkDCF,
    FMPBulkEarningsSurprise,
    FMPBulkEOD,
    FMPBulkETFHolder,
    FMPBulkPriceTargetSummary,
    FMPBulkRating,
    FMPBulkStockPeers,
    FMPBulkUpgradeDowngradeConsensus,
    FMPCashFlowGrowth,
    FMPCashFlowStatement,
    FMPCompanyProfile,
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPIncomeStatement,
    FMPIncomeStatementGrowth,
    FMPKeyMetricsTTM,
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
) -> RootModel[typing.List[FMPBulkUpgradeDowngradeConsensus]]:
    """
    Get bulk data for upgrades and downgrades consensus.

    Endpoint:
        https://financialmodelingprep.com/stable/upgrades-downgrades-consensus-bulk

    Parameters
    ----------
    apikey : str
        Your API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of upgrades/downgrades consensus data as Pydantic models.
    """
    path = "upgrades-downgrades-consensus-bulk"
    query_vars = {"apikey": apikey}

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
    path = "profile-bulk"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
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
    path = "rating-bulk"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
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
    path = "dcf-bulk"
    query_vars = {"apikey": apikey, "symbols": symbols_str}
    return __return_json(path, query_vars)


@parse_response
def price_target_summary_bulk(
    apikey: str,
) -> RootModel[typing.List[FMPBulkPriceTargetSummary]]:
    """
    Get bulk price target summary.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of price target summaries as Pydantic models.
    """
    path = "price-target-summary-bulk"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def etf_holder_bulk(apikey: str, part: str) -> RootModel[typing.List[FMPBulkETFHolder]]:
    """
    Get bulk ETF holders for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    part : str
        Part of the ETF to retrieve (e.g., 'holdings', 'performance').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of ETF holders as Pydantic models.
    """
    path = f"etf-holder-bulk"
    query_vars = {"apikey": apikey, "part": part}
    return __return_json(path, query_vars)


@parse_response
def key_metrics_ttm_bulk(apikey: str) -> RootModel[typing.List[FMPKeyMetricsTTM]]:
    """
    Get bulk key metrics TTM for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of key metrics TTM data as Pydantic models.
    """
    path = "key-metrics-ttm-bulk"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def ratios_ttm_bulk(apikey: str) -> RootModel[typing.List[FMPFinancialRatios]]:
    """
    Get bulk ratios TTM for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of ratios TTM data as Pydantic models.
    """
    path = "ratios-ttm-bulk"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def peers_bulk(apikey: str) -> RootModel[typing.List[FMPBulkStockPeers]]:
    """
    Get bulk peers for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of peers data as Pydantic models.
    """
    path = "peers-bulk"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)


@parse_response
def earnings_surprises_bulk(
    apikey: str, year: str
) -> RootModel[typing.List[FMPBulkEarningsSurprise]]:
    """
    Get bulk earnings surprises for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve earnings surprises.
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of earnings surprises data as Pydantic models.
    """
    path = f"earnings-surprises-bulk"
    query_vars = {"apikey": apikey, "year": year}
    return __return_json(path, query_vars)


@parse_response
def income_statement_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPIncomeStatement]]:
    """
    Get bulk income statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve income statements.
    period : str
        The period for which to retrieve income statements (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of income statements as Pydantic models.
    """
    path = f"income-statement-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def income_statement_growth_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPIncomeStatementGrowth]]:
    """
    Get bulk income statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve income statement growth.
    period : str
        The period for which to retrieve income statement growth (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of income statement growth data as Pydantic models.
    """
    path = f"income-statement-growth-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def balance_sheet_statement_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPBalanceSheetStatement]]:
    """
    Get bulk balance sheet statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve balance sheet statements.
    period : str
        The period for which to retrieve balance sheet statements (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of balance sheet statements as Pydantic models.
    """
    path = f"balance-sheet-statement-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def balance_sheet_statement_growth_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPBalanceSheetGrowth]]:
    """
    Get bulk balance sheet statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve balance sheet statement growth.
    period : str
        The period for which to retrieve balance sheet statement growth (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of balance sheet statement growth data as Pydantic models.
    """
    path = f"balance-sheet-statement-growth-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def cash_flow_statement_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPCashFlowStatement]]:
    """
    Get bulk cash flow statements for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve cash flow statements.
    period : str
        The period for which to retrieve cash flow statements (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of cash flow statements as Pydantic models.
    """
    path = f"cash-flow-statement-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def cash_flow_statement_growth_bulk(
    apikey: str, year: str, period: str
) -> RootModel[typing.List[FMPCashFlowGrowth]]:
    """
    Get bulk cash flow statement growth for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    year : str
        The year for which to retrieve cash flow statement growth.
    period : str
        The period for which to retrieve cash flow statement growth (e.g., 'FY', 'Q1', 'Q2').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of cash flow statement growth data as Pydantic models.
    """
    path = f"cash-flow-statement-growth-bulk"
    query_vars = {"apikey": apikey, "year": year, "period": period}
    return __return_json(path, query_vars)


@parse_response
def eod_bulk(apikey: str, date: str) -> RootModel[typing.List[FMPBulkEOD]]:
    """
    Get bulk end-of-day (EOD) data for a list of symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    date : str
        The date for which to retrieve EOD data (format: 'YYYY-MM-DD').
    Returns
    -------
    FmpCompanySymbolsListResponse
        List of EOD data as Pydantic models.
    """
    path = f"eod-bulk"
    query_vars = {"apikey": apikey, "date": date}
    return __return_json(path, query_vars)
