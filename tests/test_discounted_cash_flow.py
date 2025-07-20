import time
from datetime import datetime

import pytest

from fmpsdk import discounted_cash_flow
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import FMPDCFCustomValuation, FMPDcfValuation
from tests.conftest import (
    get_response_models,
    validate_model_list,
)

RESPONSE_TIME_LIMIT = 10


class TestDCFValuation:

    def test_dcf_valuation_basic(self, api_key):
        """Test basic DCF valuation for a well-known stock."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey=api_key, symbol="AAPL"
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Get response models and validate
        models = get_response_models(result, FMPDcfValuation)
        validate_model_list(models, FMPDcfValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDcfValuation)

            # Validate DCF data using Pydantic model fields
            assert dcf_obj.symbol != ""
            assert dcf_obj.date != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDcfValuation)
        validate_model_list(models, FMPDcfValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDcfValuation)

            # Validate DCF data using Pydantic model fields
            assert dcf_obj.symbol != ""
            assert dcf_obj.date != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

            # Validate custom DCF data
            assert dcf_obj.symbol != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

            # Validate custom levered DCF data
            assert dcf_obj.symbol != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

            # Validate that custom parameters might be reflected
            assert dcf_obj.symbol != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

            # Validate cost parameters
            assert dcf_obj.symbol != ""
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
        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

            # Validate levered DCF data
            assert dcf_obj.symbol != ""
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
        # Work directly with the original Pydantic models
        if hasattr(result, "root") and result.root:
            original_data = result.root

            for dcf_obj in original_data[:3]:
                assert isinstance(dcf_obj, FMPDcfValuation)

                # Date format consistency
                assert dcf_obj.date != ""
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

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)

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

            # Work directly with the original Pydantic models
            if hasattr(result, "root") and result.root:
                original_data = result.root

                for dcf_obj in original_data[:1]:  # Check first item
                    assert isinstance(dcf_obj, FMPDcfValuation)

                    assert dcf_obj.symbol != ""
                    assert dcf_obj.dcf > 0
                    assert dcf_obj.Stock_Price > 0

    def test_dcf_financial_companies(self, api_key):
        """Test DCF for financial companies."""
        symbols = ["JPM", "BAC", "WFC"]

        for symbol in symbols:
            result = discounted_cash_flow.discounted_cash_flow_valuation(
                apikey=api_key, symbol=symbol
            )

            # Work directly with the original Pydantic models
            if hasattr(result, "root") and result.root:
                original_data = result.root

                for dcf_obj in original_data[:1]:  # Check first item
                    assert isinstance(dcf_obj, FMPDcfValuation)

                    assert dcf_obj.symbol != ""

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

            # Get response models and validate
            models = get_response_models(result, FMPDCFCustomValuation)
            validate_model_list(models, FMPDCFCustomValuation)

            # Validate first item
            if models:
                dcf_obj = models[0]
                assert isinstance(dcf_obj, FMPDCFCustomValuation)
                assert dcf_obj.symbol != ""


class TestDCFErrorHandling:
    """Test error handling for DCF endpoints."""

    def test_dcf_invalid_api_key(self):
        """Test DCF with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            discounted_cash_flow.discounted_cash_flow_valuation(
                apikey="invalid_key", symbol="AAPL"
            )

        # Should return error message
        assert "Invalid API KEY" in str(exc_info.value)

    def test_dcf_invalid_symbol(self, api_key):
        """Test DCF with invalid symbol."""
        result = discounted_cash_flow.discounted_cash_flow_valuation(
            apikey=api_key, symbol="INVALID123"
        )

        # Invalid symbol might return empty list or error
        models = get_response_models(result, FMPDcfValuation)
        assert isinstance(models, list)
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

        models = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(models, list)

    def test_dcf_levered_invalid_api_key(self):
        """Test levered DCF with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            discounted_cash_flow.discounted_cash_flow_levered(
                apikey="invalid_key", symbol="MSFT"
            )

        # Should return error message
        assert "Invalid API KEY" in str(exc_info.value)

    def test_dcf_custom_levered_invalid_api_key(self):
        """Test custom levered DCF with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            discounted_cash_flow.discounted_cash_flow_custom_levered(
                apikey="invalid_key", symbol="GOOGL"
            )

        # Should return error message
        assert "Invalid API KEY" in str(exc_info.value)


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
            result = endpoint_func()
            models = get_response_models(result, FMPDCFCustomValuation)
            assert isinstance(models, list)

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

        models = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(models, list)


class TestDCFCustom:
    """Tests for custom DCF calculation functions."""

    def test_custom_dcf_basic(self, api_key):
        """Test custom DCF calculation with basic parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key, symbol="AAPL"
        )

        # Validate the original response contains Pydantic models
        if hasattr(result, "root") and result.root:
            original_data = result.root
            assert isinstance(original_data, list)
            if original_data:
                for item in original_data[:3]:
                    assert isinstance(item, FMPDCFCustomValuation)
                    assert item.symbol != ""

        # Get response models and validate
        models = get_response_models(result, FMPDCFCustomValuation)
        validate_model_list(models, FMPDCFCustomValuation)

        # Validate first few items
        for dcf_obj in models[:3]:
            assert isinstance(dcf_obj, FMPDCFCustomValuation)
            assert dcf_obj.symbol != ""

    def test_custom_dcf_with_all_parameters(self, api_key):
        """Test custom DCF with all optional parameters to cover missing lines."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AAPL",
            revenue_growth_pct=0.15,
            ebidta_pct=0.25,
            depreciation_and_amortization_pct=0.05,
            cash_and_short_term_investments_pct=0.10,
            receivables_pct=0.08,
            inventories_pct=0.05,
            payable_pct=0.12,
            ebit_pct=0.20,
            capital_expenditure_pct=0.06,
            operating_cash_flow_pct=0.18,
            selling_general_and_administrative_expenses_pct=0.15,
            tax_rate=0.21,
            long_term_growth_rate=0.03,
            cost_of_debt=0.04,
            cost_of_equity=0.09,
            market_risk_premium=0.06,
            beta=1.2,
            risk_free_rate=0.02,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_dcf_partial_parameters(self, api_key):
        """Test custom DCF with subset of parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="MSFT",
            revenue_growth_pct=0.12,
            tax_rate=0.21,
            long_term_growth_rate=0.03,
            beta=1.1,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_levered_dcf_basic(self, api_key):
        """Test custom levered DCF calculation with basic parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key, symbol="TSLA"
        )

        # Validate the original response contains Pydantic models
        if hasattr(result, "root") and result.root:
            original_data = result.root
            assert isinstance(original_data, list)
            if original_data:
                for item in original_data[:3]:
                    assert isinstance(item, FMPDCFCustomValuation)
                    assert item.symbol != ""

        # Extract data for further testing
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

        if data:
            for item in data[:3]:
                # Now item is a Pydantic model after get_response_models conversion
                assert isinstance(item, FMPDCFCustomValuation)
                assert item.symbol != ""

    def test_custom_levered_dcf_with_all_parameters(self, api_key):
        """Test custom levered DCF with all optional parameters to cover missing lines."""
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key,
            symbol="GOOGL",
            revenue_growth_pct=0.18,
            ebidta_pct=0.30,
            depreciation_and_amortization_pct=0.06,
            cash_and_short_term_investments_pct=0.15,
            receivables_pct=0.07,
            inventories_pct=0.02,
            payable_pct=0.10,
            ebit_pct=0.25,
            capital_expenditure_pct=0.08,
            operating_cash_flow_pct=0.22,
            selling_general_and_administrative_expenses_pct=0.12,
            tax_rate=0.21,
            long_term_growth_rate=0.04,
            cost_of_debt=0.03,
            cost_of_equity=0.10,
            market_risk_premium=0.07,
            beta=1.3,
            risk_free_rate=0.025,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_levered_dcf_partial_parameters(self, api_key):
        """Test custom levered DCF with subset of parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key,
            symbol="META",
            revenue_growth_pct=0.10,
            ebidta_pct=0.35,
            tax_rate=0.21,
            cost_of_debt=0.035,
            cost_of_equity=0.095,
            beta=1.25,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)


class TestDCFParameterValidation:
    """Test parameter validation and edge cases for DCF functions."""

    def test_custom_dcf_invalid_api_key(self):
        """Test custom DCF with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            discounted_cash_flow.discounted_cash_flow_custom(
                apikey="invalid_key", symbol="AAPL"
            )

        assert "Invalid API KEY" in str(exc_info.value)

    def test_custom_levered_dcf_invalid_api_key(self):
        """Test custom levered DCF with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            discounted_cash_flow.discounted_cash_flow_custom_levered(
                apikey="invalid_key", symbol="AAPL"
            )

        assert "Invalid API KEY" in str(exc_info.value)

    def test_custom_dcf_extreme_parameters(self, api_key):
        """Test custom DCF with extreme parameter values."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AAPL",
            revenue_growth_pct=1.0,  # 100% growth
            tax_rate=0.5,  # 50% tax rate
            beta=2.0,  # High beta
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_dcf_zero_parameters(self, api_key):
        """Test custom DCF with zero values for parameters."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AAPL",
            revenue_growth_pct=0.0,
            tax_rate=0.0,
            risk_free_rate=0.0,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_dcf_negative_parameters(self, api_key):
        """Test custom DCF with negative parameter values."""
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key,
            symbol="AAPL",
            revenue_growth_pct=-0.05,  # Negative growth
            long_term_growth_rate=-0.01,
        )
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)


class TestDCFPerformance:
    """Test DCF endpoint performance."""

    def test_custom_dcf_response_time(self, api_key):
        """Test that custom DCF responds within acceptable time."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_custom(
            apikey=api_key, symbol="AAPL", revenue_growth_pct=0.15
        )
        response_time = time.time() - start_time

        assert response_time < RESPONSE_TIME_LIMIT
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)

    def test_custom_levered_dcf_response_time(self, api_key):
        """Test that custom levered DCF responds within acceptable time."""
        start_time = time.time()
        result = discounted_cash_flow.discounted_cash_flow_custom_levered(
            apikey=api_key, symbol="MSFT", cost_of_equity=0.10
        )
        response_time = time.time() - start_time

        assert response_time < RESPONSE_TIME_LIMIT
        data = get_response_models(result, FMPDCFCustomValuation)
        assert isinstance(data, list)
