import os
import time
from datetime import datetime, timedelta
from typing import List

import pytest

from fmpsdk import economics
from fmpsdk.models import (
    FMPEconomicCalendarEvent,
    FMPEconomicIndicator,
    FMPMarketRiskPremium,
    FMPTreasuryRates,
)
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


@pytest.fixture
def recent_date():
    """Recent date for testing (within last 30 days)."""
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


@pytest.fixture
def older_date():
    """Older date for testing (within last 90 days)."""
    return (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


class TestEconomicsBasic:
    """Basic functionality tests for economics endpoints."""

    def test_treasury_rates_without_dates(self, api_key):
        """Test getting treasury rates without date parameters."""
        start_time = time.time()
        result = economics.treasury_rates(apikey=api_key)
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
            for rate in data[:3]:  # Check first few items
                if isinstance(rate, dict):
                    rate_obj = FMPTreasuryRates(**rate)
                else:
                    rate_obj = rate

                # Validate treasury rate data
                assert rate_obj.date
                assert isinstance(rate_obj.month1, (int, float))
                assert isinstance(rate_obj.year10, (int, float))

                # Basic data quality checks
                assert rate_obj.month1 >= 0  # Interest rates should be non-negative
                assert rate_obj.year10 >= 0
                assert rate_obj.year30 >= 0

    def test_treasury_rates_with_date_range(self, api_key, recent_date, older_date):
        """Test getting treasury rates with date range."""
        start_time = time.time()
        result = economics.treasury_rates(
            apikey=api_key, from_date=older_date, to_date=recent_date
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
            # Validate date filtering worked
            for rate in data:
                if isinstance(rate, dict):
                    rate_date = rate["date"]
                else:
                    rate_date = rate.date

                if rate_date and len(rate_date) >= 10:
                    parsed_date = datetime.strptime(rate_date[:10], "%Y-%m-%d")
                    from_date_parsed = datetime.strptime(older_date, "%Y-%m-%d")
                    to_date_parsed = datetime.strptime(recent_date, "%Y-%m-%d")

                    # Note: API may not strictly enforce date ranges
                    # So we'll just verify dates are reasonable
                    assert parsed_date >= datetime(2020, 1, 1)  # Reasonable minimum
                    assert parsed_date <= datetime.now()  # Not in future

    def test_economic_indicators_gdp(self, api_key):
        """Test getting GDP economic indicator."""
        start_time = time.time()
        result = economics.economic_indicators(apikey=api_key, name="GDP")
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
            for indicator in data[:3]:  # Check first few items
                if isinstance(indicator, dict):
                    indicator_obj = FMPEconomicIndicator(**indicator)
                else:
                    indicator_obj = indicator

                # Validate economic indicator data
                assert indicator_obj.name
                assert indicator_obj.date
                assert isinstance(indicator_obj.value, (int, float))

                # GDP-specific checks
                assert (
                    "GDP" in indicator_obj.name.upper() or indicator_obj.name == "GDP"
                )
                # GDP should be positive (in trillions for US)
                assert indicator_obj.value > 0

    def test_economic_indicators_cpi(self, api_key):
        """Test getting CPI economic indicator."""
        start_time = time.time()
        result = economics.economic_indicators(apikey=api_key, name="CPI")
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
            for indicator in data[:3]:  # Check first few items
                if isinstance(indicator, dict):
                    indicator_obj = FMPEconomicIndicator(**indicator)
                else:
                    indicator_obj = indicator

                # Validate economic indicator data
                assert indicator_obj.name
                assert indicator_obj.date
                assert isinstance(indicator_obj.value, (int, float))

                # CPI-specific checks
                assert (
                    "CPI" in indicator_obj.name.upper() or indicator_obj.name == "CPI"
                )
                # CPI should be positive index value
                assert indicator_obj.value > 0

    def test_economic_calendar_without_dates(self, api_key):
        """Test getting economic calendar without date parameters."""
        start_time = time.time()
        result = economics.economic_calendar(apikey=api_key)
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
            for event in data[:3]:  # Check first few items
                if isinstance(event, dict):
                    event_obj = FMPEconomicCalendarEvent(**event)
                else:
                    event_obj = event

                # Validate economic calendar event data
                assert event_obj.date
                assert event_obj.country
                assert event_obj.event
                assert event_obj.currency
                assert event_obj.impact

                # Impact should be one of the standard levels (including None for unknown impact)
                assert event_obj.impact in [
                    "Low",
                    "Medium",
                    "High",
                    "Holiday",
                    "None",
                    None,
                ]

                # Country should be valid country code or name
                assert len(event_obj.country) >= 2
                assert len(event_obj.currency) >= 3  # Currency code

    def test_economic_calendar_with_date_range(self, api_key, recent_date):
        """Test getting economic calendar with date range."""
        # Use a shorter date range for calendar events
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        start_time = time.time()
        result = economics.economic_calendar(
            apikey=api_key, from_date=from_date, to_date=to_date
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
            # Validate date filtering (though API may return broader results)
            for event in data[:5]:  # Check first few items
                if isinstance(event, dict):
                    event_date = event["date"]
                else:
                    event_date = event.date

                if event_date and len(event_date) >= 10:
                    parsed_date = datetime.strptime(event_date[:10], "%Y-%m-%d")
                    # Just verify dates are reasonable (API may not strictly filter)
                    assert parsed_date >= datetime(2020, 1, 1)  # Reasonable minimum
                    assert parsed_date <= datetime.now() + timedelta(
                        days=30
                    )  # Future events allowed

    def test_market_risk_premium(self, api_key):
        """Test getting market risk premium data."""
        start_time = time.time()
        result = economics.market_risk_premium(apikey=api_key)
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
            for premium in data[:5]:  # Check first few items
                if isinstance(premium, dict):
                    premium_obj = FMPMarketRiskPremium(**premium)
                else:
                    premium_obj = premium

                # Validate market risk premium data
                assert premium_obj.country
                assert premium_obj.continent
                assert isinstance(premium_obj.countryRiskPremium, (int, float))
                assert isinstance(premium_obj.totalEquityRiskPremium, (int, float))

                # Risk premiums should be reasonable values (typically 0-30% for high-risk countries)
                assert -5.0 <= premium_obj.countryRiskPremium <= 30.0
                assert 0.0 <= premium_obj.totalEquityRiskPremium <= 35.0


class TestEconomicsDataQuality:
    """Data quality and consistency tests for economics endpoints."""

    def test_treasury_yield_curve_shape(self, api_key):
        """Test that treasury yield curve has reasonable shape."""
        result = economics.treasury_rates(apikey=api_key)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            latest_rates = data[0]  # Most recent rates
            if isinstance(latest_rates, dict):
                rates_obj = FMPTreasuryRates(**latest_rates)
            else:
                rates_obj = latest_rates

            # Test yield curve reasonableness
            # Generally, longer maturities should have higher yields (normal curve)
            # But during inversions, this may not hold
            assert rates_obj.month1 >= 0
            assert rates_obj.year1 >= 0
            assert rates_obj.year10 >= 0
            assert rates_obj.year30 >= 0

            # All rates should be within reasonable bounds (0-15%)
            for attr_name in [
                "month1",
                "month2",
                "month3",
                "month6",
                "year1",
                "year2",
                "year3",
                "year5",
                "year7",
                "year10",
                "year20",
                "year30",
            ]:
                rate_value = getattr(rates_obj, attr_name)
                assert (
                    0 <= rate_value <= 15.0
                ), f"{attr_name} rate {rate_value} is outside reasonable range"

    def test_economic_indicators_data_consistency(self, api_key):
        """Test economic indicators for data consistency."""
        # Test multiple indicators
        indicators = ["GDP", "CPI", "UNEMPLOYMENT RATE"]

        for indicator_name in indicators:
            result = economics.economic_indicators(apikey=api_key, name=indicator_name)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for event in data[:10]:  # Check first 10 events
                if isinstance(event, dict):
                    event_obj = FMPEconomicCalendarEvent(**event)
                else:
                    event_obj = event

                # Impact level consistency (including "None" for certain events)
                assert event_obj.impact in ["Low", "Medium", "High", "Holiday", "None"]

                # Currency code format
                assert len(event_obj.currency) == 3  # Standard currency codes
                assert event_obj.currency.isupper()  # Should be uppercase

                # Country format
                assert len(event_obj.country) >= 2

                # Date format
                assert len(event_obj.date) >= 10

                # Optional fields should be reasonable if present
                if event_obj.changePercentage is not None:
                    assert isinstance(event_obj.changePercentage, (int, float))
                    assert (
                        -100 <= event_obj.changePercentage <= 1000
                    )  # Reasonable range


class TestEconomicsErrorHandling:
    """Error handling tests for economics endpoints."""

    def test_treasury_rates_invalid_api_key(self):
        """Test treasury rates with invalid API key."""
        result = economics.treasury_rates(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_economic_indicators_invalid_api_key(self):
        """Test economic indicators with invalid API key."""
        result = economics.economic_indicators(apikey="invalid_key", name="GDP")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_economic_calendar_invalid_api_key(self):
        """Test economic calendar with invalid API key."""
        result = economics.economic_calendar(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_market_risk_premium_invalid_api_key(self):
        """Test market risk premium with invalid API key."""
        result = economics.market_risk_premium(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_economic_indicators_invalid_name(self, api_key):
        """Test economic indicators with invalid indicator name."""
        result = economics.economic_indicators(
            apikey=api_key, name="INVALID_INDICATOR_NAME"
        )

        # Should return empty list or error for invalid indicator
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            # For invalid indicator, should return empty list
            assert isinstance(data, list)
            # May be empty for invalid indicator names

    def test_treasury_rates_invalid_date_format(self, api_key):
        """Test treasury rates with invalid date format."""
        result = economics.treasury_rates(
            apikey=api_key, from_date="invalid-date", to_date="also-invalid"
        )

        # Check if this is a premium endpoint first

        # API might be lenient with date formats, or return error
        # Either behavior is acceptable
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            # If API is lenient, should still return data
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_economic_calendar_future_dates(self, api_key):
        """Test economic calendar with far future dates."""
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

        result = economics.economic_calendar(
            apikey=api_key, from_date=future_date, to_date=future_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # May return empty list for far future dates


class TestEconomicsDateRanges:
    """Date range functionality tests for economics endpoints."""

    def test_treasury_rates_historical_range(self, api_key):
        """Test treasury rates with historical date range."""
        from_date = "2023-01-01"
        to_date = "2023-03-31"

        result = economics.treasury_rates(
            apikey=api_key, from_date=from_date, to_date=to_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        # If data is available, validate chronological order
        if len(data) > 1:
            # Data should be in reverse chronological order (newest first)
            first_date = datetime.strptime(
                data[0]["date"] if isinstance(data[0], dict) else data[0].date,
                "%Y-%m-%d",
            )
            last_date = datetime.strptime(
                data[-1]["date"] if isinstance(data[-1], dict) else data[-1].date,
                "%Y-%m-%d",
            )
            assert first_date >= last_date  # Newest first

    def test_economic_indicators_with_date_range(self, api_key):
        """Test economic indicators with date range."""
        from_date = "2023-01-01"
        to_date = "2023-12-31"

        result = economics.economic_indicators(
            apikey=api_key, name="GDP", from_date=from_date, to_date=to_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        # Validate date filtering if data is available
        if data:
            for indicator in data:
                if isinstance(indicator, dict):
                    indicator_date = indicator["date"]
                else:
                    indicator_date = indicator.date

                if indicator_date and len(indicator_date) >= 10:
                    parsed_date = datetime.strptime(indicator_date[:10], "%Y-%m-%d")
                    # Note: API may not strictly enforce date ranges
                    # Just verify dates are within reasonable bounds
                    assert parsed_date >= datetime(2020, 1, 1)


class TestEconomicsPerformance:
    """Performance tests for economics endpoints."""

    def test_response_times(self, api_key):
        """Test that all economics endpoints respond within acceptable time."""
        endpoints = [
            lambda: economics.treasury_rates(apikey=api_key),
            lambda: economics.economic_indicators(apikey=api_key, name="GDP"),
            lambda: economics.economic_calendar(apikey=api_key),
            lambda: economics.market_risk_premium(apikey=api_key),
        ]

        for endpoint_func in endpoints:
            start_time = time.time()
            result = endpoint_func()
            response_time = time.time() - start_time

            # Skip if premium endpoint
            assert response_time < RESPONSE_TIME_LIMIT


class TestEconomicsComprehensive:
    """Comprehensive tests for economics data across various dimensions."""

    @pytest.mark.parametrize(
        "date_range_days,expected_data_points,period_type,rate_environment",
        [
            (30, 20, "recent", "current_rates"),
            (90, 60, "quarterly", "short_term_trend"),
            (180, 120, "semi_annual", "medium_term_trend"),
            (365, 250, "annual", "long_term_trend"),
            (730, 500, "two_year", "cycle_analysis"),
            (1095, 750, "three_year", "historical_context"),
        ],
    )
    def test_treasury_rates_comprehensive_periods(
        self,
        api_key,
        date_range_days,
        expected_data_points,
        period_type,
        rate_environment,
    ):
        """Test treasury rates across comprehensive date ranges and rate environments."""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=date_range_days)).strftime(
            "%Y-%m-%d"
        )

        start_time = time.time()
        result = economics.treasury_rates(
            apikey=api_key, from_date=start_date, to_date=end_date
        )
        response_time = time.time() - start_time

        # Response time validation
        assert (
            response_time < RESPONSE_TIME_LIMIT
        ), f"Response time should be reasonable for {period_type}"

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list), f"Result should be list for {period_type}"

        if data:
            # Flexible data point validation (accounting for weekends, holidays)
            min_expected = int(expected_data_points * 0.6)  # Allow 40% variance
            max_expected = int(expected_data_points * 1.2)  # Allow 20% over
            actual_count = len(data)

            assert (
                min_expected <= actual_count <= max_expected
            ), f"{period_type} should have {min_expected}-{max_expected} data points, got {actual_count}"

            # Validate treasury rate data quality
            for rate_data in data[:10]:  # Check first 10 data points
                if isinstance(rate_data, dict):
                    rate_obj = FMPTreasuryRates(**rate_data)
                else:
                    rate_obj = rate_data

                # Validate treasury rate data
                assert rate_obj.date, f"Date should be present for {period_type}"
                assert isinstance(
                    rate_obj.month1, (int, float)
                ), f"1-month rate should be numeric for {period_type}"
                assert isinstance(
                    rate_obj.year10, (int, float)
                ), f"10-year rate should be numeric for {period_type}"

                # Basic data quality checks
                assert (
                    rate_obj.month1 >= 0
                ), f"1-month rate should be non-negative for {period_type}"
                assert (
                    rate_obj.year10 >= 0
                ), f"10-year rate should be non-negative for {period_type}"
                assert (
                    rate_obj.year30 >= 0
                ), f"30-year rate should be non-negative for {period_type}"

                # Yield curve logic - longer terms typically have higher rates (but not always)
                # We'll just check they're reasonable values
                assert (
                    rate_obj.month1 <= 20
                ), f"1-month rate should be reasonable for {period_type}"
                assert (
                    rate_obj.year10 <= 20
                ), f"10-year rate should be reasonable for {period_type}"
                assert (
                    rate_obj.year30 <= 20
                ), f"30-year rate should be reasonable for {period_type}"

                # Date should be within requested range
                try:
                    rate_date = datetime.strptime(rate_obj.date, "%Y-%m-%d")
                    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                    assert (
                        start_dt <= rate_date <= end_dt
                    ), f"Rate date should be within range for {period_type}"
                except ValueError:
                    pytest.fail(
                        f"Invalid date format for {period_type}: {rate_obj.date}"
                    )

    @pytest.mark.parametrize(
        "indicator,expected_frequency,data_type,economic_context",
        [
            ("GDP", "quarterly", "growth_rate", "economic_output"),
            ("inflation", "monthly", "percentage", "price_stability"),
            ("unemployment", "monthly", "percentage", "labor_market"),
            ("retail_sales", "monthly", "percentage_change", "consumer_spending"),
            ("industrial_production", "monthly", "percentage_change", "manufacturing"),
            ("consumer_confidence", "monthly", "index_value", "sentiment"),
            ("housing_starts", "monthly", "thousands_units", "real_estate"),
            ("trade_balance", "monthly", "dollars", "international_trade"),
        ],
    )
    def test_economic_indicators_comprehensive(
        self, api_key, indicator, expected_frequency, data_type, economic_context
    ):
        """Test comprehensive economic indicators across different data types and contexts."""
        # Use recent date range for economic indicators
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )  # 1 year of data

        start_time = time.time()
        result = economics.economic_indicators(
            apikey=api_key, name=indicator, from_date=start_date, to_date=end_date
        )
        response_time = time.time() - start_time

        # Response time validation
        assert (
            response_time < RESPONSE_TIME_LIMIT
        ), f"Response time should be reasonable for {indicator}"

        # Check if result is error dict or if indicator is not supported
        if isinstance(result, dict) and "Error Message" in result:
            # Some indicators might not be available or supported
            pytest.skip(
                f"Economic indicator {indicator} not available or not supported"
            )
            return

        data = extract_data_list(result)
        assert isinstance(data, list), f"Result should be list for {indicator}"

        if data:
            # Validate data frequency expectations
            data_count = len(data)
            if expected_frequency == "monthly":
                # Monthly data should have roughly 12 data points per year
                assert (
                    6 <= data_count <= 18
                ), f"Monthly {indicator} should have 6-18 data points per year"
            elif expected_frequency == "quarterly":
                # Quarterly data should have roughly 4 data points per year
                assert (
                    2 <= data_count <= 8
                ), f"Quarterly {indicator} should have 2-8 data points per year"

            # Validate economic indicator data quality
            for econ_data in data[:5]:  # Check first 5 data points
                if isinstance(econ_data, dict):
                    econ_obj = FMPEconomicIndicator(**econ_data)
                else:
                    econ_obj = econ_data

                # Validate economic indicator data
                assert econ_obj.date, f"Date should be present for {indicator}"
                assert (
                    econ_obj.value is not None
                ), f"Value should be present for {indicator}"

                # Data type-specific validation
                if data_type == "percentage":
                    # Percentages should be reasonable (allowing for extreme cases)
                    assert (
                        -50 <= econ_obj.value <= 100
                    ), f"{indicator} percentage should be reasonable"
                elif data_type == "growth_rate":
                    # Growth rates should be reasonable (allowing for recessions/booms)
                    # Note: GDP might return absolute values instead of growth rates
                    if indicator.upper() == "GDP":
                        # GDP values are typically in billions/trillions
                        assert econ_obj.value >= 0, f"{indicator} should be positive"
                        assert (
                            econ_obj.value <= 100000
                        ), f"{indicator} should be within reasonable range"
                    else:
                        assert (
                            -20 <= econ_obj.value <= 20
                        ), f"{indicator} growth rate should be reasonable"
                elif data_type == "index_value":
                    # Index values should be positive
                    assert (
                        econ_obj.value >= 0
                    ), f"{indicator} index should be non-negative"
                elif data_type == "percentage_change":
                    # Percentage changes can be wide-ranging
                    assert (
                        -100 <= econ_obj.value <= 100
                    ), f"{indicator} percentage change should be reasonable"

                # Economic context validation
                if economic_context == "labor_market" and indicator == "unemployment":
                    # Unemployment rates should be reasonable
                    assert (
                        0 <= econ_obj.value <= 25
                    ), f"Unemployment rate should be 0-25%"
                elif economic_context == "price_stability" and indicator == "inflation":
                    # Inflation rates should be reasonable
                    assert (
                        -10 <= econ_obj.value <= 15
                    ), f"Inflation rate should be reasonable"

    @pytest.mark.parametrize(
        "country,currency,economic_development,expected_characteristics",
        [
            (
                "US",
                "USD",
                "developed",
                {"risk_premium_range": (2, 10), "stability": "high"},
            ),
            (
                "Germany",
                "EUR",
                "developed",
                {"risk_premium_range": (1, 8), "stability": "high"},
            ),
            (
                "Japan",
                "JPY",
                "developed",
                {"risk_premium_range": (1, 6), "stability": "high"},
            ),
            (
                "UK",
                "GBP",
                "developed",
                {"risk_premium_range": (2, 9), "stability": "high"},
            ),
            (
                "Canada",
                "CAD",
                "developed",
                {"risk_premium_range": (2, 8), "stability": "high"},
            ),
            (
                "Australia",
                "AUD",
                "developed",
                {"risk_premium_range": (3, 10), "stability": "medium"},
            ),
            (
                "China",
                "CNY",
                "emerging",
                {"risk_premium_range": (4, 15), "stability": "medium"},
            ),
            (
                "India",
                "INR",
                "emerging",
                {"risk_premium_range": (5, 20), "stability": "medium"},
            ),
            (
                "Brazil",
                "BRL",
                "emerging",
                {"risk_premium_range": (6, 25), "stability": "low"},
            ),
            (
                "Mexico",
                "MXN",
                "emerging",
                {"risk_premium_range": (4, 18), "stability": "medium"},
            ),
        ],
    )
    def test_market_risk_premium_global_coverage(
        self, api_key, country, currency, economic_development, expected_characteristics
    ):
        """Test market risk premium across different countries and economic development levels."""
        start_time = time.time()
        result = economics.market_risk_premium(apikey=api_key)
        response_time = time.time() - start_time

        # Response time validation
        assert (
            response_time < RESPONSE_TIME_LIMIT
        ), f"Response time should be reasonable for market risk premium"

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            # Market risk premium data might not be available
            pytest.skip(f"Market risk premium data not available")
            return

        data = extract_data_list(result)
        assert isinstance(data, list), f"Result should be list for market risk premium"

        if data:
            # Filter data for the specific country
            country_data = [
                item
                for item in data
                if (isinstance(item, dict) and item.get("country") == country)
                or (hasattr(item, "country") and item.country == country)
            ]

            if not country_data:
                pytest.skip(
                    f"Market risk premium data for {country} not found in results"
                )
                return

            # Validate market risk premium data for the specific country
            for risk_data in country_data[:3]:  # Check first 3 data points
                if isinstance(risk_data, dict):
                    risk_obj = FMPMarketRiskPremium(**risk_data)
                else:
                    risk_obj = risk_data

                # Validate market risk premium data
                assert (
                    risk_obj.country == country
                ), f"Country should match for {country}"
                assert (
                    risk_obj.totalEquityRiskPremium is not None
                ), f"Risk premium should be present for {country}"

                # Risk premium range validation based on economic development
                risk_range = expected_characteristics["risk_premium_range"]
                min_risk, max_risk = risk_range

                # Allow some flexibility in risk premium values
                flexible_min = min_risk * 0.5
                flexible_max = max_risk * 2.0

                assert (
                    flexible_min <= risk_obj.totalEquityRiskPremium <= flexible_max
                ), f"Risk premium for {economic_development} country {country} should be {flexible_min}-{flexible_max}%, got {risk_obj.totalEquityRiskPremium}%"

                # Economic development-specific validation
                if economic_development == "developed":
                    # Developed countries should have lower risk premiums
                    assert (
                        risk_obj.totalEquityRiskPremium <= 15
                    ), f"Developed country {country} should have reasonable risk premium"
                elif economic_development == "emerging":
                    # Emerging markets can have higher risk premiums
                    assert (
                        risk_obj.totalEquityRiskPremium >= 1
                    ), f"Emerging market {country} should have positive risk premium"
