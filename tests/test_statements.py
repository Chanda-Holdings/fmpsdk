from datetime import datetime

import pytest

from fmpsdk.models import (
    FMPAsReportedBalanceSheet,
    FMPAsReportedCashFlowStatement,
    FMPAsReportedFullStatement,
    FMPAsReportedIncomeStatement,
    FMPBalanceSheetGrowth,
    FMPBalanceSheetStatement,
    FMPCashFlowGrowth,
    FMPCashFlowStatement,
    FMPFinancialRatios,
    FMPFinancialRatiosTTM,
    FMPFinancialReportDate,
    FMPFinancialScores,
    FMPFullFinancialReport,
    FMPIncomeStatement,
    FMPIncomeStatementGrowth,
    FMPKeyMetrics,
    FMPKeyMetricsTTM,
)
from fmpsdk.statements import (
    balance_sheet_statement,
    balance_sheet_statement_as_reported,
    balance_sheet_statement_growth,
    balance_sheet_statements_ttm,
    cash_flow_statement,
    cash_flow_statement_as_reported,
    cash_flow_statement_growth,
    cashflow_statements_ttm,
    enterprise_values,
    financial_growth,
    financial_ratios,
    financial_ratios_ttm,
    financial_reports_dates,
    financial_reports_json,
    financial_reports_xlsx,
    financial_scores,
    financial_statement_full_as_reported,
    financial_statements_latest,
    income_statement,
    income_statement_as_reported,
    income_statement_growth,
    income_statement_ttm,
    key_metrics,
    key_metrics_ttm,
    owner_earnings,
    revenue_geographic_segmentation,
    revenue_product_segmentation,
)
from tests.conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper function to get field value from either dict or model."""
    if isinstance(item, dict):
        return item.get(field_name)
    else:
        return getattr(item, field_name, None)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestBasicFinancialStatements:
    """Test class for basic financial statement endpoints."""

    def test_income_statement_annual(self, api_key):
        """Test annual income statement for a reliable symbol."""
        result = income_statement(
            apikey=api_key, symbol="AAPL", period="annual", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first item structure
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPIncomeStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.revenue is not None
        assert validated.netIncome is not None
        assert validated.period == "FY"

    def test_income_statement_quarterly(self, api_key):
        """Test quarterly income statement for a reliable symbol."""
        result = income_statement(
            apikey=api_key, symbol="MSFT", period="quarter", limit=4
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate quarterly data
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPIncomeStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "MSFT"
        assert validated.period in ["Q1", "Q2", "Q3", "Q4"]
        assert validated.revenue is not None

    def test_balance_sheet_statement_annual(self, api_key):
        """Test annual balance sheet statement."""
        result = balance_sheet_statement(
            apikey=api_key, symbol="GOOGL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPBalanceSheetStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "GOOGL"
        assert validated.totalAssets is not None
        assert validated.totalEquity is not None
        assert validated.period == "FY"

    def test_cash_flow_statement_quarterly(self, api_key):
        """Test quarterly cash flow statement."""
        result = cash_flow_statement(
            apikey=api_key, symbol="AMZN", period="quarter", limit=4
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPCashFlowStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AMZN"
        assert validated.operatingCashFlow is not None
        assert validated.period in ["Q1", "Q2", "Q3", "Q4"]

    def test_financial_statements_latest(self, api_key):
        """Test latest financial statements endpoint."""
        result = financial_statements_latest(apikey=api_key, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Check that we have recent data
        first_item = result_list[0]
        symbol_value = get_field_value(first_item, "symbol")
        assert symbol_value is not None
        assert len(symbol_value) > 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTTMFinancialStatements:
    """Test class for trailing twelve months (TTM) financial statements."""

    def test_income_statement_ttm(self, api_key):
        """Test TTM income statement."""
        result = income_statement_ttm(apikey=api_key, symbol="AAPL", limit=5)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPIncomeStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.revenue is not None
        assert validated.netIncome is not None

    def test_balance_sheet_statements_ttm(self, api_key):
        """Test TTM balance sheet statements."""
        result = balance_sheet_statements_ttm(apikey=api_key, symbol="MSFT", limit=3)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPBalanceSheetStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "MSFT"
        assert validated.totalAssets is not None

    def test_cashflow_statements_ttm(self, api_key):
        """Test TTM cash flow statements."""
        result = cashflow_statements_ttm(apikey=api_key, symbol="GOOGL", limit=3)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPCashFlowStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "GOOGL"
        assert validated.operatingCashFlow is not None


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFinancialMetricsAndRatios:
    """Test class for financial metrics and ratios."""

    def test_key_metrics_annual(self, api_key):
        """Test key metrics for annual periods."""
        result = key_metrics(apikey=api_key, symbol="AAPL", period="annual", limit=5)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPKeyMetrics.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.marketCap is not None
        assert validated.returnOnEquity is not None

    def test_key_metrics_quarterly(self, api_key):
        """Test key metrics for quarterly periods."""
        result = key_metrics(apikey=api_key, symbol="MSFT", period="quarter", limit=4)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        symbol_value = get_field_value(first_item, "symbol")
        assert symbol_value == "MSFT"

        market_cap = get_field_value(first_item, "marketCap")
        assert market_cap is not None

    def test_financial_ratios_annual(self, api_key):
        """Test financial ratios for annual periods."""
        result = financial_ratios(
            apikey=api_key, symbol="GOOGL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPFinancialRatios.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "GOOGL"
        assert validated.currentRatio is not None

    def test_key_metrics_ttm(self, api_key):
        """Test TTM key metrics."""
        result = key_metrics_ttm(apikey=api_key, symbol="AMZN")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPKeyMetricsTTM.model_validate(first_item)
        else:
            validated = first_item

        # TTM metrics should have symbol and specific TTM fields
        assert validated.symbol == "AMZN"
        assert validated.marketCap is not None
        assert validated.evToSalesTTM is not None

    def test_financial_ratios_ttm(self, api_key):
        """Test TTM financial ratios."""
        result = financial_ratios_ttm(apikey=api_key, symbol="TSLA")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPFinancialRatiosTTM.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "TSLA"

    def test_financial_scores(self, api_key):
        """Test financial scores."""
        result = financial_scores(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPFinancialScores.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestValuationMetrics:
    """Test class for valuation and enterprise metrics."""

    def test_owner_earnings(self, api_key):
        """Test owner earnings calculation."""
        result = owner_earnings(apikey=api_key, symbol="MSFT", limit=5)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        symbol_value = get_field_value(first_item, "symbol")
        assert symbol_value == "MSFT"

        # Owner earnings should have some value
        owner_earnings_value = get_field_value(first_item, "ownersEarnings")
        assert owner_earnings_value is not None

    def test_enterprise_values(self, api_key):
        """Test enterprise values."""
        result = enterprise_values(
            apikey=api_key, symbol="GOOGL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        symbol_value = get_field_value(first_item, "symbol")
        assert symbol_value == "GOOGL"

        # Enterprise value should be present
        ev_value = get_field_value(first_item, "enterpriseValue")
        assert ev_value is not None


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestGrowthMetrics:
    """Test class for financial growth metrics."""

    def test_income_statement_growth(self, api_key):
        """Test income statement growth metrics."""
        result = income_statement_growth(
            apikey=api_key, symbol="AAPL", period="annual", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPIncomeStatementGrowth.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        # Note: Growth metrics may be None for some periods/companies
        # Just ensure the structure is correct
        assert validated.date is not None

    def test_balance_sheet_statement_growth(self, api_key):
        """Test balance sheet growth metrics."""
        result = balance_sheet_statement_growth(
            apikey=api_key, symbol="MSFT", period="quarter", limit=4
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPBalanceSheetGrowth.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "MSFT"

    def test_cash_flow_statement_growth(self, api_key):
        """Test cash flow growth metrics."""
        result = cash_flow_statement_growth(
            apikey=api_key, symbol="GOOGL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPCashFlowGrowth.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "GOOGL"

    def test_financial_growth(self, api_key):
        """Test comprehensive financial growth metrics."""
        result = financial_growth(
            apikey=api_key, symbol="AMZN", period="annual", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPIncomeStatementGrowth.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AMZN"
        assert validated.revenueGrowth is not None


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestFinancialReports:
    """Test class for financial reports and dates."""

    def test_financial_reports_dates(self, api_key):
        """Test financial report dates availability."""
        result = financial_reports_dates(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPFinancialReportDate.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.fiscalYear is not None
        assert validated.fiscalYear > 2000  # Should be a reasonable year

    def test_financial_reports_json(self, api_key):
        """Test financial reports in JSON format."""
        current_year = datetime.now().year
        result = financial_reports_json(
            apikey=api_key, symbol="MSFT", year=current_year - 1, period="FY"
        )

        # This endpoint returns a single object, not a list
        assert isinstance(result, FMPFullFinancialReport)
        assert result.symbol == "MSFT"
        assert result.period == "FY"
        assert result.year == str(current_year - 1)

    def test_financial_reports_xlsx(self, api_key):
        """Test financial reports in Excel format."""
        current_year = datetime.now().year
        result = financial_reports_xlsx(
            apikey=api_key, symbol="GOOGL", year=current_year - 1, period="FY"
        )

        # Excel format returns bytes
        assert isinstance(result, bytes)
        assert len(result) > 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestRevenueSegmentation:
    """Test class for revenue segmentation analysis."""

    def test_revenue_product_segmentation(self, api_key):
        """Test revenue by product segments."""
        # Apple has clear product segmentation
        result = revenue_product_segmentation(
            apikey=api_key, symbol="AAPL", period="annual"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Segmentation data may be empty for some companies
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            assert symbol_value == "AAPL"

    def test_revenue_geographic_segmentation(self, api_key):
        """Test revenue by geographic segments."""
        # Microsoft has geographic segmentation
        result = revenue_geographic_segmentation(
            apikey=api_key, symbol="MSFT", period="annual"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Geographic segmentation may be empty for some companies
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            assert symbol_value == "MSFT"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestAsReportedStatements:
    """Test class for as-reported financial statements."""

    def test_income_statement_as_reported(self, api_key):
        """Test as-reported income statement."""
        result = income_statement_as_reported(
            apikey=api_key, symbol="AAPL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAsReportedIncomeStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"

    def test_balance_sheet_statement_as_reported(self, api_key):
        """Test as-reported balance sheet statement."""
        result = balance_sheet_statement_as_reported(
            apikey=api_key, symbol="MSFT", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAsReportedBalanceSheet.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "MSFT"

    def test_cash_flow_statement_as_reported(self, api_key):
        """Test as-reported cash flow statement."""
        result = cash_flow_statement_as_reported(
            apikey=api_key, symbol="GOOGL", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAsReportedCashFlowStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "GOOGL"

    def test_financial_statement_full_as_reported(self, api_key):
        """Test full as-reported financial statements."""
        result = financial_statement_full_as_reported(
            apikey=api_key, symbol="AMZN", period="annual", limit=3
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAsReportedFullStatement.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AMZN"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStatementsErrorHandling:
    """Test class for error handling in statements endpoints."""

    def test_income_statement_invalid_symbol(self, api_key):
        """Test income statement with invalid symbol."""
        result = income_statement(apikey=api_key, symbol="INVALID123", period="annual")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_key_metrics_invalid_api_key(self):
        """Test key metrics with invalid API key."""
        result = key_metrics(apikey="invalid_key", symbol="AAPL")

        # Should return an error response
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]

    def test_financial_ratios_invalid_period(self, api_key):
        """Test financial ratios with invalid period."""
        result = financial_ratios(apikey=api_key, symbol="AAPL", period="invalid")

        result_list = extract_data_list(result)
        # Should return empty list or handle gracefully
        assert isinstance(result_list, list)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStatementsResponseTimes:
    """Test class for response time validation in statements endpoints."""

    def test_income_statement_response_time(self, api_key):
        """Test income statement response time."""
        import time

        start_time = time.time()

        result = income_statement(
            apikey=api_key, symbol="AAPL", period="annual", limit=5
        )

        end_time = time.time()
        response_time = end_time - start_time

        assert response_time < 10.0  # Should respond within 10 seconds

        result_list = extract_data_list(result)
        assert len(result_list) > 0

    def test_key_metrics_response_time(self, api_key):
        """Test key metrics response time."""
        import time

        start_time = time.time()

        result = key_metrics(apikey=api_key, symbol="MSFT", period="annual", limit=5)

        end_time = time.time()
        response_time = end_time - start_time

        assert response_time < 10.0  # Should respond within 10 seconds

        result_list = extract_data_list(result)
        assert len(result_list) > 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStatementsDataConsistency:
    """Test class for data consistency across statements endpoints."""

    def test_income_statement_periods_consistency(self, api_key):
        """Test consistency between annual and quarterly income statements."""
        annual_result = income_statement(
            apikey=api_key, symbol="AAPL", period="annual", limit=1
        )
        quarterly_result = income_statement(
            apikey=api_key, symbol="AAPL", period="quarter", limit=4
        )

        annual_list = extract_data_list(annual_result)
        quarterly_list = extract_data_list(quarterly_result)

        assert len(annual_list) > 0
        assert len(quarterly_list) > 0

        # Both should be for same symbol
        annual_symbol = get_field_value(annual_list[0], "symbol")
        quarterly_symbol = get_field_value(quarterly_list[0], "symbol")

        assert annual_symbol == quarterly_symbol == "AAPL"

    def test_ttm_vs_regular_statements_consistency(self, api_key):
        """Test consistency between TTM and regular statements."""
        regular_result = income_statement(
            apikey=api_key, symbol="MSFT", period="annual", limit=1
        )
        ttm_result = income_statement_ttm(apikey=api_key, symbol="MSFT", limit=1)

        regular_list = extract_data_list(regular_result)
        ttm_list = extract_data_list(ttm_result)

        assert len(regular_list) > 0
        assert len(ttm_list) > 0

        # Both should be for same symbol
        regular_symbol = get_field_value(regular_list[0], "symbol")
        ttm_symbol = get_field_value(ttm_list[0], "symbol")

        assert regular_symbol == ttm_symbol == "MSFT"

    def test_key_metrics_vs_ratios_consistency(self, api_key):
        """Test consistency between key metrics and financial ratios."""
        metrics_result = key_metrics(
            apikey=api_key, symbol="GOOGL", period="annual", limit=1
        )
        ratios_result = financial_ratios(
            apikey=api_key, symbol="GOOGL", period="annual", limit=1
        )

        metrics_list = extract_data_list(metrics_result)
        ratios_list = extract_data_list(ratios_result)

        assert len(metrics_list) > 0
        assert len(ratios_list) > 0

        # Both should be for same symbol
        metrics_symbol = get_field_value(metrics_list[0], "symbol")
        ratios_symbol = get_field_value(ratios_list[0], "symbol")

        assert metrics_symbol == ratios_symbol == "GOOGL"

    def test_financial_statement_dates_chronology(self, api_key):
        """Test that financial statement dates are in chronological order."""
        result = income_statement(
            apikey=api_key, symbol="AAPL", period="annual", limit=5
        )

        result_list = extract_data_list(result)
        assert len(result_list) >= 2

        # Dates should be in descending order (newest first)
        dates = []
        for item in result_list:
            date_value = get_field_value(item, "date")
            if date_value:
                dates.append(date_value)

        # Check that dates are sorted (newest first)
        for i in range(len(dates) - 1):
            assert dates[i] >= dates[i + 1]
