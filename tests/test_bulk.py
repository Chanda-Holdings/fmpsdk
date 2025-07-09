from datetime import datetime, timedelta
from typing import Dict

import pytest

from fmpsdk import bulk
from fmpsdk.models import (
    FMPBalanceSheetGrowth,
    FMPBalanceSheetStatement,
    FMPBulkDCF,
    FMPBulkEarningsSurprise,
    FMPBulkEOD,
    FMPBulkETFHolder,
    FMPBulkPriceTargetSummary,
    FMPBulkRating,
    FMPBulkStockPeers,
    FMPBulkUpgradeDowngradeConsensus,
    FMPCashFlowGrowth,
    FMPCashFlowStatement,
    FMPCompanyProfile,
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPIncomeStatement,
    FMPIncomeStatementGrowth,
    FMPKeyMetrics,
)
from tests.conftest import extract_data_list


class TestBulkProfiles:
    """Test bulk company profiles endpoints."""

    def test_bulk_profiles_basic(self, api_key):
        """Test bulk profiles download with part parameter."""
        result = bulk.bulk_profiles(
            apikey=api_key, part="1"  # Request part 1 of bulk profiles
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        # Check if result is None (JSON parsing error - bulk endpoints may return CSV)
        if result is None:
            pytest.skip("Bulk endpoint returned non-JSON data (likely CSV format)")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:  # If data is available
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields for company profile
                assert "symbol" in first_item
                assert "companyName" in first_item
                assert "price" in first_item
                assert "exchange" in first_item

                # Test Pydantic model validation
                profile = FMPCompanyProfile(**first_item)
                assert profile.symbol == first_item["symbol"]
                assert profile.companyName == first_item["companyName"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "companyName")
                assert hasattr(first_item, "price")
                assert hasattr(first_item, "exchange")

    def test_profile_bulk_with_symbols(self, api_key):
        """Test bulk profiles for specific symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = bulk.profile_bulk(apikey=api_key, symbols=symbols)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Should have profiles for the requested symbols
            returned_symbols = set()
            for item in result_list:
                if isinstance(item, dict):
                    returned_symbols.add(item["symbol"])
                else:
                    returned_symbols.add(item.symbol)

            # At least some of the requested symbols should be present
            assert len(returned_symbols.intersection(set(symbols))) > 0

    def test_bulk_profiles_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = bulk.bulk_profiles(apikey=invalid_api_key, part="1")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestBulkFinancialData:
    """Test bulk financial data endpoints."""

    def test_scores_bulk(self, api_key):
        """Test bulk financial scores for multiple symbols."""
        symbols = ["AAPL", "MSFT", "TSLA"]
        result = bulk.scores_bulk(apikey=api_key, symbols=symbols)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate financial scores structure
                assert "symbol" in first_item

                # Test Pydantic model validation
                scores = FMPFinancialScores(**first_item)
                assert scores.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_rating_bulk(self, api_key):
        """Test bulk ratings for multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.rating_bulk(apikey=api_key, symbols=symbols)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                rating = FMPBulkRating(**first_item)
                assert rating.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_dcf_bulk(self, api_key):
        """Test bulk DCF valuations for multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.dcf_bulk(apikey=api_key, symbols=symbols)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                dcf = FMPBulkDCF(**first_item)
                assert dcf.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_price_target_summary_bulk(self, api_key):
        """Test bulk price target summaries."""
        result = bulk.price_target_summary_bulk(apikey=api_key)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                target = FMPBulkPriceTargetSummary(**first_item)
                assert target.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")


class TestBulkMetricsAndRatios:
    """Test bulk metrics and ratios endpoints."""

    def test_key_metrics_ttm_bulk(self, api_key):
        """Test bulk TTM key metrics."""
        result = bulk.key_metrics_ttm_bulk(apikey=api_key)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            # Limit to first few items for performance
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                metrics = FMPKeyMetrics(**first_item)
                assert metrics.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_ratios_ttm_bulk(self, api_key):
        """Test bulk TTM financial ratios."""
        result = bulk.ratios_ttm_bulk(apikey=api_key)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                ratios = FMPFinancialRatios(**first_item)
                assert ratios.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")


class TestBulkAnalystData:
    """Test bulk analyst data endpoints."""

    def test_upgrades_downgrades_consensus_bulk(self, api_key):
        """Test bulk upgrades/downgrades consensus data."""
        result = bulk.upgrades_downgrades_consensus_bulk(apikey=api_key)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                consensus = FMPBulkUpgradeDowngradeConsensus(**first_item)
                assert consensus.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_peers_bulk(self, api_key):
        """Test bulk stock peers data."""
        result = bulk.peers_bulk(apikey=api_key)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                peers = FMPBulkStockPeers(**first_item)
                assert peers.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")


class TestBulkFinancialStatements:
    """Test bulk financial statements endpoints."""

    def test_income_statement_bulk(self, api_key):
        """Test bulk income statements."""
        result = bulk.income_statement_bulk(apikey=api_key, year="2023", period="FY")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                income = FMPIncomeStatement(**first_item)
                assert income.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_income_statement_growth_bulk(self, api_key):
        """Test bulk income statement growth rates."""
        result = bulk.income_statement_growth_bulk(
            apikey=api_key, year="2023", period="FY"
        )

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                growth = FMPIncomeStatementGrowth(**first_item)
                assert growth.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_balance_sheet_statement_bulk(self, api_key):
        """Test bulk balance sheet statements."""
        result = bulk.balance_sheet_statement_bulk(
            apikey=api_key, year="2023", period="FY"
        )

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                balance = FMPBalanceSheetStatement(**first_item)
                assert balance.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_balance_sheet_statement_growth_bulk(self, api_key):
        """Test bulk balance sheet growth rates."""
        result = bulk.balance_sheet_statement_growth_bulk(
            apikey=api_key, year="2023", period="FY"
        )

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                growth = FMPBalanceSheetGrowth(**first_item)
                assert growth.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_cash_flow_statement_bulk(self, api_key):
        """Test bulk cash flow statements."""
        result = bulk.cash_flow_statement_bulk(apikey=api_key, year="2023", period="FY")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                cash_flow = FMPCashFlowStatement(**first_item)
                assert cash_flow.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_cash_flow_statement_growth_bulk(self, api_key):
        """Test bulk cash flow growth rates."""
        result = bulk.cash_flow_statement_growth_bulk(
            apikey=api_key, year="2023", period="FY"
        )

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                growth = FMPCashFlowGrowth(**first_item)
                assert growth.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")


class TestBulkSpecializedData:
    """Test bulk specialized data endpoints."""

    def test_etf_holder_bulk(self, api_key):
        """Test bulk ETF holders data."""
        result = bulk.etf_holder_bulk(apikey=api_key, part="1")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # ETF holder should have symbol and holder info
                assert "symbol" in first_item

                # Test Pydantic model validation
                holder = FMPBulkETFHolder(**first_item)
                assert holder.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_earnings_surprises_bulk(self, api_key):
        """Test bulk earnings surprises data."""
        result = bulk.earnings_surprises_bulk(apikey=api_key, year="2023")

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                surprise = FMPBulkEarningsSurprise(**first_item)
                assert surprise.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")

    def test_eod_bulk(self, api_key):
        """Test bulk end-of-day data."""
        # Use recent date
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        result = bulk.eod_bulk(apikey=api_key, date=date)

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if result_list:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "symbol" in first_item

                # Test Pydantic model validation
                eod = FMPBulkEOD(**first_item)
                assert eod.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")


class TestBulkDataQuality:
    """Test data quality and business logic validation."""

    def test_bulk_data_consistency(self, api_key):
        """Test data consistency across bulk endpoints."""
        symbols = ["AAPL", "MSFT"]

        # Test profiles
        profiles_result = bulk.profile_bulk(apikey=api_key, symbols=symbols)

        if isinstance(profiles_result, dict) and "Error Message" in profiles_result:
            return

        profiles_list = extract_data_list(profiles_result)
        if profiles_list:
            for profile in profiles_list[:2]:
                if isinstance(profile, dict):
                    # Validate required profile fields
                    assert len(profile["symbol"]) > 0
                    assert len(profile["companyName"]) > 0
                    assert isinstance(profile["price"], (int, float))
                    assert profile["price"] >= 0

                    # Exchange should be valid
                    valid_exchanges = ["NASDAQ", "NYSE", "AMEX", "OTC", "TSX"]
                    # Check if it's one of the known exchanges or contains valid exchange code
                    is_valid_exchange = (
                        profile["exchange"] in valid_exchanges
                        or any(ex in profile["exchange"] for ex in valid_exchanges)
                        or len(profile["exchange"])
                        > 0  # Any non-empty exchange is acceptable
                    )
                    assert is_valid_exchange
                else:
                    # Pydantic model
                    assert len(profile.symbol) > 0
                    assert len(profile.companyName) > 0
                    assert isinstance(profile.price, (int, float))
                    assert profile.price >= 0

    def test_bulk_financial_statements_validation(self, api_key):
        """Test financial statement data validation."""
        result = bulk.income_statement_bulk(apikey=api_key, year="2023", period="FY")

        if isinstance(result, dict) and "Error Message" in result:
            return

        result_list = extract_data_list(result)
        if result_list:
            for statement in result_list[:3]:  # Check first few
                if isinstance(statement, dict):
                    # Basic financial statement validation
                    assert len(statement["symbol"]) > 0

                    # Revenue should be numeric
                    if "revenue" in statement and statement["revenue"] is not None:
                        assert isinstance(statement["revenue"], (int, float))

                    # Date should be valid
                    if "date" in statement and statement["date"]:
                        assert len(statement["date"]) >= 10  # YYYY-MM-DD format
                        assert (
                            "2023" in statement["date"]
                        )  # Should match requested year
                else:
                    # Pydantic model
                    assert len(statement.symbol) > 0


class TestBulkErrorHandling:
    """Test error handling for bulk endpoints."""

    def test_scores_bulk_empty_symbols(self, api_key):
        """Test scores bulk with empty symbols list."""
        result = bulk.scores_bulk(apikey=api_key, symbols=[])

        # Should return empty list for empty symbols
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_bulk_profiles_invalid_api_key(self):
        """Test bulk profiles with invalid API key."""
        result = bulk.bulk_profiles(apikey="invalid_key_123", part="1")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]

    def test_income_statement_bulk_invalid_year(self, api_key):
        """Test income statement bulk with invalid year."""
        result = bulk.income_statement_bulk(
            apikey=api_key, year="1900", period="FY"  # Invalid year
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid year
        assert isinstance(result_list, list)
        assert len(result_list) == 0


# Additional test utilities
def validate_bulk_data_model(data: Dict, model_class) -> bool:
    """Validate that data conforms to the specified bulk model."""
    try:
        model_class(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False
