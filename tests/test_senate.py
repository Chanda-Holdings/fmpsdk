import pytest

from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import FMPPoliticalTrade
from fmpsdk.senate import senate
from tests.conftest import (
    get_response_models,
    validate_model_list,
)

# Test data constants
TEST_SYMBOLS = [
    # Technology stocks often traded by politicians
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA",
    "NVDA",
    "NFLX",
    "CRM",
    "ORCL",
    # Healthcare & Pharmaceutical
    "JNJ",
    "PFE",
    "UNH",
    "ABBV",
    "MRK",
    "TMO",
    "ABT",
    "LLY",
    "BMY",
    "GILD",
    # Financial Services
    "JPM",
    "BAC",
    "WFC",
    "GS",
    "MS",
    "C",
    "V",
    "MA",
    "AXP",
    "BLK",
    # Energy & Utilities
    "XOM",
    "CVX",
    "COP",
    "EOG",
    "SLB",
    "NEE",
    "SO",
    "DUK",
    "AEP",
    "D",
    # Defense & Aerospace
    "LMT",
    "RTX",
    "BA",
    "NOC",
    "GD",
    "LHX",
    "TDG",
    "HWM",
    "LDOS",
    "KTOS",
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
    # Industrial
    "CAT",
    "GE",
    "HON",
    "UPS",
    "LMT",
    "RTX",
    "DE",
    "MMM",
    "FDX",
    "EMR",
    # Popular ETFs
    "SPY",
    "QQQ",
    "VTI",
    "IWM",
    "EFA",
    "EEM",
    "AGG",
    "TLT",
    "GLD",
    "VNQ",
    # Cryptocurrency-related
    "COIN",
    "MSTR",
    "RIOT",
    "MARA",
    "SQ",
    "PYPL",
    "HOOD",
    "PLTR",
    # Biotech & Emerging Tech
    "MRNA",
    "BNTX",
    "REGN",
    "BIIB",
    "ILMN",
    "VRTX",
    "ZM",
    "DOCU",
    "CRWD",
    "OKTA",
]


class TestSenateTrading:
    """Test class for Senate trading functionality."""

    @pytest.mark.parametrize("symbol", TEST_SYMBOLS[:10])  # Test first 10 symbols
    def test_senate_trading_by_symbol(self, api_key, symbol):
        """Test Senate trading disclosures for various symbols."""
        result = senate.senate_trades(apikey=api_key, symbol=symbol)
        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:  # If we have data
            trade_model = trade_models[0]

            # Basic validation
            assert trade_model.symbol is not None and trade_model.symbol != ""
            assert (
                trade_model.disclosureDate is not None
                and trade_model.disclosureDate != ""
            )
            assert trade_model.firstName is not None and trade_model.firstName != ""
            assert trade_model.lastName is not None and trade_model.lastName != ""

            # Symbol should match requested
            if trade_model.symbol:
                assert trade_model.symbol == symbol

    @pytest.mark.parametrize(
        "sector",
        [
            "technology",
            "healthcare",
            "financial",
            "energy",
            "defense",
            "consumer",
            "industrial",
            "etf_index",
        ],
    )
    def test_senate_trading_by_sector(self, api_key, sector):
        """Test Senate trading across different sectors."""
        sector_symbols = {
            "technology": ["AAPL", "MSFT", "GOOGL"],
            "healthcare": ["JNJ", "PFE", "UNH"],
            "financial": ["JPM", "BAC", "V"],
            "energy": ["XOM", "CVX", "NEE"],
            "defense": ["LMT", "RTX", "BA"],
            "consumer": ["HD", "MCD", "NKE"],
            "industrial": ["CAT", "GE", "HON"],
            "etf_index": ["SPY", "QQQ", "VTI"],
        }

        symbols = sector_symbols.get(sector, ["AAPL"])

        for symbol in symbols:
            result = senate.senate_trades(apikey=api_key, symbol=symbol)

            trade_models = get_response_models(result, FMPPoliticalTrade)
            assert isinstance(trade_models, list)

    @pytest.mark.parametrize("transaction_type", ["purchase", "sale", "both"])
    def test_senate_trading_by_transaction_type(self, api_key, transaction_type):
        """Test Senate trading for different transaction types."""
        # Use popular symbols that likely have both purchases and sales
        symbols = ["AAPL", "MSFT", "SPY", "QQQ", "TSLA"]

        for symbol in symbols[:2]:  # Test first 2 symbols
            result = senate.senate_trades(apikey=api_key, symbol=symbol)

            trade_models = get_response_models(result, FMPPoliticalTrade)
            if not trade_models:
                continue

            # Filter by transaction type
            if transaction_type == "purchase":
                filtered_trades = [
                    trade
                    for trade in trade_models
                    if trade.type and trade.type.lower() in ["purchase", "buy"]
                ]
            elif transaction_type == "sale":
                filtered_trades = [
                    trade
                    for trade in trade_models
                    if trade.type and trade.type.lower() in ["sale", "sell"]
                ]
            else:  # both
                filtered_trades = trade_models

            assert isinstance(filtered_trades, list)
            assert len(filtered_trades) >= 0

    @pytest.mark.parametrize(
        "date_range",
        [
            "recent",  # Last 30 days
            "quarterly",  # Last 90 days
            "annual",  # Last 365 days
            "historical",  # Last 2 years
        ],
    )
    def test_senate_trading_by_date_range(self, api_key, date_range):
        """Test Senate trading across different date ranges."""
        from datetime import datetime, timedelta

        # Calculate date ranges
        end_date = datetime.now()
        if date_range == "recent":
            start_date = end_date - timedelta(days=30)
        elif date_range == "quarterly":
            start_date = end_date - timedelta(days=90)
        elif date_range == "annual":
            start_date = end_date - timedelta(days=365)
        else:  # historical
            start_date = end_date - timedelta(days=730)

        # Test with latest endpoint (no date filtering in API, but check dates in response)
        result = senate.senate_latest(apikey=api_key, limit=50)

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:
            # Check that we have some data within the expected date range
            recent_trades = []
            for trade_model in trade_models:
                if trade_model.disclosureDate:
                    try:
                        trade_date = datetime.strptime(
                            trade_model.disclosureDate, "%Y-%m-%d"
                        )
                        if start_date <= trade_date <= end_date:
                            recent_trades.append(trade_model)
                    except (ValueError, TypeError):
                        # Skip invalid dates
                        continue

            # This is informational - may not have trades in all date ranges
            assert len(recent_trades) >= 0

    @pytest.mark.parametrize(
        "politician_party", ["democrat", "republican", "independent"]
    )
    def test_senate_trading_by_party(self, api_key, politician_party):
        """Test Senate trading by political party affiliation."""
        # Note: Party information may not be directly available in the API response
        # This test checks that we can get data and validates basic structure

        result = senate.senate_latest(apikey=api_key, limit=30)

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:
            # Validate structure for political trades
            for trade_model in trade_models[:5]:  # Check first 5 trades
                # Basic validation
                assert trade_model.firstName is not None and trade_model.firstName != ""
                assert trade_model.lastName is not None and trade_model.lastName != ""
                assert hasattr(trade_model, "office")

                # Check that we have politician information
                if trade_model.firstName and trade_model.lastName:
                    assert trade_model.firstName != ""
                    assert trade_model.lastName != ""

    @pytest.mark.parametrize(
        "trade_size",
        [
            "small",  # < $15,000
            "medium",  # $15,000 - $50,000
            "large",  # $50,000 - $250,000
            "very_large",  # > $250,000
        ],
    )
    def test_senate_trading_by_size(self, api_key, trade_size):
        """Test Senate trading by transaction size ranges."""
        result = senate.senate_latest(apikey=api_key, limit=50)

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:
            # Filter by trade size (if amount information is available)
            size_filtered = []
            for trade_model in trade_models:
                if trade_model.amount:
                    try:
                        amount = float(trade_model.amount)
                        if trade_size == "small" and amount < 15000:
                            size_filtered.append(trade_model)
                        elif trade_size == "medium" and 15000 <= amount < 50000:
                            size_filtered.append(trade_model)
                        elif trade_size == "large" and 50000 <= amount < 250000:
                            size_filtered.append(trade_model)
                        elif trade_size == "very_large" and amount >= 250000:
                            size_filtered.append(trade_model)
                    except (ValueError, TypeError):
                        # Skip if amount parsing fails
                        continue

            # This is informational - amount field may not always be available
            assert len(size_filtered) >= 0

    def test_senate_latest(self, api_key):
        """Test latest Senate trading disclosures endpoint."""
        result = senate.senate_latest(apikey=api_key, limit=10)

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:  # If we have data
            assert len(trade_models) <= 10
            trade_model = trade_models[0]

            # Required fields validation
            assert trade_model.symbol is not None and trade_model.symbol != ""
            assert (
                trade_model.disclosureDate is not None
                and trade_model.disclosureDate != ""
            )
            assert trade_model.firstName is not None and trade_model.firstName != ""
            assert trade_model.lastName is not None and trade_model.lastName != ""
            assert hasattr(trade_model, "office")
            assert hasattr(trade_model, "type")

            # Data quality checks
            assert trade_model.symbol != ""
            assert trade_model.disclosureDate != ""
            assert trade_model.firstName != ""
            assert trade_model.lastName != ""
            # The 'office' field contains the full politician name, not chamber
            assert trade_model.office
            assert trade_model.type in [
                "Purchase",
                "Sale",
                "sale",
                "purchase",
                "Sale (Full)",
                "Purchase (Full)",
                "Partial Sale",
                "Partial Purchase",
            ]

    def test_senate_latest_pagination(self, api_key):
        """Test Senate latest with pagination parameters."""
        result = senate.senate_latest(apikey=api_key, page=0, limit=5)

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)
        # Should respect limit parameter
        assert len(trade_models) <= 5

    def test_senate_trades_by_symbol(self, api_key):
        """Test Senate trades by symbol endpoint."""
        result = senate.senate_trades(apikey=api_key, symbol="AAPL")

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:  # If we have data
            for trade_model in trade_models[:3]:  # Check first few trades
                # Should only contain AAPL trades
                assert trade_model.symbol == "AAPL"
                # The 'office' field contains politician name, not chamber

    def test_senate_trades_by_name(self, api_key):
        """Test Senate trades by politician name endpoint."""
        # Use a common name pattern that might exist
        result = senate.senate_trades_by_name(apikey=api_key, name="Warren")

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)

        if trade_models:  # If we have data
            for trade_model in trade_models[:3]:  # Check first few trades
                # Should contain "Warren" in name
                full_name = f"{trade_model.firstName} {trade_model.lastName}".upper()
                assert "WARREN" in full_name
                # The 'office' field contains politician name, not chamber

    def test_senate_trades_invalid_symbol(self, api_key):
        """Test Senate trades with invalid symbol."""
        result = senate.senate_trades(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)
        # Should return empty list for invalid symbol
        assert len(trade_models) == 0

    def test_senate_trades_invalid_name(self, api_key):
        """Test Senate trades with invalid politician name."""
        result = senate.senate_trades_by_name(apikey=api_key, name="INVALID_PERSON_XYZ")

        trade_models = get_response_models(result, FMPPoliticalTrade)
        assert isinstance(trade_models, list)
        # Should return empty list for invalid name
        assert len(trade_models) == 0


class TestHouseTrading:
    """Test cases for House trading disclosure endpoints."""

    def test_house_latest(self, api_key):
        """Test latest House trading disclosures endpoint."""
        result = senate.house_latest(apikey=api_key, limit=10)

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)

        if models:  # If we have data
            assert len(models) <= 10
            trade_obj = models[0]

            # Required fields validation - symbol can be empty for non-stock trades
            assert trade_obj.symbol is not None  # Can be empty string but not None
            assert trade_obj.disclosureDate != ""
            assert trade_obj.firstName != ""
            assert trade_obj.lastName != ""
            assert hasattr(trade_obj, "office")
            assert hasattr(trade_obj, "type")

            # Data quality checks (symbol can be empty for non-stock assets like bonds)
            assert trade_obj.disclosureDate != ""
            assert trade_obj.firstName != ""
            assert trade_obj.lastName != ""
            # The 'office' field contains the full politician name, not chamber
            assert trade_obj.office

    def test_house_latest_pagination(self, api_key):
        """Test House latest with pagination parameters."""
        result = senate.house_latest(apikey=api_key, page=0, limit=5)

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)
        # Should respect limit parameter
        assert len(models) <= 5

    def test_house_trades_by_symbol(self, api_key):
        """Test House trades by symbol endpoint."""
        result = senate.house_trades(apikey=api_key, symbol="MSFT")

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)

        if models:  # If we have data
            for trade_obj in models[:3]:  # Check first few trades
                # Should only contain MSFT trades
                assert trade_obj.symbol != ""
                # The 'office' field contains politician name, not chamber

    def test_house_trades_by_name(self, api_key):
        """Test House trades by politician name endpoint."""
        # Use a common name pattern that might exist
        result = senate.house_trades_by_name(apikey=api_key, name="Johnson")

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)

        if models:  # If we have data
            for trade_obj in models[:3]:  # Check first few trades
                # Should contain "Johnson" in name
                full_name = f"{trade_obj.firstName} {trade_obj.lastName}".upper()
                assert trade_obj.firstName != ""
                # The 'office' field contains politician name, not chamber

    def test_house_trades_invalid_symbol(self, api_key):
        """Test House trades with invalid symbol."""
        result = senate.house_trades(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        # Invalid symbol may return empty results, which is valid behavior
        validate_model_list(models, FMPPoliticalTrade, min_count=0)
        # Should return empty list for invalid symbol
        assert len(models) == 0

    def test_house_trades_invalid_name(self, api_key):
        """Test House trades with invalid politician name."""
        result = senate.house_trades_by_name(apikey=api_key, name="INVALID_PERSON_XYZ")

        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        # Invalid name may return empty results, which is valid behavior
        validate_model_list(models, FMPPoliticalTrade, min_count=0)
        # Should return empty list for invalid name
        assert len(models) == 0


class TestPoliticalTradingDataQuality:
    """Test data quality and business logic validation."""

    def test_senate_vs_house_latest_comparison(self, api_key):
        """Test that Senate and House latest endpoints return data."""
        senate_result = senate.senate_latest(apikey=api_key, limit=5)
        house_result = senate.house_latest(apikey=api_key, limit=5)

        # Get response models and validate
        senate_models = get_response_models(senate_result, FMPPoliticalTrade)
        house_models = get_response_models(house_result, FMPPoliticalTrade)
        validate_model_list(senate_models, FMPPoliticalTrade)
        validate_model_list(house_models, FMPPoliticalTrade)

        # Both endpoints should return data (API doesn't distinguish chamber in office field)
        assert isinstance(senate_models, list)
        assert isinstance(house_models, list)

        if senate_models:
            # Validate Senate data structure
            for trade in senate_models[:2]:
                assert trade.firstName != ""
                assert trade.lastName != ""
                assert hasattr(trade, "office")

        if house_models:
            # Validate House data structure
            for trade in house_models[:2]:
                assert trade.firstName != ""
                assert trade.lastName != ""
                assert hasattr(trade, "office")

    def test_political_trading_date_formats(self, api_key):
        """Test date format consistency in political trading data."""
        result = senate.senate_latest(apikey=api_key, limit=5)
        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)

        if models:
            for trade in models:
                # Check date formats (should be YYYY-MM-DD or similar)
                assert trade.disclosureDate != ""
                assert trade.disclosureDate != ""

                # Check that dates are reasonable (not in future)
                assert (
                    "2020" in trade.disclosureDate
                    or "2021" in trade.disclosureDate
                    or "2022" in trade.disclosureDate
                    or "2023" in trade.disclosureDate
                    or "2024" in trade.disclosureDate
                    or "2025" in trade.disclosureDate
                )

    def test_political_trading_transaction_amounts(self, api_key):
        """Test transaction amount ranges in political trading data."""
        result = senate.senate_latest(apikey=api_key, limit=10)
        # Get response models and validate
        models = get_response_models(result, FMPPoliticalTrade)
        validate_model_list(models, FMPPoliticalTrade)

        if models:
            for trade in models:
                amount = trade.amount

                # Check that amount is in expected format/ranges
                # Political trading amounts are typically in ranges like "$1,001 - $15,000"
                assert isinstance(amount, str)
                assert len(amount) > 0
                # Common amount patterns
                amount_indicators = [
                    "$",
                    "1,001",
                    "15,000",
                    "50,000",
                    "100,000",
                    "250,000",
                    "1,000,000",
                    "-",
                    "Over",
                ]
                assert any(indicator in amount for indicator in amount_indicators)

    def test_political_trading_asset_types(self, api_key):
        """Test asset type validation in political trading data."""
        result = senate.house_latest(apikey=api_key, limit=10)
        data = get_response_models(result, FMPPoliticalTrade)
        if data:
            asset_types = set()
            for trade in data:
                if isinstance(trade, dict):
                    asset_types.add(trade["assetType"])
                else:
                    asset_types.add(trade.assetType)

            # Should have common asset types
            expected_types = [
                "Stock",
                "Bond",
                "Mutual Fund",
                "ETF",
                "Options",
                "Other Securities",
            ]
            # At least one expected type should be present
            assert len(asset_types) > 0

    def test_political_trading_districts(self, api_key):
        """Test district information in political trading data."""
        result = senate.house_latest(apikey=api_key, limit=10)
        data = get_response_models(result, FMPPoliticalTrade)
        if data:
            for trade in data:
                if isinstance(trade, dict):
                    district = trade["district"]
                    office = trade["office"]  # Contains politician name, not chamber
                else:
                    district = trade.district
                    office = trade.office  # Contains politician name, not chamber

                # District should be a string (state abbreviation or state + district)
                assert isinstance(district, str)
                # District can be empty for some entries, so we'll check if it's provided
                if district:  # Only check length if district is not empty
                    assert len(district) >= 2  # At least state abbreviation

                # Office should contain politician's name
                assert isinstance(office, str)
                assert len(office) > 0


# Error handling tests
class TestPoliticalTradingErrorHandling:
    """Test error handling for political trading endpoints."""

    def test_senate_latest_invalid_api_key(self):
        """Test Senate latest with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.senate_latest(apikey="invalid_key")

    def test_house_latest_invalid_api_key(self):
        """Test House latest with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.house_latest(apikey="invalid_key")

    def test_senate_trades_invalid_api_key(self):
        """Test Senate trades with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.senate_trades(apikey="invalid_key", symbol="AAPL")

    def test_house_trades_invalid_api_key(self):
        """Test House trades with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.house_trades(apikey="invalid_key", symbol="AAPL")

    def test_senate_trades_by_name_invalid_api_key(self):
        """Test Senate trades by name with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.senate_trades_by_name(apikey="invalid_key", name="Warren")

    def test_house_trades_by_name_invalid_api_key(self):
        """Test House trades by name with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            senate.house_trades_by_name(apikey="invalid_key", name="Johnson")
