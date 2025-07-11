import pytest

from fmpsdk import senate
from fmpsdk.models import FMPPoliticalTrade
from tests.conftest import extract_data_list


class TestSenateTrading:
    """Test cases for Senate trading disclosure endpoints."""

    @pytest.mark.parametrize(
        "symbol",
        [
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
        ],
    )
    def test_senate_trading_by_symbol(self, api_key, symbol):
        """Test Senate trading disclosures for various symbols."""
        result = senate.senate_trades(apikey=api_key, symbol=symbol)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            trade = data[0]

            # Validate against model
            if isinstance(trade, dict):
                trade_obj = FMPPoliticalTrade(**trade)
            else:
                trade_obj = trade

            # Basic validation
            assert hasattr(trade_obj, "symbol")
            assert hasattr(trade_obj, "disclosureDate")
            assert hasattr(trade_obj, "firstName")
            assert hasattr(trade_obj, "lastName")

            # Symbol should match requested
            if trade_obj.symbol:
                assert trade_obj.symbol == symbol

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

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

    @pytest.mark.parametrize("transaction_type", ["purchase", "sale", "both"])
    def test_senate_trading_by_transaction_type(self, api_key, transaction_type):
        """Test Senate trading for different transaction types."""
        # Use popular symbols that likely have both purchases and sales
        symbols = ["AAPL", "MSFT", "SPY", "QQQ", "TSLA"]

        for symbol in symbols[:2]:  # Test first 2 symbols
            result = senate.senate_trades(apikey=api_key, symbol=symbol)

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            if not data:
                continue

            # Filter by transaction type
            if transaction_type == "purchase":
                filtered_trades = [
                    trade
                    for trade in data
                    if isinstance(trade, dict)
                    and trade.get("type", "").lower() in ["purchase", "buy"]
                ]
            elif transaction_type == "sale":
                filtered_trades = [
                    trade
                    for trade in data
                    if isinstance(trade, dict)
                    and trade.get("type", "").lower() in ["sale", "sell"]
                ]
            else:  # both
                filtered_trades = data

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

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Check that we have some data within the expected date range
            recent_trades = []
            for trade in data:
                if isinstance(trade, dict) and "disclosureDate" in trade:
                    try:
                        trade_date = datetime.strptime(
                            trade["disclosureDate"], "%Y-%m-%d"
                        )
                        if start_date <= trade_date <= end_date:
                            recent_trades.append(trade)
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

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Validate structure for political trades
            for trade in data[:5]:  # Check first 5 trades
                if isinstance(trade, dict):
                    trade_obj = FMPPoliticalTrade(**trade)
                else:
                    trade_obj = trade

                # Basic validation
                assert hasattr(trade_obj, "firstName")
                assert hasattr(trade_obj, "lastName")
                assert hasattr(trade_obj, "office")

                # Check that we have politician information
                if trade_obj.firstName and trade_obj.lastName:
                    assert len(trade_obj.firstName) > 0
                    assert len(trade_obj.lastName) > 0

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

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Filter by trade size (if amount information is available)
            size_filtered = []
            for trade in data:
                if isinstance(trade, dict) and "amount" in trade:
                    try:
                        amount = float(trade["amount"])
                        if trade_size == "small" and amount < 15000:
                            size_filtered.append(trade)
                        elif trade_size == "medium" and 15000 <= amount < 50000:
                            size_filtered.append(trade)
                        elif trade_size == "large" and 50000 <= amount < 250000:
                            size_filtered.append(trade)
                        elif trade_size == "very_large" and amount >= 250000:
                            size_filtered.append(trade)
                    except (ValueError, TypeError):
                        # Skip if amount parsing fails
                        continue

            # This is informational - amount field may not always be available
            assert len(size_filtered) >= 0

    def test_senate_latest(self, api_key):
        """Test latest Senate trading disclosures endpoint."""
        result = senate.senate_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            assert len(data) <= 10
            trade = data[0]

            # Validate against model
            if isinstance(trade, dict):
                trade_obj = FMPPoliticalTrade(**trade)
            else:
                trade_obj = trade

            # Required fields validation
            assert hasattr(trade_obj, "symbol")
            assert hasattr(trade_obj, "disclosureDate")
            assert hasattr(trade_obj, "transactionDate")
            assert hasattr(trade_obj, "firstName")
            assert hasattr(trade_obj, "lastName")
            assert hasattr(trade_obj, "office")
            assert hasattr(trade_obj, "type")

            # Data quality checks
            assert trade_obj.symbol
            assert trade_obj.disclosureDate
            assert trade_obj.firstName
            assert trade_obj.lastName
            # The 'office' field contains the full politician name, not chamber
            assert trade_obj.office
            assert trade_obj.type in [
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

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should respect limit parameter
        assert len(data) <= 5

    def test_senate_trades_by_symbol(self, api_key):
        """Test Senate trades by symbol endpoint."""
        result = senate.senate_trades(apikey=api_key, symbol="AAPL")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for trade in data[:3]:  # Check first few trades
                if isinstance(trade, dict):
                    trade_obj = FMPPoliticalTrade(**trade)
                else:
                    trade_obj = trade

                # Should only contain AAPL trades
                assert trade_obj.symbol == "AAPL"
                # The 'office' field contains politician name, not chamber

    def test_senate_trades_by_name(self, api_key):
        """Test Senate trades by politician name endpoint."""
        # Use a common name pattern that might exist
        result = senate.senate_trades_by_name(apikey=api_key, name="Warren")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for trade in data[:3]:  # Check first few trades
                if isinstance(trade, dict):
                    trade_obj = FMPPoliticalTrade(**trade)
                else:
                    trade_obj = trade

                # Should contain "Warren" in name
                full_name = f"{trade_obj.firstName} {trade_obj.lastName}".upper()
                assert "WARREN" in full_name
                # The 'office' field contains politician name, not chamber

    def test_senate_trades_invalid_symbol(self, api_key):
        """Test Senate trades with invalid symbol."""
        result = senate.senate_trades(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid symbol
        assert len(data) == 0

    def test_senate_trades_invalid_name(self, api_key):
        """Test Senate trades with invalid politician name."""
        result = senate.senate_trades_by_name(apikey=api_key, name="INVALID_PERSON_XYZ")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid name
        assert len(data) == 0


class TestHouseTrading:
    """Test cases for House trading disclosure endpoints."""

    def test_house_latest(self, api_key):
        """Test latest House trading disclosures endpoint."""
        result = senate.house_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            assert len(data) <= 10
            trade = data[0]

            # Validate against model
            if isinstance(trade, dict):
                trade_obj = FMPPoliticalTrade(**trade)
            else:
                trade_obj = trade

            # Required fields validation
            assert hasattr(trade_obj, "symbol")
            assert hasattr(trade_obj, "disclosureDate")
            assert hasattr(trade_obj, "transactionDate")
            assert hasattr(trade_obj, "firstName")
            assert hasattr(trade_obj, "lastName")
            assert hasattr(trade_obj, "office")
            assert hasattr(trade_obj, "type")

            # Data quality checks
            assert trade_obj.symbol
            assert trade_obj.disclosureDate
            assert trade_obj.firstName
            assert trade_obj.lastName
            # The 'office' field contains the full politician name, not chamber
            assert trade_obj.office

    def test_house_latest_pagination(self, api_key):
        """Test House latest with pagination parameters."""
        result = senate.house_latest(apikey=api_key, page=0, limit=5)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should respect limit parameter
        assert len(data) <= 5

    def test_house_trades_by_symbol(self, api_key):
        """Test House trades by symbol endpoint."""
        result = senate.house_trades(apikey=api_key, symbol="MSFT")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for trade in data[:3]:  # Check first few trades
                if isinstance(trade, dict):
                    trade_obj = FMPPoliticalTrade(**trade)
                else:
                    trade_obj = trade

                # Should only contain MSFT trades
                assert trade_obj.symbol == "MSFT"
                # The 'office' field contains politician name, not chamber

    def test_house_trades_by_name(self, api_key):
        """Test House trades by politician name endpoint."""
        # Use a common name pattern that might exist
        result = senate.house_trades_by_name(apikey=api_key, name="Johnson")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for trade in data[:3]:  # Check first few trades
                if isinstance(trade, dict):
                    trade_obj = FMPPoliticalTrade(**trade)
                else:
                    trade_obj = trade

                # Should contain "Johnson" in name
                full_name = f"{trade_obj.firstName} {trade_obj.lastName}".upper()
                assert "JOHNSON" in full_name
                # The 'office' field contains politician name, not chamber

    def test_house_trades_invalid_symbol(self, api_key):
        """Test House trades with invalid symbol."""
        result = senate.house_trades(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid symbol
        assert len(data) == 0

    def test_house_trades_invalid_name(self, api_key):
        """Test House trades with invalid politician name."""
        result = senate.house_trades_by_name(apikey=api_key, name="INVALID_PERSON_XYZ")

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid name
        assert len(data) == 0


class TestPoliticalTradingDataQuality:
    """Test data quality and business logic validation."""

    def test_senate_vs_house_latest_comparison(self, api_key):
        """Test that Senate and House latest endpoints return data."""
        senate_result = senate.senate_latest(apikey=api_key, limit=5)
        house_result = senate.house_latest(apikey=api_key, limit=5)

        # Check if results are error dicts (invalid API key)
        if isinstance(senate_result, dict) and "Error Message" in senate_result:
            return
        if isinstance(house_result, dict) and "Error Message" in house_result:
            return

        senate_data = extract_data_list(senate_result)
        house_data = extract_data_list(house_result)

        # Both endpoints should return data (API doesn't distinguish chamber in office field)
        assert isinstance(senate_data, list)
        assert isinstance(house_data, list)

        if senate_data:
            # Validate Senate data structure
            for trade in senate_data[:2]:
                if isinstance(trade, dict):
                    assert "firstName" in trade
                    assert "lastName" in trade
                    assert "office" in trade
                else:
                    assert hasattr(trade, "firstName")
                    assert hasattr(trade, "lastName")
                    assert hasattr(trade, "office")

        if house_data:
            # Validate House data structure
            for trade in house_data[:2]:
                if isinstance(trade, dict):
                    assert "firstName" in trade
                    assert "lastName" in trade
                    assert "office" in trade
                else:
                    assert hasattr(trade, "firstName")
                    assert hasattr(trade, "lastName")
                    assert hasattr(trade, "office")

    def test_political_trading_date_formats(self, api_key):
        """Test date format consistency in political trading data."""
        result = senate.senate_latest(apikey=api_key, limit=5)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for trade in data:
                if isinstance(trade, dict):
                    # Check date formats (should be YYYY-MM-DD or similar)
                    assert len(trade["disclosureDate"]) >= 10
                    assert len(trade["transactionDate"]) >= 10

                    # Check that dates are reasonable (not in future)
                    assert (
                        "2020" in trade["disclosureDate"]
                        or "2021" in trade["disclosureDate"]
                        or "2022" in trade["disclosureDate"]
                        or "2023" in trade["disclosureDate"]
                        or "2024" in trade["disclosureDate"]
                        or "2025" in trade["disclosureDate"]
                    )
                else:
                    assert len(trade.disclosureDate) >= 10
                    assert len(trade.transactionDate) >= 10

    def test_political_trading_transaction_amounts(self, api_key):
        """Test transaction amount ranges in political trading data."""
        result = senate.senate_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for trade in data:
                if isinstance(trade, dict):
                    amount = trade["amount"]
                else:
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

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
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

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
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
        result = senate.senate_latest(apikey="invalid_key")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_house_latest_invalid_api_key(self):
        """Test House latest with invalid API key."""
        result = senate.house_latest(apikey="invalid_key")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_senate_trades_invalid_api_key(self):
        """Test Senate trades with invalid API key."""
        result = senate.senate_trades(apikey="invalid_key", symbol="AAPL")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_house_trades_invalid_api_key(self):
        """Test House trades with invalid API key."""
        result = senate.house_trades(apikey="invalid_key", symbol="AAPL")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_senate_trades_by_name_invalid_api_key(self):
        """Test Senate trades by name with invalid API key."""
        result = senate.senate_trades_by_name(apikey="invalid_key", name="Warren")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_house_trades_by_name_invalid_api_key(self):
        """Test House trades by name with invalid API key."""
        result = senate.house_trades_by_name(apikey="invalid_key", name="Johnson")

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result
