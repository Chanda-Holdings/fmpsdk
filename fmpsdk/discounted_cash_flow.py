import typing

from pydantic import RootModel

from .models import (
    FMPDCFCustomValuation,
    FMPDcfValuation,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def discounted_cash_flow_valuation(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Get the discounted cash flow (DCF) valuation for a specific stock.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The stock symbol to get the DCF valuation for.

    Returns:
       FMPDcfValuation
    """
    path = "discounted-cash-flow"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def discounted_cash_flow_levered(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPDcfValuation]]:
    """
    Get the levered discounted cash flow (DCF) valuation for a specific stock.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The stock symbol to get the DCF valuation for.

    Returns:
       FMPDcfValuation
    """
    path = "levered-discounted-cash-flow"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def discounted_cash_flow_custom(
    apikey: str,
    symbol: str,
    revenue_growth_pct: float = None,
    ebidta_pct: float = None,
    depreciation_and_amortization_pct: float = None,
    cash_and_short_term_investments_pct: float = None,
    receivables_pct: float = None,
    inventories_pct: float = None,
    payable_pct: float = None,
    ebit_pct: float = None,
    capital_expenditure_pct: float = None,
    operating_cash_flow_pct: float = None,
    selling_general_and_administrative_expenses_pct: float = None,
    tax_rate: float = None,
    long_term_growth_rate: float = None,
    cost_of_debt: float = None,
    cost_of_equity: float = None,
    market_risk_premium: float = None,
    beta: float = None,
    risk_free_rate: float = None,
) -> RootModel[typing.List[FMPDCFCustomValuation]]:
    """
    Get the discounted cash flow (DCF) valuation for a specific stock.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The stock symbol to get the DCF valuation for.
        revenue_growth_pct (float, optional): Revenue growth percentage.
        ebidta_pct (float, optional): EBITDA percentage.
        depreciation_and_amortization_pct (float, optional): Depreciation and amortization percentage.
        cash_and_short_term_investments_pct (float, optional): Cash and short-term investments percentage.
        receivables_pct (float, optional): Receivables percentage.
        inventories_pct (float, optional): Inventories percentage.
        payable_pct (float, optional): Payable percentage.
        ebit_pct (float, optional): EBIT percentage.
        capital_expenditure_pct (float, optional): Capital expenditure percentage.
        operating_cash_flow_pct (float, optional): Operating cash flow percentage.
        selling_general_and_administrative_expenses_pct (float, optional): Selling, general, and administrative expenses percentage.
        tax_rate (float, optional): Tax rate.
        long_term_growth_rate (float, optional): Long-term growth rate.
        cost_of_debt (float, optional): Cost of debt.
        cost_of_equity (float, optional): Cost of equity.
        market_risk_premium (float, optional): Market risk premium.
        beta (float, optional): Beta value.
        risk_free_rate (float, optional): Risk-free rate.

    Returns:
       FMPDCFCustomValuation
    """
    path = "custom-discounted-cash-flow"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if revenue_growth_pct is not None:
        query_vars["revenueGrowthPct"] = str(revenue_growth_pct)
    if ebidta_pct is not None:
        query_vars["ebidtaPct"] = str(ebidta_pct)
    if depreciation_and_amortization_pct is not None:
        query_vars["depreciationAndAmortizationPct"] = str(
            depreciation_and_amortization_pct
        )
    if cash_and_short_term_investments_pct is not None:
        query_vars["cashAndShortTermInvestmentsPct"] = str(
            cash_and_short_term_investments_pct
        )
    if receivables_pct is not None:
        query_vars["receivablesPct"] = str(receivables_pct)
    if inventories_pct is not None:
        query_vars["inventoriesPct"] = str(inventories_pct)
    if payable_pct is not None:
        query_vars["payablePct"] = str(payable_pct)
    if ebit_pct is not None:
        query_vars["ebitPct"] = str(ebit_pct)
    if capital_expenditure_pct is not None:
        query_vars["capitalExpenditurePct"] = str(capital_expenditure_pct)
    if operating_cash_flow_pct is not None:
        query_vars["operatingCashFlowPct"] = str(operating_cash_flow_pct)
    if selling_general_and_administrative_expenses_pct is not None:
        query_vars["sellingGeneralAndAdministrativeExpensesPct"] = str(
            selling_general_and_administrative_expenses_pct
        )
    if tax_rate is not None:
        query_vars["taxRate"] = str(tax_rate)
    if long_term_growth_rate is not None:
        query_vars["longTermGrowthRate"] = str(long_term_growth_rate)
    if cost_of_debt is not None:
        query_vars["costOfDebt"] = str(cost_of_debt)
    if cost_of_equity is not None:
        query_vars["costOfEquity"] = str(cost_of_equity)
    if market_risk_premium is not None:
        query_vars["marketRiskPremium"] = str(market_risk_premium)
    if beta is not None:
        query_vars["beta"] = str(beta)
    if risk_free_rate is not None:
        query_vars["riskFreeRate"] = str(risk_free_rate)
    return __return_json(path=path, query_vars=query_vars)


@parse_response
def discounted_cash_flow_custom_levered(
    apikey: str,
    symbol: str,
    revenue_growth_pct: float = None,
    ebidta_pct: float = None,
    depreciation_and_amortization_pct: float = None,
    cash_and_short_term_investments_pct: float = None,
    receivables_pct: float = None,
    inventories_pct: float = None,
    payable_pct: float = None,
    ebit_pct: float = None,
    capital_expenditure_pct: float = None,
    operating_cash_flow_pct: float = None,
    selling_general_and_administrative_expenses_pct: float = None,
    tax_rate: float = None,
    long_term_growth_rate: float = None,
    cost_of_debt: float = None,
    cost_of_equity: float = None,
    market_risk_premium: float = None,
    beta: float = None,
    risk_free_rate: float = None,
) -> RootModel[typing.List[FMPDCFCustomValuation]]:
    """
    Get the levered discounted cash flow (DCF) valuation for a specific stock.

    Parameters:
        apikey (str): Your API key.
        symbol (str): The stock symbol to get the DCF valuation for.
        revenue_growth_pct (float, optional): Revenue growth percentage.
        ebidta_pct (float, optional): EBITDA percentage.
        depreciation_and_amortization_pct (float, optional): Depreciation and amortization percentage.
        cash_and_short_term_investments_pct (float, optional): Cash and short-term investments percentage.
        receivables_pct (float, optional): Receivables percentage.
        inventories_pct (float, optional): Inventories percentage.
        payable_pct (float, optional): Payable percentage.
        ebit_pct (float, optional): EBIT percentage.
        capital_expenditure_pct (float, optional): Capital expenditure percentage.
        operating_cash_flow_pct (float, optional): Operating cash flow percentage.
        selling_general_and_administrative_expenses_pct (float, optional): Selling, general, and administrative expenses percentage.
        tax_rate (float, optional): Tax rate.
        long_term_growth_rate (float, optional): Long-term growth rate.
        cost_of_debt (float, optional): Cost of debt.
        cost_of_equity (float, optional): Cost of equity.
        market_risk_premium (float, optional): Market risk premium.
        beta (float, optional): Beta value.
        risk_free_rate (float, optional): Risk-free rate.

    Returns:
       FMPDCFCustomValuation
    """
    path = "custom-levered-discounted-cash-flow"
    query_vars = {"apikey": apikey, "symbol": symbol}
    if revenue_growth_pct is not None:
        query_vars["revenueGrowthPct"] = str(revenue_growth_pct)
    if ebidta_pct is not None:
        query_vars["ebidtaPct"] = str(ebidta_pct)
    if depreciation_and_amortization_pct is not None:
        query_vars["depreciationAndAmortizationPct"] = str(
            depreciation_and_amortization_pct
        )
    if cash_and_short_term_investments_pct is not None:
        query_vars["cashAndShortTermInvestmentsPct"] = str(
            cash_and_short_term_investments_pct
        )
    if receivables_pct is not None:
        query_vars["receivablesPct"] = str(receivables_pct)
    if inventories_pct is not None:
        query_vars["inventoriesPct"] = str(inventories_pct)
    if payable_pct is not None:
        query_vars["payablePct"] = str(payable_pct)
    if ebit_pct is not None:
        query_vars["ebitPct"] = str(ebit_pct)
    if capital_expenditure_pct is not None:
        query_vars["capitalExpenditurePct"] = str(capital_expenditure_pct)
    if operating_cash_flow_pct is not None:
        query_vars["operatingCashFlowPct"] = str(operating_cash_flow_pct)
    if selling_general_and_administrative_expenses_pct is not None:
        query_vars["sellingGeneralAndAdministrativeExpensesPct"] = str(
            selling_general_and_administrative_expenses_pct
        )
    if tax_rate is not None:
        query_vars["taxRate"] = str(tax_rate)
    if long_term_growth_rate is not None:
        query_vars["longTermGrowthRate"] = str(long_term_growth_rate)
    if cost_of_debt is not None:
        query_vars["costOfDebt"] = str(cost_of_debt)
    if cost_of_equity is not None:
        query_vars["costOfEquity"] = str(cost_of_equity)
    if market_risk_premium is not None:
        query_vars["marketRiskPremium"] = str(market_risk_premium)
    if beta is not None:
        query_vars["beta"] = str(beta)
    if risk_free_rate is not None:
        query_vars["riskFreeRate"] = str(risk_free_rate)
    return __return_json(path=path, query_vars=query_vars)
