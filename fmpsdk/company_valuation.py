import logging
import typing

from pydantic import RootModel

from .models import *
from .settings import (
    BALANCE_SHEET_STATEMENT_AS_REPORTED_FILENAME,
    CASH_FLOW_STATEMENT_AS_REPORTED_FILENAME,
    DEFAULT_LIMIT,
    INCOME_STATEMENT_AS_REPORTED_FILENAME,
)
from .url_methods import (
    __return_json_stable,
    __validate_industry,
    __validate_period,
    __validate_sector,
)
from .utils import parse_response


@parse_response
def company_profile(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Retrieve the company profile for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpCompanyNameSearchResponse
        Company profile data as a Pydantic model.
    """
    path = "/profile/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def company_profile_cik(
    apikey: str, cik: str
) -> RootModel[typing.List[FMPCompanyProfile]]:
    """
    Retrieve the company profile by Central Index Key (CIK).

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    cik : str
        Central Index Key (CIK).

    Returns
    -------
    FmpCikSearchResponse
        Company profile data as a Pydantic model.
    """
    path = "/profile-cik/{cik}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def stock_peers(apikey: str, symbol: str) -> RootModel[typing.List[FMPStockPeer]]:
    """
    Retrieve peer companies for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of peer companies as a Pydantic model.
    """
    path = "/stock-peers"
    query_vars = {"symbol": symbol, "apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def delisted_companies(
    apikey: str, limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPDelistedCompany]]:
    """
    Retrieve a list of delisted companies.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    limit : int, optional
        Number of results to return.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of delisted companies as a Pydantic model.
    """
    path = "/delisted-companies"
    query_vars = {"apikey": apikey, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def employee_count(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPEmployeeCount]]:
    """
    Retrieve employee count for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpFinancialEstimatesResponse
        Employee count data as a Pydantic model.
    """
    path = "/employee-count/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_employee_count(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPHistoricalEmployeeCount]]:
    """
    Retrieve historical employee count for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpFinancialEstimatesResponse
        Historical employee count data as a Pydantic model.
    """
    path = "/historical-employee-count/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def income_statement(
    apikey: str, symbol: str, period: str = "annual", limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPFinancialStatement]]:
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
    path = "/income-statement/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def balance_sheet_statement(
    apikey: str, symbol: str, period: str = "annual", limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPFinancialStatement]]:
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
    path = "/balance-sheet-statement/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def cash_flow_statement(
    apikey: str, symbol: str, period: str = "annual", limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPFinancialStatement]]:
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
    path = "/cash-flow-statement/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def income_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
    filename: str = INCOME_STATEMENT_AS_REPORTED_FILENAME,
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
    filename : str, optional
        The name of the file to save the data (default: INCOME_STATEMENT_AS_REPORTED_FILENAME).

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported income statement data as a Pydantic model, or None if downloaded.
    """
    path = "/income-statement-as-reported/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def balance_sheet_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
    filename: str = BALANCE_SHEET_STATEMENT_AS_REPORTED_FILENAME,
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
    filename : str, optional
        The name of the file to save the data (default: BALANCE_SHEET_STATEMENT_AS_REPORTED_FILENAME).

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported balance sheet statement data as a Pydantic model, or None if downloaded.
    """
    path = "/balance-sheet-statement-as-reported/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def cash_flow_statement_as_reported(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
    filename: str = CASH_FLOW_STATEMENT_AS_REPORTED_FILENAME,
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
    filename : str, optional
        The name of the file to save the data (default: CASH_FLOW_STATEMENT_AS_REPORTED_FILENAME).

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse or None
        List of as-reported cash flow statement data as a Pydantic model, or None if downloaded.
    """
    path = "/cash-flow-statement-as-reported/{symbol}"
    query_vars = {"apikey": apikey, "period": period, "limit": limit}
    return __return_json_stable(path, query_vars)


@parse_response
def financial_statement_full_as_reported(
    apikey: str,
    symbol: str,
    period: str = "annual",
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

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of full as-reported financial statement data as a Pydantic model.
    """
    path = "/financial-statement-full-as-reported/{symbol}"
    query_vars = {"apikey": apikey, "period": period}
    return __return_json_stable(path, query_vars)


@parse_response
def financial_statement_symbol_lists(
    apikey: str,
) -> RootModel[typing.List[FMPFinancialStatementSymbolList]]:
    """
    Retrieve the list of symbols that have financial statements.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of symbols as a Pydantic model.
    """
    path = "financial-statement-symbol-lists"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def income_statement_growth(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPFinancialStatementGrowth]]:
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
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "symbol": symbol,
        "period": __validate_period(period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def balance_sheet_statement_growth(
    apikey: str, symbol: str, limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPFinancialStatementGrowth]]:
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
    FmpFinancialStatementSymbolsListResponse
        List of balance sheet statement growth data as a Pydantic model.
    """
    path = "balance-sheet-statement-growth/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def cash_flow_statement_growth(
    apikey: str, symbol: str, limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPFinancialStatementGrowth]]:
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
    path = "cash-flow-statement-growth/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def financial_ratios_ttm(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPFinancialRatios]]:
    """
    Retrieve trailing twelve months (TTM) financial ratios for a company.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of TTM financial ratios as a Pydantic model.
    """
    path = "ratios-ttm/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def financial_ratios(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
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
    query_vars = {
        "apikey": apikey,
        "symbol": symbol,
        "limit": limit,
        "period": __validate_period(value=period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def enterprise_values(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[Any]]:
    """
    Retrieve enterprise values for a company.

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
        List of enterprise values as a Pydantic model.
    """
    path = "enterprise-values"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "symbol": symbol,
        "period": __validate_period(value=period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def key_metrics_ttm(
    apikey: str,
    symbol: str,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPKeyMetrics]]:
    """
    Retrieve trailing twelve months (TTM) key metrics for a company.

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
        List of TTM key metrics as a Pydantic model.
    """
    path = "key-metrics-ttm/{symbol}"
    query_vars = {"apikey": apikey, "limit": limit}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def key_metrics(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
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
    path = "key-metrics/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "period": __validate_period(value=period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def financial_growth(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[Any]]:
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
    path = "financial-growth/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "period": __validate_period(value=period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def rating(apikey: str, symbol: str) -> RootModel[typing.List[FMPStockGrade]]:
    """
    Retrieve company rating for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialStatementSymbolsListResponse
        List of company rating data as a Pydantic model.
    """
    path = "rating/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars=query_vars)


@parse_response
def historical_rating(
    apikey: str,
    symbol: str,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPHistoricalStockGrade]]:
    """
    Retrieve historical company rating for a given symbol.

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
        List of historical company rating data as a Pydantic model.
    """
    path = "historical-rating/{symbol}"
    query_vars = {"apikey": apikey, "limit": limit}
    return __return_json_stable(path, query_vars=query_vars)


@parse_response
def discounted_cash_flow(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve discounted cash flow (DCF) for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialEstimatesResponse
        List of discounted cash flow data as a Pydantic model.
    """
    path = "/discounted-cash-flow/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def levered_discounted_cash_flow(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve levered discounted cash flow for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialEstimatesResponse
        List of levered discounted cash flow data as a Pydantic model.
    """
    path = "/levered-discounted-cash-flow/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def custom_discounted_cash_flow(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve custom discounted cash flow for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialEstimatesResponse
        List of custom discounted cash flow data as a Pydantic model.
    """
    path = "/custom-discounted-cash-flow/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def custom_levered_discounted_cash_flow(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve custom levered discounted cash flow for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        Company ticker.

    Returns
    -------
    FmpFinancialEstimatesResponse
        List of custom levered discounted cash flow data as a Pydantic model.
    """
    path = "/custom-levered-discounted-cash-flow/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def historical_discounted_cash_flow(
    apikey: str,
    symbol: str,
    period: str = "annual",
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve historical discounted cash flow (DCF) for a given symbol.

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
    FmpFinancialEstimatesResponse
        List of historical discounted cash flow data as a Pydantic model.
    """
    path = "historical-discounted-cash-flow/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "period": __validate_period(value=period),
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_daily_discounted_cash_flow(
    apikey: str,
    symbol: str,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Retrieve daily historical discounted cash flow (DCF) for a given symbol.

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
    FmpFinancialEstimatesResponse
        List of daily historical discounted cash flow data as a Pydantic model.
    """
    path = "historical-daily-discounted-cash-flow/{symbol}"
    query_vars = {"apikey": apikey, "limit": limit}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def market_capitalization(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPMarketCap]]:
    """
    Retrieve the market capitalization for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').

    Returns
    -------
    FmpMarketCapitalizationResponse
        List of market capitalization data as a Pydantic model.
    """
    path = "market-capitalization/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def historical_market_capitalization(
    apikey: str,
    symbol: str,
    limit: int = DEFAULT_LIMIT,
    from_date: str = None,
    to_date: str = None,
) -> RootModel[typing.List[FMPHistoricalMarketCap]]:
    """
    Retrieve historical market capitalization for a given symbol.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    limit : int, optional
        Number of rows to return.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    FmpMarketCapitalizationResponse
        List of historical market capitalization data as a Pydantic model.
    """
    path = "historical-market-capitalization/{symbol}"
    query_vars = {"apikey": apikey, "limit": limit, "from": from_date, "to": to_date}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def symbols_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Retrieve the list of all stock symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of all stock symbols as a Pydantic model.
    """
    path = "stock/list"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def etf_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Retrieve the list of all ETF symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of all ETF symbols as a Pydantic model.
    """
    path = "etf/list"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def available_traded_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Retrieve the list of all available traded symbols.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    FmpCompanySymbolsListResponse
        List of all available traded symbols as a Pydantic model.
    """
    path = "available-traded/list"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def stock_screener(
    apikey: str,
    market_cap_more_than: typing.Union[float, int] = None,
    market_cap_lower_than: typing.Union[float, int] = None,
    beta_more_than: typing.Union[float, int] = None,
    beta_lower_than: typing.Union[float, int] = None,
    volume_more_than: typing.Union[float, int] = None,
    volume_lower_than: typing.Union[float, int] = None,
    dividend_more_than: typing.Union[float, int] = None,
    dividend_lower_than: typing.Union[float, int] = None,
    price_more_than: typing.Union[float, int] = None,
    price_lower_than: typing.Union[float, int] = None,
    is_etf: bool = None,
    is_fund: bool = None,
    is_actively_trading: bool = None,
    sector: str = None,
    industry: str = None,
    country: str = None,
    exchange: typing.Union[str, typing.List[str]] = None,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPStockScreenerResult]]:
    """
    Query FMP /stock-screener/ API.

    :param apikey: Your API key.
    :param market_cap_more_than: Numeric Value
    :param market_cap_lower_than: Numeric Value
    :param beta_more_than:  Numeric Value
    :param beta_lower_than:  Numeric Value
    :param volume_more_than:  Numeric Value
    :param volume_lower_than:  Numeric Value
    :param dividend_more_than:  Numeric Value
    :param dividend_lower_than:  Numeric Value
    :param price_more_than: Numeric Value
    :param price_lower_than: Numeric Value
    :param price_more_than: Numeric Value
    :param price_lower_than: Numeric Value
    :param is_etf: bool
    :param is_fund: bool
    :param is_actively_trading: bool
    :param sector: Valid sector name.
    :param industry: Valid industry name.
    :param country: 2 digit country code as string.
    :param exchange: Stock exchange symbol.
    :param limit: Number of rows to return.
    :return: A list of dicitonaries.
    """
    path = "company-screener"
    query_vars = {"apikey": apikey, "limit": limit}
    if market_cap_more_than:
        query_vars["marketCapMoreThan"] = market_cap_more_than
    if market_cap_lower_than:
        query_vars["marketCapLowerThan"] = market_cap_lower_than
    if beta_more_than:
        query_vars["betaMoreThan"] = beta_more_than
    if beta_lower_than:
        query_vars["betaLowerThan"] = beta_lower_than
    if volume_more_than:
        query_vars["volumeMoreThan"] = volume_more_than
    if volume_lower_than:
        query_vars["volumeLowerThan"] = volume_lower_than
    if dividend_more_than:
        query_vars["dividendMoreThan"] = dividend_more_than
    if dividend_lower_than:
        query_vars["dividendLowerThan"] = dividend_lower_than
    if price_more_than:
        query_vars["priceMoreThan"] = price_more_than
    if price_lower_than:
        query_vars["priceLowerThan"] = price_lower_than
    if is_etf is not None:
        query_vars["isEtf"] = is_etf
    if is_fund is not None:
        query_vars["isFund"] = is_fund
    if is_actively_trading is not None:
        query_vars["isActivelyTrading"] = is_actively_trading
    if sector:
        query_vars["sector"] = __validate_sector(sector)
    if industry:
        query_vars["industry"] = __validate_industry(industry)
    if country:
        query_vars["country"] = country
    if exchange:
        if type(exchange) is list:
            query_vars["exchange"] = ",".join(exchange)
        else:
            query_vars["exchange"] = exchange
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def stock_news(
    apikey: str,
    tickers: typing.Union[str, typing.List] = "",
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /stock_news/ API.

    :param apikey: Your API key.
    :param tickers: List of ticker symbols.
    :param from_date: The starting time for the API ("yyyy-mm-dd").
    :param to_date: The ending time for the API ("yyyy-mm-dd")
    :param page: Page number.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "stock_news"
    query_vars = {"apikey": apikey, "limit": limit, "page": page}
    if tickers:
        if type(tickers) is list:
            tickers = ",".join(tickers)
        query_vars["tickers"] = tickers
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def earnings_surprises(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPBulkEarningsSurprise]]:
    """
    Query FMP /earnings-surprises/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of dictionaries.
    """
    path = "earnings-surprises/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def earning_call_transcript(
    apikey: str, symbol: str, year: int, quarter: int
) -> RootModel[typing.List[FMPEarningsTranscript]]:
    """
    Query FMP /earning_call_transcript/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param year: Year of the transcripts
    :param quarter: Quarter of the transcripts
    :return: A list of dictionaries.
    """
    path = "earning_call_transcript/{symbol}"
    query_vars = {"apikey": apikey, "year": year, "quarter": quarter}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def batch_earning_call_transcript(
    apikey: str, symbol: str, year: int
) -> RootModel[typing.List[FMPEarningsTranscript]]:
    """
    Query FMP /batch_earning_call_transcript/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param year: Year of the transcripts
    :return: A list of dictionaries.
    """
    path = "batch_earning_call_transcript/{symbol}"
    query_vars = {"apikey": apikey, "year": year}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def earning_call_transcripts_available_dates(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPEarningsTranscriptDate]]:
    """
    Query FMP /earning_call_transcript/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :return: A list of lists.
    """
    path = "earning_call_transcript"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def sec_filings(
    apikey: str, symbol: str, filing_type: str = "", limit: int = DEFAULT_LIMIT
) -> RootModel[typing.List[FMPCompanySECFilings]]:
    """
    Query FMP /sec_filings/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param filing_type: Name of filing.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "sec_filings/{symbol}"
    query_vars = {"apikey": apikey, "type": filing_type, "limit": limit}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def press_releases(
    apikey: str,
    symbol: str,
    from_date: str = None,
    to_date: str = None,
    page: int = 0,
    limit: int = DEFAULT_LIMIT,
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Query FMP /press-releases/ API.

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param limit: Number of rows to return.
    :return: A list of dictionaries.
    """
    path = "press-releases/{symbol}"
    query_vars = {
        "apikey": apikey,
        "limit": limit,
        "from": from_date,
        "to": to_date,
        "page": page,
    }
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def social_sentiments(
    apikey: str, symbol: str, page: int = 0
) -> RootModel[typing.List[Any]]:
    """
    Query FMP /historical/social-sentiment/ API

    :param apikey: Your API key.
    :param symbol: Company ticker.
    :param page: Page number.
    :return: A list of dictionaries.
    """
    path = "historical/social-sentiment"
    query_vars = {"apikey": apikey, "symbol": symbol, "page": page}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def analyst_estimates(
    apikey: str, symbol: str, period: str = "annual", limit: int = None
) -> RootModel[typing.List[FMPAnalystEstimates]]:
    """
    Get analyst estimates using the /stable/analyst-estimates endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get analyst estimates for.
        period (str): The period for estimates ('annual' or 'quarter').
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with analyst estimates.
    """
    path = "analyst-estimates"
    query_vars = {"apikey": apikey, "symbol": symbol, "period": period}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def ratings_snapshot(
    apikey: str, symbol: str, date: str = None
) -> RootModel[typing.List[FMPRatingSnapshot]]:
    """
    Get ratings snapshot using the /stable/ratings-snapshot endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get ratings for.
        date (str, optional): Filter by date (YYYY-MM-DD).
    Returns:
        List of dictionaries with ratings snapshot.
    """
    path = "ratings-snapshot"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if date:
        query_vars["date"] = date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def ratings_historical(
    apikey: str, symbol: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPHistoricalRating]]:
    """
    Get historical ratings using the /stable/ratings-historical endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get historical ratings for.
        from_date (str, optional): Start date (YYYY-MM-DD).
        to_date (str, optional): End date (YYYY-MM-DD).
    Returns:
        List of dictionaries with historical ratings.
    """
    path = "ratings-historical"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def price_target_summary(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPPriceTargetSummary]]:
    """
    Get price target summary using the /stable/price-target-summary endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target summary for.
    Returns:
        List of dictionaries with price target summary.
    """
    path = "price-target-summary"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def price_target_consensus(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPPriceTargetConsensus]]:
    """
    Get price target consensus using the /stable/price-target-consensus endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target consensus for.
    Returns:
        List of dictionaries with price target consensus.
    """
    path = "price-target-consensus"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def price_target_news(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPPriceTargetNews]]:
    """
    Get price target news using the /stable/price-target-news endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get price target news for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with price target news.
    """
    path = "price-target-news"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def price_target_latest_news(
    apikey: str, symbol: str, limit: int = None
) -> RootModel[typing.List[FMPPressRelease]]:
    """
    Get latest price target news using the /stable/price-target-latest-news endpoint.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The symbol to get latest price target news for.
        limit (int, optional): Limit the number of results.
    Returns:
        List of dictionaries with latest price target news.
    """
    path = "price-target-latest-news"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if limit:
        query_vars["limit"] = limit
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def available_industries(apikey: str) -> RootModel[typing.List[FMPIndustry]]:
    """
    Query FMP /available-industries/ API.

    Get a list of all available industries.
    :param apikey: Your API key.
    :return: A list of industry names.
    """
    path = "available-industries"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def upgrades_downgrades_consensus(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPBulkUpgradeDowngradeConsensus]]:
    """
    Query FMP /upgrades-downgrades-consensus/ API.

    Get analyst upgrades and downgrades consensus for a specific company.

    https://site.financialmodelingprep.com/developer/docs#upgrades-downgrades-consensus

    Endpoint:
        https://financialmodelingprep.com/api/v4/upgrades-downgrades-consensus?symbol=AAPL

    :param apikey: Your API key.
    :param symbol: Company ticker symbol.
    :return: A list of dictionaries containing analyst consensus data with fields:
             - symbol: The stock symbol
             - date: The date of the consensus
             - gradingCompany: The company providing the rating
             - previousGrade: The previous rating
             - newGrade: The new rating
             - action: The type of action (upgrade/downgrade)
             - consensusType: The type of consensus
             - text: Additional commentary or notes
    """
    if not symbol:
        logging.warning(
            "No symbol provided for upgrades & downgrades consensus request."
        )
        return None

    path = "upgrades-downgrades-consensus"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def esg_disclosures(apikey: str, symbol: str) -> RootModel[typing.List[FMPESGFiling]]:
    """
    Get ESG disclosures for a given symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    apikey : str
        Your FMP API key.
    kwargs : dict
        Additional query parameters.

    Returns
    -------
    list
        List of ESG disclosures.
    """
    path = "/esg-disclosures/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def esg_ratings(apikey: str, symbol: str) -> RootModel[typing.List[FMPESGRating]]:
    """
    Get ESG ratings for a given symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    apikey : str
        Your FMP API key.
    kwargs : dict
        Additional query parameters.

    Returns
    -------
    list
        List of ESG ratings.
    """
    path = "/esg-ratings/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def esg_benchmark(apikey: str, symbol: str) -> RootModel[typing.List[FMPESGBenchmark]]:
    """
    Get ESG benchmark data for a given symbol.

    Parameters
    ----------
    symbol : str
        The ticker symbol (e.g., 'AAPL').
    apikey : str
        Your FMP API key.
    kwargs : dict
        Additional query parameters.

    Returns
    -------
    list
        List of ESG benchmark data.
    """
    path = "/esg-benchmark/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path, query_vars)


@parse_response
def earnings(
    apikey: str, symbol: str = None, limit: int = 100
) -> RootModel[typing.List[FMPEarningsReport]]:
    """
    Query FMP /earnings endpoint.

    :param apikey: Your API key.
    :param symbol: Optional ticker symbol to filter earnings (if supported by API).
    :param limit: Number of records to return (default 100).
    :return: A list of dictionaries with earnings data.
    """
    path = "earnings"
    query_vars = {"apikey": apikey, "limit": limit}
    if symbol:
        query_vars["symbol"] = symbol
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def company_notes(apikey: str, symbol: str) -> RootModel[typing.List[FMPCompanyNote]]:
    """
    Query FMP /company-notes endpoint.
    :param apikey: Your API key.
    :param symbol: Ticker symbol.
    :return: List of company notes.
    """
    path = "company-notes/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)


@parse_response
def market_capitalization_batch(
    apikey: str, symbols: typing.List[str]
) -> RootModel[typing.List[FMPMarketCap]]:
    """
    Query FMP /market-capitalization-batch endpoint.
    :param apikey: Your API key.
    :param symbols: List of ticker symbols.
    :return: List of market capitalization data for the batch.
    """
    path = f"market-capitalization-batch/{','.join(symbols)}"
    query_vars = {"apikey": apikey}
    return __return_json_stable(path=path, query_vars=query_vars)
