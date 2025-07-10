"""
Integration tests for earnings transcript endpoints.

This module tests all earnings transcript-related API endpoints,
including latest transcripts, specific transcripts by symbol/quarter/year,
transcript dates, and transcript lists.
"""

import time
from datetime import datetime, timedelta
from typing import List

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
from tests.conftest import extract_data_list

# Test configuration
RESPONSE_TIME_LIMIT = 15.0  # seconds (transcript endpoints might be slower)
TEST_SYMBOLS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "TSLA",
    "AMZN",
]  # Large companies with regular earnings calls


def get_field_value(item, field_name):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name)
    else:
        return getattr(item, field_name, None)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsTranscriptLatest:
    """Test class for latest earnings transcript functionality."""

    def test_earnings_transcript_latest_basic(self, api_key):
        """Test getting latest earnings transcripts."""
        start_time = time.time()
        result = earnings_transcript_latest(apikey=api_key, limit="10")
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Test first transcript structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscript.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.period is not None
            assert validated.fiscalYear is not None
            assert validated.date is not None

    def test_earnings_transcript_latest_with_limit(self, api_key):
        """Test latest earnings transcripts with different limits."""
        limits = ["5", "10", "20"]

        for limit in limits:
            result = earnings_transcript_latest(apikey=api_key, limit=limit)
            result_list = extract_data_list(result)

            assert isinstance(result_list, list)
            assert len(result_list) <= int(limit)

            if result_list:
                # Validate structure of first item
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                period_value = get_field_value(first_item, "period")
                fiscal_year_value = get_field_value(first_item, "fiscalYear")
                date_value = get_field_value(first_item, "date")

                assert symbol_value is not None
                assert period_value is not None
                assert fiscal_year_value is not None
                assert date_value is not None

    def test_earnings_transcript_latest_pagination(self, api_key):
        """Test pagination for latest earnings transcripts."""
        # Get first page
        page1 = earnings_transcript_latest(apikey=api_key, limit="5", page=1)
        result_list1 = extract_data_list(page1)

        # Get second page
        page2 = earnings_transcript_latest(apikey=api_key, limit="5", page=2)
        result_list2 = extract_data_list(page2)

        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

        if result_list1 and result_list2:
            # Pages should have different content
            first_symbols_page1 = [
                get_field_value(item, "symbol") for item in result_list1[:3]
            ]
            first_symbols_page2 = [
                get_field_value(item, "symbol") for item in result_list2[:3]
            ]

            # At least some symbols should be different between pages
            assert first_symbols_page1 != first_symbols_page2

    def test_earnings_transcript_latest_data_quality(self, api_key):
        """Test data quality for latest earnings transcripts."""
        result = earnings_transcript_latest(apikey=api_key, limit="10")
        result_list = extract_data_list(result)

        if result_list:
            for item in result_list[:3]:  # Check first 3 items
                symbol_value = get_field_value(item, "symbol")
                period_value = get_field_value(item, "period")
                fiscal_year_value = get_field_value(item, "fiscalYear")
                date_value = get_field_value(item, "date")

                # Basic validation
                assert isinstance(symbol_value, str)
                assert len(symbol_value) > 0
                assert isinstance(period_value, str)
                assert period_value in ["Q1", "Q2", "Q3", "Q4", "FY"]
                assert isinstance(fiscal_year_value, int)
                assert fiscal_year_value >= 2020
                assert isinstance(date_value, str)
                assert len(date_value) >= 10  # Should be a valid date string

    def test_earnings_transcript_latest_error_handling(self, api_key):
        """Test error handling for latest earnings transcripts."""
        # Test with very large limit (might be rejected)
        result = earnings_transcript_latest(apikey=api_key, limit="10000")
        result_list = extract_data_list(result)
        # Should either work or return reasonable amount of data
        assert isinstance(result_list, list)

        # Test with zero limit
        result = earnings_transcript_latest(apikey=api_key, limit="0")
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsTranscript:
    """Test class for specific earnings transcript functionality."""

    def test_earnings_transcript_basic(self, api_key):
        """Test getting specific earnings transcript."""
        # Use Apple Q4 2023 as a known transcript
        start_time = time.time()
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=2023, quarter=4
        )
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Test transcript structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscript.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.fiscalYear == 2023
            assert "Q4" in validated.period or "FY" in validated.period

    def test_earnings_transcript_multiple_companies(self, api_key):
        """Test earnings transcripts for multiple companies."""
        # Test recent quarters for major companies
        current_year = datetime.now().year
        test_year = current_year - 1  # Use previous year to ensure data exists

        for symbol in TEST_SYMBOLS[:3]:  # Test first 3 symbols
            result = earnings_transcript(
                apikey=api_key, symbol=symbol, year=test_year, quarter=4
            )
            result_list = extract_data_list(result)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            if result_list:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                fiscal_year_value = get_field_value(first_item, "fiscalYear")

                assert symbol_value == symbol
                assert fiscal_year_value == test_year

    def test_earnings_transcript_all_quarters(self, api_key):
        """Test earnings transcripts for all quarters."""
        symbol = "AAPL"
        year = 2023
        quarters = [1, 2, 3, 4]

        for quarter in quarters:
            result = earnings_transcript(
                apikey=api_key, symbol=symbol, year=year, quarter=quarter
            )
            result_list = extract_data_list(result)

            assert isinstance(result_list, list)

            if result_list:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                fiscal_year_value = get_field_value(first_item, "fiscalYear")

                assert symbol_value == symbol
                assert fiscal_year_value == year

    def test_earnings_transcript_with_limit(self, api_key):
        """Test earnings transcript with limit parameter."""
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=2023, quarter=4, limit="1"
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list)
        assert len(result_list) <= 1

    def test_earnings_transcript_content_validation(self, api_key):
        """Test earnings transcript content validation."""
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=2023, quarter=4
        )
        result_list = extract_data_list(result)

        if result_list:
            first_item = result_list[0]
            content_value = get_field_value(first_item, "content")

            # Content might be None for some transcripts
            if content_value is not None:
                assert isinstance(content_value, str)
                assert len(content_value) > 0

    def test_earnings_transcript_invalid_parameters(self, api_key):
        """Test earnings transcript with invalid parameters."""
        # Test invalid year (too old)
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=1990, quarter=1
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) == 0

        # Test invalid quarter
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=2023, quarter=5
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Test invalid symbol
        result = earnings_transcript(
            apikey=api_key, symbol="INVALID", year=2023, quarter=1
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsTranscriptBySymbol:
    """Test class for earnings transcript dates by symbol functionality."""

    def test_earnings_transcript_by_symbol_basic(self, api_key):
        """Test getting earnings transcript dates by symbol."""
        start_time = time.time()
        result = earnings_transcript_by_symbol(apikey=api_key, symbol="AAPL")
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Test transcript date structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscriptBySymbol.model_validate(first_item)
            else:
                validated = first_item

            assert validated.quarter is not None
            assert validated.fiscalYear is not None
            assert validated.date is not None

    def test_earnings_transcript_by_symbol_multiple_companies(self, api_key):
        """Test earnings transcript dates for multiple companies."""
        for symbol in TEST_SYMBOLS[:3]:  # Test first 3 symbols
            result = earnings_transcript_by_symbol(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            if result_list:
                # Should have multiple quarters/years
                assert len(result_list) > 0

                # Check data structure
                first_item = result_list[0]
                quarter_value = get_field_value(first_item, "quarter")
                fiscal_year_value = get_field_value(first_item, "fiscalYear")
                date_value = get_field_value(first_item, "date")

                assert quarter_value is not None
                assert fiscal_year_value is not None
                assert date_value is not None

    def test_earnings_transcript_by_symbol_chronological_order(self, api_key):
        """Test that transcript dates are in chronological order."""
        result = earnings_transcript_by_symbol(apikey=api_key, symbol="AAPL")
        result_list = extract_data_list(result)

        if len(result_list) > 1:
            # Check if dates are in descending order (most recent first)
            dates = [get_field_value(item, "date") for item in result_list[:5]]
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
        result = earnings_transcript_by_symbol(apikey=api_key, symbol="AAPL")
        result_list = extract_data_list(result)

        if result_list:
            for item in result_list[:3]:  # Check first 3 items
                quarter_value = get_field_value(item, "quarter")
                fiscal_year_value = get_field_value(item, "fiscalYear")
                date_value = get_field_value(item, "date")

                # Validate quarter format
                assert isinstance(quarter_value, str)
                assert (
                    quarter_value in ["Q1", "Q2", "Q3", "Q4"] or "FY" in quarter_value
                )

                # Validate fiscal year
                assert isinstance(fiscal_year_value, int)
                assert 2020 <= fiscal_year_value <= datetime.now().year + 1

                # Validate date
                assert isinstance(date_value, str)
                assert len(date_value) >= 10

    def test_earnings_transcript_by_symbol_invalid_symbol(self, api_key):
        """Test earnings transcript dates with invalid symbol."""
        result = earnings_transcript_by_symbol(apikey=api_key, symbol="INVALID_SYMBOL")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list)
        assert len(result_list) == 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsTranscriptList:
    """Test class for earnings transcript list functionality."""

    def test_earnings_transcript_list_basic(self, api_key):
        """Test getting earnings transcript list."""
        start_time = time.time()
        result = earnings_transcript_list(apikey=api_key)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Test transcript list structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPEarningsTranscriptList.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol is not None
            assert validated.companyName is not None
            assert validated.noOfTranscripts is not None

    def test_earnings_transcript_list_data_quality(self, api_key):
        """Test data quality for earnings transcript list."""
        result = earnings_transcript_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Should have many companies
            assert len(result_list) > 100

            for item in result_list[:10]:  # Check first 10 items
                symbol_value = get_field_value(item, "symbol")
                company_name_value = get_field_value(item, "companyName")
                no_of_transcripts_value = get_field_value(item, "noOfTranscripts")

                # Basic validation
                assert isinstance(symbol_value, str)
                assert len(symbol_value) > 0
                assert isinstance(company_name_value, str)
                assert len(company_name_value) > 0
                assert isinstance(no_of_transcripts_value, str)

                # Number of transcripts should be parseable as int
                try:
                    transcript_count = int(no_of_transcripts_value)
                    assert transcript_count >= 0
                except ValueError:
                    pytest.fail(
                        f"noOfTranscripts should be a valid number: {no_of_transcripts_value}"
                    )

    def test_earnings_transcript_list_contains_major_companies(self, api_key):
        """Test that transcript list contains major companies."""
        result = earnings_transcript_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            symbols = [get_field_value(item, "symbol") for item in result_list]

            # Should contain some major companies
            major_companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
            found_companies = [
                symbol for symbol in major_companies if symbol in symbols
            ]

            # Should find at least some major companies
            assert len(found_companies) > 0

    def test_earnings_transcript_list_symbol_uniqueness(self, api_key):
        """Test that each symbol appears only once in transcript list."""
        result = earnings_transcript_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            symbols = [get_field_value(item, "symbol") for item in result_list]

            # Check for duplicates
            unique_symbols = set(symbols)
            assert len(symbols) == len(
                unique_symbols
            ), "Each symbol should appear only once"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestEarningsTranscriptDataQuality:
    """Test class for overall earnings transcript data quality and consistency."""

    def test_earnings_transcript_data_consistency(self, api_key):
        """Test data consistency across different transcript endpoints."""
        symbol = "AAPL"

        # Get transcript list for the symbol
        transcript_list = earnings_transcript_list(apikey=api_key)
        transcript_list_data = extract_data_list(transcript_list)

        # Find Apple in the list
        apple_transcript_info = None
        for item in transcript_list_data:
            if get_field_value(item, "symbol") == symbol:
                apple_transcript_info = item
                break

        if apple_transcript_info:
            # Get transcript dates for Apple
            transcript_dates = earnings_transcript_by_symbol(
                apikey=api_key, symbol=symbol
            )
            transcript_dates_data = extract_data_list(transcript_dates)

            # Should have transcript dates if listed in transcript list
            no_of_transcripts = int(
                get_field_value(apple_transcript_info, "noOfTranscripts")
            )
            if no_of_transcripts > 0:
                assert len(transcript_dates_data) > 0

    def test_earnings_transcript_error_handling_comprehensive(self, api_key):
        """Test comprehensive error handling across all endpoints."""
        # Test invalid API key simulation (won't actually test with invalid key)
        # Instead test edge cases

        # Test very old year
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=1900, quarter=1
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Test future year
        future_year = datetime.now().year + 10
        result = earnings_transcript(
            apikey=api_key, symbol="AAPL", year=future_year, quarter=1
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_earnings_transcript_performance_benchmarks(self, api_key):
        """Test performance benchmarks for earnings transcript endpoints."""
        # Test latest transcripts performance
        start_time = time.time()
        earnings_transcript_latest(apikey=api_key, limit="10")
        latest_time = time.time() - start_time
        assert latest_time < RESPONSE_TIME_LIMIT

        # Test specific transcript performance
        start_time = time.time()
        earnings_transcript(apikey=api_key, symbol="AAPL", year=2023, quarter=4)
        specific_time = time.time() - start_time
        assert specific_time < RESPONSE_TIME_LIMIT

        # Test transcript dates performance
        start_time = time.time()
        earnings_transcript_by_symbol(apikey=api_key, symbol="AAPL")
        dates_time = time.time() - start_time
        assert dates_time < RESPONSE_TIME_LIMIT

        # Test transcript list performance (might be slower)
        start_time = time.time()
        earnings_transcript_list(apikey=api_key)
        list_time = time.time() - start_time
        assert list_time < RESPONSE_TIME_LIMIT * 2  # Allow more time for list endpoint
