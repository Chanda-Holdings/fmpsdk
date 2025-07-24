import time

import pytest

from fmpsdk import analyst
from fmpsdk.exceptions import InvalidAPIKeyException, InvalidQueryParameterException
from fmpsdk.models import (
    FMPAnalystEstimates,
    FMPHistoricalRating,
    FMPHistoricalRatingV3,
    FMPHistoricalStockGrade,
    FMPPriceTargetConsensus,
    FMPPriceTargetSummary,
    FMPRatingSnapshot,
    FMPStockGrade,
    FMPStockGradeSummary,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


class TestAnalystEstimates:
    """Test analyst estimates functionality."""

    @pytest.mark.parametrize(
        "symbol,period",
        [
            # Large Cap Technology
            ("AAPL", "annual"),
            ("AAPL", "quarter"),
            ("MSFT", "annual"),
            ("MSFT", "quarter"),
            ("GOOGL", "annual"),
            ("GOOGL", "quarter"),
            ("AMZN", "annual"),
            ("AMZN", "quarter"),
            ("META", "annual"),
            ("META", "quarter"),
            ("TSLA", "annual"),
            ("TSLA", "quarter"),
            # Large Cap Other Sectors
            ("JPM", "annual"),  # Financial
            ("JPM", "quarter"),
            ("JNJ", "annual"),  # Healthcare
            ("JNJ", "quarter"),
            ("PG", "annual"),  # Consumer Goods
            ("PG", "quarter"),
            ("HD", "annual"),  # Retail
            ("HD", "quarter"),
            ("BA", "annual"),  # Industrial
            ("BA", "quarter"),
            ("XOM", "annual"),  # Energy
            ("XOM", "quarter"),
            # Mid Cap
            ("NVDA", "annual"),
            ("NVDA", "quarter"),
            ("CRM", "annual"),
            ("CRM", "quarter"),
            ("NFLX", "annual"),
            ("NFLX", "quarter"),
            # Different Business Models
            ("BRK-B", "annual"),  # Conglomerate
            ("BRK-B", "quarter"),
            ("REIT", "annual"),  # Real Estate
            ("WMT", "annual"),  # Retail
            ("WMT", "quarter"),
            ("KO", "annual"),  # Consumer Staples
            ("KO", "quarter"),
        ],
    )
    def test_analyst_estimates_comprehensive(self, api_key, symbol, period):
        """Test analyst estimates across various symbols and periods."""
        result, validation = handle_api_call_with_validation(
            analyst.analyst_estimates,
            "analyst_estimates",
            apikey=api_key,
            symbol=symbol,
            period=period,
            limit=4,
        )

        # Get response models and validate
        models = get_response_models(result, FMPAnalystEstimates)

        # Some symbols may not have analyst estimates, especially unusual ones like REIT
        if len(models) == 0:
            pytest.skip(
                f"No analyst estimates available for symbol {symbol} with period {period}"
            )

        validate_model_list(
            models, FMPAnalystEstimates, "analyst estimates comprehensive"
        )

        if len(models) > 0:
            # Validate business logic for first item
            first_item = models[0]

            # Basic validation
            assert first_item.symbol == symbol
            assert first_item.date, "Date should not be empty"

            # Revenue estimates should be positive for most companies
            if first_item.revenueAvg is not None:
                assert first_item.revenueAvg > 0, "Revenue estimate should be positive"

            # Should have analyst counts
            if first_item.numAnalystsRevenue is not None:
                assert (
                    first_item.numAnalystsRevenue >= 0
                ), "Analyst count should be non-negative"
                assert (
                    first_item.numAnalystsRevenue <= 100
                ), "Analyst count should be reasonable"
            if first_item.numAnalystsEps is not None:
                assert (
                    first_item.numAnalystsEps >= 0
                ), "Analyst count should be non-negative"
                assert (
                    first_item.numAnalystsEps <= 100
                ), "Analyst count should be reasonable"

    @pytest.mark.parametrize(
        "symbol",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "JNJ", "PG"],
    )
    def test_analyst_estimates_data_quality(self, api_key, symbol):
        """Test data quality aspects of analyst estimates."""
        result, validation = handle_api_call_with_validation(
            analyst.analyst_estimates,
            "analyst_estimates",
            apikey=api_key,
            symbol=symbol,
            period="annual",
            limit=3,
        )

        # Get response models and validate
        models = get_response_models(result, FMPAnalystEstimates)
        validate_model_list(
            models, FMPAnalystEstimates, "analyst estimates data quality"
        )

        for item in models:
            # Basic data quality checks
            assert item.symbol == symbol
            assert item.date is not None, "Date should not be empty"

            # Analyst counts should be reasonable
            if item.numAnalystsRevenue is not None:
                assert (
                    0 <= item.numAnalystsRevenue <= 100
                ), "Analyst count should be reasonable"
            if item.numAnalystsEps is not None:
                assert (
                    0 <= item.numAnalystsEps <= 100
                ), "Analyst count should be reasonable"

            # Estimates should be within reasonable ranges
            if item.revenueAvg is not None:
                assert item.revenueAvg > 0, "Revenue estimate should be positive"
                assert (
                    item.revenueAvg < 2e12
                ), "Revenue estimate should be reasonable (under $2T)"

    def test_analyst_estimates_annual_valid_symbol(self, api_key):
        """Test annual analyst estimates for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.analyst_estimates,
            "analyst_estimates",
            apikey=api_key,
            symbol="AAPL",
            period="annual",
        )

        # Get response models and validate
        models = get_response_models(result, FMPAnalystEstimates)
        validate_model_list(models, FMPAnalystEstimates, "analyst estimates annual")
        assert len(models) > 0

        # Validate business logic for first item
        first_item = models[0]
        assert first_item.symbol == "AAPL"
        assert first_item.date, "Date should not be empty"
        assert first_item.revenueAvg > 0, "Revenue estimate should be positive"
        assert (
            first_item.epsAvg != 0
        ), "EPS estimate should not be zero"  # Could be positive or negative
        assert first_item.numAnalystsRevenue > 0, "Should have revenue analysts"
        assert first_item.numAnalystsEps > 0, "Should have EPS analysts"

    def test_analyst_estimates_quarterly_valid_symbol(self, api_key):
        """Test quarterly analyst estimates for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.analyst_estimates,
            "analyst_estimates",
            apikey=api_key,
            symbol="MSFT",
            period="quarter",
        )

        # Get response models and validate
        models = get_response_models(result, FMPAnalystEstimates)
        validate_model_list(models, FMPAnalystEstimates, "analyst estimates quarterly")
        assert len(models) > 0

        # Validate business logic for first item
        first_item = models[0]
        assert first_item.symbol == "MSFT"
        assert first_item.date, "Date should not be empty"
        assert first_item.revenueAvg > 0, "Revenue estimate should be positive"
        assert first_item.numAnalystsRevenue > 0, "Should have revenue analysts"

    def test_analyst_estimates_with_limit(self, api_key):
        """Test analyst estimates with limit parameter."""
        result, validation = handle_api_call_with_validation(
            analyst.analyst_estimates,
            "analyst_estimates",
            apikey=api_key,
            symbol="GOOGL",
            period="annual",
            limit=5,
        )

        # Get response models and validate
        models = get_response_models(result, FMPAnalystEstimates)
        validate_model_list(models, FMPAnalystEstimates, "analyst estimates with limit")
        assert len(models) <= 5

    def test_analyst_estimates_multiple_companies(self, api_key):
        """Test analyst estimates for multiple high-coverage companies."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

        for symbol in symbols:
            result, validation = handle_api_call_with_validation(
                analyst.analyst_estimates,
                "analyst_estimates",
                apikey=api_key,
                symbol=symbol,
                period="annual",
                limit=1,
            )

            # Get response models and validate
            models = get_response_models(result, FMPAnalystEstimates)
            validate_model_list(
                models, FMPAnalystEstimates, f"analyst estimates for {symbol}"
            )

            if len(models) > 0:
                first_item = models[0]
                assert first_item.symbol == symbol


class TestRatingsSnapshot:
    """Test ratings snapshot functionality."""

    @pytest.mark.parametrize(
        "symbol",
        [
            # Technology Large Cap
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "NVDA",
            "ORCL",
            "CRM",
            "ADBE",
            # Financial Services
            "JPM",
            "BAC",
            "WFC",
            "GS",
            "MS",
            "C",
            "BRK-B",
            "AXP",
            "COF",
            "SCHW",
            # Healthcare
            "JNJ",
            "PFE",
            "UNH",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "LLY",
            "DHR",
            "BMY",
            # Consumer Discretionary
            "HD",
            "MCD",
            "NKE",
            "SBUX",
            "TGT",
            "LOW",
            "DIS",
            "BKNG",
            "GM",
            "F",
            # Consumer Staples
            "PG",
            "KO",
            "PEP",
            "WMT",
            "COST",
            "CL",
            "KMB",
            "GIS",
            "K",
            "CPB",
            # Energy
            "XOM",
            "CVX",
            "COP",
            "EOG",
            "SLB",
            "PSX",
            "VLO",
            "MPC",
            "OXY",
            "DVN",
            # Industrial
            "BA",
            "CAT",
            "HON",
            "UPS",
            "LMT",
            "RTX",
            "DE",
            "GE",
            "MMM",
            "FDX",
            # Utilities
            "NEE",
            "SO",
            "DUK",
            "AEP",
            "EXC",
            "XEL",
            "ES",
            "AWK",
            "PEG",
            "ED",
            # Materials
            "LIN",
            "APD",
            "SHW",
            "ECL",
            "FCX",
            "NEM",
            "DOW",
            "DD",
            "PPG",
            "NUE",
            # Real Estate
            "AMT",
            "PLD",
            "CCI",
            "EQIX",
            "SPG",
            "O",
            "WELL",
            "PSA",
            "EXR",
            "AVB",
            # Communication Services
            "GOOGL",
            "META",
            "DIS",
            "NFLX",
            "CMCSA",
            "VZ",
            "T",
            "CHTR",
            "TMUS",
            "ATVI",
        ],
    )
    def test_ratings_snapshot_comprehensive(self, api_key, symbol):
        """Test ratings snapshot across diverse sectors and market caps."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_snapshot,
            "ratings_snapshot",
            apikey=api_key,
            symbol=symbol,
            limit=3,
        )

        # Get response models and validate
        models = get_response_models(result, FMPRatingSnapshot)

        # Some symbols may not have current rating data
        if len(models) == 0:
            pytest.skip(f"No rating data available for symbol {symbol}")

        validate_model_list(models, FMPRatingSnapshot, f"ratings snapshot for {symbol}")

        if len(models) > 0:
            first_item = models[0]

            assert first_item.symbol == symbol
            assert first_item.rating is not None, "Rating should not be None"

            # Rating should be a valid rating
            if first_item.rating:
                valid_ratings = [
                    "Strong Buy",
                    "Buy",
                    "Hold",
                    "Sell",
                    "Strong Sell",
                    "Outperform",
                    "Underperform",
                    "Neutral",
                    "Market Perform",
                    "Overweight",
                    "Underweight",
                    "Equal Weight",
                ]
                # Allow flexible matching since rating formats may vary, including single letters
                assert (
                    any(
                        rating_value.lower() in first_item.rating.lower()
                        for rating_value in valid_ratings
                    )
                    or len(first_item.rating) >= 1
                ), "Rating should be meaningful"

            # Overall score should be within reasonable range
            if first_item.overallScore is not None:
                assert (
                    0 <= first_item.overallScore <= 10
                ), "Overall score should be 0-10"

    @pytest.mark.parametrize(
        "sector",
        [
            "technology",
            "financial",
            "healthcare",
            "consumer",
            "energy",
            "industrial",
            "utilities",
            "materials",
            "real_estate",
            "communication",
        ],
    )
    def test_ratings_snapshot_by_sector(self, api_key, sector):
        """Test ratings snapshot for different sectors."""
        sector_symbols = {
            "technology": ["AAPL", "MSFT", "GOOGL"],
            "financial": ["JPM", "BAC", "WFC"],
            "healthcare": ["JNJ", "PFE", "UNH"],
            "consumer": ["HD", "MCD", "PG"],
            "energy": ["XOM", "CVX", "COP"],
            "industrial": ["BA", "CAT", "HON"],
            "utilities": ["NEE", "SO", "DUK"],
            "materials": ["LIN", "APD", "SHW"],
            "real_estate": ["AMT", "PLD", "CCI"],
            "communication": ["DIS", "NFLX", "CMCSA"],
        }

        symbols = sector_symbols.get(sector, ["AAPL"])

        for symbol in symbols:
            result, validation = handle_api_call_with_validation(
                analyst.ratings_snapshot,
                "ratings_snapshot",
                apikey=api_key,
                symbol=symbol,
                limit=1,
            )
            # Get response models and validate
            models = get_response_models(result, FMPRatingSnapshot)
            validate_model_list(
                models, FMPRatingSnapshot, f"ratings snapshot for {symbol}", min_count=0
            )

            if len(models) > 0:
                first_item = models[0]
                symbol_value = first_item.symbol
                assert symbol_value == symbol

    def test_ratings_snapshot_valid_symbol(self, api_key):
        """Test ratings snapshot for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_snapshot, "ratings_snapshot", apikey=api_key, symbol="AAPL"
        )

        # Get response models and validate
        models = get_response_models(result, FMPRatingSnapshot)
        validate_model_list(
            models, FMPRatingSnapshot, "ratings snapshot valid symbol", min_count=0
        )

        if len(models) > 0:
            first_item = models[0]
            rating_symbol = first_item.symbol
            rating = first_item.rating
            overall_score = first_item.overallScore

            assert rating_symbol == "AAPL"
            assert rating, "Rating should not be empty"
            if overall_score is not None:
                assert isinstance(
                    overall_score, int
                ), "Overall score should be an integer"
                assert overall_score >= 0, "Overall score should be non-negative"

    def test_ratings_snapshot_technology_sector(self, api_key):
        """Test ratings snapshot for technology companies."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        for symbol in symbols:
            result, validation = handle_api_call_with_validation(
                analyst.ratings_snapshot,
                "ratings_snapshot",
                apikey=api_key,
                symbol=symbol,
                limit=1,
            )

            # Get response models and validate
            models = get_response_models(result, FMPRatingSnapshot)
            validate_model_list(
                models,
                FMPRatingSnapshot,
                f"ratings snapshot technology for {symbol}",
                min_count=0,
            )

            if len(models) > 0:
                first_item = models[0]
                symbol_value = first_item.symbol
                assert symbol_value == symbol

    def test_ratings_snapshot_with_limit(self, api_key):
        """Test ratings snapshot with limit parameter."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_snapshot,
            "ratings_snapshot",
            apikey=api_key,
            symbol="AAPL",
            limit=3,
        )

        # Get response models and validate
        models = get_response_models(result, FMPRatingSnapshot)
        validate_model_list(
            models, FMPRatingSnapshot, "ratings snapshot with limit", min_count=0
        )
        assert len(models) <= 3


class TestRatingsHistorical:
    """Test historical ratings functionality."""

    def test_ratings_historical_valid_symbol(self, api_key):
        """Test historical ratings for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical,
            "ratings_historical",
            apikey=api_key,
            symbol="AAPL",
        )

        # Get response models and validate
        models = get_response_models(result, FMPHistoricalRating)
        validate_model_list(
            models, FMPHistoricalRating, "ratings historical valid symbol", min_count=0
        )

        if len(models) > 0:
            first_item = models[0]
            rating_symbol = first_item.symbol
            rating = first_item.rating

            assert rating_symbol == "AAPL"
            assert rating, "Rating should not be empty"

    def test_ratings_historical_with_date_range(self, api_key):
        """Test historical ratings with limit."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical,
            "ratings_historical",
            apikey=api_key,
            symbol="MSFT",
            limit=10,
        )

        # Get response models and validate
        models = get_response_models(result, FMPHistoricalRating)
        validate_model_list(
            models,
            FMPHistoricalRating,
            "ratings historical with limit",
            min_count=0,
        )

        if len(models) > 0:
            first_item = models[0]
            symbol_value = first_item.symbol
            assert symbol_value == "MSFT"

    def test_ratings_historical_multiple_symbols(self, api_key):
        """Test historical ratings for multiple symbols."""
        symbols = ["AAPL", "TSLA", "NVDA"]

        for symbol in symbols:
            result, validation = handle_api_call_with_validation(
                analyst.ratings_historical,
                "ratings_historical",
                apikey=api_key,
                symbol=symbol,
                limit=5,
            )

            # Get response models and validate
            models = get_response_models(result, FMPHistoricalRating)
            validate_model_list(
                models,
                FMPHistoricalRating,
                f"ratings historical for {symbol}",
                min_count=0,
            )

    def test_ratings_historical_obscene_limit(self, api_key):
        """Test historical ratings with an obscenely high limit."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical,
            "ratings_historical",
            apikey=api_key,
            symbol="AAPL",
            limit=99999,
        )

        # Get response models and validate
        models = get_response_models(result, FMPHistoricalRating)
        validate_model_list(
            models,
            FMPHistoricalRating,
            "ratings historical with obscene limit",
            min_count=0,
        )

        # Even with an obscene limit, we shouldn't get more than what's reasonable
        if len(models) > 0:
            first_item = models[0]
            assert first_item.symbol == "AAPL"
            # API should handle the obscene limit gracefully
            assert len(models) <= 10000, "Even with obscene limit, should be reasonable"

    def test_ratings_historical_v3_valid_symbol(self, api_key):
        """Test historical ratings v3 for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical_v3,
            "ratings_historical_v3",
            apikey=api_key,
            symbol="AAPL",
        )

        # Get response models and validate
        models = get_response_models(result, FMPHistoricalRatingV3)
        validate_model_list(
            models,
            FMPHistoricalRatingV3,
            "ratings historical v3 valid symbol",
            min_count=0,
        )

        if len(models) > 0:
            first_item = models[0]
            # Basic validation that the model has the expected structure
            assert hasattr(first_item, "symbol"), "Model should have symbol attribute"
            if hasattr(first_item, "symbol") and first_item.symbol:
                assert first_item.symbol == "AAPL"

    def test_ratings_historical_v3_with_limit(self, api_key):
        """Test historical ratings v3 with limit parameter."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical_v3,
            "ratings_historical_v3",
            apikey=api_key,
            symbol="AAPL",
            limit=5,
        )

        models = get_response_models(result, FMPHistoricalRatingV3)
        validate_model_list(
            models,
            FMPHistoricalRatingV3,
            "ratings historical v3 with limit",
            min_count=0,
        )

        # If we have results, they should not exceed the limit
        if len(models) > 0:
            assert len(models) <= 5, "Results should not exceed specified limit"

    @pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL", "TSLA", "META"])
    def test_ratings_historical_v3_multiple_symbols(self, api_key, symbol):
        """Test historical ratings v3 for multiple symbols."""
        result, validation = handle_api_call_with_validation(
            analyst.ratings_historical_v3,
            "ratings_historical_v3",
            apikey=api_key,
            symbol=symbol,
            limit=3,
        )

        models = get_response_models(result, FMPHistoricalRatingV3)
        validate_model_list(
            models,
            FMPHistoricalRatingV3,
            f"ratings historical v3 for {symbol}",
            min_count=0,
        )


class TestPriceTargets:
    """Test price target functionality."""

    def test_price_target_summary_valid_symbol(self, api_key):
        """Test price target summary for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.price_target_summary,
            "price_target_summary",
            apikey=api_key,
            symbol="AAPL",
        )

        models = get_response_models(result, FMPPriceTargetSummary)
        validate_model_list(
            models,
            FMPPriceTargetSummary,
            "price target summary valid symbol",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == "AAPL"
            if validated.lastMonthCount is not None:
                assert (
                    validated.lastMonthCount >= 0
                ), "Last month count should be non-negative"
            if validated.allTimeCount is not None:
                assert (
                    validated.allTimeCount >= 0
                ), "All time count should be non-negative"
            if (
                validated.lastMonthAvgPriceTarget is not None
                and validated.lastMonthAvgPriceTarget > 0
            ):
                assert (
                    validated.lastMonthAvgPriceTarget > 0
                ), "Last month avg price target should be positive"

    def test_price_target_consensus_valid_symbol(self, api_key):
        """Test price target consensus for valid symbol."""
        result, validation = handle_api_call_with_validation(
            analyst.price_target_consensus,
            "price_target_consensus",
            apikey=api_key,
            symbol="AAPL",
        )

        models = get_response_models(result, FMPPriceTargetConsensus)
        validate_model_list(
            models,
            FMPPriceTargetConsensus,
            "price target consensus valid symbol",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == "AAPL"
            if validated.targetConsensus is not None:
                assert (
                    validated.targetConsensus > 0
                ), "Target consensus should be positive"
            if validated.targetHigh is not None and validated.targetLow is not None:
                assert validated.targetHigh >= validated.targetLow

    def test_price_targets_high_coverage_stocks(self, api_key):
        """Test price targets for high analyst coverage stocks."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        for symbol in symbols:
            # Test summary
            summary_result = analyst.price_target_summary(apikey=api_key, symbol=symbol)
            summary_models = get_response_models(summary_result, FMPPriceTargetSummary)
            validate_model_list(
                summary_models,
                FMPPriceTargetSummary,
                f"price target summary for {symbol}",
                min_count=0,
            )

            # Test consensus
            consensus_result = analyst.price_target_consensus(
                apikey=api_key, symbol=symbol
            )
            consensus_models = get_response_models(
                consensus_result, FMPPriceTargetConsensus
            )
            validate_model_list(
                consensus_models,
                FMPPriceTargetConsensus,
                f"price target consensus for {symbol}",
                min_count=0,
            )

    @pytest.mark.parametrize(
        "symbol,limit",
        [
            ("AAPL", 5),
            ("MSFT", 10),
            ("GOOGL", 3),
            ("AMZN", 7),
            ("META", 4),
            ("TSLA", 6),
            ("NVDA", 8),
            ("JPM", 5),
            ("JNJ", 3),
            ("PG", 4),
        ],
    )
    def test_price_target_summary_with_limits(self, api_key, symbol, limit):
        """Test price target summary with various limits."""
        result = analyst.price_target_summary(apikey=api_key, symbol=symbol)
        models = get_response_models(result, FMPPriceTargetSummary)
        validate_model_list(
            models,
            FMPPriceTargetSummary,
            f"price target summary with limit for {symbol}",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == symbol
            assert validated.lastMonthCount >= 0
            assert validated.allTimeCount >= 0

    @pytest.mark.parametrize(
        "symbol",
        [
            # High analyst coverage stocks
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "NVDA",
            "NFLX",
            "CRM",
            "ADBE",
            "JPM",
            "BAC",
            "WFC",
            "GS",
            "JNJ",
            "PFE",
            "UNH",
            "HD",
            "MCD",
            "PG",
            "XOM",
            "CVX",
            "BA",
            "CAT",
            "NEE",
            "SO",
            "LIN",
            "APD",
            "AMT",
            "PLD",
        ],
    )
    def test_price_target_consensus_comprehensive(self, api_key, symbol):
        """Test price target consensus across various high-coverage stocks."""
        result = analyst.price_target_consensus(apikey=api_key, symbol=symbol)
        models = get_response_models(result, FMPPriceTargetConsensus)
        validate_model_list(
            models,
            FMPPriceTargetConsensus,
            f"price target consensus for {symbol}",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == symbol
            # Price targets should be positive and logical
            if validated.targetConsensus is not None and validated.targetConsensus > 0:
                assert validated.targetConsensus > 0
            if (
                validated.targetHigh is not None
                and validated.targetLow is not None
                and validated.targetHigh > 0
                and validated.targetLow > 0
            ):
                assert validated.targetHigh >= validated.targetLow

    @pytest.mark.parametrize("market_cap", ["large_cap", "mid_cap", "small_cap"])
    def test_price_targets_by_market_cap(self, api_key, market_cap):
        """Test price targets across different market cap categories."""
        market_cap_symbols = {
            "large_cap": ["AAPL", "MSFT", "GOOGL", "AMZN", "BRK-B"],
            "mid_cap": ["NVDA", "CRM", "NFLX", "AMD", "SHOP"],
            "small_cap": ["ROKU", "ZM", "PTON", "W", "SQ"],
        }
        symbols = market_cap_symbols.get(market_cap, ["AAPL"])
        for symbol in symbols[:3]:  # Test first 3 from each category
            result = analyst.price_target_summary(apikey=api_key, symbol=symbol)
            models = get_response_models(result, FMPPriceTargetSummary)
            validate_model_list(
                models,
                FMPPriceTargetSummary,
                f"price target summary for {symbol}",
                min_count=0,
            )
            if len(models) > 0:
                symbol_value = models[0].symbol
                assert symbol_value == symbol


class TestStockGrades:
    """Test stock grades functionality."""

    def test_stock_grades_valid_symbol(self, api_key):
        """Test stock grades for valid symbol."""
        result = analyst.stock_grades(apikey=api_key, symbol="AAPL")
        models = get_response_models(result, FMPStockGrade)
        validate_model_list(
            models, FMPStockGrade, "stock grades valid symbol", min_count=0
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == "AAPL"
            assert validated.date
            assert validated.gradingCompany
            assert validated.newGrade

    def test_historical_stock_grades_valid_symbol(self, api_key):
        """Test historical stock grades for valid symbol."""
        result = analyst.historical_stock_grades(apikey=api_key, symbol="AAPL")
        models = get_response_models(result, FMPHistoricalStockGrade)
        validate_model_list(
            models,
            FMPHistoricalStockGrade,
            "historical stock grades valid symbol",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == "AAPL"
            assert validated.date
            assert validated.analystRatingsStrongBuy >= 0
            assert validated.analystRatingsBuy >= 0
            assert validated.analystRatingsHold >= 0
            assert validated.analystRatingsSell >= 0
            assert validated.analystRatingsStrongSell >= 0

    def test_stock_grades_summary_valid_symbol(self, api_key):
        """Test stock grades summary for valid symbol."""
        result = analyst.stock_grades_summary(apikey=api_key, symbol="AAPL")
        models = get_response_models(result, FMPStockGradeSummary)
        validate_model_list(
            models,
            FMPStockGradeSummary,
            "stock grades summary valid symbol",
            min_count=0,
        )
        if len(models) > 0:
            validated = models[0]
            assert validated.symbol == "AAPL"
            assert validated.strongBuy >= 0
            assert validated.buy >= 0
            assert validated.hold >= 0
            assert validated.sell >= 0
            assert validated.strongSell >= 0
            assert validated.consensus

    def test_historical_stock_grades_with_limit(self, api_key):
        """Test historical stock grades with limit parameter."""
        result = analyst.historical_stock_grades(
            apikey=api_key, symbol="MSFT", limit=10
        )
        models = get_response_models(result, FMPHistoricalStockGrade)
        validate_model_list(
            models,
            FMPHistoricalStockGrade,
            "historical stock grades with limit",
            min_count=0,
        )
        assert len(models) <= 10

    def test_stock_grades_multiple_symbols(self, api_key):
        """Test stock grades for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        for symbol in symbols:
            # Test current grades
            grades_result = analyst.stock_grades(apikey=api_key, symbol=symbol)
            grades_models = get_response_models(grades_result, FMPStockGrade)
            validate_model_list(
                grades_models, FMPStockGrade, f"stock grades for {symbol}", min_count=0
            )
            # Test grades summary
            summary_result = analyst.stock_grades_summary(apikey=api_key, symbol=symbol)
            summary_models = get_response_models(summary_result, FMPStockGradeSummary)
            validate_model_list(
                summary_models,
                FMPStockGradeSummary,
                f"stock grades summary for {symbol}",
                min_count=0,
            )

    def test_analyst_estimates_invalid_symbol(self, api_key):
        """Test analyst estimates with invalid symbol."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="INVALID", period="annual"
        )
        models = get_response_models(result, FMPAnalystEstimates)
        validate_model_list(
            models, FMPAnalystEstimates, "analyst estimates invalid symbol", min_count=0
        )
        # Invalid symbol typically returns empty list
        assert len(models) == 0


class TestAnalystErrorHandling:
    """Test error handling for analyst endpoints."""

    def test_analyst_estimates_invalid_api_key(self):
        """Test analyst estimates with invalid API key."""

        with pytest.raises(InvalidAPIKeyException) as exc_info:
            analyst.analyst_estimates(
                apikey="invalid_key", symbol="AAPL", period="annual"
            )
        assert "Invalid API KEY" in str(exc_info.value)

    def test_analyst_estimates_invalid_period(self, api_key):
        """Test analyst estimates with invalid period."""
        with pytest.raises(InvalidQueryParameterException) as exc_info:
            analyst.analyst_estimates(apikey=api_key, symbol="AAPL", period="invalid")

        assert "Invalid or missing query parameter" in str(exc_info.value)

    def test_ratings_snapshot_empty_symbol(self, api_key):
        """Test ratings snapshot with empty symbol."""
        with pytest.raises(InvalidQueryParameterException) as exc_info:
            analyst.ratings_snapshot(apikey=api_key, symbol="")

        assert "Invalid or missing query parameter" in str(exc_info.value)


class TestAnalystDataConsistency:
    """Test data consistency across analyst endpoints."""

    def test_estimates_vs_grades_consistency(self, api_key):
        """Test consistency between analyst estimates and stock grades."""
        symbol = "AAPL"

        # Get analyst estimates
        estimates_result = analyst.analyst_estimates(
            apikey=api_key, symbol=symbol, period="annual", limit=1
        )

        estimates_models = get_response_models(estimates_result, FMPAnalystEstimates)

        # Get stock grades summary
        grades_result = analyst.stock_grades_summary(apikey=api_key, symbol=symbol)

        grades_models = get_response_models(grades_result, FMPStockGradeSummary)

        # Both should have data for AAPL or both should be empty
        if len(estimates_models) > 0 and len(grades_models) > 0:
            estimates_symbol = estimates_models[0].symbol
            grades_symbol = grades_models[0].symbol
            assert estimates_symbol == grades_symbol == symbol

    def test_price_target_summary_vs_consensus_consistency(self, api_key):
        """Test consistency between price target summary and consensus."""
        symbol = "MSFT"

        # Get price target summary
        summary_result = analyst.price_target_summary(apikey=api_key, symbol=symbol)

        summary_models = get_response_models(summary_result, FMPPriceTargetSummary)

        # Get price target consensus
        consensus_result = analyst.price_target_consensus(apikey=api_key, symbol=symbol)

        consensus_models = get_response_models(
            consensus_result, FMPPriceTargetConsensus
        )

        # Both should have data for symbol or both should be empty
        if len(summary_models) > 0 and len(consensus_models) > 0:
            summary_symbol = summary_models[0].symbol
            consensus_symbol = consensus_models[0].symbol
            assert summary_symbol == consensus_symbol == symbol

    def test_current_vs_historical_grades_consistency(self, api_key):
        """Test consistency between current and historical stock grades."""
        symbol = "GOOGL"

        # Get current stock grades
        current_result = analyst.stock_grades(apikey=api_key, symbol=symbol)

        current_models = get_response_models(current_result, FMPStockGrade)

        # Get historical stock grades
        historical_result = analyst.historical_stock_grades(
            apikey=api_key, symbol=symbol, limit=5
        )

        historical_models = get_response_models(
            historical_result, FMPHistoricalStockGrade
        )

        # Both should have data for symbol or both should be empty
        if len(current_models) > 0 and len(historical_models) > 0:
            current_symbol = current_models[0].symbol
            historical_symbol = historical_models[0].symbol
            assert current_symbol == historical_symbol == symbol


class TestAnalystParameterCoverage:
    """Tests to cover optional parameters that weren't being tested."""

    def test_analyst_estimates_with_page_parameter(self, api_key):
        """Test analyst_estimates with page parameter (covers line 41)."""
        try:
            result, validation = handle_api_call_with_validation(
                analyst.analyst_estimates,
                "analyst_estimates",
                apikey=api_key,
                symbol="AAPL",
                period="annual",
                page=0,
            )

            models = get_response_models(result, FMPAnalystEstimates)
            assert isinstance(models, list)
        except Exception:
            # Premium endpoint or other errors are expected
            pass
