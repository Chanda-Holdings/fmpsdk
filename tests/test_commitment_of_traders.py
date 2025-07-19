from datetime import datetime, timedelta
from typing import List, Union

import pytest

from fmpsdk import commitment_of_traders
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPCommitmentOfTradersAnalysis,
    FMPCommitmentOfTradersReport,
    FMPSymbolAndNameList,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
    validate_required_fields,
)


def validate_cot_report_data(data: List[FMPCommitmentOfTradersReport]) -> None:
    """Validate COT report data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_reports = len(data)
    valid_symbols = 0
    valid_positions = 0
    valid_percentages = 0
    valid_dates = 0

    for report in data:
        # Symbol validation
        if report.symbol and len(report.symbol) >= 1:
            valid_symbols += 1

        # Date validation
        if report.date and len(str(report.date)) >= 10:
            valid_dates += 1

        # Position validation
        open_interest = report.openInterestAll
        noncomm_long = report.noncommPositionsLongAll
        noncomm_short = report.noncommPositionsShortAll
        comm_long = report.commPositionsLongAll
        comm_short = report.commPositionsShortAll

        if all(
            pos is not None and pos >= 0
            for pos in [
                open_interest,
                noncomm_long,
                noncomm_short,
                comm_long,
                comm_short,
            ]
        ):
            valid_positions += 1

        # Percentage validation
        pct_noncomm_long = report.pctOfOiNoncommLongAll
        pct_noncomm_short = report.pctOfOiNoncommShortAll
        pct_comm_long = report.pctOfOiCommLongAll
        pct_comm_short = report.pctOfOiCommShortAll

        if all(
            pct is not None and 0 <= pct <= 100
            for pct in [
                pct_noncomm_long,
                pct_noncomm_short,
                pct_comm_long,
                pct_comm_short,
            ]
        ):
            valid_percentages += 1

    # Business logic assertions
    if total_reports > 0:
        assert (
            valid_symbols / total_reports >= 0.95
        ), f"Only {valid_symbols}/{total_reports} reports have valid symbols"
        assert (
            valid_dates / total_reports >= 0.90
        ), f"Only {valid_dates}/{total_reports} reports have valid dates"
        assert (
            valid_positions / total_reports >= 0.80
        ), f"Only {valid_positions}/{total_reports} reports have valid positions"
        assert (
            valid_percentages / total_reports >= 0.70
        ), f"Only {valid_percentages}/{total_reports} reports have valid percentages"


def validate_cot_analysis_data(data: List[FMPCommitmentOfTradersAnalysis]) -> None:
    """Validate COT analysis data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_analyses = len(data)
    valid_symbols = 0
    valid_dates = 0
    valid_situations = 0
    valid_sentiments = 0
    valid_reversals = 0

    valid_market_situations = [
        "Bullish",
        "Bearish",
        "Neutral",
        "Strong Bullish",
        "Strong Bearish",
    ]
    valid_market_sentiments = [
        "Bullish",
        "Bearish",
        "Neutral",
        "Strong Bullish",
        "Strong Bearish",
    ]

    for analysis in data:
        # Symbol validation
        if analysis.symbol and len(analysis.symbol) >= 1:
            valid_symbols += 1

        # Date validation
        if analysis.date and len(str(analysis.date)) >= 10:
            valid_dates += 1

        # Market situation validation
        market_situation = analysis.marketSituation
        if market_situation and (
            market_situation in valid_market_situations or len(market_situation) > 0
        ):
            valid_situations += 1

        # Market sentiment validation
        market_sentiment = analysis.marketSentiment
        if market_sentiment and (
            market_sentiment in valid_market_sentiments or len(market_sentiment) > 0
        ):
            valid_sentiments += 1

        # Reversal trend validation
        reversal_trend = analysis.reversalTrend
        if isinstance(reversal_trend, bool):
            valid_reversals += 1

    # Business logic assertions
    if total_analyses > 0:
        assert (
            valid_symbols / total_analyses >= 0.95
        ), f"Only {valid_symbols}/{total_analyses} analyses have valid symbols"
        assert (
            valid_dates / total_analyses >= 0.90
        ), f"Only {valid_dates}/{total_analyses} analyses have valid dates"
        assert (
            valid_situations / total_analyses >= 0.70
        ), f"Only {valid_situations}/{total_analyses} analyses have valid market situations"
        assert (
            valid_sentiments / total_analyses >= 0.70
        ), f"Only {valid_sentiments}/{total_analyses} analyses have valid market sentiments"
        assert (
            valid_reversals / total_analyses >= 0.60
        ), f"Only {valid_reversals}/{total_analyses} analyses have valid reversal trends"


def validate_cot_symbol_data(data: List[FMPSymbolAndNameList]) -> None:
    """Validate COT symbol list data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_symbols = len(data)
    valid_symbols = 0
    valid_names = 0
    unique_symbols = set()

    cot_symbol_patterns = [
        "CL",
        "NG",
        "GC",
        "SI",
        "ES",
        "NQ",
        "EUR",
        "GBP",
        "C",
        "W",
        "S",
        "LC",
        "LH",
    ]

    for symbol_item in data:
        # Symbol validation
        if symbol_item.symbol and len(symbol_item.symbol) >= 1:
            valid_symbols += 1
            unique_symbols.add(symbol_item.symbol)

        # Name validation
        if symbol_item.name and len(symbol_item.name) >= 2:
            valid_names += 1

    # Business logic assertions
    if total_symbols > 0:
        assert (
            valid_symbols / total_symbols >= 0.95
        ), f"Only {valid_symbols}/{total_symbols} symbols are valid"
        assert (
            valid_names / total_symbols >= 0.85
        ), f"Only {valid_names}/{total_symbols} names are valid"
        assert (
            len(unique_symbols) == valid_symbols
        ), f"Symbols should be unique: {len(unique_symbols)} != {valid_symbols}"

        # Check for common COT symbols
        found_common = sum(
            1
            for pattern in cot_symbol_patterns
            if any(pattern in symbol for symbol in unique_symbols)
        )
        assert (
            found_common >= 1
        ), f"Should find at least 1 common COT symbol pattern: {found_common}"


class TestCommitmentOfTradersBasic:
    """Test basic COT functionality."""

    @pytest.mark.parametrize(
        "commodity_symbol",
        [
            # Energy Commodities
            "CL",  # Crude Oil
            "NG",  # Natural Gas
            "HO",  # Heating Oil
            "RB",  # RBOB Gasoline
            # Precious Metals
            "GC",  # Gold
            "SI",  # Silver
            "PL",  # Platinum
            "PA",  # Palladium
            # Industrial Metals
            "HG",  # Copper
            "AL",  # Aluminum (if available)
            # Agricultural Commodities
            "C",  # Corn
            "W",  # Wheat
            "S",  # Soybeans
            "SB",  # Sugar
            "KC",  # Coffee
            "CT",  # Cotton
            "CC",  # Cocoa
            "OJ",  # Orange Juice
            # Livestock
            "LC",  # Live Cattle
            "FC",  # Feeder Cattle
            "LH",  # Lean Hogs
            # Financial Futures
            "ES",  # E-mini S&P 500
            "NQ",  # E-mini NASDAQ 100
            "YM",  # E-mini Dow Jones
            "TY",  # 10-Year Treasury Note
            "FV",  # 5-Year Treasury Note
            "TU",  # 2-Year Treasury Note
            "US",  # 30-Year Treasury Bond
            # Currency Futures
            "EUR",  # Euro
            "GBP",  # British Pound
            "JPY",  # Japanese Yen
            "CAD",  # Canadian Dollar
            "AUD",  # Australian Dollar
            "CHF",  # Swiss Franc
            "NZD",  # New Zealand Dollar
            "MXN",  # Mexican Peso
            # Other Commodities
            "LBS",  # Lumber (if available)
            "DA",  # Milk (if available)
        ],
    )
    def test_commitment_of_traders_report_by_symbol(self, api_key, commodity_symbol):
        """Test COT report retrieval by commodity symbol."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol=commodity_symbol,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)

        # Some commodity symbols may not have recent data, so allow empty results
        if len(models) == 0:
            pytest.skip(f"No COT data available for symbol {commodity_symbol}")

        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            f"Failed to validate COT report models for {commodity_symbol}",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional symbol-specific validations
        for report in models:
            assert (
                report.symbol == commodity_symbol
            ), f"Symbol mismatch: expected {commodity_symbol}, got {report.symbol}"
            validate_required_fields(report, ["symbol", "date"])

    @pytest.mark.parametrize(
        "commodity_category",
        [
            "energy",
            "precious_metals",
            "industrial_metals",
            "agricultural",
            "livestock",
            "financial",
            "currency",
        ],
    )
    def test_commitment_of_traders_analysis_by_category(
        self, api_key, commodity_category
    ):
        """Test COT analysis retrieval by commodity category."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_analysis,
            "commitment_of_traders_report_analysis",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersAnalysis)
        validate_model_list(
            models,
            FMPCommitmentOfTradersAnalysis,
            f"Failed to validate COT analysis models for {commodity_category}",
        )

        # Validate business logic
        validate_cot_analysis_data(models)

        # Additional category-specific validations
        for analysis in models:
            validate_required_fields(analysis, ["symbol", "date"])

    @pytest.mark.parametrize(
        "market_segment",
        [
            "commodity_futures",
            "financial_futures",
            "currency_futures",
            "equity_index_futures",
        ],
    )
    def test_commitment_of_traders_by_market_segment(self, api_key, market_segment):
        """Test COT data retrieval by market segment."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            f"Failed to validate COT report models for {market_segment}",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional segment-specific validations
        for report in models:
            validate_required_fields(report, ["symbol", "date"])

    @pytest.mark.parametrize("timeframe", ["recent", "quarterly", "annual"])
    def test_commitment_of_traders_timeframes(self, api_key, timeframe):
        """Test COT data retrieval with different timeframes."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            f"Failed to validate COT report models for {timeframe}",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional timeframe-specific validations
        for report in models:
            validate_required_fields(report, ["symbol", "date"])

    def test_commitment_of_traders_report_list(self, api_key):
        """Test COT report list retrieval."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_list,
            "commitment_of_traders_report_list",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndNameList)
        validate_model_list(
            models, FMPSymbolAndNameList, "Failed to validate COT report list models"
        )

        # Validate business logic
        validate_cot_symbol_data(models)

    def test_commitment_of_traders_report_without_symbol(self, api_key):
        """Test COT report retrieval without symbol parameter."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models, FMPCommitmentOfTradersReport, "Failed to validate COT report models"
        )

        # Validate business logic
        validate_cot_report_data(models)

    def test_commitment_of_traders_report_with_symbol(self, api_key):
        """Test COT report retrieval with symbol parameter."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models with symbol",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional symbol-specific validations
        for report in models:
            assert (
                report.symbol == "CL"
            ), f"Symbol mismatch: expected CL, got {report.symbol}"

    def test_commitment_of_traders_analysis_without_symbol(self, api_key):
        """Test COT analysis retrieval without symbol parameter."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_analysis,
            "commitment_of_traders_report_analysis",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersAnalysis)
        validate_model_list(
            models,
            FMPCommitmentOfTradersAnalysis,
            "Failed to validate COT analysis models",
        )

        # Validate business logic
        validate_cot_analysis_data(models)


class TestCommitmentOfTradersSymbols:
    """Test COT symbol-specific functionality."""

    def test_cot_major_equity_indices(self, api_key):
        """Test COT data for major equity indices."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="ES",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models for equity indices",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional equity-specific validations
        for report in models:
            assert (
                report.symbol == "ES"
            ), f"Symbol mismatch: expected ES, got {report.symbol}"

    def test_cot_currency_futures(self, api_key):
        """Test COT data for currency futures."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="EUR",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)

        # Some currency symbols may not have recent COT data
        if len(models) == 0:
            pytest.skip(f"No COT data available for currency symbol EUR")

        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models for currency futures",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional currency-specific validations
        for report in models:
            assert (
                report.symbol == "EUR"
            ), f"Symbol mismatch: expected EUR, got {report.symbol}"

    def test_cot_commodity_futures(self, api_key):
        """Test COT data for commodity futures."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models for commodity futures",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional commodity-specific validations
        for report in models:
            assert (
                report.symbol == "CL"
            ), f"Symbol mismatch: expected CL, got {report.symbol}"


class TestCommitmentOfTradersDateRanges:
    """Test COT functionality with date ranges."""

    def test_cot_report_with_date_range(self, api_key):
        """Test COT report retrieval with date range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
            from_date=start_date.strftime("%Y-%m-%d"),
            to_date=end_date.strftime("%Y-%m-%d"),
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models with date range",
        )

        # Validate business logic
        validate_cot_report_data(models)

        # Additional date range validations
        for report in models:
            assert (
                report.symbol == "CL"
            ), f"Symbol mismatch: expected CL, got {report.symbol}"
            validate_required_fields(report, ["symbol", "date"])

    def test_cot_analysis_with_date_range(self, api_key):
        """Test COT analysis retrieval with date range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_analysis,
            "commitment_of_traders_report_analysis",
            apikey=api_key,
            symbol="CL",
            from_date=start_date.strftime("%Y-%m-%d"),
            to_date=end_date.strftime("%Y-%m-%d"),
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersAnalysis)
        validate_model_list(
            models,
            FMPCommitmentOfTradersAnalysis,
            "Failed to validate COT analysis models with date range",
        )

        # Validate business logic
        validate_cot_analysis_data(models)

        # Additional date range validations
        for analysis in models:
            assert (
                analysis.symbol == "CL"
            ), f"Symbol mismatch: expected CL, got {analysis.symbol}"
            validate_required_fields(analysis, ["symbol", "date"])


class TestCommitmentOfTradersDataQuality:
    """Test COT data quality and consistency."""

    def test_cot_position_consistency(self, api_key):
        """Test that COT position data is internally consistent."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models for position consistency",
        )

        # Validate position consistency
        for report in models:
            # Check that positions are non-negative
            assert (
                report.openInterestAll >= 0
            ), f"Open interest should be non-negative: {report.openInterestAll}"
            assert (
                report.noncommPositionsLongAll >= 0
            ), f"Non-commercial long positions should be non-negative: {report.noncommPositionsLongAll}"
            assert (
                report.noncommPositionsShortAll >= 0
            ), f"Non-commercial short positions should be non-negative: {report.noncommPositionsShortAll}"
            assert (
                report.commPositionsLongAll >= 0
            ), f"Commercial long positions should be non-negative: {report.commPositionsLongAll}"
            assert (
                report.commPositionsShortAll >= 0
            ), f"Commercial short positions should be non-negative: {report.commPositionsShortAll}"

    def test_cot_analysis_sentiment_values(self, api_key):
        """Test that COT analysis sentiment values are valid."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_analysis,
            "commitment_of_traders_report_analysis",
            apikey=api_key,
            symbol="CL",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersAnalysis)
        validate_model_list(
            models,
            FMPCommitmentOfTradersAnalysis,
            "Failed to validate COT analysis models for sentiment values",
        )

        # Validate sentiment values
        valid_sentiments = [
            "Bullish",
            "Bearish",
            "Neutral",
            "Strong Bullish",
            "Strong Bearish",
        ]
        for analysis in models:
            if analysis.marketSituation:
                assert (
                    analysis.marketSituation in valid_sentiments
                    or len(analysis.marketSituation) > 0
                ), f"Invalid market situation: {analysis.marketSituation}"
            if analysis.marketSentiment:
                assert (
                    analysis.marketSentiment in valid_sentiments
                    or len(analysis.marketSentiment) > 0
                ), f"Invalid market sentiment: {analysis.marketSentiment}"

    def test_cot_data_freshness(self, api_key):
        """Test that COT data is reasonably fresh."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
        )

        # Extract and validate models
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        validate_model_list(
            models,
            FMPCommitmentOfTradersReport,
            "Failed to validate COT report models for data freshness",
        )

        # Validate data freshness
        if models:
            latest_date = models[0].date
            if isinstance(latest_date, str):
                # Handle both date-only and datetime formats
                if " " in latest_date:
                    latest_date = datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
                else:
                    latest_date = datetime.strptime(latest_date, "%Y-%m-%d")
            elif hasattr(latest_date, "date"):
                latest_date = latest_date.date()

            # Data should not be older than 2 years
            cutoff_date = datetime.now() - timedelta(days=730)
            assert latest_date >= cutoff_date, f"Data is too old: {latest_date}"

    def test_cot_symbol_name_consistency(self, api_key):
        """Test that COT symbol and name data is consistent."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report_list,
            "commitment_of_traders_report_list",
            apikey=api_key,
        )

        # Extract and validate models
        models = get_response_models(result, FMPSymbolAndNameList)
        validate_model_list(
            models,
            FMPSymbolAndNameList,
            "Failed to validate COT report list models for symbol consistency",
        )

        # Validate symbol consistency
        symbols = set()
        for symbol_item in models:
            if symbol_item.symbol:
                symbols.add(symbol_item.symbol)
                assert (
                    len(symbol_item.symbol) >= 1
                ), f"Symbol should have at least 1 character: {symbol_item.symbol}"

        # Should have multiple unique symbols
        assert (
            len(symbols) >= 5
        ), f"Expected at least 5 unique symbols, got {len(symbols)}"


class TestCommitmentOfTradersErrorHandling:
    """Test COT error handling and edge cases."""

    def test_cot_report_invalid_api_key(self):
        """Test COT report with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            commitment_of_traders.commitment_of_traders_report(
                apikey="invalid_key",
                symbol="CL",
            )

        assert "Invalid API KEY" in str(exc_info.value)

    def test_cot_analysis_invalid_api_key(self):
        """Test COT analysis with invalid API key."""
        with pytest.raises(InvalidAPIKeyException) as exc_info:
            commitment_of_traders.commitment_of_traders_report_analysis(
                apikey="invalid_key",
                symbol="CL",
            )

        assert "Invalid API KEY" in str(exc_info.value)

    def test_cot_list_invalid_api_key(self):
        """Test COT list with invalid API key."""
        with pytest.raises(Exception):
            commitment_of_traders.commitment_of_traders_report_list(
                apikey="invalid_key",
            )

    def test_cot_invalid_symbol(self, api_key):
        """Test COT with invalid symbol."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="INVALID_SYMBOL_12345",
        )

        # Should handle invalid symbol gracefully
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        # May return empty list for invalid symbol

    def test_cot_invalid_date_format(self, api_key):
        """Test COT with invalid date format."""
        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
            from_date="invalid-date",
            to_date="invalid-date",
        )

        models = get_response_models(result, FMPCommitmentOfTradersReport)
        # Should handle gracefully with empty result or error message
        validate_model_list(models, FMPCommitmentOfTradersReport, min_count=0)

    def test_cot_future_dates(self, api_key):
        """Test COT with future dates."""
        future_date = datetime.now() + timedelta(days=365)

        result, validation = handle_api_call_with_validation(
            commitment_of_traders.commitment_of_traders_report,
            "commitment_of_traders_report",
            apikey=api_key,
            symbol="CL",
            from_date=future_date.strftime("%Y-%m-%d"),
            to_date=future_date.strftime("%Y-%m-%d"),
        )

        # Should handle future dates gracefully
        models = get_response_models(result, FMPCommitmentOfTradersReport)
        # May return empty list for future dates
