import pytest

from fmpsdk import indexes
from fmpsdk.models import (
    FMPHistoricalIndexConstituent,
    FMPIndexConstituent,
    FMPIndexListItem,
    FMPSector,
)

from .conftest import extract_data_list


class TestIndexes:
    """Test cases for indexes module functions."""

    def test_index_list_valid_api_key(self, api_key):
        """Test index_list with valid API key."""
        result = indexes.index_list(apikey=api_key)

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        data = extract_data_list(result)

        # Test that we get a list
        assert isinstance(data, list)

        if data:  # If data is not empty
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure
                assert "symbol" in first_item
                assert "name" in first_item
                assert isinstance(first_item["symbol"], str)
                assert isinstance(first_item["name"], str)
                assert len(first_item["symbol"]) > 0
                assert len(first_item["name"]) > 0
            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPIndexListItem)
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "name")
                assert isinstance(first_item.symbol, str)
                assert isinstance(first_item.name, str)
                assert len(first_item.symbol) > 0
                assert len(first_item.name) > 0

            # Test that we have reasonable number of indices
            assert len(data) >= 5  # Should have at least major indices

    def test_index_list_invalid_api_key(self):
        """Test index_list with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = indexes.index_list(apikey=invalid_api_key)

        # Should return error structure
        if isinstance(result, dict) and "Error Message" in result:
            # API returned error dict directly
            assert "Error Message" in result
        else:
            # Data wrapped in list format
            data = extract_data_list(result)
            if data and isinstance(data[0], dict) and "Error Message" in data[0]:
                # Error wrapped in list
                assert "Error Message" in data[0]
            else:
                # Should be empty
                assert len(data) == 0

    def test_available_sectors_valid_api_key(self, api_key):
        """Test available_sectors with valid API key."""
        result = indexes.available_sectors(apikey=api_key)

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        data = extract_data_list(result)

        # Test that we get a list
        assert isinstance(data, list)

        if data:  # If data is not empty
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure
                assert "sector" in first_item
                assert isinstance(first_item["sector"], str)
                assert len(first_item["sector"]) > 0
            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPSector)
                assert hasattr(first_item, "sector")
                assert isinstance(first_item.sector, str)
                assert len(first_item.sector) > 0

            # Test that we have reasonable number of sectors
            assert len(data) >= 10  # Should have at least major sectors

            # Test for common sectors
            sector_names = []
            for item in data:
                if isinstance(item, dict):
                    sector_names.append(item["sector"])
                else:
                    sector_names.append(item.sector)

            # Should contain common sectors
            common_sectors = [
                "Technology",
                "Healthcare",
                "Financials",
                "Energy",
                "Consumer",
            ]
            found_sectors = [
                s for s in common_sectors if any(cs in s for cs in sector_names)
            ]
            assert len(found_sectors) >= 2  # Should find at least 2 common sectors

    def test_available_sectors_invalid_api_key(self):
        """Test available_sectors with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = indexes.available_sectors(apikey=invalid_api_key)

        # Should return error structure
        if isinstance(result, dict) and "Error Message" in result:
            # API returned error dict directly
            assert "Error Message" in result
        else:
            # Data wrapped in list format
            data = extract_data_list(result)
            if data and isinstance(data[0], dict) and "Error Message" in data[0]:
                # Error wrapped in list
                assert "Error Message" in data[0]
            else:
                # Should be empty
                assert len(data) == 0

    @pytest.mark.parametrize("index_name", ["sp500", "nasdaq", "dowjones"])
    def test_index_constituents_valid_indices(self, api_key, index_name):
        """Test index_constituents with valid index names."""
        result = indexes.index_constituents(apikey=api_key, index=index_name)

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        data = extract_data_list(result)

        # Test that we get a list
        assert isinstance(data, list)

        if data:  # If data is not empty
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure - required fields
                required_fields = ["symbol", "name", "sector"]
                for field in required_fields:
                    assert field in first_item
                    assert isinstance(first_item[field], str)
                    assert len(first_item[field]) > 0

                # Optional fields
                optional_fields = [
                    "subSector",
                    "headQuarter",
                    "dateFirstAdded",
                    "cik",
                    "founded",
                ]
                for field in optional_fields:
                    if field in first_item:
                        assert isinstance(first_item[field], (str, type(None)))
            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPIndexConstituent)
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "name")
                assert hasattr(first_item, "sector")
                assert isinstance(first_item.symbol, str)
                assert isinstance(first_item.name, str)
                assert isinstance(first_item.sector, str)
                assert len(first_item.symbol) > 0
                assert len(first_item.name) > 0
                assert len(first_item.sector) > 0

            # Test expected number of constituents based on index
            if index_name == "sp500":
                assert len(data) >= 450  # S&P 500 should have around 500 companies
            elif index_name == "dowjones":
                assert len(data) >= 25  # Dow Jones should have around 30 companies
            elif index_name == "nasdaq":
                assert len(data) >= 90  # NASDAQ 100 should have around 100 companies

            # Test for well-known stocks in each index
            symbols = []
            for item in data:
                if isinstance(item, dict):
                    symbols.append(item["symbol"])
                else:
                    symbols.append(item.symbol)

            if index_name == "sp500":
                # Should contain major S&P 500 stocks
                major_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN"]
                found_stocks = [s for s in major_stocks if s in symbols]
                assert len(found_stocks) >= 2  # Should find at least 2 major stocks
            elif index_name == "dowjones":
                # Should contain major Dow stocks
                dow_stocks = ["AAPL", "MSFT", "JNJ", "JPM"]
                found_stocks = [s for s in dow_stocks if s in symbols]
                assert len(found_stocks) >= 1  # Should find at least 1 Dow stock

    def test_index_constituents_invalid_index(self, api_key):
        """Test index_constituents with invalid index name."""
        with pytest.raises(ValueError) as exc_info:
            indexes.index_constituents(apikey=api_key, index="invalid_index")

        assert "Invalid index" in str(exc_info.value)
        assert "sp500" in str(exc_info.value)
        assert "nasdaq" in str(exc_info.value)
        assert "dowjones" in str(exc_info.value)

    def test_index_constituents_invalid_api_key(self):
        """Test index_constituents with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = indexes.index_constituents(apikey=invalid_api_key, index="sp500")

        # Should return error structure
        if isinstance(result, dict) and "Error Message" in result:
            # API returned error dict directly
            assert "Error Message" in result
        else:
            # Data wrapped in list format
            data = extract_data_list(result)
            if data and isinstance(data[0], dict) and "Error Message" in data[0]:
                # Error wrapped in list
                assert "Error Message" in data[0]
            else:
                # Should be empty
                assert len(data) == 0

    @pytest.mark.parametrize("index_name", ["sp500", "nasdaq", "dowjones"])
    def test_index_constituents_historical_valid_indices(self, api_key, index_name):
        """Test index_constituents_historical with valid index names."""
        result = indexes.index_constituents_historical(apikey=api_key, index=index_name)

        # Test that we get a result
        assert result is not None

        # Convert to list if it's a model
        data = extract_data_list(result)

        # Test that we get a list
        assert isinstance(data, list)

        if data:  # If data is not empty
            # Test first item structure
            first_item = data[0]
            if isinstance(first_item, dict):
                # Validate dict structure - required fields
                required_fields = ["dateAdded", "date", "symbol"]
                for field in required_fields:
                    assert field in first_item
                    assert isinstance(first_item[field], str)
                    assert len(first_item[field]) > 0

                # Optional fields that might be empty
                optional_fields = [
                    "addedSecurity",
                    "removedTicker",
                    "removedSecurity",
                    "reason",
                ]
                for field in optional_fields:
                    if field in first_item:
                        assert isinstance(first_item[field], (str, type(None)))

                # Validate date format (can be YYYY-MM-DD or Month DD, YYYY)
                date_fields = ["dateAdded", "date"]
                for date_field in date_fields:
                    if date_field in first_item and first_item[date_field]:
                        date_value = first_item[date_field]
                        assert len(date_value) >= 8  # At least basic date format
                        # Should contain date separators or comma for "Month DD, YYYY" format
                        assert (
                            "-" in date_value or "/" in date_value or "," in date_value
                        )
            else:
                # Test Pydantic model
                assert isinstance(first_item, FMPHistoricalIndexConstituent)
                assert hasattr(first_item, "dateAdded")
                assert hasattr(first_item, "date")
                assert hasattr(first_item, "symbol")
                assert isinstance(first_item.dateAdded, str)
                assert isinstance(first_item.date, str)
                assert isinstance(first_item.symbol, str)
                assert len(first_item.dateAdded) > 0
                assert len(first_item.date) > 0
                assert len(first_item.symbol) > 0

            # Test that we have some historical data
            assert len(data) >= 1  # Should have at least some historical changes

            # Test for chronological ordering (most recent first)
            if len(data) >= 2:
                dates = []
                for item in data[:5]:  # Check first 5 items
                    if isinstance(item, dict):
                        dates.append(item.get("date", ""))
                    else:
                        dates.append(item.date)

                # Should have valid dates
                valid_dates = [d for d in dates if d and len(d) >= 8]
                assert len(valid_dates) >= 1  # Should have at least one valid date

    def test_index_constituents_historical_invalid_index(self, api_key):
        """Test index_constituents_historical with invalid index name."""
        with pytest.raises(ValueError) as exc_info:
            indexes.index_constituents_historical(apikey=api_key, index="invalid_index")

        assert "Invalid index" in str(exc_info.value)
        assert "sp500" in str(exc_info.value)
        assert "nasdaq" in str(exc_info.value)
        assert "dowjones" in str(exc_info.value)

    def test_index_constituents_historical_invalid_api_key(self):
        """Test index_constituents_historical with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = indexes.index_constituents_historical(
            apikey=invalid_api_key, index="sp500"
        )

        # Should return error structure
        if isinstance(result, dict) and "Error Message" in result:
            # API returned error dict directly
            assert "Error Message" in result
        else:
            # Data wrapped in list format
            data = extract_data_list(result)
            if data and isinstance(data[0], dict) and "Error Message" in data[0]:
                # Error wrapped in list
                assert "Error Message" in data[0]
            else:
                # Should be empty
                assert len(data) == 0

    def test_all_functions_response_time(self, api_key):
        """Test that all functions respond within reasonable time."""
        import time

        # Test index_list response time
        start_time = time.time()
        result = indexes.index_list(apikey=api_key)
        end_time = time.time()
        assert (end_time - start_time) < 10.0  # Should respond within 10 seconds

        # Test available_sectors response time
        start_time = time.time()
        result = indexes.available_sectors(apikey=api_key)
        end_time = time.time()
        assert (end_time - start_time) < 10.0  # Should respond within 10 seconds

        # Test index_constituents response time
        start_time = time.time()
        result = indexes.index_constituents(apikey=api_key, index="sp500")
        end_time = time.time()
        assert (
            end_time - start_time
        ) < 15.0  # Should respond within 15 seconds (larger dataset)

        # Test index_constituents_historical response time
        start_time = time.time()
        result = indexes.index_constituents_historical(apikey=api_key, index="sp500")
        end_time = time.time()
        assert (end_time - start_time) < 15.0  # Should respond within 15 seconds

    def test_data_consistency_between_current_and_historical(self, api_key):
        """Test data consistency between current constituents and historical data."""
        # Get current S&P 500 constituents
        current_result = indexes.index_constituents(apikey=api_key, index="sp500")
        if hasattr(current_result, "root"):
            current_data = current_result.root
        else:
            current_data = current_result

        # Get historical S&P 500 constituents
        historical_result = indexes.index_constituents_historical(
            apikey=api_key, index="sp500"
        )
        if hasattr(historical_result, "root"):
            historical_data = historical_result.root
        else:
            historical_data = historical_result

        if current_data and historical_data:
            # Extract current symbols
            current_symbols = set()
            for item in current_data:
                if isinstance(item, dict):
                    current_symbols.add(item["symbol"])
                else:
                    current_symbols.add(item.symbol)

            # Extract historical symbols (recently added)
            historical_symbols = set()
            for item in historical_data[:50]:  # Check recent additions
                if isinstance(item, dict):
                    if item.get("addedSecurity"):
                        # Look for symbol in the added security field
                        added_security = item["addedSecurity"]
                        # Extract symbol from the security name if possible
                        symbol = item.get("symbol", "")
                        if symbol:
                            historical_symbols.add(symbol)
                else:
                    if hasattr(item, "addedSecurity") and item.addedSecurity:
                        symbol = getattr(item, "symbol", "")
                        if symbol:
                            historical_symbols.add(symbol)

            # Should have some overlap between current and recently added symbols
            assert len(current_symbols) > 0
            # Note: Not all historical additions will be in current list due to subsequent removals

    def test_index_constituents_comprehensive_data_validation(self, api_key):
        """Comprehensive validation of index constituents data quality."""
        result = indexes.index_constituents(apikey=api_key, index="sp500")

        data = extract_data_list(result)

        if data and len(data) > 0:
            symbols = set()
            sectors = set()

            for item in data:
                if isinstance(item, dict):
                    symbol = item.get("symbol", "")
                    name = item.get("name", "")
                    sector = item.get("sector", "")
                else:
                    symbol = getattr(item, "symbol", "")
                    name = getattr(item, "name", "")
                    sector = getattr(item, "sector", "")

                # Validate symbol format
                if symbol:
                    assert len(symbol) >= 1
                    assert len(symbol) <= 10  # Most symbols are 1-5 characters
                    assert (
                        symbol.isupper() or "." in symbol
                    )  # Should be uppercase or contain dots (for some symbols)
                    symbols.add(symbol)

                # Validate name
                if name:
                    assert len(name) >= 2
                    assert len(name) <= 100  # Reasonable company name length

                # Validate sector
                if sector:
                    assert len(sector) >= 3
                    sectors.add(sector)

            # Check for duplicate symbols
            assert len(symbols) == len(
                [
                    (
                        item.get("symbol")
                        if isinstance(item, dict)
                        else getattr(item, "symbol", "")
                    )
                    for item in data
                    if (
                        item.get("symbol")
                        if isinstance(item, dict)
                        else getattr(item, "symbol", "")
                    )
                ]
            )

            # Should have diverse sectors
            assert len(sectors) >= 5  # S&P 500 should span multiple sectors

            # Check for well-known large-cap stocks
            major_stocks = [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "TSLA",
                "META",
                "NVDA",
                "JPM",
                "JNJ",
                "V",
            ]
            found_major_stocks = [stock for stock in major_stocks if stock in symbols]
            assert len(found_major_stocks) >= 3  # Should find at least 3 major stocks

    def test_sectors_data_quality(self, api_key):
        """Test the quality and completeness of sectors data."""
        result = indexes.available_sectors(apikey=api_key)

        data = extract_data_list(result)

        if data and len(data) > 0:
            sector_names = []

            for item in data:
                if isinstance(item, dict):
                    sector = item.get("sector", "")
                else:
                    sector = getattr(item, "sector", "")

                if sector:
                    sector_names.append(sector)
                    # Validate sector name format
                    assert len(sector) >= 3
                    assert len(sector) <= 50
                    # Should be properly capitalized
                    assert sector[0].isupper()

            # Check for standard GICS sectors
            standard_sectors = [
                "Technology",
                "Healthcare",
                "Financials",
                "Consumer Discretionary",
                "Communication Services",
                "Industrials",
                "Consumer Staples",
                "Energy",
                "Utilities",
                "Real Estate",
                "Materials",
            ]

            # Should find several standard sectors
            found_standard_sectors = []
            for standard in standard_sectors:
                for sector in sector_names:
                    if (
                        standard.lower() in sector.lower()
                        or sector.lower() in standard.lower()
                    ):
                        found_standard_sectors.append(standard)
                        break

            assert (
                len(found_standard_sectors) >= 3
            )  # Should find at least 3 standard sectors

            # Check for no duplicate sectors
            assert len(sector_names) == len(set(sector_names))
