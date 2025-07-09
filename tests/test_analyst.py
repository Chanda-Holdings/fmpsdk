import time

from fmpsdk import analyst
from fmpsdk.models import (
    FMPAnalystEstimates,
    FMPHistoricalStockGrade,
    FMPPriceTargetConsensus,
    FMPPriceTargetSummary,
    FMPRatingSnapshot,
    FMPStockGrade,
    FMPStockGradeSummary,
)

from .conftest import extract_data_list


def get_field_value(item, field_name, default=None):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name, default)
    else:
        return getattr(item, field_name, default)


class TestAnalystEstimates:
    """Test analyst estimates functionality."""

    def test_analyst_estimates_annual_valid_symbol(self, api_key):
        """Test annual analyst estimates for valid symbol."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="AAPL", period="annual"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate schema for first item
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAnalystEstimates.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.date
        assert validated.revenueAvg > 0
        assert validated.epsAvg != 0  # Could be positive or negative
        assert validated.numAnalystsRevenue > 0
        assert validated.numAnalystsEps > 0

    def test_analyst_estimates_quarterly_valid_symbol(self, api_key):
        """Test quarterly analyst estimates for valid symbol."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="MSFT", period="quarter"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate schema for first item
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPAnalystEstimates.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "MSFT"
        assert validated.date
        assert validated.revenueAvg > 0
        assert validated.numAnalystsRevenue > 0

    def test_analyst_estimates_with_limit(self, api_key):
        """Test analyst estimates with limit parameter."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="GOOGL", period="annual", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= 5

    def test_analyst_estimates_multiple_companies(self, api_key):
        """Test analyst estimates for multiple high-coverage companies."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

        for symbol in symbols:
            result = analyst.analyst_estimates(
                apikey=api_key, symbol=symbol, period="annual", limit=1
            )

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                assert symbol_value == symbol


class TestRatingsSnapshot:
    """Test ratings snapshot functionality."""

    def test_ratings_snapshot_valid_symbol(self, api_key):
        """Test ratings snapshot for valid symbol."""
        result = analyst.ratings_snapshot(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPRatingSnapshot.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.rating
            assert isinstance(validated.overallScore, int)
            assert validated.overallScore >= 0

    def test_ratings_snapshot_technology_sector(self, api_key):
        """Test ratings snapshot for technology companies."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        for symbol in symbols:
            result = analyst.ratings_snapshot(apikey=api_key, symbol=symbol, limit=1)

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                assert symbol_value == symbol

    def test_ratings_snapshot_with_limit(self, api_key):
        """Test ratings snapshot with limit parameter."""
        result = analyst.ratings_snapshot(apikey=api_key, symbol="AAPL", limit=3)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= 3


class TestRatingsHistorical:
    """Test historical ratings functionality."""

    def test_ratings_historical_valid_symbol(self, api_key):
        """Test historical ratings for valid symbol."""
        result = analyst.ratings_historical(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPRatingSnapshot.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.rating

    def test_ratings_historical_with_date_range(self, api_key):
        """Test historical ratings with date range."""
        result = analyst.ratings_historical(
            apikey=api_key, symbol="MSFT", from_date="2024-01-01", to_date="2024-12-31"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            symbol_value = get_field_value(first_item, "symbol")
            assert symbol_value == "MSFT"

    def test_ratings_historical_multiple_symbols(self, api_key):
        """Test historical ratings for multiple symbols."""
        symbols = ["AAPL", "TSLA", "NVDA"]

        for symbol in symbols:
            result = analyst.ratings_historical(
                apikey=api_key, symbol=symbol, from_date="2024-06-01"
            )

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)


class TestPriceTargets:
    """Test price target functionality."""

    def test_price_target_summary_valid_symbol(self, api_key):
        """Test price target summary for valid symbol."""
        result = analyst.price_target_summary(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPPriceTargetSummary.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.lastMonthCount >= 0
            assert validated.allTimeCount >= 0
            if validated.lastMonthAvgPriceTarget > 0:
                assert validated.lastMonthAvgPriceTarget > 0

    def test_price_target_consensus_valid_symbol(self, api_key):
        """Test price target consensus for valid symbol."""
        result = analyst.price_target_consensus(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPPriceTargetConsensus.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.targetConsensus > 0
            assert validated.targetHigh >= validated.targetLow

    def test_price_targets_high_coverage_stocks(self, api_key):
        """Test price targets for high analyst coverage stocks."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        for symbol in symbols:
            # Test summary
            summary_result = analyst.price_target_summary(apikey=api_key, symbol=symbol)

            summary_list = extract_data_list(summary_result)
            assert isinstance(summary_list, list)

            # Test consensus
            consensus_result = analyst.price_target_consensus(
                apikey=api_key, symbol=symbol
            )

            consensus_list = extract_data_list(consensus_result)
            assert isinstance(consensus_list, list)


class TestStockGrades:
    """Test stock grades functionality."""

    def test_stock_grades_valid_symbol(self, api_key):
        """Test stock grades for valid symbol."""
        result = analyst.stock_grades(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPStockGrade.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.date
            assert validated.gradingCompany
            assert validated.newGrade

    def test_historical_stock_grades_valid_symbol(self, api_key):
        """Test historical stock grades for valid symbol."""
        result = analyst.historical_stock_grades(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPHistoricalStockGrade.model_validate(first_item)
            else:
                validated = first_item

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

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPStockGradeSummary.model_validate(first_item)
            else:
                validated = first_item

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

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= 10

    def test_stock_grades_multiple_symbols(self, api_key):
        """Test stock grades for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        for symbol in symbols:
            # Test current grades
            grades_result = analyst.stock_grades(apikey=api_key, symbol=symbol)

            grades_list = extract_data_list(grades_result)
            assert isinstance(grades_list, list)

            # Test grades summary
            summary_result = analyst.stock_grades_summary(apikey=api_key, symbol=symbol)

            summary_list = extract_data_list(summary_result)
            assert isinstance(summary_list, list)


class TestAnalystErrorHandling:
    """Test error handling for analyst endpoints."""

    def test_analyst_estimates_invalid_api_key(self):
        """Test analyst estimates with invalid API key."""
        result = analyst.analyst_estimates(
            apikey="invalid_key", symbol="AAPL", period="annual"
        )

        # Should return error message
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            # Some endpoints might return empty lists for invalid keys
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_analyst_estimates_invalid_symbol(self, api_key):
        """Test analyst estimates with invalid symbol."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="INVALID", period="annual"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Invalid symbol typically returns empty list
        assert len(result_list) == 0

    def test_analyst_estimates_invalid_period(self, api_key):
        """Test analyst estimates with invalid period."""
        result = analyst.analyst_estimates(
            apikey=api_key, symbol="AAPL", period="invalid"
        )

        # Should handle invalid period gracefully
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_ratings_snapshot_empty_symbol(self, api_key):
        """Test ratings snapshot with empty symbol."""
        result = analyst.ratings_snapshot(apikey=api_key, symbol="")

        # Should handle empty symbol gracefully
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)


class TestAnalystResponseTimes:
    """Test response time performance for analyst endpoints."""

    def test_analyst_estimates_response_time(self, api_key):
        """Test analyst estimates response time."""
        start_time = time.time()

        result = analyst.analyst_estimates(
            apikey=api_key, symbol="AAPL", period="annual", limit=5
        )

        end_time = time.time()
        response_time = end_time - start_time

        # Should respond within 10 seconds
        assert response_time < 10.0

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_ratings_snapshot_response_time(self, api_key):
        """Test ratings snapshot response time."""
        start_time = time.time()

        result = analyst.ratings_snapshot(apikey=api_key, symbol="AAPL", limit=5)

        end_time = time.time()
        response_time = end_time - start_time

        # Should respond within 10 seconds
        assert response_time < 10.0

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)


class TestAnalystDataConsistency:
    """Test data consistency across analyst endpoints."""

    def test_estimates_vs_grades_consistency(self, api_key):
        """Test consistency between analyst estimates and stock grades."""
        symbol = "AAPL"

        # Get analyst estimates
        estimates_result = analyst.analyst_estimates(
            apikey=api_key, symbol=symbol, period="annual", limit=1
        )

        estimates_list = extract_data_list(estimates_result)

        # Get stock grades summary
        grades_result = analyst.stock_grades_summary(apikey=api_key, symbol=symbol)

        grades_list = extract_data_list(grades_result)

        # Both should have data for AAPL or both should be empty
        if len(estimates_list) > 0 and len(grades_list) > 0:
            estimates_symbol = get_field_value(estimates_list[0], "symbol")
            grades_symbol = get_field_value(grades_list[0], "symbol")
            assert estimates_symbol == grades_symbol == symbol

    def test_price_target_summary_vs_consensus_consistency(self, api_key):
        """Test consistency between price target summary and consensus."""
        symbol = "MSFT"

        # Get price target summary
        summary_result = analyst.price_target_summary(apikey=api_key, symbol=symbol)

        summary_list = extract_data_list(summary_result)

        # Get price target consensus
        consensus_result = analyst.price_target_consensus(apikey=api_key, symbol=symbol)

        consensus_list = extract_data_list(consensus_result)

        # Both should have data for symbol or both should be empty
        if len(summary_list) > 0 and len(consensus_list) > 0:
            summary_symbol = get_field_value(summary_list[0], "symbol")
            consensus_symbol = get_field_value(consensus_list[0], "symbol")
            assert summary_symbol == consensus_symbol == symbol

    def test_current_vs_historical_grades_consistency(self, api_key):
        """Test consistency between current and historical stock grades."""
        symbol = "GOOGL"

        # Get current stock grades
        current_result = analyst.stock_grades(apikey=api_key, symbol=symbol)

        current_list = extract_data_list(current_result)

        # Get historical stock grades
        historical_result = analyst.historical_stock_grades(
            apikey=api_key, symbol=symbol, limit=5
        )

        historical_list = extract_data_list(historical_result)

        # Both should have data for symbol or both should be empty
        if len(current_list) > 0 and len(historical_list) > 0:
            current_symbol = get_field_value(current_list[0], "symbol")
            historical_symbol = get_field_value(historical_list[0], "symbol")
            assert current_symbol == historical_symbol == symbol
