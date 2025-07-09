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

from .conftest import extract_data_list


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

    def test_sector_performance_snapshot(self, api_key):
        """Test sector performance snapshot."""
        test_date = get_test_date()
        result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                sector_data = FMPSectorPerformanceSnapshot(**first_item)
            else:
                sector_data = first_item
            assert hasattr(sector_data, "sector") or hasattr(
                sector_data, "sectorName"
            ), "Should have sector field"

    def test_sector_performance_with_exchange(self, api_key):
        """Test sector performance with exchange filter."""
        test_date = get_test_date()
        result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=test_date, exchange="NASDAQ"
        )
        result_list = extract_data_list(result)
        assert isinstance(result_list, list), "Response should be a list"

    def test_historical_sector_performance(self, api_key):
        """Test historical sector performance."""
        result = market_performance.historical_sector_performance(
            apikey=api_key, sector="Technology"
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                historical_data = FMPHistoricalSectorPerformance(**first_item)
            else:
                historical_data = first_item
            assert hasattr(historical_data, "date") or hasattr(
                historical_data, "sector"
            ), "Should have date or sector field"

    def test_sector_pe_snapshot(self, api_key):
        """Test sector PE snapshot."""
        test_date = get_test_date()
        result = market_performance.sector_pe_snapshot(apikey=api_key, date=test_date)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                pe_data = FMPSectorPESnapshot(**first_item)
            else:
                pe_data = first_item
            assert hasattr(pe_data, "sector") or hasattr(
                pe_data, "pe"
            ), "Should have sector or PE field"

    def test_historical_sector_pe(self, api_key):
        """Test historical sector PE."""
        result = market_performance.historical_sector_pe(
            apikey=api_key, sector="Technology"
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                historical_pe = FMPHistoricalSectorPE(**first_item)
            else:
                historical_pe = first_item
            assert hasattr(historical_pe, "date") or hasattr(
                historical_pe, "sector"
            ), "Should have date or sector field"


class TestIndustryPerformance:
    """Test industry performance functions."""

    def test_industry_performance_snapshot(self, api_key):
        """Test industry performance snapshot."""
        test_date = get_test_date()
        result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=test_date
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                industry_data = FMPIndustryPerformanceSnapshot(**first_item)
            else:
                industry_data = first_item
            assert hasattr(industry_data, "industry") or hasattr(
                industry_data, "industryName"
            ), "Should have industry field"

    def test_historical_industry_performance(self, api_key):
        """Test historical industry performance."""
        result = market_performance.historical_industry_performance(
            apikey=api_key, industry="Software"
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                historical_data = FMPHistoricalIndustryPerformance(**first_item)
            else:
                historical_data = first_item
            assert hasattr(historical_data, "date") or hasattr(
                historical_data, "industry"
            ), "Should have date or industry field"

    def test_industry_pe_snapshot(self, api_key):
        """Test industry PE snapshot."""
        test_date = get_test_date()
        result = market_performance.industry_pe_snapshot(apikey=api_key, date=test_date)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                pe_data = FMPIndustryPESnapshot(**first_item)
            else:
                pe_data = first_item
            assert hasattr(pe_data, "industry") or hasattr(
                pe_data, "pe"
            ), "Should have industry or PE field"

    def test_historical_industry_pe(self, api_key):
        """Test historical industry PE."""
        result = market_performance.historical_industry_pe(
            apikey=api_key, industry="Software"
        )
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                historical_pe = FMPHistoricalIndustryPE(**first_item)
            else:
                historical_pe = first_item
            assert hasattr(historical_pe, "date") or hasattr(
                historical_pe, "industry"
            ), "Should have date or industry field"


class TestMarketMovers:
    """Test market mover functions."""

    def test_biggest_gainers(self, api_key):
        """Test biggest gainers."""
        result = market_performance.biggest_gainers(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                gainer = FMPMarketMover(**first_item)
            else:
                gainer = first_item

            assert hasattr(gainer, "symbol"), "Should have symbol field"
            # Gainers should have positive change (when data is available)
            if (
                hasattr(gainer, "changePercentage")
                and gainer.changePercentage is not None
            ):
                assert (
                    float(gainer.changePercentage) > 0
                ), "Biggest gainers should have positive change"

    def test_biggest_losers(self, api_key):
        """Test biggest losers."""
        result = market_performance.biggest_losers(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                loser = FMPMarketMover(**first_item)
            else:
                loser = first_item

            assert hasattr(loser, "symbol"), "Should have symbol field"
            # Losers should have negative change (when data is available)
            if (
                hasattr(loser, "changePercentage")
                and loser.changePercentage is not None
            ):
                assert (
                    float(loser.changePercentage) < 0
                ), "Biggest losers should have negative change"

    def test_most_active_stocks(self, api_key):
        """Test most active stocks."""
        result = market_performance.most_active_stocks(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                active_stock = FMPMarketMover(**first_item)
            else:
                active_stock = first_item

            assert hasattr(active_stock, "symbol"), "Should have symbol field"
            # Most active stocks should have volume data
            if hasattr(active_stock, "volume") and active_stock.volume is not None:
                assert (
                    int(active_stock.volume) > 0
                ), "Most active stocks should have positive volume"


class TestMarketPerformanceComprehensive:
    """Comprehensive market performance tests."""

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

        # All should return lists
        assert isinstance(extract_data_list(snapshot_result), list)
        assert isinstance(extract_data_list(historical_result), list)
        assert isinstance(extract_data_list(pe_snapshot_result), list)
        assert isinstance(extract_data_list(historical_pe_result), list)

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

        # All should return lists
        assert isinstance(extract_data_list(snapshot_result), list)
        assert isinstance(extract_data_list(historical_result), list)
        assert isinstance(extract_data_list(pe_snapshot_result), list)
        assert isinstance(extract_data_list(historical_pe_result), list)

    def test_market_mover_functions_consistency(self, api_key):
        """Test that all market mover functions work consistently."""
        gainers_result = market_performance.biggest_gainers(apikey=api_key)
        losers_result = market_performance.biggest_losers(apikey=api_key)
        active_result = market_performance.most_active_stocks(apikey=api_key)

        # All should return lists
        assert isinstance(extract_data_list(gainers_result), list)
        assert isinstance(extract_data_list(losers_result), list)
        assert isinstance(extract_data_list(active_result), list)

    def test_response_times(self, api_key):
        """Test that all functions respond within reasonable time."""
        test_date = get_test_date()

        functions_and_params = [
            (
                market_performance.sector_performance_snapshot,
                {"apikey": api_key, "date": test_date},
            ),
            (
                market_performance.industry_performance_snapshot,
                {"apikey": api_key, "date": test_date},
            ),
            (market_performance.biggest_gainers, {"apikey": api_key}),
            (market_performance.biggest_losers, {"apikey": api_key}),
            (market_performance.most_active_stocks, {"apikey": api_key}),
        ]

        for func, params in functions_and_params:
            start_time = time.time()
            result = func(**params)
            extract_data_list(result)
            response_time = time.time() - start_time

            assert (
                response_time < 15.0
            ), f"{func.__name__} took {response_time:.2f}s, expected < 15.0s"

    def test_date_validation(self, api_key):
        """Test functions with different date formats."""
        # Test recent date
        recent_date = get_test_date()

        snapshot_result = market_performance.sector_performance_snapshot(
            apikey=api_key, date=recent_date
        )
        assert isinstance(extract_data_list(snapshot_result), list)

        industry_result = market_performance.industry_performance_snapshot(
            apikey=api_key, date=recent_date
        )
        assert isinstance(extract_data_list(industry_result), list)

    def test_sector_and_industry_names(self, api_key):
        """Test with different sector and industry names."""
        test_date = get_test_date()

        # Test different sectors
        sectors = ["Technology", "Healthcare", "Financials", "Energy"]
        for sector in sectors:
            result = market_performance.historical_sector_performance(
                apikey=api_key, sector=sector
            )
            assert isinstance(
                extract_data_list(result), list
            ), f"Failed for sector: {sector}"

        # Test different industries
        industries = ["Software", "Pharmaceuticals", "Banking", "Oil & Gas"]
        for industry in industries:
            result = market_performance.historical_industry_performance(
                apikey=api_key, industry=industry
            )
            assert isinstance(
                extract_data_list(result), list
            ), f"Failed for industry: {industry}"

    def test_invalid_api_keys(self):
        """Test all functions with invalid API keys."""
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
            result = func(**params)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"{func.__name__} should return list with invalid key"
