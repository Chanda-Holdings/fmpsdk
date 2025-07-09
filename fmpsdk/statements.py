import typing

from pydantic import RootModel

from .models import (
    FMPAsReportedBalanceSheet,
    FMPAsReportedCashFlowStatement,
    FMPAsReportedFullStatement,
    FMPAsReportedIncomeStatement,
    FMPBalanceSheetGrowth,
    FMPBalanceSheetStatement,
    FMPCashFlowGrowth,
    FMPCashFlowStatement,
    FMPEnterpriseValue,
    FMPFinancialRatios,
    FMPFinancialRatiosTTM,
    FmpFinancialReportDatesListResponse,
    FmpFinancialStatementSymbolsListResponse,
    FMPFullFinancialReport,
    FMPIncomeStatement,
    FMPIncomeStatementGrowth,
    FMPKeyMetrics,
    FMPKeyMetricsTTM,
    FMPOwnerEarnings,
    FMPRevenueSegmentation,
)
from .url_methods import __return_binary_stable, __return_json
from .utils import parse_response


@parse_response
def income_statement(
    apikey: str, symbol: str, period: str = None, limit: int = None
) -> RootModel[typing.List[FMPIncomeStatement]]:
    """
    Retrieve the income statement for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the income statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of income statement data as a Pydantic model.
    """
    path = "income-statement"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def balance_sheet_statement(
    apikey: str, symbol: str, period: str = None, limit: int = None
) -> RootModel[typing.List[FMPBalanceSheetStatement]]:
    """
    Retrieve the balance sheet statement for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the balance sheet statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of balance sheet statement data as a Pydantic model.
    """
    path = "balance-sheet-statement"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def cash_flow_statement(
    apikey: str, symbol: str, period: str = None, limit: int = None
) -> RootModel[typing.List[FMPCashFlowStatement]]:
    """
    Retrieve the cash flow statement for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the cash flow statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of cash flow statement data as a Pydantic model.
    """
    path = "cash-flow-statement"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_statements_latest(
    apikey: str, page: int = None, limit: int = None
) -> RootModel[typing.List[FmpFinancialStatementSymbolsListResponse]]:
    """
    Retrieve the latest financial statements for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    page : int, optional
        The page number to retrieve.
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of latest financial statement data as a Pydantic model.
    """

    path = "latest-financial-statements"
    query_vars = {"apikey": apikey}
    if page is not None:
        query_vars["page"] = str(page)
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def income_statement_ttm(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPIncomeStatement]]:
    """
    Retrieve the trailing twelve months (TTM) income statement for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of TTM income statement data as a Pydantic model.
    """
    path = "income-statement-ttm"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def balance_sheet_statements_ttm(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPBalanceSheetStatement]]:
    """
    Retrieve the trailing twelve months (TTM) balance sheet statement for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of TTM balance sheet statement data as a Pydantic model.
    """
    path = "balance-sheet-statement-ttm"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def cashflow_statements_ttm(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPCashFlowStatement]]:
    """
    Retrieve the trailing twelve months (TTM) cash flow statement for a given symbol.
    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of TTM cash flow statement data as a Pydantic model.
    """
    path = "cash-flow-statement-ttm"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def key_metrics(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPKeyMetrics]]:
    """
    Retrieve key metrics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    period : str, optional
        'annual' or 'quarter'.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of key metrics as a Pydantic model.
    """
    path = "key-metrics"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_ratios(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPFinancialRatios]]:
    """
    Retrieve financial ratios for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    period : str, optional
        'annual' or 'quarter'.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of financial ratios as a Pydantic model.
    """
    path = "ratios"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def key_metrics_ttm(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPKeyMetricsTTM]]:
    """
    Retrieve trailing twelve months (TTM) key metrics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of TTM key metrics as a Pydantic model.
    """
    path = "key-metrics-ttm"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_ratios_ttm(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPFinancialRatiosTTM]]:
    """
    Retrieve financial ratios for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of financial ratios as a Pydantic model.
    """
    path = "ratios-ttm"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_scores(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FMPIncomeStatement]]:
    """
    Retrieve financial scores for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of financial scores as a Pydantic model.
    """
    path = "financial-scores"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def owner_earnings(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPOwnerEarnings]]:
    """
    Retrieve owner earnings for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of owner earnings as a Pydantic model.
    """
    path = "owner-earnings"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def enterprise_values(
    apikey: str, symbol: str, limit: int = None, period: str = None
) -> RootModel[typing.List[FMPEnterpriseValue]]:
    """
    Retrieve enterprise values for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    limit : int, optional
        Number of rows to return.
    period : str, optional
        'annual' or 'quarter'.

    Returns
    -------
    FMPEnterpriseValue
        List of enterprise values as a Pydantic model.
    """
    path = "enterprise-values"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit is not None:
        query_vars["limit"] = str(limit)
    if period is not None:
        query_vars["period"] = period
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def income_statement_growth(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPIncomeStatementGrowth]]:
    """
    Retrieve income statement growth statistics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    period : str, optional
        'annual' or 'quarter'.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of income statement growth data as a Pydantic model.
    """
    path = "income-statement-growth"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def balance_sheet_statement_growth(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPBalanceSheetGrowth]]:
    """
    Retrieve balance sheet statement growth statistics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FMPBalanceSheetStatementGrowth
        List of balance sheet statement growth data as a Pydantic model.
    """
    path = "balance-sheet-statement-growth"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def cash_flow_statement_growth(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPCashFlowGrowth]]:
    """
    Retrieve cash flow statement growth statistics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of cash flow statement growth data as a Pydantic model.
    """
    path = "cash-flow-statement-growth"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_growth(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPIncomeStatementGrowth]]:
    """
    Retrieve financial growth statistics for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    period : str, optional
        'annual' or 'quarter'.
    limit : int, optional
        Number of rows to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of financial growth data as a Pydantic model.
    """
    path = "financial-growth"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_reports_dates(
    apikey: str,
    symbol: str,
) -> RootModel[typing.List[FmpFinancialReportDatesListResponse]]:
    """
    Retrieve financial report dates for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialReportDatesListResponse
        List of financial report dates as a Pydantic model.
    """
    path = "financial-reports-dates"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_reports_json(
    apikey: str, symbol: str, year: str, period: str
) -> RootModel[typing.List[FMPFullFinancialReport]]:
    """
    Retrieve financial report dates for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.
    year : str
        The year for which to retrieve financial report dates.
    period : str
        The period for which to retrieve financial report dates ('annual' or 'quarter').

    Returns
    -------
    FmpFinancialReportDatesListResponse
        List of financial report dates as a Pydantic model.
    """
    path = "financial-reports-json"
    query_vars = {"apikey": apikey, "symbol": symbol, "year": year, "period": period}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


def financial_reports_xlsx(
    apikey: str, symbol: str, year: int, period: str
) -> typing.Optional[bytes]:
    """
    Get financial reports in XLSX format using the /stable/financial-reports-xlsx endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get financial reports for.
        year (int): The year for the financial report.
        period (str): The period for the report.
    Returns:
        Binary XLSX file content that can be saved to a file or processed.
    """
    path = "financial-reports-xlsx"
    query_vars = {
        "apikey": apikey,
        "symbol": symbol,
        "year": str(year),
        "period": period,
    }
    return __return_binary_stable(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def revenue_product_segmentation(
    apikey: str, symbol: str, period: str = None, structure: str = None
) -> RootModel[typing.List[FMPRevenueSegmentation]]:
    """
    Retrieve revenue segmentation by product for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the revenue segmentation ('annual' or 'quarter').
    structure : str, optional
        The structure for the revenue segmentation.

    Returns
    -------
    FMPRevenueSegmentation
        List of revenue segmentation data as a Pydantic model.
    """
    path = "revenue-product-segmentation"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if structure is not None:
        query_vars["structure"] = structure
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def revenue_geographic_segmentation(
    apikey: str, symbol: str, period: str = None, structure: str = None
) -> RootModel[typing.List[FMPRevenueSegmentation]]:
    """
    Retrieve revenue segmentation by geography for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the revenue segmentation ('annual' or 'quarter').
    structure : str, optional
        The structure for the revenue segmentation.

    Returns
    -------
    FMPRevenueSegmentation
        List of revenue segmentation data as a Pydantic model.
    """
    path = "revenue-geographic-segmentation"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if structure is not None:
        query_vars["structure"] = structure
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def income_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> typing.Union[RootModel[typing.List[FMPAsReportedIncomeStatement]], None]:
    """
    Retrieve the as-reported income statement for a given symbol, or download as CSV.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the as-reported income statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported income statement data as a Pydantic model, or None if downloaded.
    """
    path = "income-statement-as-reported"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def balance_sheet_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> typing.Union[RootModel[typing.List[FMPAsReportedBalanceSheet]], None]:
    """
    Retrieve the as-reported balance sheet statement for a given symbol, or download as CSV.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the as-reported balance sheet statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported balance sheet statement data as a Pydantic model, or None if downloaded.
    """
    path = "balance-sheet-statement-as-reported"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def cash_flow_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> typing.Union[RootModel[typing.List[FMPAsReportedCashFlowStatement]], None]:
    """
    Retrieve the as-reported cash flow statement for a given symbol, or download as CSV.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the as-reported cash flow statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported cash flow statement data as a Pydantic model, or None if downloaded.
    """
    path = "cash-flow-statement-as-reported"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def financial_statement_full_as_reported(
    apikey: str,
    symbol: str,
    period: str = None,
    limit: int = None,
) -> RootModel[typing.List[FMPAsReportedFullStatement]]:
    """
    Retrieve the full as-reported financial statement for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    period : str, optional
        The period for the full as-reported financial statement ('annual' or 'quarter').
    limit : int, optional
        The number of results to return.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of full as-reported financial statement data as a Pydantic model.
    """
    path = "financial-statement-full-as-reported"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if period is not None:
        query_vars["period"] = period
    if limit is not None:
        query_vars["limit"] = str(limit)
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
