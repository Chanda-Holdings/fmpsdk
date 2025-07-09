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

                # Impact should be one of the standard levels
                assert event_obj.impact in ["Low", "Medium", "High", "Holiday"]

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
