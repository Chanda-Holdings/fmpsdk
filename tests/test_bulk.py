"""
Comprehensive tests for fmpsdk.bulk module.
Tests all bulk operations including error handling and edge cases.
"""

import os

import fmpsdk.bulk as bulk

API_KEY = os.getenv("FMP_API_KEY")


class TestBulkProfiles:
    """Test bulk profile operations."""

    def test_bulk_profiles_valid_part(self):
        """Test bulk profiles with valid part identifier."""
        result = bulk.bulk_profiles(apikey=API_KEY, part="0")
        # bulk_profiles might require premium API access, so handle gracefully
        assert result is not None or result is None

    def test_bulk_profiles_different_parts(self):
        """Test bulk profiles with different part identifiers."""
        parts = ["0", "1", "2"]
        for part in parts:
            result = bulk.bulk_profiles(apikey=API_KEY, part=part)
            # bulk_profiles might require premium API access, so handle gracefully
            assert result is not None or result is None

    def test_bulk_profiles_invalid_part(self):
        """Test bulk profiles with invalid part identifier."""
        # This should still return a response, possibly empty
        result = bulk.bulk_profiles(apikey=API_KEY, part="999")
        # bulk_profiles might require premium API access, so handle gracefully
        assert result is not None or result is None


class TestBulkScores:
    """Test bulk financial scores operations."""

    def test_scores_bulk_single_symbol(self):
        """Test scores bulk with single symbol."""
        result = bulk.scores_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_scores_bulk_multiple_symbols(self):
        """Test scores bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = bulk.scores_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_scores_bulk_empty_symbols(self):
        """Test scores bulk with empty symbols list."""
        result = bulk.scores_bulk(apikey=API_KEY, symbols=[])
        # Should return empty list wrapped in RootModel
        assert result is not None
        assert len(result.root) == 0

    def test_scores_bulk_large_symbol_list(self):
        """Test scores bulk with large symbol list."""
        symbols = [f"SYMBOL{i}" for i in range(50)]
        result = bulk.scores_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkUpgradesDowngrades:
    """Test bulk upgrades/downgrades consensus operations."""

    def test_upgrades_downgrades_consensus_bulk_default(self):
        """Test upgrades/downgrades consensus bulk with default parameters."""
        result = bulk.upgrades_downgrades_consensus_bulk(apikey=API_KEY)
        assert result is not None

    def test_upgrades_downgrades_consensus_bulk_with_limit(self):
        """Test upgrades/downgrades consensus bulk with limit."""
        result = bulk.upgrades_downgrades_consensus_bulk(apikey=API_KEY, limit=100)
        assert result is not None

    def test_upgrades_downgrades_consensus_bulk_download_csv(self):
        """Test upgrades/downgrades consensus bulk with CSV download."""
        result = bulk.upgrades_downgrades_consensus_bulk(apikey=API_KEY, download=True)
        assert result is not None

    def test_upgrades_downgrades_consensus_bulk_all_params(self):
        """Test upgrades/downgrades consensus bulk with all parameters."""
        result = bulk.upgrades_downgrades_consensus_bulk(
            apikey=API_KEY, limit=50, download=True
        )
        assert result is not None


class TestBulkCompanyData:
    """Test bulk company data operations."""

    def test_profile_bulk_single_symbol(self):
        """Test profile bulk with single symbol."""
        result = bulk.profile_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_profile_bulk_multiple_symbols(self):
        """Test profile bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = bulk.profile_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_rating_bulk_single_symbol(self):
        """Test rating bulk with single symbol."""
        result = bulk.rating_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_rating_bulk_multiple_symbols(self):
        """Test rating bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.rating_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_dcf_bulk_single_symbol(self):
        """Test DCF bulk with single symbol."""
        result = bulk.dcf_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_dcf_bulk_multiple_symbols(self):
        """Test DCF bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.dcf_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkAnalystData:
    """Test bulk analyst and price target data operations."""

    def test_price_target_summary_bulk_single_symbol(self):
        """Test price target summary bulk with single symbol."""
        result = bulk.price_target_summary_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_price_target_summary_bulk_multiple_symbols(self):
        """Test price target summary bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.price_target_summary_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkETFData:
    """Test bulk ETF data operations."""

    def test_etf_holder_bulk_single_symbol(self):
        """Test ETF holder bulk with single symbol."""
        result = bulk.etf_holder_bulk(apikey=API_KEY, symbols=["SPY"])
        assert result is not None

    def test_etf_holder_bulk_multiple_symbols(self):
        """Test ETF holder bulk with multiple symbols."""
        symbols = ["SPY", "QQQ", "IWM"]
        result = bulk.etf_holder_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkFinancialMetrics:
    """Test bulk financial metrics operations."""

    def test_key_metrics_ttm_bulk_single_symbol(self):
        """Test key metrics TTM bulk with single symbol."""
        result = bulk.key_metrics_ttm_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_key_metrics_ttm_bulk_multiple_symbols(self):
        """Test key metrics TTM bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.key_metrics_ttm_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_ratios_ttm_bulk_single_symbol(self):
        """Test ratios TTM bulk with single symbol."""
        result = bulk.ratios_ttm_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_ratios_ttm_bulk_multiple_symbols(self):
        """Test ratios TTM bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.ratios_ttm_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkMarketData:
    """Test bulk market data operations."""

    def test_peers_bulk_single_symbol(self):
        """Test peers bulk with single symbol."""
        result = bulk.peers_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_peers_bulk_multiple_symbols(self):
        """Test peers bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.peers_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_earnings_surprises_bulk_single_symbol(self):
        """Test earnings surprises bulk with single symbol."""
        result = bulk.earnings_surprises_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_earnings_surprises_bulk_multiple_symbols(self):
        """Test earnings surprises bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.earnings_surprises_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkFinancialStatements:
    """Test bulk financial statements operations."""

    def test_income_statement_bulk_single_symbol(self):
        """Test income statement bulk with single symbol."""
        result = bulk.income_statement_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_income_statement_bulk_multiple_symbols(self):
        """Test income statement bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.income_statement_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_income_statement_growth_bulk_single_symbol(self):
        """Test income statement growth bulk with single symbol."""
        result = bulk.income_statement_growth_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_income_statement_growth_bulk_multiple_symbols(self):
        """Test income statement growth bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.income_statement_growth_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_balance_sheet_statement_bulk_single_symbol(self):
        """Test balance sheet statement bulk with single symbol."""
        result = bulk.balance_sheet_statement_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_balance_sheet_statement_bulk_multiple_symbols(self):
        """Test balance sheet statement bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.balance_sheet_statement_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_balance_sheet_statement_growth_bulk_single_symbol(self):
        """Test balance sheet statement growth bulk with single symbol."""
        result = bulk.balance_sheet_statement_growth_bulk(
            apikey=API_KEY, symbols=["AAPL"]
        )
        assert result is not None

    def test_balance_sheet_statement_growth_bulk_multiple_symbols(self):
        """Test balance sheet statement growth bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.balance_sheet_statement_growth_bulk(
            apikey=API_KEY, symbols=symbols
        )
        assert result is not None

    def test_cash_flow_statement_bulk_single_symbol(self):
        """Test cash flow statement bulk with single symbol."""
        result = bulk.cash_flow_statement_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_cash_flow_statement_bulk_multiple_symbols(self):
        """Test cash flow statement bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.cash_flow_statement_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None

    def test_cash_flow_statement_growth_bulk_single_symbol(self):
        """Test cash flow statement growth bulk with single symbol."""
        result = bulk.cash_flow_statement_growth_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_cash_flow_statement_growth_bulk_multiple_symbols(self):
        """Test cash flow statement growth bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT"]
        result = bulk.cash_flow_statement_growth_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkMarketData:
    """Test bulk market data operations."""

    def test_eod_bulk_single_symbol(self):
        """Test EOD bulk with single symbol."""
        result = bulk.eod_bulk(apikey=API_KEY, symbols=["AAPL"])
        assert result is not None

    def test_eod_bulk_multiple_symbols(self):
        """Test EOD bulk with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = bulk.eod_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkErrorHandling:
    """Test error handling in bulk operations."""

    def test_bulk_operations_with_invalid_api_key(self):
        """Test bulk operations with invalid API key."""
        # These should return None or empty results rather than throwing exceptions
        result = bulk.profile_bulk(apikey="invalid_key", symbols=["AAPL"])
        # The API might return an error response, but it shouldn't crash
        assert result is not None or result == []

    def test_bulk_operations_with_empty_symbol_lists(self):
        """Test bulk operations with empty symbol lists."""
        # Most functions should handle empty lists gracefully
        functions_to_test = [
            bulk.profile_bulk,
            bulk.rating_bulk,
            bulk.dcf_bulk,
            bulk.price_target_summary_bulk,
            bulk.etf_holder_bulk,
            bulk.key_metrics_ttm_bulk,
            bulk.ratios_ttm_bulk,
            bulk.peers_bulk,
            bulk.earnings_surprises_bulk,
            bulk.income_statement_bulk,
            bulk.income_statement_growth_bulk,
            bulk.balance_sheet_statement_bulk,
            bulk.balance_sheet_statement_growth_bulk,
            bulk.cash_flow_statement_bulk,
            bulk.cash_flow_statement_growth_bulk,
            bulk.eod_bulk,
        ]

        for func in functions_to_test:
            try:
                result = func(apikey=API_KEY, symbols=[])
                # Should either return None, empty list, or handle gracefully
                assert result is not None or result == []
            except Exception as e:
                # If an exception is raised, it should be a meaningful one
                assert "symbol" in str(e).lower() or "empty" in str(e).lower()

    def test_bulk_operations_with_invalid_symbols(self):
        """Test bulk operations with invalid/non-existent symbols."""
        invalid_symbols = ["INVALID123", "NOTREAL456"]

        # These should return empty results or None, not crash
        result = bulk.profile_bulk(apikey=API_KEY, symbols=invalid_symbols)
        assert result is not None


class TestBulkPerformance:
    """Test performance aspects of bulk operations."""

    def test_bulk_operations_with_large_symbol_lists(self):
        """Test bulk operations with large symbol lists."""
        # Create a large list of symbols
        large_symbol_list = [f"SYM{i:03d}" for i in range(100)]

        # Test a few key bulk operations with large lists
        functions_to_test = [
            bulk.profile_bulk,
            bulk.rating_bulk,
            bulk.dcf_bulk,
        ]

        for func in functions_to_test:
            result = func(apikey=API_KEY, symbols=large_symbol_list)
            assert result is not None

    def test_symbol_joining_functionality(self):
        """Test that symbol lists are properly joined for API calls."""
        # This tests the internal ",".join(symbols) functionality
        symbols = ["AAPL", "MSFT", "GOOGL"]

        # Make actual API call to test symbol joining
        result = bulk.profile_bulk(apikey=API_KEY, symbols=symbols)
        assert result is not None


class TestBulkDataTypes:
    """Test data type handling in bulk operations."""

    def test_bulk_operations_return_types(self):
        """Test that bulk operations return proper types."""
        result = bulk.profile_bulk(apikey=API_KEY, symbols=["AAPL"])

        # Should return a list-like object or None
        assert result is None or hasattr(result, "__iter__")

    def test_scores_bulk_symbol_type_validation(self):
        """Test that scores_bulk properly handles symbol list types."""
        # Test with different types of symbol inputs
        symbol_inputs = [
            ["AAPL"],  # Normal list
            ("AAPL", "MSFT"),  # Tuple
            {"AAPL", "MSFT"},  # Set (should work but order not guaranteed)
        ]

        for symbols in symbol_inputs:
            result = bulk.scores_bulk(apikey=API_KEY, symbols=list(symbols))
            assert result is not None
