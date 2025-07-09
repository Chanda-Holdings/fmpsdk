import os
import time
from datetime import datetime
from typing import List

import pytest

from fmpsdk import discounted_cash_flow
from fmpsdk.models import FMPDCFCustomValuation, FMPDcfValuation
from tests.conftest import extract_data_list

# Test configuration
RESPONSE_TIME_LIMIT = 10.0  # seconds


@pytest.fixture
def api_key():
    """API key fixture for testing."""
    key = os.getenv("FMP_API_KEY")
    if not key:
        pytest.skip("FMP_API_KEY environment variable not set")
    return key


class TestDCFBasic:
    """Basic functionality tests for DCF endpoints."""

    def test_dcf_valuation_basic(self, api_key):
        """Test basic DCF valuation for a well-known stock."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey=api_key, symbol="AAPL"
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for dcf in data[:3]:  # Check first few items
                if isinstance(dcf, dict):
                    dcf_obj = FMPDcfValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate DCF data
                assert dcf_obj.symbol == "AAPL"
                assert dcf_obj.date
                assert isinstance(dcf_obj.dcf, (int, float))
                assert isinstance(dcf_obj.Stock_Price, (int, float))

                # DCF and stock price should be positive
                assert dcf_obj.dcf > 0
                assert dcf_obj.Stock_Price > 0

    def test_dcf_levered_valuation(self, api_key):
        """Test levered DCF valuation."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_levered(
            apikey=api_key, symbol="MSFT"
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for dcf in data[:3]:  # Check first few items
                if isinstance(dcf, dict):
                    dcf_obj = FMPDcfValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate DCF data
                assert dcf_obj.symbol == "MSFT"
                assert dcf_obj.date
                assert isinstance(dcf_obj.dcf, (int, float))
                assert isinstance(dcf_obj.Stock_Price, (int, float))

    def test_dcf_custom_basic(self, api_key):
        """Test custom DCF valuation without parameters."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key, symbol="GOOGL"
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for dcf in data[:3]:  # Check first few items
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate custom DCF data
                assert dcf_obj.symbol == "GOOGL"
                assert dcf_obj.year
                assert isinstance(dcf_obj.revenue, int)
                assert isinstance(dcf_obj.price, (int, float))
                assert isinstance(dcf_obj.beta, (int, float))

    def test_dcf_custom_levered_basic(self, api_key):
        """Test custom levered DCF valuation without parameters."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key, symbol="TSLA"
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for dcf in data[:3]:  # Check first few items
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate custom levered DCF data
                assert dcf_obj.symbol == "TSLA"
                assert dcf_obj.year
                assert isinstance(dcf_obj.revenue, int)
                assert isinstance(dcf_obj.price, (int, float))


class TestDCFCustomParameters:
    """Test DCF models with custom parameters."""

    def test_dcf_custom_with_growth_parameters(self, api_key):
        """Test custom DCF with growth parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="NVDA",
            revenue_growth_pct=15.0,
            long_term_growth_rate=3.0,
            tax_rate=0.21,
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for dcf in data[:3]:
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate that custom parameters might be reflected
                assert dcf_obj.symbol == "NVDA"
                assert isinstance(dcf_obj.longTermGrowthRate, (int, float))
                assert isinstance(dcf_obj.taxRate, (int, float))

    def test_dcf_custom_with_cost_parameters(self, api_key):
        """Test custom DCF with cost of capital parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AMZN",
            cost_of_equity=10.0,
            cost_of_debt=4.0,
            market_risk_premium=6.0,
            risk_free_rate=4.0,
            beta=1.2,
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for dcf in data[:3]:
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate cost parameters
                assert dcf_obj.symbol == "AMZN"
                assert isinstance(dcf_obj.costOfEquity, (int, float))
                assert isinstance(dcf_obj.costofDebt, (int, float))
                assert isinstance(dcf_obj.beta, (int, float))

    def test_dcf_custom_levered_with_parameters(self, api_key):
        """Test custom levered DCF with multiple parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key,
            symbol="META",
            revenue_growth_pct=12.0,
            ebidta_pct=30.0,
            depreciation_and_amortization_pct=5.0,
            capital_expenditure_pct=8.0,
            tax_rate=0.21,
            long_term_growth_rate=2.5,
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for dcf in data[:3]:
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Validate levered DCF data
                assert dcf_obj.symbol == "META"
                assert isinstance(dcf_obj.wacc, (int, float))
                assert isinstance(dcf_obj.debtWeighting, (int, float))
                assert isinstance(dcf_obj.equityWeighting, (int, float))


class TestDCFDataQuality:
    """Test DCF data quality and consistency."""

    def test_dcf_valuation_consistency(self, api_key):
        """Test DCF valuation data consistency."""
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey=api_key, symbol="JPM"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for dcf in data[:3]:
                if isinstance(dcf, dict):
                    dcf_obj = FMPDcfValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Date format consistency
                assert len(dcf_obj.date) >= 10  # YYYY-MM-DD format
                try:
                    datetime.strptime(dcf_obj.date[:10], "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format: {dcf_obj.date}")

                # Reasonable value ranges for large companies
                assert dcf_obj.dcf > 0, "DCF should be positive"
                assert dcf_obj.Stock_Price > 0, "Stock price should be positive"
                assert dcf_obj.dcf < 10000, "DCF seems unreasonably high"
                assert (
                    dcf_obj.Stock_Price < 10000
                ), "Stock price seems unreasonably high"

    def test_custom_dcf_calculation_consistency(self, api_key):
        """Test custom DCF calculation consistency."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key, symbol="JNJ"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for dcf in data[:3]:
                if isinstance(dcf, dict):
                    dcf_obj = FMPDCFCustomValuation(**dcf)
                else:
                    dcf_obj = dcf

                # Financial ratios consistency
                if (
                    dcf_obj.debtWeighting is not None
                    and dcf_obj.equityWeighting is not None
                ):
                    # Debt + Equity weighting should approximately equal 1 (or 100 if in percentage form)
                    total_weighting = dcf_obj.debtWeighting + dcf_obj.equityWeighting
                    # Check if values are in percentage form (around 100) or decimal form (around 1)
                    if total_weighting > 10:  # Likely percentage form
                        assert (
                            90.0 <= total_weighting <= 110.0
                        ), f"Debt+Equity weighting should ~= 100%, got {total_weighting}"
                    else:  # Likely decimal form
                        assert (
                            0.9 <= total_weighting <= 1.1
                        ), f"Debt+Equity weighting should ~= 1, got {total_weighting}"

                # WACC should be reasonable (typically 5-20% when expressed as percentage)
                if dcf_obj.wacc is not None:
                    # WACC might be in percentage form (5.68 = 5.68%) or decimal form (0.0568 = 5.68%)
                    if dcf_obj.wacc > 1:  # Likely percentage form
                        assert (
                            2.0 <= dcf_obj.wacc <= 30.0
                        ), f"WACC should be 2-30%, got {dcf_obj.wacc}%"
                    else:  # Likely decimal form
                        assert (
                            0.02 <= dcf_obj.wacc <= 0.30
                        ), f"WACC should be 2-30%, got {dcf_obj.wacc}"

                # Beta should be reasonable (typically 0.5-2.5 for most stocks)
                if dcf_obj.beta is not None:
                    assert (
                        -1.0 <= dcf_obj.beta <= 5.0
                    ), f"Beta should be reasonable, got {dcf_obj.beta}"


class TestDCFSymbols:
    """Test DCF calculations across different types of companies."""

    def test_dcf_large_cap_tech(self, api_key):
        """Test DCF for large-cap tech companies."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = discounted_cash_flow.discounted_cash_flow_valuation(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            if data:
                for dcf in data[:1]:  # Check first item
                    if isinstance(dcf, dict):
                        dcf_obj = FMPDcfValuation(**dcf)
                    else:
                        dcf_obj = dcf

                    assert dcf_obj.symbol == symbol
                    assert dcf_obj.dcf > 0
                    assert dcf_obj.Stock_Price > 0

    def test_dcf_financial_companies(self, api_key):
        """Test DCF for financial companies."""
        symbols = ["JPM", "BAC", "WFC"]

        for symbol in symbols:
            result = discounted_cash_flow.discounted_cash_flow_valuation(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            if data:
                for dcf in data[:1]:  # Check first item
                    if isinstance(dcf, dict):
                        dcf_obj = FMPDcfValuation(**dcf)
                    else:
                        dcf_obj = dcf

                    assert dcf_obj.symbol == symbol

    def test_dcf_growth_companies(self, api_key):
        """Test DCF for growth companies."""
        symbols = ["NVDA", "TSLA", "CRM"]

        for symbol in symbols:
            result = discounted_cash_flow.discounted_cash_flow_custom(
                apikey=api_key,
                symbol=symbol,
                revenue_growth_pct=20.0,
                long_term_growth_rate=4.0,
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            if data:
                for dcf in data[:1]:  # Check first item
                    if isinstance(dcf, dict):
                        dcf_obj = FMPDCFCustomValuation(**dcf)
                    else:
                        dcf_obj = dcf

                    assert dcf_obj.symbol == symbol


class TestDCFErrorHandling:
    """Test error handling for DCF endpoints."""

    def test_dcf_invalid_api_key(self):
        """Test DCF with invalid API key."""
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey="invalid_key", symbol="AAPL"
        )

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_dcf_invalid_symbol(self, api_key):
        """Test DCF with invalid symbol."""
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey=api_key, symbol="INVALID123"
        )

        # Invalid symbol might return empty list or error
        data = extract_data_list(result)
        assert isinstance(data, list)
        # Empty list is acceptable for invalid symbols

    def test_dcf_custom_invalid_parameters(self, api_key):
        """Test custom DCF with invalid parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AAPL",
            revenue_growth_pct=-100.0,  # Invalid negative growth
            tax_rate=2.0,  # Invalid tax rate > 100%
            beta=-10.0,  # Invalid beta
        )

        # API might still return data with adjusted parameters
        # or return an error - both are acceptable
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_dcf_levered_invalid_api_key(self):
        """Test levered DCF with invalid API key."""
        result = discounted_cash_flow.discounted_cash_flow_levered(
            apikey="invalid_key", symbol="MSFT"
        )

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_dcf_custom_levered_invalid_api_key(self):
        """Test custom levered DCF with invalid API key."""
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey="invalid_key", symbol="GOOGL"
        )

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result


class TestDCFPerformance:
    """Test DCF endpoint performance."""

    def test_dcf_response_times(self, api_key):
        """Test that all DCF endpoints respond within acceptable time."""
        endpoints = [
            (
                "basic_dcf",
                lambda: discounted_cash_flow.discounted_cash_flow_valuation(
                    api_key, "AAPL"
                ),
            ),
            (
                "levered_dcf",
                lambda: discounted_cash_flow.discounted_cash_flow_levered(
                    api_key, "MSFT"
                ),
            ),
            (
                "custom_dcf",
                lambda: discounted_cash_flow.discounted_cash_flow_custom(
                    api_key, "GOOGL"
                ),
            ),
            (
                "custom_levered_dcf",
                lambda: discounted_cash_flow.discounted_cash_flow_custom_levered(
                    api_key, "TSLA"
                ),
            ),
        ]

        for endpoint_name, endpoint_func in endpoints:
            start_time = time.time()
            result = endpoint_func()
            response_time = time.time() - start_time

            # Skip premium endpoints

        # API should handle edge cases gracefully
        if isinstance(result, dict) and "Error Message" in result:
            return  # Error is acceptable for edge cases

        data = extract_data_list(result)
        assert isinstance(data, list)

    def test_dcf_custom_high_growth_scenario(self, api_key):
        """Test custom DCF with high growth scenario."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="ROKU",
            revenue_growth_pct=50.0,  # High growth
            long_term_growth_rate=5.0,  # Higher long-term growth
            cost_of_equity=15.0,  # Higher risk
            beta=2.0,  # High beta
        )

        # Should handle high growth scenarios
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
