import pytest

from fmpsdk import company
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPCompanyNote,
    FMPCompanyProfile,
    FMPDelistedCompany,
    FMPEmployeeCount,
    FMPExecutiveCompensation,
    FMPExecutiveProfile,
    FMPHistoricalEmployeeCount,
    FMPMarketCap,
    FMPMergerAcquisition,
    FMPShareFloat,
    FMPStockPeer,
)
from tests.conftest import (
    get_response_models,
    validate_model_list,
    validate_required_fields,
)


class TestCompanyProfile:
    """Tests for company profile functions."""

    def test_company_profile_valid_symbol(self, api_key):
        """Test company profile with valid symbol using enhanced validation."""
        response = company.company_profile(apikey=api_key, symbol="AAPL")

        models = get_response_models(response, FMPCompanyProfile)
        validate_model_list(models, FMPCompanyProfile, min_count=1)

        # Check specific fields using the validated data
        first_model = models[0]
        assert first_model.symbol == "AAPL"
        assert first_model.companyName is not None
        assert first_model.industry is not None
        assert first_model.sector is not None
        assert first_model.exchange is not None
        assert first_model.currency is not None

    @pytest.mark.parametrize(
        "symbol,market_cap_threshold",
        [
            ("AAPL", 1000000000000),  # $1T+
            ("MSFT", 1000000000000),  # $1T+
            ("GOOGL", 500000000000),  # $500B+
            ("AMZN", 500000000000),  # $500B+
            ("NVDA", 500000000000),  # $500B+
        ],
    )
    def test_company_profile_large_cap_stocks(
        self, api_key, symbol, market_cap_threshold
    ):
        """Test company profile for major large cap stocks with enhanced validation."""
        response = company.company_profile(apikey=api_key, symbol=symbol)

        models = get_response_models(response, FMPCompanyProfile)
        validate_model_list(models, FMPCompanyProfile, min_count=1)

        # Validate first result with automatic model validation
        first_model = models[0]
        assert first_model.symbol == symbol
        
        # Check market cap threshold
        if first_model.mktCap is not None:
            assert first_model.mktCap > market_cap_threshold

    def test_company_profile_invalid_symbol(self, api_key):
        """Test company profile with invalid symbol."""
        response = company.company_profile(apikey=api_key, symbol="INVALID999")

        models = get_response_models(response, FMPCompanyProfile)
        validate_model_list(models, FMPCompanyProfile)
        # Should return empty list for invalid symbol
        assert isinstance(models, list)

    def test_company_profile_cik_valid(self, api_key):
        """Test company profile by CIK number with validation."""
        # Apple's CIK
        response = company.company_profile_cik(apikey=api_key, cik="0000320193")

        models = get_response_models(response, FMPCompanyProfile)
        validate_model_list(models, FMPCompanyProfile)

        if models:
            first_model = models[0]
            assert first_model.cik == "0000320193"

    def test_company_profile_cik_invalid(self, api_key):
        """Test company profile with invalid CIK."""
        from fmpsdk.exceptions import InvalidQueryParameterException
        
        with pytest.raises(InvalidQueryParameterException):
            company.company_profile_cik(apikey=api_key, cik="INVALID")


class TestCompanyNotes:
    """Tests for company_notes function."""

    def test_company_notes_valid_symbol(self, api_key):
        """Test company notes with valid symbol using enhanced validation."""
        response = company.company_notes(apikey=api_key, symbol="AAPL")

        models = get_response_models(response, FMPCompanyNote)
        validate_model_list(models, FMPCompanyNote)

        # If we have notes, validate them
        if models:
            first_model = models[0]
            # The model validation is automatic, but we can add business logic
            assert first_model.symbol is not None
            assert first_model.cik is not None

    def test_company_notes_multiple_symbols(self, api_key):
        """Test company notes with multiple symbols."""
        for symbol in ["AAPL", "MSFT", "GOOGL"]:
            response = company.company_notes(apikey=api_key, symbol=symbol)
            
            models = get_response_models(response, FMPCompanyNote)
            validate_model_list(models, FMPCompanyNote)


class TestStockPeers:
    """Tests for stock_peers function."""

    def test_stock_peers_valid_symbol(self, api_key):
        """Test stock peers with valid symbol using enhanced validation."""
        response = company.stock_peers(apikey=api_key, symbol="AAPL")

        models = get_response_models(response, FMPStockPeer)
        validate_model_list(models, FMPStockPeer)

        # If we have peers, validate them
        if models:
            for peer in models:
                # Automatic model validation + business logic
                assert peer.symbol is not None
                assert peer.companyName is not None
                if peer.price is not None:
                    assert isinstance(peer.price, (int, float))
                    assert peer.price >= 0

    @pytest.mark.parametrize(
        "sector,symbols,expected_peer_count",
        [
            ("technology", ["AAPL", "MSFT", "GOOGL"], 3),
            ("financial", ["JPM", "BAC", "WFC"], 3),
            ("healthcare", ["JNJ", "UNH", "PFE"], 3),
        ],
    )
    def test_stock_peers_by_sector(self, api_key, sector, symbols, expected_peer_count):
        """Test stock peers across different sectors with validation."""
        for symbol in symbols:
            response = company.stock_peers(apikey=api_key, symbol=symbol)
            
            models = get_response_models(response, FMPStockPeer)
            validate_model_list(models, FMPStockPeer)

            # Validate peer count if we have data
            if models:
                # Should have at least one peer
                assert len(models) >= 1


class TestMarketCapitalization:
    """Tests for market capitalization functions."""

    def test_market_capitalization_single_symbol(self, api_key):
        """Test market capitalization with single symbol using enhanced validation."""
        response = company.market_capitalization(apikey=api_key, symbol="AAPL")

        models = get_response_models(response, FMPMarketCap)
        validate_model_list(models, FMPMarketCap, min_count=1)

        # Validate market cap data
        first_model = models[0]
        assert first_model.symbol == "AAPL"
        
        assert first_model.marketCap is not None
        assert isinstance(first_model.marketCap, (int, float))
        assert first_model.marketCap > 0

    def test_market_capitalization_batch(self, api_key):
        """Test batch market capitalization with enhanced validation."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        
        response = company.market_capitalization_batch(apikey=api_key, symbols=symbols)

        models = get_response_models(response, FMPMarketCap)
        validate_model_list(models, FMPMarketCap, min_count=1)

        # Should have data for multiple symbols
        returned_symbols = [model.symbol for model in models]
        for symbol in symbols:
            # Check if symbol appears in results (some may not have data)
            if symbol in returned_symbols:
                symbol_data = next(model for model in models if model.symbol == symbol)
                assert symbol_data.marketCap is not None
                assert isinstance(symbol_data.marketCap, (int, float))
                assert symbol_data.marketCap > 0


class TestEmployeeCount:
    """Tests for employee count functions."""

    def test_employee_count_valid_symbol(self, api_key):
        """Test employee count with valid symbol using enhanced validation."""
        response = company.employee_count(apikey=api_key, symbol="AAPL")

        models = get_response_models(response, FMPEmployeeCount)
        validate_model_list(models, FMPEmployeeCount)

        # If we have employee data, validate it
        if models:
            first_model = models[0]
            assert first_model.symbol == "AAPL"
            
            if first_model.employeeCount is not None:
                assert isinstance(first_model.employeeCount, (int, float))
                assert first_model.employeeCount > 0


class TestCompanyErrorHandling:
    """Tests for error handling in company functions."""

    def test_company_profile_invalid_api_key(self):
        """Test company profile with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            company.company_profile(apikey="invalid_key", symbol="AAPL")

    def test_company_profile_empty_symbol(self, api_key):
        """Test company profile with empty symbol."""
        from fmpsdk.exceptions import InvalidQueryParameterException
        
        with pytest.raises(InvalidQueryParameterException):
            company.company_profile(apikey=api_key, symbol="")


class TestCompanyDataConsistency:
    """Tests for data consistency across different company endpoints."""

    def test_profile_vs_market_cap_consistency(self, api_key):
        """Test consistency between profile and market cap data."""
        symbol = "AAPL"

        # Get profile data
        profile_response = company.company_profile(apikey=api_key, symbol=symbol)

        # Get market cap data
        market_cap_response = company.market_capitalization(apikey=api_key, symbol=symbol)

        profile_models = get_response_models(profile_response, FMPCompanyProfile)
        market_cap_models = get_response_models(market_cap_response, FMPMarketCap)

        if profile_models and market_cap_models:
            profile_model = profile_models[0]
            market_cap_model = market_cap_models[0]

            # Both should have the same symbol
            assert profile_model.symbol == market_cap_model.symbol
            
            # Market cap values should be reasonable
            profile_mkt_cap = profile_model.mktCap
            standalone_mkt_cap = market_cap_model.marketCap
            
            if profile_mkt_cap is not None and standalone_mkt_cap is not None:
                # Values should be in the same order of magnitude (allowing for timing differences)
                ratio = max(profile_mkt_cap, standalone_mkt_cap) / min(profile_mkt_cap, standalone_mkt_cap)
                assert ratio < 2.0  # Should not differ by more than 2x
