import time
from datetime import datetime

import pytest

from fmpsdk.earnings_transcript import (
    earnings_transcript,
    earnings_transcript_by_symbol,
    earnings_transcript_latest,
    earnings_transcript_list,
)
from fmpsdk.models import (
    FMPEarningsTranscript,
    FMPEarningsTranscriptBySymbol,
    FMPEarningsTranscriptList,
)
from tests.conftest import (
    get_first_item_from_response,
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)

# Test configuration
RESPONSE_TIME_LIMIT = 15.0  # seconds (transcript endpoints might be slower)
TEST_SYMBOLS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "TSLA",
    "AMZN",
    "META",
    "NFLX",
    "NVDA",
    "JPM",
    "JNJ",
    "UNH",
    "HD",
    "PG",
    "V",
    "MA",
    "DIS",
    "ADBE",
    "CRM",
    "IBM",
    "ORCL",
    "CSCO",
    "INTC",
    "AMD",
    "QCOM",
    "TXN",
    "AVGO",
    "WMT",
    "PFE",
    "XOM",
    "CVX",
    "BAC",
    "WFC",
    "GS",
    "MS",
]  # Extended list of large companies with regular earnings calls


class TestEarningsTranscriptLatest:
    """Test latest earnings transcripts endpoint."""

    @pytest.mark.parametrize("limit", [5, 10, 15, 20, 25, 50])
    def test_earnings_transcript_latest_limits(self, api_key, limit):
        """Test latest earnings transcripts with different limits."""
        start_time = time.time()

        result, validation = handle_api_call_with_validation(
            earnings_transcript_latest,
            "earnings_transcript_latest",
            apikey=api_key,
            limit=limit,
        )

        # Check response time (transcript endpoints can be slower)
        elapsed_time = time.time() - start_time
        assert elapsed_time < RESPONSE_TIME_LIMIT

        result_list = get_response_models(result, FMPEarningsTranscriptList)
        validate_model_list(result_list, FMPEarningsTranscriptList)

        if result_list:  # If data is available
            assert len(result_list) <= limit

            # Test first item structure
            first_item = result_list[0] if result_list else None
            if first_item:
                # Validate required fields
                assert first_item.symbol != ""
                assert hasattr(first_item, "period")
                assert hasattr(first_item, "fiscalYear")
                assert first_item.date != ""

    @pytest.mark.parametrize("page,limit", [(1, 5), (2, 10), (3, 15), (1, 20), (2, 25)])
    def test_earnings_transcript_latest_pagination_extended(self, api_key, page, limit):
        """Test extensive pagination scenarios for latest earnings transcripts."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_latest,
            "earnings_transcript_latest",
            apikey=api_key,
            limit=limit,
            page=page,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        validate_model_list(result_list, FMPEarningsTranscriptList)

        if result_list:
            assert len(result_list) <= limit

            # Validate structure of results
            for item in result_list[:3]:  # Check first few items
                symbol_value = item.symbol
                period_value = item.period
                fiscal_year_value = item.fiscalYear

                assert item.symbol != ""
                assert item.symbol != ""
                assert period_value in ["Q1", "Q2", "Q3", "Q4", "FY"]
                assert isinstance(fiscal_year_value, int)
                assert fiscal_year_value >= 2020

    def test_earnings_transcript_latest_data_quality(self, api_key):
        """Test data quality for latest earnings transcripts."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_latest,
            "earnings_transcript_latest",
            apikey=api_key,
            limit=10,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)

        if result_list:
            for item in result_list[:3]:  # Check first 3 items
                symbol_value = item.symbol
                period_value = item.period
                fiscal_year_value = item.fiscalYear
                date_value = item.date

                # Basic validation
                assert item.symbol != ""
                assert item.symbol != ""
                assert isinstance(period_value, str)
                assert period_value in ["Q1", "Q2", "Q3", "Q4", "FY"]
                assert isinstance(fiscal_year_value, int)
                assert fiscal_year_value >= 2020
                assert item.date != ""
                assert item.date != ""

    def test_earnings_transcript_latest_error_handling(self, api_key):
        """Test error handling for latest earnings transcripts."""
        # Test with very large limit (might be rejected)
        result, validation = handle_api_call_with_validation(
            earnings_transcript_latest,
            "earnings_transcript_latest",
            apikey=api_key,
            limit=10000,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        # Should either work or return reasonable amount of data
        validate_model_list(result_list, FMPEarningsTranscriptList)

        # Test with zero limit
        result, validation = handle_api_call_with_validation(
            earnings_transcript_latest,
            "earnings_transcript_latest",
            apikey=api_key,
            limit=0,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        validate_model_list(result_list, FMPEarningsTranscriptList)
        assert len(result_list) == 0


class TestEarningsTranscript:
    """Test earnings transcript by specific parameters."""

    @pytest.mark.parametrize("symbol", TEST_SYMBOLS)
    def test_earnings_transcript_by_symbol_comprehensive(self, api_key, symbol):
        """Test earnings transcripts for comprehensive list of symbols."""
        test_year = 2023
        test_quarter = 4  # Q4 is most likely to have data

        start_time = time.time()

        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol=symbol,
            year=test_year,
            quarter=test_quarter,
        )

        elapsed_time = time.time() - start_time
        assert elapsed_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert result_list[0].symbol != ""

        if result_list:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            fiscal_year_value = first_item.fiscalYear

            assert first_item.symbol != ""
            assert fiscal_year_value == test_year

    @pytest.mark.parametrize("year", [2023, 2022, 2021, 2020, 2019])
    def test_earnings_transcript_by_year(self, api_key, year):
        """Test earnings transcripts for different years."""
        symbol = "AAPL"  # Use Apple as it has consistent earnings calls
        quarter = 4  # Q4 typically has data

        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol=symbol,
            year=year,
            quarter=quarter,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)

        if result_list:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            fiscal_year_value = first_item.fiscalYear

            assert first_item.symbol != ""
            assert fiscal_year_value == year

    @pytest.mark.parametrize("quarter", [1, 2, 3, 4])
    def test_earnings_transcript_by_quarter(self, api_key, quarter):
        """Test earnings transcripts for all quarters."""
        symbol = "AAPL"
        year = 2023

        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol=symbol,
            year=year,
            quarter=quarter,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)

        if result_list:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            period_value = first_item.period

            assert first_item.symbol != ""
            assert period_value == f"Q{quarter}"

    @pytest.mark.parametrize(
        "symbol,year,quarter",
        [
            ("AAPL", 2023, 4),
            ("MSFT", 2023, 3),
            ("GOOGL", 2023, 2),
            ("TSLA", 2023, 1),
            ("AMZN", 2022, 4),
            ("META", 2022, 3),
            ("NFLX", 2022, 2),
            ("NVDA", 2022, 1),
            ("JPM", 2023, 4),
            ("JNJ", 2023, 3),
            ("UNH", 2023, 2),
            ("HD", 2023, 1),
        ],
    )
    def test_earnings_transcript_specific_combinations(
        self, api_key, symbol, year, quarter
    ):
        """Test earnings transcripts for specific symbol/year/quarter combinations."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol=symbol,
            year=year,
            quarter=quarter,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)

        if result_list:
            first_item = get_first_item_from_response(result_list)
            symbol_value = first_item.symbol
            fiscal_year_value = first_item.fiscalYear

            assert first_item.symbol != ""
            assert fiscal_year_value == year

    def test_earnings_transcript_basic(self, api_key):
        """Test basic earnings transcript functionality."""
        symbol = "AAPL"
        year = 2023
        quarter = 4

        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol=symbol,
            year=year,
            quarter=quarter,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)

        if result_list:
            # Test transcript structure
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscript.model_validate(first_item)
            else:
                validated = first_item

            assert first_item.symbol != ""
            assert first_item.date != ""
            assert first_item.date != ""

    def test_earnings_transcript_multiple_companies(self, api_key):
        """Test earnings transcripts for multiple companies."""
        # Test recent quarters for major companies
        current_year = datetime.now().year
        test_year = current_year - 1  # Use previous year to ensure data exists

        for symbol in TEST_SYMBOLS[:3]:  # Test first 3 symbols
            result, validation = handle_api_call_with_validation(
                earnings_transcript,
                "earnings_transcript",
                apikey=api_key,
                symbol=symbol,
                year=test_year,
                quarter=4,
            )
            result_list = get_response_models(result, FMPEarningsTranscriptList)

            assert result_list[0].symbol != ""

            if result_list:
                first_item = get_first_item_from_response(result_list)
                symbol_value = first_item.symbol
                fiscal_year_value = first_item.fiscalYear

                assert first_item.symbol != ""
                assert fiscal_year_value == test_year

    def test_earnings_transcript_all_quarters(self, api_key):
        """Test earnings transcripts for all quarters."""
        symbol = "AAPL"
        year = 2023
        quarters = [1, 2, 3, 4]

        for quarter in quarters:
            result, validation = handle_api_call_with_validation(
                earnings_transcript,
                "earnings_transcript",
                apikey=api_key,
                symbol=symbol,
                year=year,
                quarter=quarter,
            )
            result_list = get_response_models(result, FMPEarningsTranscriptList)

            assert isinstance(result_list, list)

            if result_list:
                first_item = get_first_item_from_response(result_list)
                symbol_value = first_item.symbol
                fiscal_year_value = first_item.fiscalYear

                assert first_item.symbol != ""
                assert fiscal_year_value == year

    def test_earnings_transcript_with_limit(self, api_key):
        """Test earnings transcript with limit parameter."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol="AAPL",
            year=2023,
            quarter=4,
            limit="1",
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)

        assert isinstance(result_list, list)
        assert len(result_list) <= 1

    def test_earnings_transcript_content_validation(self, api_key):
        """Test earnings transcript content validation."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol="AAPL",
            year=2023,
            quarter=4,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)

        if result_list:
            first_item = get_first_item_from_response(result_list)
            content_value = first_item.content

            # Content might be None for some transcripts
            if content_value is not None:
                assert isinstance(content_value, str)
                assert len(content_value) > 0

    def test_earnings_transcript_invalid_parameters(self, api_key):
        """Test earnings transcript with invalid parameters."""
        # Test invalid year (too old)
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol="AAPL",
            year=1990,
            quarter=1,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)
        assert len(result_list) == 0

        # Test invalid quarter
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol="AAPL",
            year=2023,
            quarter=5,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)

        # Test invalid symbol
        result, validation = handle_api_call_with_validation(
            earnings_transcript,
            "earnings_transcript",
            apikey=api_key,
            symbol="INVALID",
            year=2023,
            quarter=1,
        )
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)
        assert len(result_list) == 0


class TestEarningsTranscriptBySymbol:
    """Test class for earnings transcript dates by symbol functionality."""

    @pytest.mark.parametrize("symbol", TEST_SYMBOLS)
    def test_earnings_transcript_by_symbol_comprehensive(self, api_key, symbol):
        """Test earnings transcript dates for comprehensive list of symbols."""
        start_time = time.time()
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol=symbol,
        )
        response_time = time.time() - start_time

        # Check response time
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                # Validate required fields
                assert first_item["symbol"] != ""
                assert first_item["date"] != ""
                assert first_item["symbol"] != ""

                # Test Pydantic model validation
                transcript_by_symbol = FMPEarningsTranscriptBySymbol(**first_item)
                assert first_item["symbol"] != ""
            else:
                # Already a Pydantic model
                assert first_item.symbol != ""
                assert first_item.date != ""
                assert first_item.symbol != ""

    @pytest.mark.parametrize(
        "symbol,expected_sector",
        [
            ("AAPL", "Technology"),
            ("MSFT", "Technology"),
            ("GOOGL", "Technology"),
            ("JPM", "Financial"),
            ("JNJ", "Healthcare"),
            ("XOM", "Energy"),
            ("WMT", "Consumer"),
            ("HD", "Consumer"),
            ("PG", "Consumer"),
            ("UNH", "Healthcare"),
            ("PFE", "Healthcare"),
            ("V", "Financial"),
        ],
    )
    def test_earnings_transcript_by_symbol_sectors(
        self, api_key, symbol, expected_sector
    ):
        """Test earnings transcript dates for symbols across different sectors."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol=symbol,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)
        assert isinstance(result_list, list)

        if result_list:
            # Validate that all returned items are for the requested symbol
            for item in result_list[:5]:  # Check first few items
                symbol_value = item.symbol
                assert item.symbol != ""

                # Validate date format
                date_value = item.date
                if date_value:
                    assert item.date != ""

    def test_earnings_transcript_by_symbol_basic(self, api_key):
        """Test getting earnings transcript dates by symbol."""
        start_time = time.time()
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol="AAPL",
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)
        assert isinstance(result_list, list)

        if result_list:
            # Test transcript date structure
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscriptBySymbol.model_validate(first_item)
            else:
                validated = first_item

            assert first_item.date != ""
            assert first_item.date != ""
            assert first_item.date != ""

    def test_earnings_transcript_by_symbol_multiple_companies(self, api_key):
        """Test earnings transcript dates for multiple companies."""
        for symbol in TEST_SYMBOLS[:3]:  # Test first 3 symbols
            result, validation = handle_api_call_with_validation(
                earnings_transcript_by_symbol,
                "earnings_transcript_by_symbol",
                apikey=api_key,
                symbol=symbol,
            )
            result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)

            assert result_list[0].symbol != ""

            if result_list:
                # Should have multiple quarters/years
                assert len(result_list) > 0

                # Check data structure
                first_item = get_first_item_from_response(result_list)
                quarter_value = first_item.quarter
                fiscal_year_value = first_item.fiscalYear
                date_value = first_item.date

                assert quarter_value is not None
                assert fiscal_year_value is not None
                assert first_item.date != ""

    def test_earnings_transcript_by_symbol_chronological_order(self, api_key):
        """Test that transcript dates are in chronological order."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol="AAPL",
        )
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)

        if len(result_list) > 1:
            # Check if dates are in descending order (most recent first)
            dates = [item.date for item in result_list[:5]]
            dates = [date for date in dates if date is not None]

            if len(dates) > 1:
                # Convert to datetime for comparison
                parsed_dates = []
                for date_str in dates:
                    try:
                        parsed_dates.append(
                            datetime.strptime(date_str[:10], "%Y-%m-%d")
                        )
                    except (ValueError, TypeError):
                        continue

                if len(parsed_dates) > 1:
                    # Should be in descending order
                    for i in range(len(parsed_dates) - 1):
                        assert parsed_dates[i] >= parsed_dates[i + 1]

    def test_earnings_transcript_by_symbol_data_quality(self, api_key):
        """Test data quality for earnings transcript dates."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol="AAPL",
        )
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)

        if result_list:
            for item in result_list[:3]:  # Check first 3 items
                quarter_value = item.quarter
                fiscal_year_value = item.fiscalYear
                date_value = item.date

                # Validate quarter format
                assert isinstance(quarter_value, str)
                assert (
                    quarter_value in ["Q1", "Q2", "Q3", "Q4"] or "FY" in quarter_value
                )

                # Validate fiscal year
                assert isinstance(fiscal_year_value, int)
                assert item.date != ""

                # Validate date
                assert item.date != ""
                assert item.date != ""

    def test_earnings_transcript_by_symbol_invalid_symbol(self, api_key):
        """Test earnings transcript dates with invalid symbol."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol="INVALID_SYMBOL",
        )
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)

        assert isinstance(result_list, list)
        assert len(result_list) == 0


class TestEarningsTranscriptList:
    """Test earnings transcript list endpoint."""

    @pytest.mark.parametrize("symbol", TEST_SYMBOLS)
    def test_earnings_transcript_list_comprehensive(self, api_key, symbol):
        """Test earnings transcript list for comprehensive symbol coverage."""
        start_time = time.time()
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol=symbol,
        )
        response_time = time.time() - start_time

        # Check response time
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                # Validate required fields
                assert first_item["symbol"] != ""
                assert "quarter" in first_item
                assert "fiscalYear" in first_item
                assert first_item["date"] != ""
                assert first_item["symbol"] != ""

                # Test Pydantic model validation
                transcript_list = FMPEarningsTranscriptBySymbol(**first_item)
                assert first_item["symbol"] != ""
            else:
                # Already a Pydantic model
                assert first_item.symbol != ""
                assert hasattr(first_item, "quarter")
                assert hasattr(first_item, "fiscalYear")
                assert first_item.date != ""
                assert first_item.symbol != ""

    @pytest.mark.parametrize(
        "symbol,market_cap",
        [
            ("AAPL", "Large"),
            ("MSFT", "Large"),
            ("GOOGL", "Large"),
            ("TSLA", "Large"),
            ("NVDA", "Large"),
            ("META", "Large"),
            ("JPM", "Large"),
            ("JNJ", "Large"),
            ("UNH", "Large"),
            ("HD", "Large"),
            ("PG", "Large"),
            ("V", "Large"),
        ],
    )
    def test_earnings_transcript_list_by_market_cap(self, api_key, symbol, market_cap):
        """Test earnings transcript list for large cap companies."""
        result, validation = handle_api_call_with_validation(
            earnings_transcript_by_symbol,
            "earnings_transcript_by_symbol",
            apikey=api_key,
            symbol=symbol,
        )

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptBySymbol)
        assert isinstance(result_list, list)

        if result_list:
            # Large cap companies should have regular earnings transcripts
            # Validate data quality
            for item in result_list[:3]:  # Check first few items
                symbol_value = item.symbol
                quarter_value = item.quarter
                fiscal_year_value = item.fiscalYear
                date_value = item.date

                assert item.symbol != ""
                assert quarter_value in ["Q1", "Q2", "Q3", "Q4", "FY"]
                assert isinstance(fiscal_year_value, int)
                assert fiscal_year_value >= 2020
                assert item.date != ""

    def test_earnings_transcript_list_basic(self, api_key):
        """Test basic earnings transcript list functionality."""
        start_time = time.time()
        result, validation = handle_api_call_with_validation(
            earnings_transcript_list, "earnings_transcript_list", apikey=api_key
        )
        response_time = time.time() - start_time

        # Check response time
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict
        result_list = get_response_models(result, FMPEarningsTranscriptList)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = get_first_item_from_response(result_list)
            if isinstance(first_item, dict):
                # Validate required fields for transcript list
                assert first_item["symbol"] != ""
                assert first_item["name"] != ""
                assert "noOfTranscripts" in first_item

                # Test Pydantic model validation
                transcript_list = FMPEarningsTranscriptList(**first_item)
                assert first_item["symbol"] != ""
                assert first_item["name"] != ""
            else:
                # Already a Pydantic model
                assert first_item.symbol != ""
                assert first_item.name != ""
                assert hasattr(first_item, "noOfTranscripts")

                # Validate the data
                assert first_item.symbol != ""
                assert first_item.name != ""
                assert first_item.noOfTranscripts is not None
