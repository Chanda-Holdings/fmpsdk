from datetime import datetime, timedelta

import pytest

from fmpsdk import economics
from fmpsdk.models import (
    FMPEconomicCalendarEvent,
    FMPEconomicIndicator,
    FMPMarketRiskPremium,
    FMPTreasuryRates,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


@pytest.fixture
def recent_date():
    """Recent date for testing (within last 30 days)."""
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


@pytest.fixture
def older_date():
    """Older date for testing (within last 90 days)."""
    return (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


class TestEconomicsBasic:
    """Basic functionality tests for economics endpoints with enhanced validation."""

    def test_treasury_rates_without_dates(self, api_key):
        """Test getting treasury rates without date parameters using enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.treasury_rates, "treasury_rates", apikey=api_key
        )

        treasury_rates = get_response_models(response, FMPTreasuryRates)
        validate_model_list(treasury_rates, FMPTreasuryRates)

        if treasury_rates:
            # Test first 3 items for comprehensive validation
            for rate in treasury_rates[:3]:
                # Core validation
                assert rate.date is not None, "Date should not be None"
                assert rate.month1 is not None, "1-month rate should not be None"
                assert rate.year10 is not None, "10-year rate should not be None"
                assert rate.year30 is not None, "30-year rate should not be None"

                # Economics-specific business logic validation
                assert rate.month1 >= 0, "Interest rates should be non-negative"
                assert rate.year10 >= 0, "Interest rates should be non-negative"
                assert rate.year30 >= 0, "Interest rates should be non-negative"

                # Reasonable rate bounds (0-15% for normal economic conditions)
                assert (
                    rate.month1 <= 15.0
                ), "1-month rate should be within reasonable bounds"
                assert (
                    rate.year10 <= 15.0
                ), "10-year rate should be within reasonable bounds"
                assert (
                    rate.year30 <= 15.0
                ), "30-year rate should be within reasonable bounds"

    def test_treasury_rates_with_date_range(self, api_key, recent_date, older_date):
        """Test getting treasury rates with date range using enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.treasury_rates,
            "treasury_rates",
            apikey=api_key,
            from_date=older_date,
            to_date=recent_date,
        )

        treasury_rates = get_response_models(response, FMPTreasuryRates)
        validate_model_list(treasury_rates, FMPTreasuryRates)

        if treasury_rates:
            # Validate date filtering and data quality
            for rate in treasury_rates:
                if rate.date and len(rate.date) >= 10:
                    parsed_date = datetime.strptime(rate.date[:10], "%Y-%m-%d")
                    # Verify dates are reasonable (API may not strictly filter)
                    assert parsed_date >= datetime(
                        2020, 1, 1
                    ), "Date should be reasonable minimum"
                    assert parsed_date <= datetime.now(), "Date should not be in future"

    def test_economic_indicators_gdp(self, api_key):
        """Test getting GDP economic indicator with enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.economic_indicators,
            "economic_indicators",
            apikey=api_key,
            name="GDP",
        )

        indicators = get_response_models(response, FMPEconomicIndicator)
        validate_model_list(indicators, FMPEconomicIndicator)

        if indicators:
            # Test first 3 items for comprehensive validation
            for indicator in indicators[:3]:
                # Core validation
                assert indicator.name is not None, "Indicator name should not be None"
                assert indicator.date is not None, "Date should not be None"
                assert indicator.value is not None, "Value should not be None"
                assert isinstance(
                    indicator.value, (int, float)
                ), "Value should be numeric"

                # GDP-specific business logic validation
                assert (
                    "GDP" in indicator.name.upper() or indicator.name == "GDP"
                ), "Should be GDP-related indicator"
                assert (
                    indicator.value > 0
                ), "GDP should be positive (in trillions for US)"

    def test_economic_indicators_cpi(self, api_key):
        """Test getting CPI economic indicator with enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.economic_indicators,
            "economic_indicators",
            apikey=api_key,
            name="CPI",
        )

        indicators = get_response_models(response, FMPEconomicIndicator)
        validate_model_list(indicators, FMPEconomicIndicator)

        if indicators:
            # Test first 3 items for comprehensive validation
            for indicator in indicators[:3]:
                # Core validation
                assert indicator.name is not None, "Indicator name should not be None"
                assert indicator.date is not None, "Date should not be None"
                assert indicator.value is not None, "Value should not be None"
                assert isinstance(
                    indicator.value, (int, float)
                ), "Value should be numeric"

                # CPI-specific business logic validation
                assert (
                    "CPI" in indicator.name.upper() or indicator.name == "CPI"
                ), "Should be CPI-related indicator"
                assert indicator.value > 0, "CPI should be positive index value"

    def test_economic_calendar_without_dates(self, api_key):
        """Test getting economic calendar without date parameters using enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.economic_calendar, "economic_calendar", apikey=api_key
        )

        calendar_events = get_response_models(response, FMPEconomicCalendarEvent)
        validate_model_list(calendar_events, FMPEconomicCalendarEvent)

        if calendar_events:
            # Test first 3 items for comprehensive validation
            for event in calendar_events[:3]:
                # Core validation
                assert event.date is not None, "Date should not be None"
                assert event.country is not None, "Country should not be None"
                assert event.event is not None, "Event name should not be None"
                assert event.currency is not None, "Currency should not be None"

                # Economics-specific business logic validation
                if event.impact:
                    assert event.impact in [
                        "Low",
                        "Medium",
                        "High",
                        "Holiday",
                        "None",
                    ], "Impact should be valid level"
                assert (
                    len(event.country) >= 2
                ), "Country should be valid country code or name"
                assert len(event.currency) >= 3, "Currency should be 3-letter code"
                assert event.currency.isupper(), "Currency code should be uppercase"

    def test_economic_calendar_with_date_range(self, api_key):
        """Test getting economic calendar with date range using enhanced validation."""
        # Use a shorter date range for calendar events
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response, validation = handle_api_call_with_validation(
            economics.economic_calendar,
            "economic_calendar",
            apikey=api_key,
            from_date=from_date,
            to_date=to_date,
        )

        calendar_events = get_response_models(response, FMPEconomicCalendarEvent)
        validate_model_list(calendar_events, FMPEconomicCalendarEvent)

        if calendar_events:
            # Validate date filtering and data quality
            for event in calendar_events[:5]:
                if event.date and len(event.date) >= 10:
                    parsed_date = datetime.strptime(event.date[:10], "%Y-%m-%d")
                    # Just verify dates are reasonable (API may not strictly filter)
                    assert parsed_date >= datetime(
                        2020, 1, 1
                    ), "Date should be reasonable minimum"
                    assert parsed_date <= datetime.now() + timedelta(
                        days=30
                    ), "Future events allowed"

    def test_market_risk_premium(self, api_key):
        """Test getting market risk premium data with enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.market_risk_premium, "market_risk_premium", apikey=api_key
        )

        risk_premiums = get_response_models(response, FMPMarketRiskPremium)
        validate_model_list(risk_premiums, FMPMarketRiskPremium)

        if risk_premiums:
            # Test first 5 items for comprehensive validation
            for premium in risk_premiums[:5]:
                # Core validation
                assert premium.country is not None, "Country should not be None"
                assert premium.continent is not None, "Continent should not be None"
                assert (
                    premium.countryRiskPremium is not None
                ), "Country risk premium should not be None"
                assert (
                    premium.totalEquityRiskPremium is not None
                ), "Total equity risk premium should not be None"
                assert isinstance(
                    premium.countryRiskPremium, (int, float)
                ), "Country risk premium should be numeric"
                assert isinstance(
                    premium.totalEquityRiskPremium, (int, float)
                ), "Total equity risk premium should be numeric"

                # Economics-specific business logic validation
                # Risk premiums should be reasonable values (typically 0-30% for high-risk countries)
                assert (
                    -5.0 <= premium.countryRiskPremium <= 30.0
                ), "Country risk premium should be within reasonable range"
                assert (
                    0.0 <= premium.totalEquityRiskPremium <= 35.0
                ), "Total equity risk premium should be within reasonable range"


class TestEconomicsDataQuality:
    """Data quality and consistency tests for economics endpoints with enhanced validation."""

    def test_treasury_yield_curve_shape(self, api_key):
        """Test that treasury yield curve has reasonable shape using enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.treasury_rates, "treasury_rates", apikey=api_key
        )

        treasury_rates = get_response_models(response, FMPTreasuryRates)
        validate_model_list(treasury_rates, FMPTreasuryRates)

        if treasury_rates:
            latest_rates = treasury_rates[0]  # Most recent rates

            # Test all yield curve points for reasonableness
            rate_attributes = [
                ("month1", latest_rates.month1),
                ("month2", latest_rates.month2),
                ("month3", latest_rates.month3),
                ("month6", latest_rates.month6),
                ("year1", latest_rates.year1),
                ("year2", latest_rates.year2),
                ("year3", latest_rates.year3),
                ("year5", latest_rates.year5),
                ("year7", latest_rates.year7),
                ("year10", latest_rates.year10),
                ("year20", latest_rates.year20),
                ("year30", latest_rates.year30),
            ]

            for attr_name, rate_value in rate_attributes:
                if rate_value is not None:
                    assert (
                        0 <= rate_value <= 15.0
                    ), f"{attr_name} rate {rate_value} is outside reasonable range"

    def test_economic_indicators_data_consistency(self, api_key):
        """Test economic indicators for data consistency using enhanced validation."""
        # Test multiple indicators (using valid indicator names only)
        indicators = ["GDP", "CPI"]

        for indicator_name in indicators:
            try:
                response, validation = handle_api_call_with_validation(
                    economics.economic_indicators,
                    "economic_indicators",
                    apikey=api_key,
                    name=indicator_name,
                )

                indicator_data = get_response_models(response, FMPEconomicIndicator)
                validate_model_list(indicator_data, FMPEconomicIndicator)

                if indicator_data:
                    # Validate data consistency for each indicator
                    for indicator in indicator_data[:3]:
                        if indicator.name and indicator.value is not None:
                            # Indicator-specific validation
                            if "GDP" in indicator.name.upper():
                                assert indicator.value > 0, "GDP should be positive"
                            elif "CPI" in indicator.name.upper():
                                assert indicator.value > 0, "CPI should be positive"
            except Exception as e:
                # Handle API errors for invalid indicator names gracefully
                if "Invalid name" in str(e) or "JSONDecodeError" in str(e):
                    pytest.skip(f"Indicator {indicator_name} not supported by API")
                else:
                    raise

    def test_economic_calendar_data_consistency(self, api_key):
        """Test economic calendar for data consistency using enhanced validation."""
        response, validation = handle_api_call_with_validation(
            economics.economic_calendar, "economic_calendar", apikey=api_key
        )

        calendar_events = get_response_models(response, FMPEconomicCalendarEvent)
        validate_model_list(calendar_events, FMPEconomicCalendarEvent)

        if calendar_events:
            # Test first 10 events for comprehensive validation
            for event in calendar_events[:10]:
                # Impact level consistency
                if event.impact:
                    assert event.impact in [
                        "Low",
                        "Medium",
                        "High",
                        "Holiday",
                        "None",
                    ], "Impact level should be valid"

                # Currency code format
                if event.currency:
                    assert len(event.currency) == 3, "Currency should be 3-letter code"
                    assert event.currency.isupper(), "Currency code should be uppercase"

                # Country format
                if event.country:
                    assert len(event.country) >= 2, "Country should be valid"

                # Date format
                if event.date:
                    assert len(event.date) >= 10, "Date should have proper format"

                # Optional fields validation
                if (
                    hasattr(event, "changePercentage")
                    and event.changePercentage is not None
                ):
                    assert isinstance(
                        event.changePercentage, (int, float)
                    ), "Change percentage should be numeric"

    def test_market_risk_premium_by_development_level(self, api_key):
        """Test market risk premium validation by economic development level."""
        response, validation = handle_api_call_with_validation(
            economics.market_risk_premium, "market_risk_premium", apikey=api_key
        )

        risk_premiums = get_response_models(response, FMPMarketRiskPremium)
        validate_model_list(risk_premiums, FMPMarketRiskPremium)

        if risk_premiums:
            developed_countries = []
            emerging_countries = []

            for premium in risk_premiums:
                if premium.country and premium.countryRiskPremium is not None:
                    # Categorize by typical development level
                    if premium.country.upper() in [
                        "US",
                        "GERMANY",
                        "JAPAN",
                        "UK",
                        "CANADA",
                        "AUSTRALIA",
                    ]:
                        developed_countries.append(premium.countryRiskPremium)
                    elif premium.country.upper() in [
                        "BRAZIL",
                        "INDIA",
                        "CHINA",
                        "MEXICO",
                        "RUSSIA",
                    ]:
                        emerging_countries.append(premium.countryRiskPremium)

            # Developed countries should generally have lower risk premiums
            if developed_countries:
                avg_developed = sum(developed_countries) / len(developed_countries)
                assert (
                    avg_developed <= 10.0
                ), "Developed countries should have reasonable risk premiums"

            # Emerging countries may have higher risk premiums
            if emerging_countries:
                avg_emerging = sum(emerging_countries) / len(emerging_countries)
                assert (
                    avg_emerging <= 25.0
                ), "Emerging countries should have reasonable risk premiums"
