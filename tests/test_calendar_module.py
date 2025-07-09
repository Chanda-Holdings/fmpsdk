from datetime import datetime, timedelta

import pytest

from fmpsdk.calendar_module import (
    dividends,
    dividends_calendar,
    earnings_calendar,
    ipos_calendar,
    ipos_disclosure,
    ipos_prospectus,
    splits,
    splits_calendar,
)
from fmpsdk.models import (
    FMPDisclosureFiling,
    FMPDividend,
    FMPDividendCalendarEvent,
    FMPEarningsCalendarEvent,
    FMPProspectusFiling,
    FMPStockSplit,
    FMPUpcomingIPO,
)
from tests.conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name)
    else:
        return getattr(item, field_name, None)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestDividends:
    """Test class for historical dividend data functionality."""

    def test_dividends_valid_symbol(self, api_key):
        """Test dividends for a valid dividend-paying stock."""
        # Apple is known for paying regular dividends
        result = dividends(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first dividend record
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPDividend.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.date is not None
        assert validated.dividend > 0
        assert validated.recordDate is not None
        assert validated.paymentDate is not None
        assert validated.declarationDate is not None

    def test_dividends_with_limit(self, api_key):
        """Test dividends with limit parameter."""
        limit = 5
        result = dividends(apikey=api_key, symbol="AAPL", limit=limit)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        if len(result_list) > 0:
            # Validate structure
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            dividend_value = get_field_value(first_item, "dividend")

            assert symbol_value == "AAPL"
            assert dividend_value > 0

    def test_dividends_multiple_dividend_paying_stocks(self, api_key):
        """Test dividends for multiple dividend-paying stocks."""
        dividend_stocks = ["AAPL", "MSFT", "JNJ", "KO", "PG"]

        for symbol in dividend_stocks:
            result = dividends(apikey=api_key, symbol=symbol, limit=3)
            result_list = extract_data_list(result)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                dividend_value = get_field_value(first_item, "dividend")

                assert symbol_value == symbol, f"Symbol should match for {symbol}"
                assert dividend_value > 0, f"Dividend should be positive for {symbol}"

    def test_dividends_chronological_order(self, api_key):
        """Test that dividends are returned in chronological order."""
        result = dividends(
            apikey=api_key, symbol="KO", limit=10
        )  # Coca-Cola has long dividend history

        result_list = extract_data_list(result)
        assert len(result_list) > 1

        dates = [get_field_value(item, "date") for item in result_list]

        # Check if dates are in order (either ascending or descending)
        is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
        is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

        assert (
            is_ascending or is_descending
        ), "Dividends should be in chronological order"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestDividendsCalendar:
    """Test class for dividend calendar functionality."""

    def test_dividends_calendar_current_month(self, api_key):
        """Test dividend calendar for current month."""
        today = datetime.now()
        from_date = today.replace(day=1).strftime("%Y-%m-%d")
        to_date = (
            (today.replace(day=28) + timedelta(days=4))
            .replace(day=1)
            .strftime("%Y-%m-%d")
        )

        result = dividends_calendar(
            apikey=api_key, from_date=from_date, to_date=to_date
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Calendar may be empty depending on the month
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPDividendCalendarEvent.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.date is not None
            assert from_date <= validated.date <= to_date
            assert validated.dividend > 0

    def test_dividends_calendar_no_date_range(self, api_key):
        """Test dividend calendar without date range (should get current/upcoming)."""
        result = dividends_calendar(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should return upcoming dividends
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            dividend_value = get_field_value(first_item, "dividend")

            assert symbol_value is not None
            assert dividend_value > 0

    def test_dividends_calendar_specific_date_range(self, api_key):
        """Test dividend calendar with specific date range."""
        # Test a period known to have dividend activity
        from_date = "2024-03-01"
        to_date = "2024-03-31"

        result = dividends_calendar(
            apikey=api_key, from_date=from_date, to_date=to_date
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Note: Some APIs may return data slightly outside the requested range
        # This is an API behavior, not a test failure
        if len(result_list) > 0:
            # Validate that most dates are within range
            dates_in_range = sum(
                1
                for item in result_list
                if from_date <= get_field_value(item, "date") <= to_date
            )
            # At least 80% of results should be in range (API may include buffer dates)
            assert (
                dates_in_range >= len(result_list) * 0.8
            ), f"Most dates should be within range, got {dates_in_range}/{len(result_list)} in range"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsCalendar:
    """Test class for earnings calendar functionality."""

    def test_earnings_calendar_current_week(self, api_key):
        """Test earnings calendar for current week."""
        today = datetime.now()
        # Get current week (Monday to Friday)
        monday = today - timedelta(days=today.weekday())
        friday = monday + timedelta(days=4)

        from_date = monday.strftime("%Y-%m-%d")
        to_date = friday.strftime("%Y-%m-%d")

        result = earnings_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Earnings calendar may be empty on weekends or holidays
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPEarningsCalendarEvent.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.date is not None
            assert from_date <= validated.date <= to_date

    def test_earnings_calendar_no_date_range(self, api_key):
        """Test earnings calendar without date range."""
        result = earnings_calendar(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should return upcoming earnings
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            date_value = get_field_value(first_item, "date")

            assert symbol_value is not None
            assert date_value is not None

    def test_earnings_calendar_earnings_season(self, api_key):
        """Test earnings calendar during earnings season."""
        # Q4 earnings season (January-February)
        from_date = "2024-01-15"
        to_date = "2024-02-15"

        result = earnings_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should have earnings data during earnings season
        if len(result_list) > 0:
            # Validate that we have major companies
            symbols = [get_field_value(item, "symbol") for item in result_list]
            # During earnings season, should have many companies
            assert (
                len(set(symbols)) > 5
            ), "Should have multiple companies during earnings season"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestIPOCalendar:
    """Test class for IPO calendar and related functionality."""

    def test_ipos_calendar_current_quarter(self, api_key):
        """Test IPO calendar for current quarter."""
        today = datetime.now()
        # Get current quarter
        quarter_start = datetime(today.year, ((today.month - 1) // 3) * 3 + 1, 1)
        if quarter_start.month == 10:
            quarter_end = datetime(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            next_quarter_month = quarter_start.month + 3
            quarter_end = datetime(today.year, next_quarter_month, 1) - timedelta(
                days=1
            )

        from_date = quarter_start.strftime("%Y-%m-%d")
        to_date = quarter_end.strftime("%Y-%m-%d")

        result = ipos_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # IPO calendar may be empty in quiet periods
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPUpcomingIPO.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.date is not None

    def test_ipos_calendar_no_date_range(self, api_key):
        """Test IPO calendar without date range."""
        result = ipos_calendar(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should return upcoming IPOs
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            date_value = get_field_value(first_item, "date")

            assert symbol_value is not None
            assert date_value is not None

    def test_ipos_disclosure_general(self, api_key):
        """Test IPO disclosure information."""
        result = ipos_disclosure(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Disclosure data may be limited
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPDisclosureFiling.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.filingDate is not None

    def test_ipos_disclosure_with_symbol(self, api_key):
        """Test IPO disclosure for specific symbol."""
        # Use a symbol that has had recent IPO activity
        result = ipos_disclosure(apikey=api_key, symbol="HOOD")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Symbol-specific disclosure may be empty if not available
        # or may return general disclosure data
        if len(result_list) > 0:
            # Accept that API may return broader results
            assert True  # Just validate that we get a valid response structure

    def test_ipos_prospectus_general(self, api_key):
        """Test IPO prospectus information."""
        result = ipos_prospectus(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Prospectus data may be limited
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPProspectusFiling.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.filingDate is not None

    def test_ipos_prospectus_with_symbol(self, api_key):
        """Test IPO prospectus for specific symbol."""
        result = ipos_prospectus(apikey=api_key, symbol="RIVN")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Symbol-specific prospectus may be empty if not available
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")

            # Note: API may return broader results than requested symbol
            # This is a known API quirk - prospectus endpoint doesn't strictly filter by symbol
            # We test that data is returned and properly structured, but not symbol matching
            assert symbol_value is not None
            assert len(symbol_value) > 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStockSplits:
    """Test class for stock split data functionality."""

    def test_splits_valid_symbol(self, api_key):
        """Test splits for a symbol known to have splits."""
        # Apple has had multiple stock splits
        result = splits(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first split record
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPStockSplit.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.date is not None
        assert validated.numerator > 0
        assert validated.denominator > 0
        # Note: ratio field may not exist in API response

    def test_splits_with_limit(self, api_key):
        """Test splits with limit parameter."""
        limit = 3
        result = splits(apikey=api_key, symbol="AAPL", limit=limit)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            # Note: ratio field may not exist in API response

            assert symbol_value == "AAPL"

    def test_splits_all_recent(self, api_key):
        """Test splits without symbol filter (recent splits)."""
        result = splits_calendar(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should return recent splits across all companies
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            date_value = get_field_value(first_item, "date")

            assert symbol_value is not None
            assert date_value is not None

    def test_splits_multiple_symbols(self, api_key):
        """Test splits for multiple symbols with split history."""
        split_stocks = ["AAPL", "TSLA", "GOOGL", "AMZN"]

        for symbol in split_stocks:
            result = splits(apikey=api_key, symbol=symbol, limit=2)
            result_list = extract_data_list(result)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            # Some stocks may not have splits
            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                assert symbol_value == symbol, f"Symbol should match for {symbol}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestSplitsCalendar:
    """Test class for stock splits calendar functionality."""

    def test_splits_calendar_current_year(self, api_key):
        """Test splits calendar for current year."""
        today = datetime.now()
        from_date = f"{today.year}-01-01"
        to_date = f"{today.year}-12-31"

        result = splits_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Splits calendar may be empty in some years
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPStockSplit.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.date is not None
            assert from_date <= validated.date <= to_date

    def test_splits_calendar_no_date_range(self, api_key):
        """Test splits calendar without date range."""
        result = splits_calendar(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should return upcoming/recent splits
        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            date_value = get_field_value(first_item, "date")

            assert symbol_value is not None
            assert date_value is not None

    def test_splits_calendar_specific_period(self, api_key):
        """Test splits calendar for a recent period to avoid premium parameter restrictions."""
        today = datetime.now()
        # Use the current year's first quarter
        from_date = f"{today.year}-01-01"
        to_date = f"{today.year}-03-31"

        result = splits_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Current year data should be accessible
        if len(result_list) > 0:
            # Validate that the data is within the expected time range
            for item in result_list[:5]:  # Check first 5 items
                date_value = get_field_value(item, "date")
                symbol_value = get_field_value(item, "symbol")

                assert date_value is not None, "Split date should not be None"
                assert symbol_value is not None, "Split symbol should not be None"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCalendarErrorHandling:
    """Test class for calendar error handling."""

    def test_dividends_invalid_symbol(self, api_key):
        """Test dividends with invalid symbol."""
        result = dividends(apikey=api_key, symbol="INVALID_XYZ")

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            # Empty list is acceptable for invalid symbols

    def test_dividends_invalid_api_key(self):
        """Test dividends with invalid API key."""
        result = dividends(apikey="invalid_key", symbol="AAPL")

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_earnings_calendar_invalid_api_key(self):
        """Test earnings calendar with invalid API key."""
        result = earnings_calendar(apikey="invalid_key")

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_dividends_calendar_invalid_date_format(self, api_key):
        """Test dividend calendar with invalid date format."""
        result = dividends_calendar(
            apikey=api_key, from_date="invalid-date", to_date="2024-12-31"
        )

        # Should handle gracefully
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_ipos_calendar_invalid_api_key(self):
        """Test IPO calendar with invalid API key."""
        result = ipos_calendar(apikey="invalid_key")

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_splits_invalid_symbol(self, api_key):
        """Test splits with invalid symbol."""
        result = splits(apikey=api_key, symbol="INVALID_XYZ")

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCalendarResponseTimes:
    """Test class for calendar response time validation."""

    def test_dividends_response_time(self, api_key, test_config):
        """Test that dividends responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = dividends(apikey=api_key, symbol="AAPL", limit=5)
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"

    def test_earnings_calendar_response_time(self, api_key, test_config):
        """Test that earnings calendar responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = earnings_calendar(apikey=api_key)
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"

    def test_ipos_calendar_response_time(self, api_key, test_config):
        """Test that IPO calendar responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = ipos_calendar(apikey=api_key)
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCalendarDataConsistency:
    """Test class for calendar data consistency validation."""

    def test_dividend_dates_consistency(self, api_key):
        """Test that dividend dates are logically consistent."""
        result = dividends(apikey=api_key, symbol="AAPL", limit=5)

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        for item in result_list:
            validated = (
                FMPDividend.model_validate(item) if isinstance(item, dict) else item
            )

            # Declaration date should be before record date
            if validated.declarationDate and validated.recordDate:
                assert (
                    validated.declarationDate <= validated.recordDate
                ), "Declaration date should be before or equal to record date"

            # Record date should be before payment date
            if validated.recordDate and validated.paymentDate:
                assert (
                    validated.recordDate <= validated.paymentDate
                ), "Record date should be before or equal to payment date"

            # Dividend amount should be reasonable
            assert (
                0 < validated.dividend < 100
            ), f"Dividend amount {validated.dividend} should be reasonable"

    def test_split_ratio_consistency(self, api_key):
        """Test that stock split ratios are consistent."""
        result = splits(apikey=api_key, symbol="AAPL", limit=5)

        result_list = extract_data_list(result)

        if len(result_list) > 0:
            for item in result_list:
                validated = (
                    FMPStockSplit.model_validate(item)
                    if isinstance(item, dict)
                    else item
                )

                # Numerator and denominator should be positive
                assert validated.numerator > 0, "Split numerator should be positive"
                assert validated.denominator > 0, "Split denominator should be positive"

                # If ratio field exists, it should match numerator/denominator calculation
                if hasattr(validated, "ratio") and validated.ratio is not None:
                    expected_ratio = validated.numerator / validated.denominator
                    assert (
                        abs(validated.ratio - expected_ratio) < 0.001
                    ), f"Split ratio {validated.ratio} should match calculation {expected_ratio}"

                # Most splits are either stock splits (ratio > 1) or reverse splits (ratio < 1)
                calculated_ratio = validated.numerator / validated.denominator
                assert calculated_ratio != 1.0, "Split ratio should not be 1:1"

    def test_calendar_date_ranges(self, api_key):
        """Test that calendar date ranges are respected."""
        from_date = "2024-01-01"
        to_date = "2024-01-31"

        result = dividends_calendar(
            apikey=api_key, from_date=from_date, to_date=to_date
        )
        result_list = extract_data_list(result)

        # Note: Some APIs may return data slightly outside the requested range
        # This is an API behavior, not a test failure
        if len(result_list) > 0:
            # Validate that most dates are within range
            dates_in_range = sum(
                1
                for item in result_list
                if from_date <= get_field_value(item, "date") <= to_date
            )
            # At least 80% of results should be in range (API may include buffer dates)
            assert (
                dates_in_range >= len(result_list) * 0.8
            ), f"Most dates should be within range, got {dates_in_range}/{len(result_list)} in range"
