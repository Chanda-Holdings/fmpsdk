import pytest

from fmpsdk.models import (
    FMPAftermarketQuote,
    FMPAftermarketTrade,
    FMPQuoteFull,
    FMPQuoteShort,
    FMPStockPriceChange,
)
from fmpsdk.quote import (
    aftermarket_quote,
    aftermarket_trade,
    batch_aftermarket_quote,
    batch_aftermarket_trade,
    batch_commodity_quote,
    batch_crypto_quote,
    batch_etf_quote,
    batch_exchange_quote,
    batch_forex_quote,
    batch_index_quote,
    batch_mutual_fund_quote,
    batch_quote_short,
    quote,
    quote_short,
    stock_batch_quote,
    stock_price_change,
)

from .conftest import extract_data_list


def get_field_value(item, field_name, default=None):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name, default)
    else:
        return getattr(item, field_name, default)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestQuoteEndpoint:
    """Test class for core quote endpoint functionality."""

    def test_quote_single_symbol(self, api_key, test_symbols, test_helpers):
        """Test fetching quote for a single symbol."""
        symbol = test_symbols["large_cap"][0]  # Use AAPL from fixtures
        result = quote(apikey=api_key, symbol=symbol)

        # Check for API errors first
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip(f"API Error: {result['Error Message']}")

        # Validate we got data
        assert result is not None, "Quote result should not be None"
        assert hasattr(result, "root"), "Result should have root attribute"
        assert isinstance(result.root, list), "Quote result should be a list"
        assert len(result.root) > 0, "Quote result should contain at least one item"

        # Validate the first item matches our expected schema
        quote_data = result.root[0]
        assert isinstance(
            quote_data, FMPQuoteFull
        ), f"Quote data should be FMPQuoteFull instance, got {type(quote_data)}"

        # Use helper for common validations
        test_helpers.validate_price_data(quote_data, symbol)
        test_helpers.validate_market_data_consistency(quote_data)

        # Validate additional essential fields
        assert quote_data.name is not None, "Company name should be present"

    def test_quote_multiple_symbols(self, api_key, test_symbols):
        """Test fetching quotes for multiple symbols using individual calls."""
        symbols = test_symbols["large_cap"][:3]  # Use first 3 large cap stocks
        results = []

        # Make individual calls for each symbol (correct usage of quote function)
        for symbol in symbols:
            result = quote(apikey=api_key, symbol=symbol)
            assert result is not None, f"Quote result should not be None for {symbol}"
            assert hasattr(
                result, "root"
            ), f"Result should have root attribute for {symbol}"
            assert isinstance(
                result.root, list
            ), f"Quote result should be a list for {symbol}"
            assert (
                len(result.root) > 0
            ), f"Quote result should contain data for {symbol}"
            results.extend(result.root)

        # Validate we got data for all symbols
        assert len(results) == len(
            symbols
        ), f"Should get quotes for all {len(symbols)} symbols"

        # Validate each quote
        returned_symbols = [q.symbol for q in results]
        for symbol in symbols:
            assert symbol in returned_symbols, f"Symbol {symbol} should be in results"

        # Validate schema for each result
        for quote_data in results:
            assert isinstance(
                quote_data, FMPQuoteFull
            ), "Each quote should be FMPQuoteFull instance"
            assert (
                quote_data.symbol in symbols
            ), "Symbol should be one of the requested symbols"
            assert quote_data.price is not None, "Price should be present"
            assert quote_data.price > 0, "Price should be positive"

    def test_quote_invalid_symbol(self, api_key, test_symbols):
        """Test handling of invalid symbol."""
        invalid_symbol = test_symbols["invalid"][0]
        result = quote(apikey=api_key, symbol=invalid_symbol)

        # The API might return an empty list or an error object for invalid symbols
        # We should handle both cases gracefully
        if hasattr(result, "root") and isinstance(result.root, list):
            if len(result.root) == 0:
                # Empty result is expected for invalid symbols
                assert True, "Empty result is valid for invalid symbol"
            else:
                # Some APIs return data even for invalid symbols, check if it's actually invalid
                quote_data = result.root[0]
                if hasattr(quote_data, "price") and quote_data.price is None:
                    assert True, "Null price is valid for invalid symbol"
                else:
                    pytest.skip(
                        f"API returned data for supposedly invalid symbol {invalid_symbol}"
                    )

    @pytest.mark.parametrize(
        "symbol_category", ["large_cap", "etf", "crypto", "forex", "commodity"]
    )
    def test_quote_different_asset_types(self, api_key, test_symbols, symbol_category):
        """Test quotes for different types of assets."""
        symbol = test_symbols[symbol_category][0]
        result = quote(apikey=api_key, symbol=symbol)

        assert (
            result is not None
        ), f"Quote result should not be None for {symbol_category}"
        assert hasattr(result, "root"), "Result should have root attribute"
        assert isinstance(result.root, list), "Quote result should be a list"
        assert len(result.root) > 0, "Quote result should contain at least one item"

        quote_data = result.root[0]
        assert isinstance(
            quote_data, FMPQuoteFull
        ), f"Quote data should be FMPQuoteFull instance for {symbol_category}"
        assert quote_data.symbol == symbol, f"Symbol should match for {symbol_category}"
        assert (
            quote_data.price is not None
        ), f"Price should be present for {symbol_category}"
        assert quote_data.price > 0, f"Price should be positive for {symbol_category}"

        # Asset-specific validations
        if symbol_category == "crypto":
            assert "USD" in symbol, f"Crypto symbol {symbol} should be USD-denominated"
        elif symbol_category == "forex":
            assert len(symbol) == 6, f"Forex symbol {symbol} should be 6 characters"
        elif symbol_category == "commodity":
            assert (
                "USD" in symbol
            ), f"Commodity symbol {symbol} should be USD-denominated"
        elif symbol_category in ["large_cap", "etf"]:
            # Traditional securities should have certain fields
            if hasattr(quote_data, "volume"):
                assert (
                    quote_data.volume is None or quote_data.volume >= 0
                ), "Volume should be non-negative"

    def test_quote_response_time(self, api_key, test_symbols, test_config):
        """Test that quote responses are within acceptable time limits."""
        import time

        symbol = test_symbols["large_cap"][0]
        start_time = time.time()
        result = quote(apikey=api_key, symbol=symbol)
        response_time = time.time() - start_time

        assert result is not None, "Quote result should not be None"
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"

    def test_quote_data_consistency(self, api_key, test_symbols, test_helpers):
        """Test that quote data is internally consistent."""
        symbol = test_symbols["large_cap"][0]
        result = quote(apikey=api_key, symbol=symbol)

        assert (
            result is not None and hasattr(result, "root") and len(result.root) > 0
        ), "Should get quote data"
        quote_data = result.root[0]

        # Use helper to validate data consistency
        test_helpers.validate_market_data_consistency(quote_data)

        # Additional consistency checks
        if hasattr(quote_data, "volume") and quote_data.volume is not None:
            assert quote_data.volume >= 0, "Volume should be non-negative"

        if hasattr(quote_data, "marketCap") and quote_data.marketCap is not None:
            assert quote_data.marketCap > 0, "Market cap should be positive"

    def test_quote_apple_specific_validation(self, api_key, test_config):
        """Test specific validation for Apple stock (high-quality data expectations)."""
        symbol = "AAPL"
        result = quote(apikey=api_key, symbol=symbol)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0, "Should get Apple quote data"

        quote_data = result_list[0]

        # Apple-specific validations (high-volume, high-value stock)
        assert quote_data.symbol == symbol, f"Symbol should match: {symbol}"
        assert quote_data.name is not None, "Apple name should be present"
        assert (
            quote_data.price is not None and quote_data.price > 0
        ), "Apple price should be positive"
        assert (
            quote_data.volume is not None and quote_data.volume > 0
        ), "Apple volume should be positive"

        # Apple should have substantial market cap
        if hasattr(quote_data, "marketCap") and quote_data.marketCap is not None:
            assert (
                quote_data.marketCap > test_config["min_market_cap"]
            ), f"Apple market cap should be > {test_config['min_market_cap']:,}"

        # Price consistency checks for Apple
        if all(
            hasattr(quote_data, field) and getattr(quote_data, field) is not None
            for field in ["dayLow", "dayHigh", "price"]
        ):
            assert (
                quote_data.dayLow <= quote_data.price <= quote_data.dayHigh
            ), "Apple price should be between day low and high"

        if all(
            hasattr(quote_data, field) and getattr(quote_data, field) is not None
            for field in ["yearLow", "yearHigh", "price"]
        ):
            assert (
                quote_data.yearLow <= quote_data.price <= quote_data.yearHigh
            ), "Apple price should be between year low and high"

    def test_stock_batch_quote(self, api_key, test_symbols):
        """Test the batch quote function for multiple symbols."""
        symbols = test_symbols["large_cap"][:3]  # Use first 3 large cap stocks
        result = stock_batch_quote(apikey=api_key, symbols=symbols)

        # Validate we got data
        assert result is not None, "Batch quote result should not be None"
        assert hasattr(result, "root"), "Result should have root attribute"
        assert isinstance(result.root, list), "Batch quote result should be a list"
        assert len(result.root) == len(
            symbols
        ), f"Should get quotes for all {len(symbols)} symbols"

        # Validate each quote
        returned_symbols = [q.symbol for q in result.root]
        for symbol in symbols:
            assert (
                symbol in returned_symbols
            ), f"Symbol {symbol} should be in batch results"

        # Validate schema for each result
        for quote_data in result.root:
            assert isinstance(
                quote_data, FMPQuoteFull
            ), "Each batch quote should be FMPQuoteFull instance"
            assert (
                quote_data.symbol in symbols
            ), "Symbol should be one of the requested symbols"
            assert quote_data.price is not None, "Price should be present"
            assert quote_data.price > 0, "Price should be positive"

    def test_quote_crypto_pairs(self, api_key, test_symbols, test_helpers):
        """Test quote function with cryptocurrency pairs."""
        symbol = test_symbols["crypto"][0]  # BTCUSD
        result = quote(apikey=api_key, symbol=symbol)

        assert result is not None, "Crypto quote result should not be None"
        assert hasattr(result, "root"), "Result should have root attribute"
        assert isinstance(result.root, list), "Crypto quote result should be a list"
        assert len(result.root) > 0, "Crypto quote result should contain data"

        quote_data = result.root[0]
        assert isinstance(
            quote_data, FMPQuoteFull
        ), "Crypto quote should be FMPQuoteFull instance"
        assert quote_data.symbol == symbol, f"Symbol should match: {symbol}"
        assert (
            quote_data.price is not None and quote_data.price > 0
        ), "Crypto price should be positive"

        # Crypto-specific validations
        assert "USD" in symbol, "Test symbol should be USD-denominated"
        if hasattr(quote_data, "volume") and quote_data.volume is not None:
            assert quote_data.volume >= 0, "Crypto volume should be non-negative"

    def test_quote_forex_pairs(self, api_key, test_symbols, test_helpers):
        """Test quote function with forex currency pairs."""
        symbol = test_symbols["forex"][0]  # EURUSD
        result = quote(apikey=api_key, symbol=symbol)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list), "Forex quote result should be a list"
        assert len(result_list) > 0, "Forex quote result should contain data"

        quote_data = result_list[0]
        assert isinstance(
            quote_data, FMPQuoteFull
        ), "Forex quote should be FMPQuoteFull instance"
        assert quote_data.symbol == symbol, f"Symbol should match: {symbol}"
        assert (
            quote_data.price is not None and quote_data.price > 0
        ), "Forex price should be positive"

        # Forex-specific validations
        assert len(symbol) == 6, "Forex pair should be 6 characters (XXXYYY format)"
        # Ensure forex price is a reasonable decimal number (not checking specific ranges)
        assert isinstance(
            quote_data.price, (int, float)
        ), "Forex price should be numeric"

    def test_quote_commodity_symbols(self, api_key, test_symbols, test_helpers):
        """Test quote function with commodity symbols."""
        symbol = test_symbols["commodity"][0]  # GCUSD (Gold)
        result = quote(apikey=api_key, symbol=symbol)

        assert result is not None, "Commodity quote result should not be None"
        assert hasattr(result, "root"), "Result should have root attribute"
        assert isinstance(result.root, list), "Commodity quote result should be a list"
        assert len(result.root) > 0, "Commodity quote result should contain data"

        quote_data = result.root[0]
        assert isinstance(
            quote_data, FMPQuoteFull
        ), "Commodity quote should be FMPQuoteFull instance"
        assert quote_data.symbol == symbol, f"Symbol should match: {symbol}"
        assert (
            quote_data.price is not None and quote_data.price > 0
        ), "Commodity price should be positive"

        # Commodity-specific validations - focus on data quality, not specific prices
        if "GC" in symbol:  # Gold
            assert quote_data.price > 100, "Gold price should be reasonable (>$100/oz)"
        elif "CL" in symbol:  # Oil
            assert quote_data.price > 5, "Oil price should be reasonable (>$5/barrel)"

        # General commodity validation
        assert isinstance(
            quote_data.price, (int, float)
        ), "Commodity price should be numeric"

    @pytest.mark.parametrize(
        "asset_type", ["large_cap", "etf", "crypto", "forex", "commodity"]
    )
    def test_quote_price_validation_by_asset_type(
        self, api_key, test_symbols, asset_type
    ):
        """Test that quote prices are valid (positive numbers) for different asset types."""
        symbol = test_symbols[asset_type][0]
        result = quote(apikey=api_key, symbol=symbol)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0, f"Should get quote data for {asset_type}"

        quote_data = result_list[0]

        # Basic price validation - should be positive number
        assert quote_data.price is not None, f"Price should be present for {asset_type}"
        assert quote_data.price > 0, f"{asset_type} price should be positive"
        assert isinstance(
            quote_data.price, (int, float)
        ), f"{asset_type} price should be numeric"

        # Symbol validation
        assert (
            quote_data.symbol == symbol
        ), f"Returned symbol should match requested symbol for {asset_type}"

        # Asset-type specific basic validations (not price ranges)
        if asset_type == "crypto":
            assert "USD" in symbol, f"Test crypto symbol should be USD-denominated"
        elif asset_type == "forex":
            assert len(symbol) == 6, f"Forex symbol should be 6 characters"
        elif asset_type == "commodity":
            assert "USD" in symbol, f"Test commodity symbol should be USD-denominated"

    def test_quote_all_asset_types_batch(self, api_key, test_symbols):
        """Test quote function across all supported asset types in one test."""
        test_cases = [
            ("large_cap", "AAPL", "stock"),
            ("etf", "SPY", "ETF"),
            ("crypto", "BTCUSD", "cryptocurrency"),
            ("forex", "EURUSD", "forex pair"),
            ("commodity", "GCUSD", "commodity"),
        ]

        results = {}

        for asset_category, symbol, asset_name in test_cases:
            if symbol in test_symbols[asset_category]:
                result = quote(apikey=api_key, symbol=symbol)

                assert (
                    result is not None
                ), f"Quote result should not be None for {asset_name} {symbol}"
                assert hasattr(
                    result, "root"
                ), f"Result should have root attribute for {asset_name}"
                assert isinstance(
                    result.root, list
                ), f"Quote result should be a list for {asset_name}"
                assert (
                    len(result.root) > 0
                ), f"Quote result should contain data for {asset_name}"

                quote_data = result.root[0]
                assert isinstance(
                    quote_data, FMPQuoteFull
                ), f"Quote should be FMPQuoteFull for {asset_name}"
                assert (
                    quote_data.symbol == symbol
                ), f"Symbol should match for {asset_name}"
                assert (
                    quote_data.price is not None and quote_data.price > 0
                ), f"Price should be positive for {asset_name}"

                results[asset_name] = {
                    "symbol": quote_data.symbol,
                    "price": quote_data.price,
                    "name": getattr(quote_data, "name", "N/A"),
                }

        # Validate we tested multiple asset types
        assert (
            len(results) >= 3
        ), f"Should test at least 3 asset types, got {len(results)}"

        # Print summary for verification
        print(f"\n✅ Successfully tested {len(results)} asset types:")
        for asset_name, data in results.items():
            print(
                f"  {asset_name}: {data['symbol']} = ${data['price']} ({data['name']})"
            )

    def test_quote_asset_type_specific_fields(self, api_key, test_symbols):
        """Test that different asset types have appropriate fields populated."""
        # Test stock - should have comprehensive data
        stock_symbol = test_symbols["large_cap"][0]
        stock_result = quote(apikey=api_key, symbol=stock_symbol)
        stock_data = stock_result.root[0]

        # Stocks should have market cap, volume, etc.
        assert hasattr(stock_data, "marketCap"), "Stocks should have market cap"
        assert hasattr(stock_data, "volume"), "Stocks should have volume"
        assert hasattr(stock_data, "name"), "Stocks should have company name"

        # Test ETF - should have similar fields to stocks
        etf_symbol = test_symbols["etf"][0]
        etf_result = quote(apikey=api_key, symbol=etf_symbol)
        etf_data = etf_result.root[0]

        assert hasattr(etf_data, "price"), "ETFs should have price"
        assert hasattr(etf_data, "volume"), "ETFs should have volume"

        # Test crypto - may have different field availability
        crypto_symbol = test_symbols["crypto"][0]
        crypto_result = quote(apikey=api_key, symbol=crypto_symbol)
        crypto_data = crypto_result.root[0]

        assert hasattr(crypto_data, "price"), "Crypto should have price"
        # Note: crypto may not have traditional volume or market cap in same format

        print(
            f"✅ Field validation passed for stock ({stock_symbol}), ETF ({etf_symbol}), and crypto ({crypto_symbol})"
        )


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestQuoteShort:
    """Test class for short quote functionality."""

    def test_quote_short_single_symbol(self, api_key):
        """Test short quote for single symbol."""
        result = quote_short(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate schema for first item
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPQuoteShort.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.price > 0
        assert validated.volume >= 0

    def test_quote_short_multiple_asset_types(self, api_key):
        """Test short quote for different asset types."""
        symbols = ["AAPL", "SPY", "EURUSD", "GCUSD"]

        for symbol in symbols:
            result = quote_short(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                assert symbol_value == symbol

                price_value = get_field_value(first_item, "price")
                assert price_value > 0

    def test_quote_short_vs_full_consistency(self, api_key):
        """Test consistency between short and full quote data."""
        symbol = "MSFT"

        # Get both short and full quotes
        short_result = quote_short(apikey=api_key, symbol=symbol)
        full_result = quote(apikey=api_key, symbol=symbol)

        short_list = extract_data_list(short_result)
        full_list = extract_data_list(full_result)

        if len(short_list) > 0 and len(full_list) > 0:
            short_data = short_list[0]
            full_data = full_list[0]

            # Prices should match (or be very close)
            short_price = get_field_value(short_data, "price")
            full_price = get_field_value(full_data, "price")

            if short_price and full_price:
                price_diff = abs(short_price - full_price) / full_price
                assert price_diff < 0.01  # Less than 1% difference


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestAftermarketQuotes:
    """Test class for aftermarket quote and trade functionality."""

    def test_aftermarket_trade_valid_symbol(self, api_key):
        """Test aftermarket trade data for valid symbol."""
        result = aftermarket_trade(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Aftermarket data might be empty during market hours
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPAftermarketTrade.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            assert validated.price > 0

    def test_aftermarket_quote_valid_symbol(self, api_key):
        """Test aftermarket quote data for valid symbol."""
        result = aftermarket_quote(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Aftermarket data might be empty during market hours
        if len(result_list) > 0:
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPAftermarketQuote.model_validate(first_item)
            else:
                validated = first_item

            assert validated.symbol == "AAPL"
            # FMPAftermarketQuote has bidPrice/askPrice, not price
            assert validated.bidPrice > 0 or validated.askPrice > 0

    def test_aftermarket_multiple_symbols(self, api_key):
        """Test aftermarket data for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            trade_result = aftermarket_trade(apikey=api_key, symbol=symbol)
            quote_result = aftermarket_quote(apikey=api_key, symbol=symbol)

            trade_list = extract_data_list(trade_result)
            quote_list = extract_data_list(quote_result)

            assert isinstance(trade_list, list)
            assert isinstance(quote_list, list)

            # Validate data if present
            for item in trade_list:
                symbol_value = get_field_value(item, "symbol")
                assert symbol_value == symbol

            for item in quote_list:
                symbol_value = get_field_value(item, "symbol")
                assert symbol_value == symbol


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestStockPriceChange:
    """Test class for stock price change functionality."""

    def test_stock_price_change_valid_symbol(self, api_key):
        """Test stock price change for valid symbol."""
        result = stock_price_change(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPStockPriceChange.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        # Check for price change fields
        assert hasattr(validated, "ytd") or hasattr(validated, "_1D")
        assert hasattr(validated, "max")

    def test_stock_price_change_multiple_symbols(self, api_key):
        """Test stock price changes for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        for symbol in symbols:
            result = stock_price_change(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                assert symbol_value == symbol


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestBatchQuotes:
    """Test class for batch quote functionality."""

    def test_stock_batch_quote(self, api_key, test_symbols):
        """Test stock batch quotes with multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

        result = stock_batch_quote(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Should get quotes for each requested symbol
        returned_symbols = {get_field_value(item, "symbol") for item in result_list}
        for symbol in symbols:
            assert (
                symbol in returned_symbols
            ), f"Expected symbol {symbol} not found in batch results"

        # Validate each quote has required fields
        for item in result_list:
            price_value = get_field_value(item, "price")
            symbol_value = get_field_value(item, "symbol")
            assert price_value > 0, f"Price should be positive for {symbol_value}"
            assert (
                symbol_value in symbols
            ), f"Unexpected symbol {symbol_value} in results"

    def test_batch_quote_short(self, api_key):
        """Test batch short quotes."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        result = batch_quote_short(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Should get quotes for multiple symbols
        returned_symbols = {get_field_value(item, "symbol") for item in result_list}
        for symbol in symbols:
            assert symbol in returned_symbols

    def test_batch_aftermarket_trade(self, api_key):
        """Test batch aftermarket trades."""
        symbols = ["AAPL", "MSFT"]

        result = batch_aftermarket_trade(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Aftermarket data might be empty, but should not error
        for item in result_list:
            symbol_value = get_field_value(item, "symbol")
            assert symbol_value in symbols

    def test_batch_aftermarket_quote(self, api_key):
        """Test batch aftermarket quotes."""
        symbols = ["AAPL", "MSFT"]

        result = batch_aftermarket_quote(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Aftermarket data might be empty, but should not error
        for item in result_list:
            symbol_value = get_field_value(item, "symbol")
            assert symbol_value in symbols

    def test_batch_exchange_quote(self, api_key):
        """Test batch quotes for multiple symbols."""
        # Use specific symbols instead of exchange parameter
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = batch_exchange_quote(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get quotes for the specified symbols
        if len(result_list) > 0:
            # Verify we have quote data
            for item in result_list[:3]:  # Check first 3 items
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None

    def test_batch_mutual_fund_quote(self, api_key):
        """Test batch mutual fund quotes."""
        result = batch_mutual_fund_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get mutual fund quotes
        if len(result_list) > 0:
            for item in result_list[:3]:  # Check first 3 items
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None

    def test_batch_etf_quote(self, api_key):
        """Test batch ETF quotes."""
        result = batch_etf_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # ETF data might be empty or limited, but should not error
        if len(result_list) > 0:
            # Should get ETF quotes
            for item in result_list[:5]:  # Check first 5 ETFs
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None

    def test_batch_commodity_quote(self, api_key):
        """Test batch commodity quotes."""
        result = batch_commodity_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get commodity quotes
        if len(result_list) > 0:
            for item in result_list[:3]:  # Check first 3 commodities
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None
                # Commodities typically have USD in symbol
                assert "USD" in symbol_value

    def test_batch_crypto_quote(self, api_key):
        """Test batch cryptocurrency quotes."""
        result = batch_crypto_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get crypto quotes
        if len(result_list) > 0:
            for item in result_list[:3]:  # Check first 3 cryptos
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None
                # Crypto symbols typically have USD suffix
                assert "USD" in symbol_value

    def test_batch_forex_quote(self, api_key):
        """Test batch forex quotes."""
        result = batch_forex_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get forex quotes
        if len(result_list) > 0:
            for item in result_list[:5]:  # Check first 5 forex pairs
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None
                # Forex pairs are typically 6 characters
                assert len(symbol_value) >= 6

    def test_batch_index_quote(self, api_key):
        """Test batch index quotes."""
        result = batch_index_quote(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get index quotes
        if len(result_list) > 0:
            for item in result_list[:3]:  # Check first 3 indices
                price_value = get_field_value(item, "price")
                symbol_value = get_field_value(item, "symbol")
                assert price_value > 0
                assert symbol_value is not None


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestQuoteErrorHandling:
    """Test class for quote error handling scenarios."""

    def test_quote_invalid_api_key(self):
        """Test quote with invalid API key."""
        result = quote(apikey="invalid_key", symbol="AAPL")

        # Should return error message
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            # Some endpoints might return empty lists for invalid keys
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_quote_invalid_symbol(self, api_key):
        """Test quote with invalid symbol."""
        result = quote(apikey=api_key, symbol="INVALID_SYMBOL_XYZ")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Invalid symbol typically returns empty list
        assert len(result_list) == 0

    def test_quote_empty_symbol(self, api_key):
        """Test quote with empty symbol."""
        result = quote(apikey=api_key, symbol="")

        # Should handle empty symbol gracefully
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_batch_quote_invalid_symbols(self, api_key):
        """Test batch quote with some invalid symbols."""
        symbols = ["AAPL", "INVALID_XYZ", "MSFT"]

        result = stock_batch_quote(apikey=api_key, symbols=symbols)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Should get quotes for valid symbols
        returned_symbols = {get_field_value(item, "symbol") for item in result_list}
        assert "AAPL" in returned_symbols
        assert "MSFT" in returned_symbols
        assert "MSFT" in returned_symbols


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestQuoteResponseTimes:
    """Test class for quote response time performance."""

    def test_single_quote_response_time(self, api_key):
        """Test single quote response time."""
        import time

        start_time = time.time()
        result = quote(apikey=api_key, symbol="AAPL")
        end_time = time.time()

        response_time = end_time - start_time

        # Should respond within 5 seconds
        assert response_time < 5.0

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_batch_quote_response_time(self, api_key):
        """Test batch quote response time."""
        import time

        symbols = "AAPL,MSFT,GOOGL,AMZN,TSLA"

        start_time = time.time()
        result = stock_batch_quote(apikey=api_key, symbols=symbols)
        end_time = time.time()

        response_time = end_time - start_time

        # Batch should respond within 10 seconds
        assert response_time < 10.0

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestQuoteDataConsistency:
    """Test class for quote data consistency across endpoints."""

    def test_single_vs_batch_quote_consistency(self, api_key):
        """Test consistency between single and batch quote results."""
        symbol = "AAPL"

        # Get single quote
        single_result = quote(apikey=api_key, symbol=symbol)
        single_list = extract_data_list(single_result)

        # Get batch quote with same symbol
        batch_result = stock_batch_quote(apikey=api_key, symbols=[symbol])
        batch_list = extract_data_list(batch_result)

        if len(single_list) > 0 and len(batch_list) > 0:
            single_data = single_list[0]
            batch_data = batch_list[0]

            # Prices should match (or be very close)
            single_price = get_field_value(single_data, "price")
            batch_price = get_field_value(batch_data, "price")

            if single_price and batch_price:
                price_diff = abs(single_price - batch_price) / single_price
                assert price_diff < 0.05  # Less than 5% difference (market movements)

    def test_different_asset_type_batch_consistency(self, api_key):
        """Test that asset-specific batch endpoints return appropriate data."""
        # Test ETF batch
        etf_result = batch_etf_quote(apikey=api_key)
        etf_list = extract_data_list(etf_result)

        # Test commodity batch
        commodity_result = batch_commodity_quote(apikey=api_key)
        commodity_list = extract_data_list(commodity_result)

        # Test crypto batch
        crypto_result = batch_crypto_quote(apikey=api_key)
        crypto_list = extract_data_list(crypto_result)

        # Each should return appropriate symbols
        if len(etf_list) > 0:
            # ETFs are typically 3-4 character symbols
            etf_symbols = [get_field_value(item, "symbol") for item in etf_list[:3]]
            for symbol in etf_symbols:
                assert len(symbol) <= 5

        if len(commodity_list) > 0:
            # Commodities typically have USD suffix
            commodity_symbols = [
                get_field_value(item, "symbol") for item in commodity_list[:3]
            ]
            for symbol in commodity_symbols:
                assert "USD" in symbol

        if len(crypto_list) > 0:
            # Crypto typically has USD suffix
            crypto_symbols = [
                get_field_value(item, "symbol") for item in crypto_list[:3]
            ]
            for symbol in crypto_symbols:
                assert "USD" in symbol
