import pytest
import time
from datetime import datetime, timedelta

from fmpsdk import market_performance
from fmpsdk.models import (
    FMPHistoricalIndustryPE,
    FMPHistoricalIndustryPerformance,
    FMPHistoricalSectorPE,
    FMPHistoricalSectorPerformance,
    FMPIndustryPerformanceSnapshot,
    FMPIndustryPESnapshot,
    FMPMarketMover,
    FMPSectorPerformanceSnapshot,
    FMPSectorPESnapshot,
)
from tests.conftest import (
    get_response_models,
    validate_model_list,
    validate_required_fields,
)


def get_test_date():
    """Get a recent business date for testing."""
    # Use a date that's likely to have data (not too recent, not weekend)
    test_date = datetime.now() - timedelta(days=7)
    # If it's a weekend, go back to Friday
    while test_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        test_date -= timedelta(days=1)
    return test_date.strftime("%Y-%m-%d")


class TestSectorPerformance:
    """Test sector performance functions."""

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_performance_snapshot(self, api_key):
        """Test sector performance snapshot."""
        test_date = get_test_date()
        result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date
        )
        models = get_response_models(result, FMPSectorPerformanceSnapshot)
        validate_model_list(models, FMPSectorPerformanceSnapshot)

        if models:
            first_model = models[0]
            # Validate required fields
            assert hasattr(first_model, "sector") or hasattr(
                first_model, "sectorName"
            ), "Should have sector field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_performance_with_exchange(self, api_key):
        """Test sector performance with exchange filter."""
        test_date = get_test_date()
        result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date, exchange="NASDAQ"
        )
        models = get_response_models(result, FMPSectorPerformanceSnapshot)
        validate_model_list(models, FMPSectorPerformanceSnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_performance_with_sector_filter(self, api_key):
        """Test sector performance with sector filter."""
        test_date = get_test_date()
        result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date, sector="Technology"
        )
        models = get_response_models(result, FMPSectorPerformanceSnapshot)
        validate_model_list(models, FMPSectorPerformanceSnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_performance(self, api_key):
        """Test historical sector performance."""
        result = market_performance.historical_sector_performance(
            apikey=api_key, sector="Technology"
        )
        models = get_response_models(result, FMPHistoricalSectorPerformance)
        validate_model_list(models, FMPHistoricalSectorPerformance)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "date") or hasattr(
                first_model, "sector"
            ), "Should have date or sector field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_performance_with_dates(self, api_key):
        """Test historical sector performance with date range."""
        from_date = "2023-01-01"
        to_date = "2023-03-31"
        result = market_performance.historical_sector_performance(
            apikey=api_key, sector="Technology", from_date=from_date, to_date=to_date
        )
        models = get_response_models(result, FMPHistoricalSectorPerformance)
        validate_model_list(models, FMPHistoricalSectorPerformance)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_performance_with_exchange(self, api_key):
        """Test historical sector performance with exchange."""
        result = market_performance.historical_sector_performance(
            apikey=api_key, sector="Technology", exchange="NASDAQ"
        )
        models = get_response_models(result, FMPHistoricalSectorPerformance)
        validate_model_list(models, FMPHistoricalSectorPerformance)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_pe_snapshot(self, api_key):
        """Test sector PE snapshot."""
        test_date = get_test_date()
        result = market_performance.sector_pe_snapshot(apikey=api_key, date=test_date)
        models = get_response_models(result, FMPSectorPESnapshot)
        validate_model_list(models, FMPSectorPESnapshot)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "sector") or hasattr(
                first_model, "pe"
            ), "Should have sector or PE field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_pe_snapshot_with_exchange(self, api_key):
        """Test sector PE snapshot with exchange filter."""
        test_date = get_test_date()
        result = market_performance.sector_pe_snapshot(
            apikey=api_key, date=test_date, exchange="NASDAQ"
        )
        models = get_response_models(result, FMPSectorPESnapshot)
        validate_model_list(models, FMPSectorPESnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_pe_snapshot_with_sector_filter(self, api_key):
        """Test sector PE snapshot with sector filter."""
        test_date = get_test_date()
        result = market_performance.sector_pe_snapshot(
            apikey=api_key, date=test_date, sector="Technology"
        )
        models = get_response_models(result, FMPSectorPESnapshot)
        validate_model_list(models, FMPSectorPESnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_pe(self, api_key):
        """Test historical sector PE."""
        result = market_performance.historical_sector_pe(
            apikey=api_key, sector="Technology"
        )
        models = get_response_models(result, FMPHistoricalSectorPE)
        validate_model_list(models, FMPHistoricalSectorPE)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "date") or hasattr(
                first_model, "sector"
            ), "Should have date or sector field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_pe_with_dates(self, api_key):
        """Test historical sector PE with date range."""
        from_date = "2023-01-01"
        to_date = "2023-03-31"
        result = market_performance.historical_sector_pe(
            apikey=api_key, sector="Technology", from_date=from_date, to_date=to_date
        )
        models = get_response_models(result, FMPHistoricalSectorPE)
        validate_model_list(models, FMPHistoricalSectorPE)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_sector_pe_with_exchange(self, api_key):
        """Test historical sector PE with exchange."""
        result = market_performance.historical_sector_pe(
            apikey=api_key, sector="Technology", exchange="NASDAQ"
        )
        models = get_response_models(result, FMPHistoricalSectorPE)
        validate_model_list(models, FMPHistoricalSectorPE)


class TestIndustryPerformance:
    """Test industry performance functions."""

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_performance_snapshot(self, api_key):
        """Test industry performance snapshot."""
        test_date = get_test_date()
        result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=test_date
        )
        models = get_response_models(result, FMPIndustryPerformanceSnapshot)
        validate_model_list(models, FMPIndustryPerformanceSnapshot)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "industry") or hasattr(
                first_model, "industryName"
            ), "Should have industry field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_performance_with_exchange(self, api_key):
        """Test industry performance with exchange filter."""
        test_date = get_test_date()
        result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=test_date, exchange="NASDAQ"
        )
        models = get_response_models(result, FMPIndustryPerformanceSnapshot)
        validate_model_list(models, FMPIndustryPerformanceSnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_performance_with_industry_filter(self, api_key):
        """Test industry performance with industry filter."""
        test_date = get_test_date()
        result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=test_date, industry="Software"
        )
        models = get_response_models(result, FMPIndustryPerformanceSnapshot)
        validate_model_list(models, FMPIndustryPerformanceSnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_performance(self, api_key):
        """Test historical industry performance."""
        result = market_performance.historical_industry_performance(
            apikey=api_key, industry="Software"
        )
        models = get_response_models(result, FMPHistoricalIndustryPerformance)
        validate_model_list(models, FMPHistoricalIndustryPerformance)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "date") or hasattr(
                first_model, "industry"
            ), "Should have date or industry field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_performance_with_dates(self, api_key):
        """Test historical industry performance with date range."""
        from_date = "2023-01-01"
        to_date = "2023-03-31"
        result = market_performance.historical_industry_performance(
            apikey=api_key, industry="Software", from_date=from_date, to_date=to_date
        )
        models = get_response_models(result, FMPHistoricalIndustryPerformance)
        validate_model_list(models, FMPHistoricalIndustryPerformance)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_performance_with_exchange(self, api_key):
        """Test historical industry performance with exchange."""
        result = market_performance.historical_industry_performance(
            apikey=api_key, industry="Software", exchange="NASDAQ"
        )
        models = get_response_models(result, FMPHistoricalIndustryPerformance)
        validate_model_list(models, FMPHistoricalIndustryPerformance)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_pe_snapshot(self, api_key):
        """Test industry PE snapshot."""
        test_date = get_test_date()
        result = market_performance.industry_pe_snapshot(apikey=api_key, date=test_date)
        models = get_response_models(result, FMPIndustryPESnapshot)
        validate_model_list(models, FMPIndustryPESnapshot)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "industry") or hasattr(
                first_model, "pe"
            ), "Should have industry or PE field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_pe_snapshot_with_exchange(self, api_key):
        """Test industry PE snapshot with exchange filter."""
        test_date = get_test_date()
        result = market_performance.industry_pe_snapshot(
            apikey=api_key, date=test_date, exchange="NASDAQ"
        )
        models = get_response_models(result, FMPIndustryPESnapshot)
        validate_model_list(models, FMPIndustryPESnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_industry_pe_snapshot_with_industry_filter(self, api_key):
        """Test industry PE snapshot with industry filter."""
        test_date = get_test_date()
        result = market_performance.industry_pe_snapshot(
            apikey=api_key, date=test_date, industry="Software"
        )
        models = get_response_models(result, FMPIndustryPESnapshot)
        validate_model_list(models, FMPIndustryPESnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_pe(self, api_key):
        """Test historical industry PE."""
        result = market_performance.historical_industry_pe(
            apikey=api_key, industry="Software"
        )
        models = get_response_models(result, FMPHistoricalIndustryPE)
        validate_model_list(models, FMPHistoricalIndustryPE)

        if models:
            first_model = models[0]
            assert hasattr(first_model, "date") or hasattr(
                first_model, "industry"
            ), "Should have date or industry field"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_pe_with_dates(self, api_key):
        """Test historical industry PE with date range."""
        from_date = "2023-01-01"
        to_date = "2023-03-31"
        result = market_performance.historical_industry_pe(
            apikey=api_key, industry="Software", from_date=from_date, to_date=to_date
        )
        models = get_response_models(result, FMPHistoricalIndustryPE)
        validate_model_list(models, FMPHistoricalIndustryPE)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_historical_industry_pe_with_exchange(self, api_key):
        """Test historical industry PE with exchange."""
        result = market_performance.historical_industry_pe(
            apikey=api_key, industry="Software", exchange="NASDAQ"
        )
        models = get_response_models(result, FMPHistoricalIndustryPE)
        validate_model_list(models, FMPHistoricalIndustryPE)


class TestMarketMovers:
    """Test market mover functions."""

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_biggest_gainers(self, api_key):
        """Test biggest gainers."""
        result = market_performance.biggest_gainers(apikey=api_key)
        models = get_response_models(result, FMPMarketMover)
        validate_model_list(models, FMPMarketMover)

        if models:
            first_model = models[0]
            validate_required_fields(first_model, ["symbol"])
            
            # Gainers should have positive change (when data is available)
            if (
                hasattr(first_model, "changePercentage")
                and first_model.changePercentage is not None
            ):
                assert (
                    float(first_model.changePercentage) > 0
                ), "Biggest gainers should have positive change"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_biggest_losers(self, api_key):
        """Test biggest losers."""
        result = market_performance.biggest_losers(apikey=api_key)
        models = get_response_models(result, FMPMarketMover)
        validate_model_list(models, FMPMarketMover)

        if models:
            first_model = models[0]
            validate_required_fields(first_model, ["symbol"])
            
            # Losers should have negative change (when data is available)
            if (
                hasattr(first_model, "changePercentage")
                and first_model.changePercentage is not None
            ):
                assert (
                    float(first_model.changePercentage) < 0
                ), "Biggest losers should have negative change"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_most_active_stocks(self, api_key):
        """Test most active stocks."""
        result = market_performance.most_active_stocks(apikey=api_key)
        models = get_response_models(result, FMPMarketMover)
        validate_model_list(models, FMPMarketMover)

        if models:
            first_model = models[0]
            validate_required_fields(first_model, ["symbol"])
            
            # Most active stocks should have volume data
            if hasattr(first_model, "volume") and first_model.volume is not None:
                assert (
                    int(first_model.volume) > 0
                ), "Most active stocks should have positive volume"


class TestMarketPerformanceComprehensive:
    """Comprehensive market performance tests."""

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_all_sector_functions_consistency(self, api_key):
        """Test that all sector functions work consistently."""
        test_date = get_test_date()

        # Test sector functions
        snapshot_result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date
        )
        historical_result = market_performance.historical_sector_performance(
            apikey=api_key, sector="Technology"
        )
        pe_snapshot_result = market_performance.sector_pe_snapshot(
            apikey=api_key, date=test_date
        )
        historical_pe_result = market_performance.historical_sector_pe(
            apikey=api_key, sector="Technology"
        )

        # All should return valid model lists
        snapshot_models = get_response_models(snapshot_result, FMPSectorPerformanceSnapshot)
        historical_models = get_response_models(historical_result, FMPHistoricalSectorPerformance)
        pe_snapshot_models = get_response_models(pe_snapshot_result, FMPSectorPESnapshot)
        historical_pe_models = get_response_models(historical_pe_result, FMPHistoricalSectorPE)

        validate_model_list(snapshot_models, FMPSectorPerformanceSnapshot)
        validate_model_list(historical_models, FMPHistoricalSectorPerformance)
        validate_model_list(pe_snapshot_models, FMPSectorPESnapshot)
        validate_model_list(historical_pe_models, FMPHistoricalSectorPE)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_all_industry_functions_consistency(self, api_key):
        """Test that all industry functions work consistently."""
        test_date = get_test_date()

        # Test industry functions
        snapshot_result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=test_date
        )
        historical_result = market_performance.historical_industry_performance(
            apikey=api_key, industry="Software"
        )
        pe_snapshot_result = market_performance.industry_pe_snapshot(
            apikey=api_key, date=test_date
        )
        historical_pe_result = market_performance.historical_industry_pe(
            apikey=api_key, industry="Software"
        )

        # All should return valid model lists
        snapshot_models = get_response_models(snapshot_result, FMPIndustryPerformanceSnapshot)
        historical_models = get_response_models(historical_result, FMPHistoricalIndustryPerformance)
        pe_snapshot_models = get_response_models(pe_snapshot_result, FMPIndustryPESnapshot)
        historical_pe_models = get_response_models(historical_pe_result, FMPHistoricalIndustryPE)

        validate_model_list(snapshot_models, FMPIndustryPerformanceSnapshot)
        validate_model_list(historical_models, FMPHistoricalIndustryPerformance)
        validate_model_list(pe_snapshot_models, FMPIndustryPESnapshot)
        validate_model_list(historical_pe_models, FMPHistoricalIndustryPE)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_market_mover_functions_consistency(self, api_key):
        """Test that all market mover functions work consistently."""
        gainers_result = market_performance.biggest_gainers(apikey=api_key)
        losers_result = market_performance.biggest_losers(apikey=api_key)
        active_result = market_performance.most_active_stocks(apikey=api_key)

        # All should return valid model lists
        gainers_models = get_response_models(gainers_result, FMPMarketMover)
        losers_models = get_response_models(losers_result, FMPMarketMover)
        active_models = get_response_models(active_result, FMPMarketMover)

        validate_model_list(gainers_models, FMPMarketMover)
        validate_model_list(losers_models, FMPMarketMover)
        validate_model_list(active_models, FMPMarketMover)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_response_times(self, api_key):
        """Test that all functions respond within reasonable time."""
        test_date = get_test_date()

        functions_and_params = [
            (
                market_performance.sector_performance_snapshot,
                {"apikey": api_key, "date": test_date},
                FMPSectorPerformanceSnapshot,
            ),
            (
                market_performance.industry_performance_snapshot,
                {"apikey": api_key, "date": test_date},
                FMPIndustryPerformanceSnapshot,
            ),
            (market_performance.biggest_gainers, {"apikey": api_key}, FMPMarketMover),
            (market_performance.biggest_losers, {"apikey": api_key}, FMPMarketMover),
            (market_performance.most_active_stocks, {"apikey": api_key}, FMPMarketMover),
        ]

        for func, params, model_type in functions_and_params:
            start_time = time.time()
            result = func(**params)
            models = get_response_models(result, model_type)
            response_time = time.time() - start_time

            assert (
                response_time < 15.0
            ), f"{func.__name__} took {response_time:.2f}s, expected < 15.0s"

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_date_validation(self, api_key):
        """Test functions with different date formats."""
        # Test recent date
        recent_date = get_test_date()

        snapshot_result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=recent_date
        )
        snapshot_models = get_response_models(snapshot_result, FMPSectorPerformanceSnapshot)
        validate_model_list(snapshot_models, FMPSectorPerformanceSnapshot)

        industry_result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=recent_date
        )
        industry_models = get_response_models(industry_result, FMPIndustryPerformanceSnapshot)
        validate_model_list(industry_models, FMPIndustryPerformanceSnapshot)

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_sector_and_industry_names(self, api_key):
        """Test with different sector and industry names."""
        test_date = get_test_date()

        # Test different sectors
        sectors = ["Technology", "Healthcare", "Financials", "Energy"]
        for sector in sectors:
            result = market_performance.historical_sector_performance(
                apikey=api_key, sector=sector
            )
            models = get_response_models(result, FMPHistoricalSectorPerformance)
            validate_model_list(models, FMPHistoricalSectorPerformance, f"Failed for sector: {sector}")

        # Test different industries
        industries = ["Software", "Pharmaceuticals", "Banking", "Oil & Gas"]
        for industry in industries:
            result = market_performance.historical_industry_performance(
                apikey=api_key, industry=industry
            )
            models = get_response_models(result, FMPHistoricalIndustryPerformance)
            validate_model_list(models, FMPHistoricalIndustryPerformance, f"Failed for industry: {industry}")

    @pytest.mark.integration
    @pytest.mark.requires_api_key
    @pytest.mark.live_data
    def test_invalid_api_keys(self):
        """Test all functions with invalid API keys."""
        from fmpsdk.exceptions import InvalidAPIKeyException
        
        test_date = get_test_date()

        functions_and_params = [
            (
                market_performance.sector_performance_snapshot,
                {"apikey": "invalid", "date": test_date},
            ),
            (
                market_performance.industry_performance_snapshot,
                {"apikey": "invalid", "date": test_date},
            ),
            (
                market_performance.historical_sector_performance,
                {"apikey": "invalid", "sector": "Technology"},
            ),
            (
                market_performance.historical_industry_performance,
                {"apikey": "invalid", "industry": "Software"},
            ),
            (
                market_performance.sector_pe_snapshot,
                {"apikey": "invalid", "date": test_date},
            ),
            (
                market_performance.industry_pe_snapshot,
                {"apikey": "invalid", "date": test_date},
            ),
            (
                market_performance.historical_sector_pe,
                {"apikey": "invalid", "sector": "Technology"},
            ),
            (
                market_performance.historical_industry_pe,
                {"apikey": "invalid", "industry": "Software"},
            ),
            (market_performance.biggest_gainers, {"apikey": "invalid"}),
            (market_performance.biggest_losers, {"apikey": "invalid"}),
            (market_performance.most_active_stocks, {"apikey": "invalid"}),
        ]

        for func, params in functions_and_params:
            # Invalid API keys should raise InvalidAPIKeyException
            with pytest.raises(InvalidAPIKeyException):
                func(**params)
