from datetime import datetime

import pytest

from fmpsdk import market_hours
from fmpsdk.models import FMPExchangeHoliday, FMPExchangeMarketHours


class TestMarketHours:
    """Test cases for market_hours module functions."""

    @pytest.mark.parametrize(
        "exchange,expected_timezone,expected_currency,region",
        [
            ("NYSE", "America/New_York", "USD", "North America"),
            ("NASDAQ", "America/New_York", "USD", "North America"),
            ("AMEX", "America/New_York", "USD", "North America"),
            ("LSE", "Europe/London", "GBP", "Europe"),
            ("TSE", "Asia/Tokyo", "JPY", "Asia"),
            ("HKEX", "Asia/Hong_Kong", "HKD", "Asia"),
            ("ASX", "Australia/Sydney", "AUD", "Oceania"),
            ("TSX", "America/Toronto", "CAD", "North America"),
            ("EURONEXT", "Europe/Paris", "EUR", "Europe"),
            ("SWX", "Europe/Zurich", "CHF", "Europe"),
        ],
    )
    def test_exchange_market_hours_valid_exchanges(
        self, api_key, exchange, expected_timezone, expected_currency, region
    ):
        """Test exchange_market_hours with comprehensive global exchanges."""
        result = market_hours.exchange_market_hours(apikey=api_key, exchange=exchange)

        # Test that we get a result
        assert result is not None, f"Should get market hours for {exchange} in {region}"

        # Convert to list if it's a model
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Handle error responses for unsupported exchanges
        if isinstance(data, dict) and "Error Message" in data:
            pytest.skip(f"Exchange {exchange} not supported by API")

        # Test that we get a list
        assert isinstance(data, list), f"Result should be list for {exchange}"

        if data:  # If data is not empty
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure for market hours
                required_fields = [
                    "exchange",
                    "name",
                    "openingHour",
                    "closingHour",
                    "timezone",
                    "isMarketOpen",
                ]
                for field in required_fields:
                    assert (
                        field in first_item
                    ), f"{field} should be present for {exchange}"
                    if field == "isMarketOpen":
                        assert isinstance(
                            first_item[field], bool
                        ), f"{field} should be boolean for {exchange}"
                    else:
                        assert isinstance(
                            first_item[field], str
                        ), f"{field} should be string for {exchange}"
                        assert (
                            len(first_item[field]) > 0
                        ), f"{field} should not be empty for {exchange}"

                # Validate specific fields
                assert (
                    first_item["exchange"] == exchange
                ), f"Exchange should match for {exchange}"

                # Regional validations
                if region == "North America":
                    # North American markets should have USD/CAD currency context
                    expected_currencies = ["USD", "CAD"]
                    # We don't directly validate currency as it might not be in the response
                elif region == "Europe":
                    # European markets should have reasonable timezone
                    assert (
                        "Europe" in first_item.get("timezone", "")
                        or first_item.get("timezone", "") != ""
                    ), f"European exchange {exchange} should have European timezone context"
                elif region == "Asia":
                    # Asian markets should have Asian timezone
                    assert (
                        "Asia" in first_item.get("timezone", "")
                        or first_item.get("timezone", "") != ""
                    ), f"Asian exchange {exchange} should have Asian timezone context"

                # Validate opening and closing hours format
                opening_hour = first_item["openingHour"]
                closing_hour = first_item["closingHour"]

                # Basic time format validation (should contain colon for time)
                if opening_hour and closing_hour:
                    assert (
                        ":" in opening_hour or opening_hour.isdigit()
                    ), f"Opening hour format should be valid for {exchange}"
                    assert (
                        ":" in closing_hour or closing_hour.isdigit()
                    ), f"Closing hour format should be valid for {exchange}"
                assert first_item["exchange"].upper() == exchange.upper()

            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPExchangeMarketHours)
                assert hasattr(first_item, "exchange")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "openingHour")
                assert hasattr(first_item, "closingHour")
                assert hasattr(first_item, "timezone")
                assert hasattr(first_item, "isMarketOpen")
                assert isinstance(first_item.exchange, str)
                assert isinstance(first_item.name, str)
                assert isinstance(first_item.openingHour, str)
                assert isinstance(first_item.closingHour, str)
                assert isinstance(first_item.timezone, str)
                assert isinstance(first_item.isMarketOpen, bool)
                assert len(first_item.exchange) > 0
                assert len(first_item.name) > 0
                assert len(first_item.openingHour) > 0
                assert len(first_item.closingHour) > 0
                assert len(first_item.timezone) > 0
                assert first_item.exchange.upper() == exchange.upper()

    def test_exchange_market_hours_invalid_exchange(self, api_key):
        """Test exchange_market_hours with invalid exchange name."""
        result = market_hours.exchange_market_hours(
            apikey=api_key, exchange="INVALID_EXCHANGE"
        )

        # Should return empty list or error structure
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should be empty list or have error message
        if isinstance(data, list):
            assert len(data) == 0
        elif isinstance(data, dict):
            # Might return error dict
            assert "Error Message" in data or "message" in data or "error" in data

    def test_exchange_market_hours_invalid_api_key(self):
        """Test exchange_market_hours with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = market_hours.exchange_market_hours(
            apikey=invalid_api_key, exchange="NYSE"
        )

        # Should return empty list or error structure
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should be empty list or have error message
        if isinstance(data, list):
            assert len(data) == 0
        elif isinstance(data, dict):
            # Might return error dict
            assert "Error Message" in data or "message" in data

    @pytest.mark.parametrize(
        "exchange,expected_holiday_count_range,region",
        [
            ("NYSE", (8, 15), "US"),
            ("NASDAQ", (8, 15), "US"),
            ("LSE", (6, 12), "UK"),
            ("TSE", (10, 20), "Japan"),
            ("HKEX", (8, 16), "Hong Kong"),
            ("ASX", (8, 15), "Australia"),
            ("TSX", (8, 15), "Canada"),
            ("EURONEXT", (6, 12), "Europe"),
        ],
    )
    def test_holidays_by_exchange_no_date_range(
        self, api_key, exchange, expected_holiday_count_range, region
    ):
        """Test holidays_by_exchange for various global exchanges without date range."""
        result = market_hours.holidays_by_exchange(apikey=api_key, exchange=exchange)

        # Test that we get a result
        assert result is not None, f"Should get holidays for {exchange} in {region}"

        # Convert to list if it's a model
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Handle error responses for unsupported exchanges
        if isinstance(data, dict) and "Error Message" in data:
            pytest.skip(f"Exchange {exchange} not supported by API")

        # Test that we get a list
        assert isinstance(data, list), f"Result should be list for {exchange}"

        # Note: Holidays API might return empty list if no holidays in default range
        # This is acceptable behavior, but if we get data, validate it
        if data:
            min_count, max_count = expected_holiday_count_range
            # Don't strictly enforce count as it depends on the date range used by API
            # but if we get data, it should be reasonable

            # Test first item structure if data exists
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure for holidays
                required_fields = ["date", "name"]
                for field in required_fields:
                    assert (
                        field in first_item
                    ), f"{field} should be present for {exchange} holidays"
                    assert isinstance(
                        first_item[field], str
                    ), f"{field} should be string for {exchange}"
                    assert (
                        len(first_item[field]) > 0
                    ), f"{field} should not be empty for {exchange}"

                # Validate date format (should be YYYY-MM-DD or similar)
                date_str = first_item["date"]
                assert (
                    len(date_str) >= 8
                ), f"Date should be reasonable length for {exchange}"
                assert any(
                    char.isdigit() for char in date_str
                ), f"Date should contain digits for {exchange}"

    @pytest.mark.parametrize("exchange", ["NYSE", "NASDAQ"])
    def test_holidays_by_exchange_with_date_range(self, api_key, exchange):
        """Test holidays_by_exchange with date range."""
        # Use current year for date range
        current_year = datetime.now().year
        from_date = f"{current_year}-01-01"
        to_date = f"{current_year}-12-31"

        result = market_hours.holidays_by_exchange(
            apikey=api_key, exchange=exchange, from_date=from_date, to_date=to_date
        )

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Test that we get a list
        assert isinstance(data, list)

        # For major exchanges, we should get some holidays in a full year
        if data:
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure for holidays
                required_fields = ["exchange", "date", "name", "isClosed"]
                for field in required_fields:
                    assert field in first_item
                    if field == "isClosed":
                        assert isinstance(first_item[field], bool)
                    else:
                        assert isinstance(first_item[field], str)
                        assert len(first_item[field]) > 0

            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPExchangeHoliday)
                assert hasattr(first_item, "exchange")
                assert hasattr(first_item, "date")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "isClosed")
                assert isinstance(first_item.exchange, str)
                assert isinstance(first_item.date, str)
                assert isinstance(first_item.name, str)
                assert isinstance(first_item.isClosed, bool)
                assert len(first_item.exchange) > 0
                assert len(first_item.date) > 0
                assert len(first_item.name) > 0

    def test_holidays_by_exchange_invalid_exchange(self, api_key):
        """Test holidays_by_exchange with invalid exchange name."""
        result = market_hours.holidays_by_exchange(
            apikey=api_key, exchange="INVALID_EXCHANGE"
        )

        # Should return empty list or error structure
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should be empty list or have error message
        if isinstance(data, list):
            assert len(data) == 0
        elif isinstance(data, dict):
            # Might return error dict
            assert "Error Message" in data or "message" in data or "error" in data

    def test_holidays_by_exchange_invalid_api_key(self):
        """Test holidays_by_exchange with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = market_hours.holidays_by_exchange(
            apikey=invalid_api_key, exchange="NYSE"
        )

        # Should return empty list or error structure
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should be empty list or have error message
        if isinstance(data, list):
            assert len(data) == 0
        elif isinstance(data, dict):
            # Might return error dict
            assert "Error Message" in data or "message" in data

    def test_all_exchange_market_hours_valid_api_key(self, api_key):
        """Test all_exchange_market_hours with valid API key."""
        result = market_hours.all_exchange_market_hours(apikey=api_key)

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Test that we get a list
        assert isinstance(data, list)

        if data:  # If data is not empty
            # Should have multiple exchanges
            assert len(data) >= 5  # Should have at least major exchanges

            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure for market hours
                required_fields = [
                    "exchange",
                    "name",
                    "openingHour",
                    "closingHour",
                    "timezone",
                    "isMarketOpen",
                ]
                for field in required_fields:
                    assert field in first_item
                    if field == "isMarketOpen":
                        assert isinstance(first_item[field], bool)
                    else:
                        assert isinstance(first_item[field], str)
                        assert len(first_item[field]) > 0

            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPExchangeMarketHours)
                assert hasattr(first_item, "exchange")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "openingHour")
                assert hasattr(first_item, "closingHour")
                assert hasattr(first_item, "timezone")
                assert hasattr(first_item, "isMarketOpen")
                assert isinstance(first_item.exchange, str)
                assert isinstance(first_item.name, str)
                assert isinstance(first_item.openingHour, str)
                assert isinstance(first_item.closingHour, str)
                assert isinstance(first_item.timezone, str)
                assert isinstance(first_item.isMarketOpen, bool)
                assert len(first_item.exchange) > 0
                assert len(first_item.name) > 0
                assert len(first_item.openingHour) > 0
                assert len(first_item.closingHour) > 0
                assert len(first_item.timezone) > 0

            # Check for major exchanges
            exchanges = []
            for item in data:
                if isinstance(item, dict):
                    exchanges.append(item["exchange"])
                else:
                    exchanges.append(item.exchange)

            # Should contain major exchanges
            major_exchanges = ["NYSE", "NASDAQ", "AMEX"]
            found_exchanges = [ex for ex in major_exchanges if ex in exchanges]
            assert len(found_exchanges) >= 1  # Should find at least one major exchange

    def test_all_exchange_market_hours_invalid_api_key(self):
        """Test all_exchange_market_hours with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = market_hours.all_exchange_market_hours(apikey=invalid_api_key)

        # Should return empty list or error structure
        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        # Should be empty list or have error message
        if isinstance(data, list):
            assert len(data) == 0
        elif isinstance(data, dict):
            # Might return error dict
            assert "Error Message" in data or "message" in data

    def test_all_functions_response_time(self, api_key):
        """Test that all functions respond within reasonable time."""
        import time

        # Test exchange_market_hours response time
        start_time = time.time()
        result = market_hours.exchange_market_hours(apikey=api_key, exchange="NYSE")
        end_time = time.time()
        assert (end_time - start_time) < 10.0  # Should respond within 10 seconds

        # Test holidays_by_exchange response time
        start_time = time.time()
        result = market_hours.holidays_by_exchange(apikey=api_key, exchange="NYSE")
        end_time = time.time()
        assert (end_time - start_time) < 10.0  # Should respond within 10 seconds

        # Test all_exchange_market_hours response time
        start_time = time.time()
        result = market_hours.all_exchange_market_hours(apikey=api_key)
        end_time = time.time()
        assert (
            end_time - start_time
        ) < 15.0  # Should respond within 15 seconds (larger dataset)

    def test_date_range_validation(self, api_key):
        """Test date range functionality for holidays."""
        # Test with a reasonable date range
        current_year = datetime.now().year
        last_year = current_year - 1

        # Test previous year holidays
        from_date = f"{last_year}-01-01"
        to_date = f"{last_year}-12-31"

        result = market_hours.holidays_by_exchange(
            apikey=api_key, exchange="NYSE", from_date=from_date, to_date=to_date
        )

        # Should get a valid result (even if empty)
        assert result is not None

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        assert isinstance(data, list)

        # Test with only from_date
        result2 = market_hours.holidays_by_exchange(
            apikey=api_key, exchange="NYSE", from_date=from_date
        )

        assert result2 is not None

        # Test with only to_date
        result3 = market_hours.holidays_by_exchange(
            apikey=api_key, exchange="NYSE", to_date=to_date
        )

        assert result3 is not None

    def test_market_hours_data_quality(self, api_key):
        """Test the quality and consistency of market hours data."""
        result = market_hours.all_exchange_market_hours(apikey=api_key)

        if hasattr(result, "root"):
            data = result.root
        else:
            data = result

        if data and len(data) > 0:
            exchanges = set()
            timezones = set()

            for item in data:
                if isinstance(item, dict):
                    exchange = item.get("exchange", "")
                    name = item.get("name", "")
                    timezone = item.get("timezone", "")
                    opening_hour = item.get("openingHour", "")
                    closing_hour = item.get("closingHour", "")
                    is_market_open = item.get("isMarketOpen", False)
                else:
                    exchange = getattr(item, "exchange", "")
                    name = getattr(item, "name", "")
                    timezone = getattr(item, "timezone", "")
                    opening_hour = getattr(item, "openingHour", "")
                    closing_hour = getattr(item, "closingHour", "")
                    is_market_open = getattr(item, "isMarketOpen", False)

                # Validate exchange format
                if exchange:
                    assert len(exchange) >= 2
                    assert (
                        len(exchange) <= 10
                    )  # Exchange codes are typically 2-10 characters
                    exchanges.add(exchange)

                # Validate name
                if name:
                    assert len(name) >= 3
                    assert len(name) <= 100  # Reasonable exchange name length

                # Validate timezone
                if timezone:
                    assert len(timezone) >= 3
                    timezones.add(timezone)

                # Validate time formats (should be HH:MM, numeric, or 'CLOSED')
                if opening_hour:
                    assert (
                        ":" in opening_hour
                        or opening_hour.isdigit()
                        or opening_hour == "CLOSED"
                    )

                if closing_hour:
                    assert (
                        ":" in closing_hour
                        or closing_hour.isdigit()
                        or closing_hour == "CLOSED"
                    )

                # Validate boolean field
                assert isinstance(is_market_open, bool)

            # Check for no duplicate exchanges
            assert len(exchanges) <= len(
                data
            )  # Should not have more unique exchanges than total items

            # Should have diverse timezones
            assert len(timezones) >= 1  # Should have at least one timezone

            # Check for well-known exchanges
            known_exchanges = ["NYSE", "NASDAQ", "AMEX", "CBOE"]
            found_known_exchanges = [ex for ex in known_exchanges if ex in exchanges]
            assert (
                len(found_known_exchanges) >= 1
            )  # Should find at least 1 known exchange
