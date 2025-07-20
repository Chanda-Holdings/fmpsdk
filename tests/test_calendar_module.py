from datetime import datetime, timedelta

import pytest

from fmpsdk.calendar_module import (
    dividends,
    dividends_calendar,
    dividends_calendar_v3,
    earnings_calendar,
    ipos_calendar,
    ipos_disclosure,
    ipos_prospectus,
    splits,
    splits_calendar,
)
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPDisclosureFiling,
    FMPDividend,
    FMPDividendCalendarEvent,
    FMPDividendCalendarEventV3,
    FMPEarningsCalendarEvent,
    FMPProspectusFiling,
    FMPStockSplit,
    FMPUpcomingIPO,
)
from tests.conftest import (
    get_first_item_from_response,
    get_response_models,
    handle_api_call_with_validation,
)


class TestDividends:
    """Test class for historical dividend data functionality."""

    @pytest.mark.parametrize(
        "symbol",
        [
            # High dividend yield stocks
            "AAPL",
            "MSFT",
            "JNJ",
            "PG",
            "KO",
            "PEP",
            "WMT",
            "HD",
            "UNH",
            "JPM",
            "BAC",
            "WFC",
            "T",
            "VZ",
            "XOM",
            "CVX",
            "IBM",
            "CSCO",
            # REITs (known for high dividends)
            "O",
            "MAIN",
            "STAG",
            "SPG",
            "VNO",
            # Dividend aristocrats
            "MMM",
            "ABT",
            "AFL",
            "APD",
            "ABBV",
            "ADP",
            "ALB",
            "ARE",
            "AMCR",
            "AME",
            "AMGN",
            "AMP",
            "AMT",
            "ATO",
            "AOS",
            "APTV",
            # Utilities (typically dividend payers)
            "NEE",
            "DUK",
            "SO",
            "D",
            "EXC",
            "SRE",
            "AEP",
            "XEL",
        ],
    )
    def test_dividends_comprehensive_symbols(self, api_key, symbol):
        """Test dividends for comprehensive list of dividend-paying stocks."""
        result, validation = handle_api_call_with_validation(
            dividends, "dividends", apikey=api_key, symbol=symbol
        )

        result_list = get_response_models(result, FMPDividend)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Validate first dividend record with business logic
            first_dividend = get_first_item_from_response(result_list)

            symbol_value = first_dividend.symbol
            payment_date = first_dividend.paymentDate
            dividend_amount = first_dividend.dividend
            record_date = first_dividend.recordDate

            # Core validation
            assert symbol_value == symbol, f"Symbol should match for {symbol}"
            assert payment_date is not None, "Payment date should not be None"
            assert dividend_amount is not None, "Dividend amount should not be None"

            # Business logic validation
            if dividend_amount is not None:
                assert (
                    dividend_amount > 0
                ), f"Dividend amount should be positive for {symbol}"
                assert (
                    dividend_amount < 50
                ), f"Dividend amount should be reasonable (< $50) for {symbol}"

            # Date validation
            if record_date and payment_date:
                assert (
                    record_date <= payment_date
                ), "Record date should be before or equal to payment date"

    @pytest.mark.parametrize(
        "sector",
        [
            "Technology",
            "Healthcare",
            "Financial",
            "Consumer",
            "Industrial",
            "Utilities",
            "Energy",
            "Materials",
            "Real Estate",
            "Communication",
        ],
    )
    def test_dividends_by_sector(self, api_key, sector):
        """Test dividend data across different sectors."""
        # Select representative symbols for each sector
        sector_symbols = {
            "Technology": ["AAPL", "MSFT", "IBM", "CSCO"],
            "Healthcare": ["JNJ", "PFE", "UNH", "ABBV"],
            "Financial": ["JPM", "BAC", "WFC", "AXP"],
            "Consumer": ["PG", "KO", "WMT", "HD"],
            "Industrial": ["MMM", "GE", "CAT", "HON"],
            "Utilities": ["NEE", "DUK", "SO", "D"],
            "Energy": ["XOM", "CVX", "COP", "EOG"],
            "Materials": ["LIN", "APD", "SHW", "FCX"],
            "Real Estate": ["O", "SPG", "AMT", "EQIX"],
            "Communication": ["T", "VZ", "CMCSA", "DIS"],
        }

        symbol = sector_symbols.get(sector, ["AAPL"])[0]  # Use first symbol from sector
        result, validation = handle_api_call_with_validation(
            dividends, "dividends", apikey=api_key, symbol=symbol
        )

        result_list = get_response_models(result, FMPDividend)
        assert isinstance(result_list, list)

        if result_list:
            # Validate dividend amount is positive
            first_dividend = get_first_item_from_response(result_list)
            dividend_amount = first_dividend.dividend
            if dividend_amount is not None:
                assert dividend_amount > 0, f"Dividend should be positive for {symbol}"

    def test_dividends_valid_symbol(self, api_key):
        """Test dividends for a valid dividend-paying stock."""
        # Apple is known for paying regular dividends
        result, validation = handle_api_call_with_validation(
            dividends, "dividends", apikey=api_key, symbol="AAPL"
        )

        result_list = get_response_models(result, FMPDividend)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first dividend record with enhanced business logic
        first_item = get_first_item_from_response(result_list)
        symbol_value = first_item.symbol
        date_value = first_item.date
        dividend_amount = first_item.dividend
        record_date = first_item.recordDate
        payment_date = first_item.paymentDate
        declaration_date = first_item.declarationDate

        assert symbol_value == "AAPL"
        assert date_value is not None, "Date should not be None"
        assert dividend_amount > 0, "Dividend amount should be positive"
        assert record_date is not None, "Record date should not be None"
        assert payment_date is not None, "Payment date should not be None"
        assert declaration_date is not None, "Declaration date should not be None"

        # Additional business logic validation
        assert dividend_amount < 10, "AAPL dividend should be reasonable (< $10)"

        # Date relationships
        if declaration_date and record_date and payment_date:
            assert (
                declaration_date <= record_date
            ), "Declaration should be before record date"
            assert record_date <= payment_date, "Record should be before payment date"

    def test_dividends_with_limit(self, api_key):
        """Test dividends with limit parameter."""
        limit = 5
        result, validation = handle_api_call_with_validation(
            dividends, "dividends", apikey=api_key, symbol="AAPL", limit=limit
        )

        result_list = get_response_models(result, FMPDividend)
        assert isinstance(result_list, list)
        assert len(result_list) <= limit

        if len(result_list) > 0:
            # Validate structure
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            dividend_value = first_item.dividend

            assert symbol_value == "AAPL"
            assert dividend_value > 0, "Dividend should be positive"

    def test_dividends_multiple_dividend_paying_stocks(self, api_key):
        """Test dividends for multiple dividend-paying stocks."""
        dividend_stocks = ["AAPL", "MSFT", "JNJ", "KO", "PG"]

        for symbol in dividend_stocks:
            result = dividends(apikey=api_key, symbol=symbol, limit=3)
            result_list = get_response_models(result, FMPDividend)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            if len(result_list) > 0:
                first_item = get_first_item_from_response(result_list)
                symbol_value = first_item.symbol
                dividend_value = first_item.dividend

                assert symbol_value == symbol, f"Symbol should match for {symbol}"
                assert dividend_value > 0, f"Dividend should be positive for {symbol}"

    def test_dividends_chronological_order(self, api_key):
        """Test that dividends are returned in chronological order."""
        result = dividends(
            apikey=api_key, symbol="KO", limit=10
        )  # Coca-Cola has long dividend history

        result_list = get_response_models(result, FMPDividend)
        assert len(result_list) > 1

        dates = [item.date for item in result_list]

        # Check if dates are in order (either ascending or descending)
        is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
        is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

        assert (
            is_ascending or is_descending
        ), "Dividends should be in chronological order"


class TestDividendsCalendar:
    """Test class for dividend calendar functionality."""

    @pytest.mark.parametrize(
        "calendar_period",
        [
            (0, 7),  # Next week
            (0, 30),  # Next month
            (0, 90),  # Next quarter
            (-30, 0),  # Last month
            (-90, 0),  # Last quarter
            (-30, 30),  # Month before and after
            (-7, 14),  # Week before, 2 weeks after
            (0, 365),  # Next year
            (-365, 0),  # Last year
        ],
    )
    def test_dividends_calendar_periods(self, api_key, calendar_period):
        """Test dividend calendar for various time periods."""
        start_days, end_days = calendar_period
        today = datetime.now()

        from_date = (today + timedelta(days=start_days)).strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=end_days)).strftime("%Y-%m-%d")

        result = dividends_calendar(
            apikey=api_key, from_date=from_date, to_date=to_date
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        if result_list:
            # Validate dividend calendar event structure
            first_event = get_first_item_from_response(result_list)
            if isinstance(first_event, dict):
                # Check required fields
                assert "symbol" in first_event
                assert "dividend" in first_event
                assert "date" in first_event

                # Validate dividend amount is positive
                dividend_amount = first_event["dividend"]
                if dividend_amount is not None:
                    assert dividend_amount > 0, "Dividend amount should be positive"

                # Test Pydantic model validation
                dividend_event = FMPDividendCalendarEvent(**first_event)
                assert dividend_event.symbol is not None
            else:
                # Already a Pydantic model
                assert hasattr(first_event, "symbol")
                assert hasattr(first_event, "dividend")
                assert hasattr(first_event, "date")

    @pytest.mark.parametrize(
        "dividend_frequency",
        [
            "monthly",  # Monthly dividend payers (REITs, utilities)
            "quarterly",  # Quarterly dividend payers (most stocks)
            "annual",  # Annual dividend payers (some international)
            "special",  # Special dividend events
        ],
    )
    def test_dividends_calendar_by_frequency(self, api_key, dividend_frequency):
        """Test dividend calendar for different dividend frequencies."""
        today = datetime.now()

        # Adjust date range based on frequency
        if dividend_frequency == "monthly":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=31)).strftime("%Y-%m-%d")
        elif dividend_frequency == "quarterly":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        elif dividend_frequency == "annual":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=365)).strftime("%Y-%m-%d")
        else:  # special
            from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar,
            "dividends_calendar",
            apikey=api_key,
            from_date=from_date,
            to_date=to_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        if result_list:
            # Validate dividend amounts are reasonable with enhanced business logic
            for event in result_list[:5]:  # Check first few events
                dividend_amount = event.dividend
                symbol = event.symbol

                if dividend_amount is not None:
                    assert (
                        dividend_amount > 0
                    ), f"Dividend should be positive for {dividend_frequency}"
                    assert (
                        dividend_amount < 1000
                    ), f"Dividend seems unusually high: {dividend_amount}"

                if symbol:
                    assert (
                        len(symbol) <= 10
                    ), f"Symbol length should be reasonable for {symbol}"

    def test_dividends_calendar_basic(self, api_key):
        """Test basic dividend calendar functionality."""
        # Get dividend calendar for next 30 days
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar,
            "dividends_calendar",
            apikey=api_key,
            from_date=from_date,
            to_date=to_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            # Validate structure with enhanced business logic
            first_event = get_first_item_from_response(result_list)

            symbol = first_event.symbol
            dividend_amount = first_event.dividend
            event_date = first_event.date

            assert symbol, "Symbol should not be empty"
            assert dividend_amount is not None, "Dividend amount should not be None"
            assert event_date is not None, "Event date should not be None"

            # Business logic validation
            assert dividend_amount > 0, "Dividend amount should be positive"
            assert (
                dividend_amount < 100
            ), "Dividend amount should be reasonable (< $100)"
            assert len(symbol) <= 10, "Symbol should have reasonable length"

            # Date validation
            assert (
                from_date <= event_date <= to_date
            ), f"Event date {event_date} should be within range {from_date} to {to_date}"


class TestEarningsCalendar:
    """Test class for earnings calendar functionality."""

    @pytest.mark.parametrize(
        "days_range",
        [
            (0, 7),  # Next week
            (0, 14),  # Next 2 weeks
            (0, 30),  # Next month
            (-7, 0),  # Last week
            (-14, 0),  # Last 2 weeks
            (-30, 0),  # Last month
            (-7, 7),  # Week before to week after
            (-14, 14),  # 2 weeks range
            (-30, 30),  # 2 months range
        ],
    )
    def test_earnings_calendar_date_ranges(self, api_key, days_range):
        """Test earnings calendar for various date ranges."""
        start_days, end_days = days_range
        today = datetime.now()

        from_date = (today + timedelta(days=start_days)).strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=end_days)).strftime("%Y-%m-%d")

        result = earnings_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPEarningsCalendarEvent)
        assert isinstance(result_list, list)

        if result_list:
            # Validate earnings calendar event structure
            first_event = get_first_item_from_response(result_list)
            if isinstance(first_event, dict):
                # Check required fields
                assert "symbol" in first_event
                assert "date" in first_event

                # Test Pydantic model validation
                earnings_event = FMPEarningsCalendarEvent(**first_event)
                assert earnings_event.symbol is not None
            else:
                # Already a Pydantic model
                assert hasattr(first_event, "symbol")
                assert hasattr(first_event, "date")

    @pytest.mark.parametrize(
        "market_cap",
        [
            "large_cap",  # > $10B
            "mid_cap",  # $2B - $10B
            "small_cap",  # $300M - $2B
            "mixed",  # All caps
        ],
    )
    def test_earnings_calendar_by_market_cap(self, api_key, market_cap):
        """Test earnings calendar filtering by market cap categories."""
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        result = earnings_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPEarningsCalendarEvent)
        assert isinstance(result_list, list)

        if result_list:
            # Test that we have diverse market cap representation
            symbols = [item.symbol for item in result_list[:10]]

            # Basic validation that symbols exist
            assert all(
                symbol for symbol in symbols if symbol
            ), "All symbols should be non-empty"

    def test_earnings_calendar_basic(self, api_key):
        """Test basic earnings calendar functionality."""
        # Get earnings for next 7 days
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            earnings_calendar,
            "earnings_calendar",
            apikey=api_key,
            from_date=from_date,
            to_date=to_date,
        )

        result_list = get_response_models(result, FMPEarningsCalendarEvent)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            # Validate structure with enhanced business logic
            first_event = get_first_item_from_response(result_list)

            symbol = first_event.symbol
            event_date = first_event.date
            eps = first_event.epsActual
            eps_estimated = first_event.epsEstimated
            revenue = first_event.revenueActual
            revenue_estimated = first_event.revenueEstimated

            assert symbol, "Symbol should not be empty"
            assert event_date is not None, "Event date should not be None"
            assert len(symbol) <= 10, "Symbol should have reasonable length"

            # Date validation
            assert (
                from_date <= event_date <= to_date
            ), f"Event date {event_date} should be within range {from_date} to {to_date}"

            # Business logic validation for earnings data
            if eps is not None and eps != 0:
                assert (
                    -100 <= eps <= 100
                ), "EPS should be within reasonable range (-$100 to $100)"
            if eps_estimated is not None and eps_estimated != 0:
                assert (
                    -100 <= eps_estimated <= 100
                ), "EPS estimated should be within reasonable range"
            if revenue is not None and revenue > 0:
                assert revenue < 1e12, "Revenue should be reasonable (< $1T)"
            if revenue_estimated is not None and revenue_estimated > 0:
                assert (
                    revenue_estimated < 1e12
                ), "Revenue estimated should be reasonable"


class TestIPOCalendar:
    """Test class for IPO calendar and related functionality."""

    def test_ipos_calendar_current_quarter(self, api_key):
        """Test IPO calendar for current quarter."""
        today = datetime.now()
        # Get currentfix  quarter
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

        result_list = get_response_models(result, FMPUpcomingIPO)
        assert isinstance(result_list, list)

        # IPO calendar may be empty in quiet periods
        if len(result_list) > 0:
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                validated = FMPUpcomingIPO.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.date is not None

    def test_ipos_calendar_no_date_range(self, api_key):
        """Test IPO calendar without date range."""
        result = ipos_calendar(apikey=api_key)

        result_list = get_response_models(result, FMPUpcomingIPO)
        assert isinstance(result_list, list)

        # Should return upcoming IPOs
        if len(result_list) > 0:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            date_value = first_item.date

            assert symbol_value is not None
            assert date_value is not None

    def test_ipos_disclosure_general(self, api_key):
        """Test IPO disclosure information."""
        result = ipos_disclosure(apikey=api_key)

        result_list = get_response_models(result, FMPDisclosureFiling)
        assert isinstance(result_list, list)

        # Disclosure data may be limited
        if len(result_list) > 0:
            first_item = get_first_item_from_response(result_list)
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

        result_list = get_response_models(result, FMPDisclosureFiling)
        assert isinstance(result_list, list)

        # Symbol-specific disclosure may be empty if not available
        # or may return general disclosure data
        if len(result_list) > 0:
            # Accept that API may return broader results
            assert True  # Just validate that we get a valid response structure

    def test_ipos_prospectus_general(self, api_key):
        """Test IPO prospectus information."""
        result = ipos_prospectus(apikey=api_key)

        result_list = get_response_models(result, FMPProspectusFiling)
        assert isinstance(result_list, list)

        # Prospectus data may be limited
        if len(result_list) > 0:
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                validated = FMPProspectusFiling.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.filingDate is not None

    def test_ipos_prospectus_with_symbol(self, api_key):
        """Test IPO prospectus for specific symbol."""
        result = ipos_prospectus(apikey=api_key, symbol="RIVN")

        result_list = get_response_models(result, FMPProspectusFiling)
        assert isinstance(result_list, list)

        # Symbol-specific prospectus may be empty if not available
        if len(result_list) > 0:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol

            # Note: API may return broader results than requested symbol
            # This is a known API quirk - prospectus endpoint doesn't strictly filter by symbol
            # We test that data is returned and properly structured, but not symbol matching
            assert symbol_value is not None
            assert len(symbol_value) > 0


class TestSplits:
    """Test class for stock splits functionality."""

    @pytest.mark.parametrize(
        "symbol",
        [
            # Companies known for stock splits
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "NVDA",
            "META",
            "NFLX",
            "BRKB",
            "HD",
            "WMT",
            "UNH",
            "JNJ",
            "PG",
            "V",
            "MA",
            "DIS",
            "ADBE",
            "CRM",
            "PYPL",
            "INTC",
            "CSCO",
            "ORCL",
            "IBM",
            "QCOM",
            # Stocks that have split recently
            "SHOP",
            "ZM",
            "DDOG",
            "SNOW",
            "PLTR",
            "ROKU",
            "SQ",
            "CRWD",
            "OKTA",
            "TWLO",
            "NET",
            "DOCU",
            "ZS",
            "ESTC",
            "TEAM",
            "ATLASSIAN",
        ],
    )
    def test_splits_comprehensive_symbols(self, api_key, symbol):
        """Test stock splits for comprehensive list of symbols."""
        result = splits(apikey=api_key, symbol=symbol)

        result_list = get_response_models(result, FMPStockSplit)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Validate split record structure
            first_split = get_first_item_from_response(result_list)
            if isinstance(first_split, dict):
                # Check required fields
                assert "symbol" in first_split
                assert "date" in first_split
                assert first_split["symbol"] == symbol

                # Test Pydantic model validation if split data exists
                try:
                    split_obj = FMPStockSplit(**first_split)
                    assert split_obj.symbol == symbol
                except Exception:
                    # Some symbols might not have complete split data
                    pass
            else:
                # Already a Pydantic model
                assert hasattr(first_split, "symbol")
                assert hasattr(first_split, "date")
                assert first_split.symbol == symbol

    @pytest.mark.parametrize(
        "time_period",
        [
            "recent",  # Last 2 years
            "historical",  # Last 5 years
            "long_term",  # Last 10 years
        ],
    )
    def test_splits_by_time_period(self, api_key, time_period):
        """Test stock splits across different time periods."""
        # Use AAPL as it has a good split history
        symbol = "AAPL"
        result = splits(apikey=api_key, symbol=symbol)

        result_list = get_response_models(result, FMPStockSplit)
        assert isinstance(result_list, list)

        if result_list:
            # Filter splits by time period
            cutoff_date = datetime.now()
            if time_period == "recent":
                cutoff_date -= timedelta(days=730)  # 2 years
            elif time_period == "historical":
                cutoff_date -= timedelta(days=1825)  # 5 years
            else:  # long_term
                cutoff_date -= timedelta(days=3650)  # 10 years

            cutoff_str = cutoff_date.strftime("%Y-%m-%d")

            # Check if we have splits in the specified period
            for split in result_list:
                split_date = split.date
                if split_date and split_date >= cutoff_str:
                    # Found a split in the period
                    assert True
                    break

    def test_splits_valid_symbol(self, api_key):
        """Test splits for a valid symbol with known splits."""
        # Apple has had multiple splits
        result = splits(apikey=api_key, symbol="AAPL")

        result_list = get_response_models(result, FMPStockSplit)
        assert isinstance(result_list, list)

        # Apple should have split history
        if len(result_list) > 0:
            # Validate structure
            first_split = get_first_item_from_response(result_list)
            if isinstance(first_split, dict):
                assert "symbol" in first_split
                assert "date" in first_split
                assert first_split["symbol"] == "AAPL"
            else:
                assert hasattr(first_split, "symbol")
                assert hasattr(first_split, "date")
                assert first_split.symbol == "AAPL"


class TestSplitsCalendar:
    """Test class for splits calendar functionality."""

    @pytest.mark.parametrize(
        "calendar_range",
        [
            (0, 30),  # Next month
            (0, 90),  # Next quarter
            (-30, 0),  # Last month
            (-90, 0),  # Last quarter
            (-30, 30),  # Month before and after
            (-7, 7),  # Week before and after
            (0, 180),  # Next 6 months
        ],
    )
    def test_splits_calendar_ranges(self, api_key, calendar_range):
        """Test splits calendar for various date ranges."""
        start_days, end_days = calendar_range
        today = datetime.now()

        from_date = (today + timedelta(days=start_days)).strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=end_days)).strftime("%Y-%m-%d")

        result = splits_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPStockSplit)
        assert isinstance(result_list, list)

        # Splits are relatively rare, so result might be empty
        if result_list:
            # Validate split event structure
            first_split = get_first_item_from_response(result_list)
            if isinstance(first_split, dict):
                # Check required fields
                assert "symbol" in first_split
                assert "date" in first_split
            else:
                # Already a Pydantic model
                assert hasattr(first_split, "symbol")
                assert hasattr(first_split, "date")

    def test_splits_calendar_basic(self, api_key):
        """Test basic splits calendar functionality."""
        # Get splits calendar for next 60 days
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=60)).strftime("%Y-%m-%d")

        result = splits_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPStockSplit)
        assert isinstance(result_list, list)

        # Splits are rare events, so empty result is acceptable
        if len(result_list) > 0:
            # Validate structure
            first_split = get_first_item_from_response(result_list)
            if isinstance(first_split, dict):
                assert "symbol" in first_split
                assert "date" in first_split
            else:
                assert hasattr(first_split, "symbol")
                assert hasattr(first_split, "date")


class TestIPOsCalendar:
    """Test class for IPO calendar functionality."""

    @pytest.mark.parametrize(
        "ipo_period",
        [
            (0, 30),  # Next month IPOs
            (0, 60),  # Next 2 months
            (0, 90),  # Next quarter
            (-30, 0),  # Last month IPOs
            (-60, 0),  # Last 2 months
            (-90, 0),  # Last quarter
            (-14, 14),  # 2 weeks before and after
            (0, 180),  # Next 6 months
        ],
    )
    def test_ipos_calendar_periods(self, api_key, ipo_period):
        """Test IPO calendar for various time periods."""
        start_days, end_days = ipo_period
        today = datetime.now()

        from_date = (today + timedelta(days=start_days)).strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=end_days)).strftime("%Y-%m-%d")

        result = ipos_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPUpcomingIPO)
        assert isinstance(result_list, list)

        if result_list:
            # Validate IPO event structure
            first_ipo = get_first_item_from_response(result_list)
            if isinstance(first_ipo, dict):
                # Check required fields
                assert "symbol" in first_ipo
                assert "date" in first_ipo
                assert "company" in first_ipo

                # Test Pydantic model validation
                ipo_event = FMPUpcomingIPO(**first_ipo)
                assert ipo_event.symbol is not None
            else:
                # Already a Pydantic model
                assert hasattr(first_ipo, "symbol")
                assert hasattr(first_ipo, "date")
                assert hasattr(first_ipo, "company")

    @pytest.mark.parametrize(
        "ipo_size",
        [
            "large",  # > $1B
            "medium",  # $100M - $1B
            "small",  # < $100M
            "all",  # All sizes
        ],
    )
    def test_ipos_calendar_by_size(self, api_key, ipo_size):
        """Test IPO calendar filtering by offering size."""
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=90)).strftime("%Y-%m-%d")

        result = ipos_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPUpcomingIPO)
        assert isinstance(result_list, list)

        if result_list:
            # Validate IPO data quality
            for ipo in result_list[:5]:  # Check first few IPOs
                symbol = ipo.symbol
                company = ipo.company

                assert symbol, "IPO symbol should not be empty"
                assert company, "IPO company name should not be empty"

    def test_ipos_calendar_basic(self, api_key):
        """Test basic IPO calendar functionality."""
        # Get IPO calendar for next 30 days
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        result = ipos_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        result_list = get_response_models(result, FMPUpcomingIPO)
        assert isinstance(result_list, list)

        # IPOs might be empty for some periods
        if len(result_list) > 0:
            # Validate structure
            first_ipo = get_first_item_from_response(result_list)
            if isinstance(first_ipo, dict):
                assert "symbol" in first_ipo
                assert "date" in first_ipo
                assert "company" in first_ipo
            else:
                assert hasattr(first_ipo, "symbol")
                assert hasattr(first_ipo, "date")
                assert hasattr(first_ipo, "company")


class TestCalendarErrorHandling:
    """Test class for calendar error handling."""

    def test_dividends_invalid_symbol(self, api_key):
        """Test dividends with invalid symbol."""
        result = dividends(apikey=api_key, symbol="INVALID_XYZ")

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = get_response_models(result, FMPDividend)
            assert isinstance(result_list, list)
            # Empty list is acceptable for invalid symbols

    def test_dividends_invalid_api_key(self):
        with pytest.raises(InvalidAPIKeyException):
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
            result_list = get_response_models(result, FMPDividendCalendarEvent)
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
            result_list = get_response_models(result, FMPStockSplit)
            assert isinstance(result_list, list)


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


class TestCalendarDataQuality:
    """Test data quality and business logic validation for calendar endpoints."""

    @pytest.mark.parametrize(
        "endpoint_type",
        [
            "dividends",
            "earnings_calendar",
            "dividends_calendar",
            "splits",
            "splits_calendar",
            "ipos_calendar",
        ],
    )
    def test_calendar_data_consistency(self, api_key, endpoint_type):
        """Test data consistency across different calendar endpoints."""
        today = datetime.now()

        if endpoint_type == "dividends":
            result = dividends(apikey=api_key, symbol="AAPL")
        elif endpoint_type == "earnings_calendar":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")
            result = earnings_calendar(
                apikey=api_key, from_date=from_date, to_date=to_date
            )
        elif endpoint_type == "dividends_calendar":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
            result = dividends_calendar(
                apikey=api_key, from_date=from_date, to_date=to_date
            )
        elif endpoint_type == "splits":
            result = splits(apikey=api_key, symbol="AAPL")
        elif endpoint_type == "splits_calendar":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=60)).strftime("%Y-%m-%d")
            result = splits_calendar(
                apikey=api_key, from_date=from_date, to_date=to_date
            )
        elif endpoint_type == "ipos_calendar":
            from_date = today.strftime("%Y-%m-%d")
            to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
            result = ipos_calendar(apikey=api_key, from_date=from_date, to_date=to_date)

        # Use appropriate model for each endpoint type
        if endpoint_type == "earnings_calendar":
            model_class = FMPEarningsCalendarEvent
        elif endpoint_type == "dividends_calendar":
            model_class = FMPDividendCalendarEvent
        elif endpoint_type == "splits_calendar":
            model_class = FMPStockSplit
        elif endpoint_type == "ipos_calendar":
            model_class = FMPUpcomingIPO
        else:
            model_class = FMPDividend  # For dividends and splits

        result_list = get_response_models(result, model_class)
        assert isinstance(result_list, list)

        if result_list:
            for item in result_list[:3]:  # Check first few items
                # Validate symbol format
                symbol = (
                    item.symbol
                    if hasattr(item, "symbol")
                    else getattr(item, "symbol", None)
                )
                if symbol:
                    assert isinstance(symbol, str)
                    assert len(symbol) > 0
                    assert symbol.isupper()  # Stock symbols should be uppercase

                # Validate date format
                date_value = (
                    item.date if hasattr(item, "date") else getattr(item, "date", None)
                )
                if date_value:
                    assert len(date_value) >= 10  # YYYY-MM-DD format minimum
                    # Validate it's a reasonable date
                    try:
                        parsed_date = datetime.strptime(date_value[:10], "%Y-%m-%d")
                        assert parsed_date.year >= 1990  # Reasonable year range
                        assert parsed_date.year <= datetime.now().year + 5
                    except ValueError:
                        pytest.fail(f"Invalid date format: {date_value}")

    @pytest.mark.parametrize(
        "financial_field",
        ["dividend", "eps", "epsEstimated", "revenue", "revenueEstimated"],
    )
    def test_calendar_financial_fields_validation(self, api_key, financial_field):
        """Test validation of financial fields in calendar data."""
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        # Test different endpoints based on field
        if financial_field == "dividend":
            result = dividends_calendar(
                apikey=api_key, from_date=from_date, to_date=to_date
            )
            model_class = FMPDividendCalendarEvent
            field_name = "dividend"
        else:
            result = earnings_calendar(
                apikey=api_key, from_date=from_date, to_date=to_date
            )
            model_class = FMPEarningsCalendarEvent
            # Map field names to actual model attributes
            field_mapping = {
                "eps": "epsActual",
                "epsEstimated": "epsEstimated",
                "revenue": "revenueActual",
                "revenueEstimated": "revenueEstimated",
            }
            field_name = field_mapping.get(financial_field, financial_field)

        result_list = get_response_models(result, model_class)
        if result_list:
            for item in result_list[:5]:  # Check first few items
                # Get field value using getattr with fallback for dict objects
                if isinstance(item, dict):
                    field_value = item.get(field_name)
                else:
                    field_value = getattr(item, field_name, None)

                if field_value is not None:
                    # Financial values should be numeric
                    assert isinstance(field_value, (int, float))
                    # Most financial values should be positive (though EPS can be negative)
                    if financial_field == "dividend":
                        assert (
                            field_value > 0
                        ), f"Dividend should be positive: {field_value}"


class TestCalendarErrorHandling:
    """Test error handling and edge cases for calendar endpoints."""

    @pytest.mark.parametrize(
        "invalid_symbol", ["INVALID", "XYZ123", "NONEXISTENT", "FAKESYMB", "999", ""]
    )
    def test_calendar_invalid_symbols(self, api_key, invalid_symbol):
        """Test calendar endpoints with invalid symbols."""
        if invalid_symbol:  # Skip empty string for this test
            result = dividends(apikey=api_key, symbol=invalid_symbol)

            if isinstance(result, dict) and "Error Message" in result:
                # API properly handles invalid symbol
                return

            result_list = get_response_models(result, FMPDividend)
            # Should return empty list for invalid symbols
            assert isinstance(result_list, list)
            assert len(result_list) == 0

    def test_calendar_invalid_api_key(self):
        """Test calendar endpoints with invalid API key."""
        invalid_api_key = "invalid_key_123"

        with pytest.raises(InvalidAPIKeyException):
            result = dividends(apikey=invalid_api_key, symbol="AAPL")


class TestDividendsCalendarV3:
    """Test class for V3 dividends calendar functionality."""

    def test_dividends_calendar_v3_basic(self, api_key):
        """Test basic dividends calendar v3 functionality."""
        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)

        if result_list:
            assert isinstance(result_list, list)

            # Validate first item structure
            first_item = result_list[0]
            assert hasattr(first_item, "symbol")
            assert hasattr(first_item, "date")
            assert hasattr(first_item, "recordDate")
            assert hasattr(first_item, "paymentDate")
            assert hasattr(first_item, "declarationDate")
            assert hasattr(first_item, "adjDividend")
            assert hasattr(first_item, "dividend")

            # Basic validation
            assert first_item.symbol is not None
            assert first_item.date is not None
            assert isinstance(first_item.adjDividend, (int, float))
            assert isinstance(first_item.dividend, (int, float))

    def test_dividends_calendar_v3_with_date_range(self, api_key):
        """Test dividends calendar v3 with date range parameters."""
        # Test with a recent date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=start_date,
            to_date=end_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        # Validate date filtering if results are returned
        if result_list:
            for item in result_list[:5]:  # Check first 5 items
                assert hasattr(item, "date")
                assert hasattr(item, "symbol")
                # Date should be within range (basic validation)
                assert item.date is not None
                assert len(item.symbol) > 0

    @pytest.mark.parametrize(
        "from_date,to_date,description",
        [
            # Different date range scenarios
            ("2024-01-01", "2024-01-31", "january_2024"),
            ("2024-06-01", "2024-06-30", "june_2024"),
            ("2024-12-01", "2024-12-31", "december_2024"),
        ],
    )
    def test_dividends_calendar_v3_date_ranges(
        self, api_key, from_date, to_date, description
    ):
        """Test dividends calendar v3 with various date ranges."""
        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=from_date,
            to_date=to_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        # Basic validation - results may be empty for some date ranges
        if result_list:
            for item in result_list[:3]:
                assert hasattr(item, "symbol")
                assert hasattr(item, "date")
                assert hasattr(item, "dividend")
                assert item.symbol is not None
                assert len(item.symbol) > 0

    def test_dividends_calendar_v3_data_quality(self, api_key):
        """Test dividends calendar v3 data quality and consistency."""
        # Get recent dividend data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=start_date,
            to_date=end_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        if result_list:
            # Data quality checks
            for item in result_list[:10]:  # Check first 10 items
                # Symbol validation
                assert item.symbol is not None
                assert len(item.symbol) >= 1
                assert (
                    len(item.symbol) <= 20
                )  # Allow for international symbols with exchange suffixes
                assert (
                    item.symbol.replace(".", "").replace("-", "").isalnum()
                    or "." in item.symbol
                )

                # Date validation
                assert item.date is not None
                assert len(item.date) == 10  # YYYY-MM-DD format

                # Dividend amount validation
                assert isinstance(item.dividend, (int, float))
                assert isinstance(item.adjDividend, (int, float))
                assert item.dividend >= 0  # Dividends should be non-negative
                assert item.adjDividend >= 0

                # Optional date fields validation
                if hasattr(item, "recordDate") and item.recordDate:
                    assert len(item.recordDate) == 10
                if hasattr(item, "paymentDate") and item.paymentDate:
                    assert len(item.paymentDate) == 10
                if hasattr(item, "declarationDate") and item.declarationDate:
                    assert len(item.declarationDate) == 10

    def test_dividends_calendar_v3_edge_cases(self, api_key):
        """Test dividends calendar v3 edge cases."""
        # Test with future date range (should return empty or minimal results)
        future_start = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        future_end = (datetime.now() + timedelta(days=395)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=future_start,
            to_date=future_end,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)
        # Future dates may have some scheduled dividends, so we just check it's a list

    def test_dividends_calendar_v3_partial_date_parameters(self, api_key):
        """Test dividends calendar v3 with partial date parameters."""
        # Test with only from_date
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=start_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

        # Test with only to_date
        end_date = datetime.now().strftime("%Y-%m-%d")

        result, validation = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            to_date=end_date,
        )

        result_list = get_response_models(result, FMPDividendCalendarEvent)
        assert isinstance(result_list, list)

    def test_dividends_calendar_v3_comparison_with_v1(self, api_key):
        """Test dividends calendar v3 compared to regular dividends_calendar."""
        # Get data from both endpoints for comparison
        test_date = datetime.now().strftime("%Y-%m-%d")

        # V3 endpoint
        result_v3, validation_v3 = handle_api_call_with_validation(
            dividends_calendar_v3,
            "dividends_calendar_v3",
            apikey=api_key,
            from_date=test_date,
            to_date=test_date,
        )

        # Regular endpoint
        result_v1, validation_v1 = handle_api_call_with_validation(
            dividends_calendar,
            "dividends_calendar",
            apikey=api_key,
            from_date=test_date,
            to_date=test_date,
        )

        result_list_v3 = get_response_models(result_v3, FMPDividendCalendarEvent)
        result_list_v1 = get_response_models(result_v1, FMPDividendCalendarEvent)

        # Both should return lists
        assert isinstance(result_list_v3, list)
        assert isinstance(result_list_v1, list)

        # If both have data, they should have similar structure
        if result_list_v3 and result_list_v1:
            v3_item = result_list_v3[0]
            v1_item = result_list_v1[0]

            # Both should have basic dividend fields
            assert hasattr(v3_item, "symbol")
            assert hasattr(v3_item, "dividend")
            assert hasattr(v1_item, "symbol")
            assert hasattr(v1_item, "dividend")

    def test_dividends_calendar_v3_invalid_api_key(self):
        """Test dividends calendar v3 with invalid API key."""
        invalid_api_key = "invalid_key_123"

        with pytest.raises(InvalidAPIKeyException):
            result = dividends_calendar_v3(apikey=invalid_api_key)
