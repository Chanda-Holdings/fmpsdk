from datetime import datetime

import pytest

from fmpsdk import market_hours
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import FMPExchangeHoliday, FMPExchangeMarketHours
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


class TestMarketHours:
    """Test class for market hours functionality."""

    @pytest.mark.parametrize(
        "exchange,expected_timezone,expected_currency,region",
        [
            ("NYSE", "America/New_York", "USD", "North America"),
            ("NASDAQ", "America/New_York", "USD", "North America"),
            ("AMEX", "America/New_York", "USD", "North America"),
            ("LSE", "Europe/London", "GBP", "Europe"),
            ("TSE", "Asia/Tokyo", "JPY", "Asia"),
            ("ASX", "Australia/Sydney", "AUD", "Oceania"),
            ("TSX", "America/Toronto", "CAD", "North America"),
            ("EURONEXT", "Europe/Paris", "EUR", "Europe"),
        ],
    )
    def test_exchange_market_hours_valid_exchanges(
        self, api_key, exchange, expected_timezone, expected_currency, region
    ):
        """Test exchange market hours with comprehensive global exchanges."""
        result, validation = handle_api_call_with_validation(
            market_hours.exchange_market_hours,
            "exchange_market_hours",
            apikey=api_key,
            exchange=exchange,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            models,
            FMPExchangeMarketHours,
            f"Failed to validate market hours models for {exchange}",
        )

        if models:  # If data is not empty
            # Enhanced validation for first item
            first_item = models[0]

            # Business logic validation
            assert (
                first_item.exchange == exchange
            ), f"Exchange should match for {exchange}"
            assert (
                first_item.name is not None and len(first_item.name) > 0
            ), f"Name should not be empty for {exchange}"
            assert (
                first_item.openingHour is not None and len(first_item.openingHour) > 0
            ), f"Opening hour should not be empty for {exchange}"
            assert (
                first_item.closingHour is not None and len(first_item.closingHour) > 0
            ), f"Closing hour should not be empty for {exchange}"
            assert (
                first_item.timezone is not None and len(first_item.timezone) > 0
            ), f"Timezone should not be empty for {exchange}"
            assert isinstance(
                first_item.isMarketOpen, bool
            ), f"isMarketOpen should be boolean for {exchange}"

            # Regional timezone validation
            if region == "North America":
                assert (
                    "America" in first_item.timezone
                ), f"North American exchange {exchange} should have America timezone"
            elif region == "Europe":
                assert (
                    "Europe" in first_item.timezone
                ), f"European exchange {exchange} should have Europe timezone"
            elif region == "Asia":
                assert (
                    "Asia" in first_item.timezone
                ), f"Asian exchange {exchange} should have Asia timezone"
            elif region == "Oceania":
                assert (
                    "Australia" in first_item.timezone
                ), f"Oceania exchange {exchange} should have Australia timezone"

            # Time format validation
            if ":" in first_item.openingHour:
                # Standard HH:MM format
                hours, minutes = first_item.openingHour.split(" ")[0].split(":")[:2]
                assert (
                    hours.isdigit() and 0 <= int(hours) <= 23
                ), f"Opening hour should be valid for {exchange}"
                assert (
                    minutes.isdigit() and 0 <= int(minutes) <= 59
                ), f"Opening minutes should be valid for {exchange}"

            if ":" in first_item.closingHour:
                # Standard HH:MM format
                hours, minutes = first_item.closingHour.split(" ")[0].split(":")[:2]
                assert (
                    hours.isdigit() and 0 <= int(hours) <= 23
                ), f"Closing hour should be valid for {exchange}"
                assert (
                    minutes.isdigit() and 0 <= int(minutes) <= 59
                ), f"Closing minutes should be valid for {exchange}"

    def test_exchange_market_hours_invalid_exchange(self, api_key):
        """Test exchange market hours with invalid exchange name."""
        # Invalid exchange should raise an exception
        with pytest.raises(Exception) as exc_info:
            market_hours.exchange_market_hours(
                apikey=api_key, exchange="INVALID_EXCHANGE"
            )

        # Should contain information about invalid exchange
        assert "Invalid Exchange" in str(exc_info.value) or "400" in str(exc_info.value)

    @pytest.mark.parametrize(
        "exchange,expected_holiday_count_range,region",
        [
            ("NYSE", (8, 15), "US"),
            ("NASDAQ", (8, 15), "US"),
            ("LSE", (6, 12), "UK"),
            ("TSE", (10, 20), "Japan"),
            ("ASX", (8, 15), "Australia"),
            ("TSX", (8, 15), "Canada"),
            ("EURONEXT", (5, 12), "Europe"),
        ],
    )
    def test_holidays_by_exchange_comprehensive(
        self, api_key, exchange, expected_holiday_count_range, region
    ):
        """Test holidays by exchange for various global exchanges."""
        result, validation = handle_api_call_with_validation(
            market_hours.holidays_by_exchange,
            "holidays_by_exchange",
            apikey=api_key,
            exchange=exchange,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeHoliday)
        validate_model_list(
            models,
            FMPExchangeHoliday,
            f"Failed to validate holiday models for {exchange}",
        )

        if models:
            # Enhanced validation for first item
            first_item = models[0]

            # Business logic validation
            if first_item.exchange:
                assert (
                    first_item.exchange == exchange
                ), f"Exchange should match for {exchange}"
            assert (
                first_item.date is not None
            ), f"Date should not be None for {exchange}"
            assert (
                first_item.name is not None and len(first_item.name) > 0
            ), f"Holiday name should not be empty for {exchange}"

            # Date format validation
            if first_item.date:
                assert (
                    len(str(first_item.date)) >= 10
                ), f"Date should be in valid format for {exchange}"
                # Try to parse the date
                try:
                    datetime.strptime(str(first_item.date)[:10], "%Y-%m-%d")
                except ValueError:
                    pytest.fail(
                        f"Invalid date format for {exchange} holiday: {first_item.date}"
                    )

            # Holiday count validation
            min_count, max_count = expected_holiday_count_range
            holiday_count = len(models)
            assert (
                min_count <= holiday_count <= max_count
            ), f"Holiday count for {exchange} should be between {min_count} and {max_count}, got {holiday_count}"

            # Regional holiday validation
            if region == "US":
                # US exchanges should have common holidays
                holiday_names = [item.name for item in models if item.name]
                us_holidays = ["New Year", "Independence", "Christmas", "Thanksgiving"]
                found_holidays = [
                    h for h in us_holidays if any(h in name for name in holiday_names)
                ]
                assert (
                    len(found_holidays) >= 1
                ), f"US exchange {exchange} should have common US holidays"

    @pytest.mark.parametrize("exchange", ["NYSE", "NASDAQ"])
    def test_holidays_by_exchange_with_date_range(self, api_key, exchange):
        """Test holidays by exchange with date range filter."""
        current_year = datetime.now().year
        from_date = f"{current_year}-01-01"
        to_date = f"{current_year}-12-31"

        result, validation = handle_api_call_with_validation(
            market_hours.holidays_by_exchange,
            "holidays_by_exchange",
            apikey=api_key,
            exchange=exchange,
            from_date=from_date,
            to_date=to_date,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeHoliday)
        validate_model_list(
            models,
            FMPExchangeHoliday,
            f"Failed to validate holiday models with date range for {exchange}",
        )

        if models:
            # Validate date range
            for item in models[:5]:  # Check first 5 items
                if item.date:
                    assert (
                        len(str(item.date)) >= 10
                    ), f"Date should be valid format for {exchange}"
                    # Check if date is within range
                    try:
                        holiday_date = datetime.strptime(
                            str(item.date)[:10], "%Y-%m-%d"
                        )
                        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
                        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
                        assert (
                            from_datetime <= holiday_date <= to_datetime
                        ), f"Holiday date should be within range for {exchange}"
                    except ValueError:
                        pytest.fail(
                            f"Invalid date format for {exchange} holiday: {item.date}"
                        )

    def test_holidays_by_exchange_invalid_exchange(self, api_key):
        """Test holidays by exchange with invalid exchange name."""
        # Invalid exchange should raise an exception
        with pytest.raises(Exception) as exc_info:
            market_hours.holidays_by_exchange(
                apikey=api_key, exchange="INVALID_EXCHANGE"
            )

        # Verify the error message indicates invalid exchange
        assert "Invalid Exchange Provided" in str(exc_info.value)

    def test_all_exchange_market_hours_comprehensive(self, api_key):
        """Test all exchange market hours endpoint."""
        result, validation = handle_api_call_with_validation(
            market_hours.all_exchange_market_hours,
            "all_exchange_market_hours",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            models,
            FMPExchangeMarketHours,
            "Failed to validate all exchange market hours models",
        )

        if models:
            # Validate each exchange
            for item in models:
                # Basic field validation
                assert (
                    item.exchange is not None and len(item.exchange) > 0
                ), f"Exchange should not be empty"
                assert (
                    item.name is not None and len(item.name) > 0
                ), f"Name should not be empty for {item.exchange}"
                assert (
                    item.openingHour is not None and len(item.openingHour) > 0
                ), f"Opening hour should not be empty for {item.exchange}"
                assert (
                    item.closingHour is not None and len(item.closingHour) > 0
                ), f"Closing hour should not be empty for {item.exchange}"
                assert (
                    item.timezone is not None and len(item.timezone) > 0
                ), f"Timezone should not be empty for {item.exchange}"
                assert isinstance(
                    item.isMarketOpen, bool
                ), f"isMarketOpen should be boolean for {item.exchange}"

            # Check for major exchanges
            exchanges = [item.exchange for item in models]
            major_exchanges = ["NYSE", "NASDAQ", "LSE", "TSE", "ASX", "TSX", "EURONEXT"]
            found_major = [ex for ex in major_exchanges if ex in exchanges]
            assert (
                len(found_major) >= 3
            ), f"Should find at least 3 major exchanges, found {len(found_major)}"

            # Check timezone diversity
            timezones = [item.timezone for item in models]
            unique_timezones = set(timezones)
            assert (
                len(unique_timezones) >= 3
            ), f"Should have at least 3 unique timezones, got {len(unique_timezones)}"

            # Check for timezone patterns
            america_timezones = [tz for tz in timezones if "America" in tz]
            europe_timezones = [tz for tz in timezones if "Europe" in tz]
            asia_timezones = [tz for tz in timezones if "Asia" in tz]

            assert (
                len(america_timezones) >= 1
            ), "Should have at least 1 America timezone"
            assert len(europe_timezones) >= 1, "Should have at least 1 Europe timezone"
            assert len(asia_timezones) >= 1, "Should have at least 1 Asia timezone"


class TestMarketHoursDataQuality:
    """Test data quality for market hours endpoints."""

    def test_date_range_validation(self, api_key):
        """Test date range validation for holidays endpoint."""
        current_year = datetime.now().year

        # Test with valid date range
        from_date = f"{current_year}-01-01"
        to_date = f"{current_year}-12-31"

        result, validation = handle_api_call_with_validation(
            market_hours.holidays_by_exchange,
            "holidays_by_exchange",
            apikey=api_key,
            exchange="NYSE",
            from_date=from_date,
            to_date=to_date,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeHoliday)
        validate_model_list(
            models,
            FMPExchangeHoliday,
            "Failed to validate holiday models with date range",
        )

        # All dates should be within the specified range
        for item in models:
            if item.date:
                holiday_date = datetime.strptime(str(item.date)[:10], "%Y-%m-%d")
                from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
                to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
                assert (
                    from_datetime <= holiday_date <= to_datetime
                ), f"Holiday date {item.date} should be within range"

    def test_market_hours_data_quality(self, api_key):
        """Test data quality for market hours data."""
        result, validation = handle_api_call_with_validation(
            market_hours.all_exchange_market_hours,
            "all_exchange_market_hours",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            models,
            FMPExchangeMarketHours,
            "Failed to validate all exchange market hours models",
        )

        if models:
            # Data quality metrics
            total_exchanges = len(models)
            valid_exchanges = 0
            valid_names = 0
            valid_hours = 0
            valid_timezones = 0
            valid_market_status = 0

            for item in models:
                # Exchange validation
                if item.exchange and len(item.exchange) >= 2:
                    valid_exchanges += 1

                # Name validation
                if item.name and len(item.name) >= 2:
                    valid_names += 1

                # Hours validation
                if (
                    item.openingHour
                    and len(item.openingHour) >= 4
                    and item.closingHour
                    and len(item.closingHour) >= 4
                ):
                    valid_hours += 1

                # Timezone validation
                if item.timezone and len(item.timezone) >= 8:
                    valid_timezones += 1

                # Market status validation
                if isinstance(item.isMarketOpen, bool):
                    valid_market_status += 1

            # Business logic assertions
            if total_exchanges > 0:
                assert (
                    valid_exchanges / total_exchanges >= 0.95
                ), f"Only {valid_exchanges}/{total_exchanges} exchanges are valid"
                assert (
                    valid_names / total_exchanges >= 0.90
                ), f"Only {valid_names}/{total_exchanges} names are valid"
                assert (
                    valid_hours / total_exchanges >= 0.85
                ), f"Only {valid_hours}/{total_exchanges} hours are valid"
                assert (
                    valid_timezones / total_exchanges >= 0.90
                ), f"Only {valid_timezones}/{total_exchanges} timezones are valid"
                assert (
                    valid_market_status / total_exchanges >= 0.95
                ), f"Only {valid_market_status}/{total_exchanges} market status values are valid"


class TestMarketHoursComprehensive:
    """Comprehensive tests for market hours functionality."""

    @pytest.mark.parametrize(
        "exchange,region,expected_characteristics",
        [
            ("NYSE", "US", {"currency": "USD", "timezone_region": "America"}),
            ("NASDAQ", "US", {"currency": "USD", "timezone_region": "America"}),
            ("LSE", "UK", {"currency": "GBP", "timezone_region": "Europe"}),
            ("TSE", "Japan", {"currency": "JPY", "timezone_region": "Asia"}),
            ("ASX", "Australia", {"currency": "AUD", "timezone_region": "Australia"}),
            ("TSX", "Canada", {"currency": "CAD", "timezone_region": "America"}),
            ("EURONEXT", "Europe", {"currency": "EUR", "timezone_region": "Europe"}),
        ],
    )
    def test_exchange_characteristics_validation(
        self, api_key, exchange, region, expected_characteristics
    ):
        """Test exchange characteristics validation."""
        result, validation = handle_api_call_with_validation(
            market_hours.exchange_market_hours,
            "exchange_market_hours",
            apikey=api_key,
            exchange=exchange,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            models,
            FMPExchangeMarketHours,
            f"Failed to validate market hours models for {exchange}",
        )

        if models:
            item = models[0]

            # Validate exchange characteristics
            assert item.exchange == exchange, f"Exchange should match for {exchange}"

            # Timezone region validation
            timezone_region = expected_characteristics["timezone_region"]
            if timezone_region == "America":
                assert (
                    "America" in item.timezone
                ), f"{exchange} should have America timezone"
            elif timezone_region == "Europe":
                assert (
                    "Europe" in item.timezone
                ), f"{exchange} should have Europe timezone"
            elif timezone_region == "Asia":
                assert "Asia" in item.timezone, f"{exchange} should have Asia timezone"
            elif timezone_region == "Australia":
                assert (
                    "Australia" in item.timezone
                ), f"{exchange} should have Australia timezone"

    @pytest.mark.parametrize(
        "exchange,market_type,expected_features",
        [
            ("NYSE", "stock", {"trading_hours": "regular", "holidays": "US"}),
            ("NASDAQ", "stock", {"trading_hours": "regular", "holidays": "US"}),
            ("LSE", "stock", {"trading_hours": "regular", "holidays": "UK"}),
            ("TSE", "stock", {"trading_hours": "regular", "holidays": "Japan"}),
            ("ASX", "stock", {"trading_hours": "regular", "holidays": "Australia"}),
        ],
    )
    def test_market_type_features(
        self, api_key, exchange, market_type, expected_features
    ):
        """Test market type features validation."""
        # Test market hours
        result, validation = handle_api_call_with_validation(
            market_hours.exchange_market_hours,
            "exchange_market_hours",
            apikey=api_key,
            exchange=exchange,
        )

        # Extract and validate models
        models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            models,
            FMPExchangeMarketHours,
            f"Failed to validate market hours models for {exchange}",
        )

        if models:
            item = models[0]

            # Validate trading hours
            if expected_features["trading_hours"] == "regular":
                # Markets can be closed, showing "CLOSED" instead of time format
                opening_hour = item.openingHour
                closing_hour = item.closingHour

                # Either should have regular time format (HH:MM) or be CLOSED
                assert (":" in opening_hour) or (
                    opening_hour == "CLOSED"
                ), f"{exchange} should have regular trading hours format or be CLOSED"
                assert (":" in closing_hour) or (
                    closing_hour == "CLOSED"
                ), f"{exchange} should have regular trading hours format or be CLOSED"

            # Test holidays
            result, validation = handle_api_call_with_validation(
                market_hours.holidays_by_exchange,
                "holidays_by_exchange",
                apikey=api_key,
                exchange=exchange,
            )

            # Extract and validate models
            holiday_models = get_response_models(result, FMPExchangeHoliday)
            validate_model_list(
                holiday_models,
                FMPExchangeHoliday,
                f"Failed to validate holiday models for {exchange}",
            )

            if holiday_models:
                # Validate holiday characteristics based on region
                holiday_region = expected_features["holidays"]
                if holiday_region == "US":
                    us_holidays = [
                        "New Year",
                        "Independence",
                        "Christmas",
                        "Thanksgiving",
                    ]
                    holiday_names = [item.name for item in holiday_models if item.name]
                    found_holidays = [
                        h
                        for h in us_holidays
                        if any(h in name for name in holiday_names)
                    ]
                    assert (
                        len(found_holidays) >= 1
                    ), f"US exchange {exchange} should have common US holidays"

    def test_market_hours_consistency_across_endpoints(self, api_key):
        """Test consistency across different market hours endpoints."""
        # Test individual exchange
        result, validation = handle_api_call_with_validation(
            market_hours.exchange_market_hours,
            "exchange_market_hours",
            apikey=api_key,
            exchange="NYSE",
        )

        # Extract and validate models
        individual_models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            individual_models,
            FMPExchangeMarketHours,
            "Failed to validate individual exchange market hours models",
        )

        # Test all exchanges
        result, validation = handle_api_call_with_validation(
            market_hours.all_exchange_market_hours,
            "all_exchange_market_hours",
            apikey=api_key,
        )

        # Extract and validate models
        all_models = get_response_models(result, FMPExchangeMarketHours)
        validate_model_list(
            all_models,
            FMPExchangeMarketHours,
            "Failed to validate all exchange market hours models",
        )

        if individual_models and all_models:
            # Find NYSE in all exchanges
            nyse_in_all = [item for item in all_models if item.exchange == "NYSE"]

            if nyse_in_all and individual_models:
                individual_nyse = individual_models[0]
                all_nyse = nyse_in_all[0]

                # Data should be consistent
                assert (
                    individual_nyse.exchange == all_nyse.exchange
                ), "NYSE exchange should be consistent"
                assert (
                    individual_nyse.name == all_nyse.name
                ), "NYSE name should be consistent"
                assert (
                    individual_nyse.openingHour == all_nyse.openingHour
                ), "NYSE opening hour should be consistent"
                assert (
                    individual_nyse.closingHour == all_nyse.closingHour
                ), "NYSE closing hour should be consistent"
                assert (
                    individual_nyse.timezone == all_nyse.timezone
                ), "NYSE timezone should be consistent"
                assert (
                    individual_nyse.isMarketOpen == all_nyse.isMarketOpen
                ), "NYSE market status should be consistent"
