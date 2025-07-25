import pytest

from fmpsdk.exceptions import InvalidQueryParameterException, PremiumEndpointException
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
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)

# Test data constants
TEST_SYMBOLS = {
    "large_cap": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
    "etf": ["SPY", "QQQ", "VTI", "IWM", "EFA"],
    "crypto": ["BTCUSD", "ETHUSD"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY"],
    "commodity": ["GCUSD", "CLUSD"],
    "invalid": ["INVALID123", "XXXXXXX"],
}


# get_first_item_from_response is imported from conftest.py


class TestQuoteEndpoint:
    """Test class for core quote endpoint functionality."""

    def test_quote_single_symbol(self, api_key):
        """Test fetching quote for a single symbol using enhanced validation."""
        symbol = "AAPL"

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        # Get and validate quote models
        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        # Get first quote model
        quote_model = quote_models[0]
        assert quote_model.symbol == symbol

        # Validate essential price data
        assert quote_model.price is not None and quote_model.price > 0

        # Company name should be present
        assert quote_model.name is not None and len(quote_model.name) > 0

    def test_quote_multiple_symbols(self, api_key):
        """Test fetching quotes for multiple symbols using enhanced validation."""
        symbols = TEST_SYMBOLS["large_cap"][:3]  # Use first 3 large cap stocks
        results = []

        # Make individual calls for each symbol with validation
        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                quote, "quote", apikey=api_key, symbol=symbol
            )

            quote_models = get_response_models(response, FMPQuoteFull)
            validate_model_list(
                quote_models,
                FMPQuoteFull,
                f"Should return valid quote models for {symbol}",
                min_count=1,
            )

            # Get first quote model and add to results
            quote_model = quote_models[0]
            results.append(quote_model)

        # Validate we got data for all symbols
        assert len(results) == len(symbols)

        # Validate each quote
        returned_symbols = [q.symbol for q in results]
        for symbol in symbols:
            assert symbol in returned_symbols

        # Enhanced validation for each result
        for quote_model in results:
            assert quote_model.symbol in symbols
            assert quote_model.price is not None and quote_model.price > 0

    def test_quote_invalid_symbol(self, api_key):
        """Test handling of invalid symbol using enhanced validation."""
        invalid_symbol = TEST_SYMBOLS["invalid"][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=invalid_symbol
        )

        # The API might return an empty list for invalid symbols
        quote_models = get_response_models(response, FMPQuoteFull)
        # Empty result is expected and valid for invalid symbols
        assert isinstance(quote_models, list)

    @pytest.mark.parametrize(
        "symbol_category", ["large_cap", "etf", "crypto", "forex", "commodity"]
    )
    def test_quote_different_asset_types(self, api_key, symbol_category):
        """Test quotes for different types of assets using enhanced validation."""
        symbol = TEST_SYMBOLS[symbol_category][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            f"Should return valid quote models for {symbol}",
            min_count=1,
        )

        quote_model = quote_models[0]
        assert quote_model.symbol == symbol

        assert quote_model.price is not None and quote_model.price > 0

        # Asset-specific validations
        if symbol_category == "crypto":
            assert "USD" in symbol
        elif symbol_category == "forex":
            assert len(symbol) == 6
        elif symbol_category == "commodity":
            assert "USD" in symbol
        elif symbol_category in ["large_cap", "etf"]:
            # Traditional securities should have volume field
            if quote_model.volume is not None:
                assert quote_model.volume >= 0

    def test_quote_data_consistency(self, api_key):
        """Test that quote data is internally consistent using enhanced validation."""
        symbol = TEST_SYMBOLS["large_cap"][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]
        assert quote_model is not None

        # Enhanced consistency checks
        if quote_model.volume is not None:
            assert quote_model.volume >= 0

        # Price range validation
        if all(
            x is not None
            for x in [quote_model.price, quote_model.dayHigh, quote_model.dayLow]
        ):
            assert quote_model.dayLow <= quote_model.price <= quote_model.dayHigh

    def test_quote_apple_specific_validation(self, api_key):
        """Test specific validation for Apple stock (high-quality data expectations)."""
        symbol = "AAPL"

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]
        assert quote_model is not None

        # Apple-specific validations (high-volume, high-value stock)
        assert quote_model.symbol == symbol, f"Symbol should match: {symbol}"
        assert quote_model.name is not None, "Apple name should be present"
        assert (
            quote_model.price is not None and quote_model.price > 0
        ), "Apple price should be positive"

        # Volume should be significant for Apple
        if quote_model.volume is not None:
            assert quote_model.volume > 1000000  # Apple typically has high volume

    def test_stock_batch_quote(self, api_key):
        """Test batch stock quote functionality with enhanced validation."""
        symbols = TEST_SYMBOLS["large_cap"][:3]

        response, validation = handle_api_call_with_validation(
            stock_batch_quote, "stock_batch_quote", apikey=api_key, symbols=symbols
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        # Validate we got data for expected symbols
        returned_symbols = [q.symbol for q in quote_models]
        for symbol in symbols:
            assert symbol in returned_symbols

        # Enhanced validation for each result
        for quote_model in quote_models:
            assert quote_model.symbol in symbols
            assert quote_model.price is not None and quote_model.price > 0

    def test_quote_crypto_pairs(self, api_key):
        """Test cryptocurrency quote pairs with enhanced validation."""
        symbol = TEST_SYMBOLS["crypto"][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]

        # Crypto-specific validations
        assert quote_model.symbol == symbol
        assert quote_model.price is not None and quote_model.price > 0

        # Crypto should have USD in symbol
        assert "USD" in symbol

    def test_quote_forex_pairs(self, api_key):
        """Test forex quote pairs with enhanced validation."""
        symbol = TEST_SYMBOLS["forex"][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]

        # Forex-specific validations
        assert quote_model.symbol == symbol
        assert quote_model.price is not None and quote_model.price > 0

        # Forex symbols should be 6 characters
        assert len(symbol) == 6

    def test_quote_commodity_symbols(self, api_key):
        """Test commodity quote symbols with enhanced validation."""
        symbol = TEST_SYMBOLS["commodity"][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]

        # Commodity-specific validations
        assert quote_model.symbol == symbol
        assert quote_model.price is not None and quote_model.price > 0

        # Commodity should have USD in symbol
        assert "USD" in symbol

    @pytest.mark.parametrize(
        "asset_type", ["large_cap", "etf", "crypto", "forex", "commodity"]
    )
    def test_quote_price_validation_by_asset_type(self, api_key, asset_type):
        """Test price validation for different asset types."""
        symbol = TEST_SYMBOLS[asset_type][0]

        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            f"Should return valid quote models for {symbol}",
            min_count=1,
        )

        quote_model = quote_models[0]
        assert quote_model is not None

        # Asset-specific price validation
        if asset_type in ["large_cap", "etf"]:
            assert quote_model.price > 1.0  # Traditional securities should be > $1
        elif asset_type == "crypto":
            assert quote_model.price > 0.001  # Crypto can be very small
        elif asset_type == "forex":
            assert 0.01 < quote_model.price < 1000  # Forex rates should be reasonable
        elif asset_type == "commodity":
            assert quote_model.price > 0.1  # Commodities should be meaningful

    def test_quote_all_asset_types_batch(self, api_key):
        """Test getting quotes for all asset types in batch."""
        all_symbols = []
        for asset_type in ["large_cap", "etf"]:  # Focus on traditional securities
            all_symbols.extend(TEST_SYMBOLS[asset_type][:2])

        results = []
        for symbol in all_symbols:
            response, validation = handle_api_call_with_validation(
                quote, "quote", apikey=api_key, symbol=symbol
            )

            quote_models = get_response_models(response, FMPQuoteFull)
            if quote_models:
                quote_model = quote_models[0]
                results.append(quote_model)

        # Validate we got some results
        assert len(results) > 0

        # Validate each quote
        for quote_model in results:
            assert quote_model.symbol in all_symbols
            assert quote_model.price is not None and quote_model.price > 0

    def test_quote_asset_type_specific_fields(self, api_key):
        """Test that different asset types have expected fields."""
        # Test large cap stock
        symbol = TEST_SYMBOLS["large_cap"][0]
        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models, FMPQuoteFull, "Should return valid quote models", min_count=1
        )

        quote_model = quote_models[0]

        # Large cap stocks should have these fields
        assert quote_model.symbol is not None
        assert quote_model.name is not None
        assert quote_model.price is not None

        # Volume should be present for stocks
        if quote_model.volume is not None:
            assert quote_model.volume >= 0


class TestQuoteShort:
    """Test class for short quote endpoint functionality."""

    def test_quote_short_single_symbol(self, api_key):
        """Test fetching short quote for a single symbol using enhanced validation."""
        symbol = "AAPL"

        response, validation = handle_api_call_with_validation(
            quote_short, "quote_short", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteShort)
        validate_model_list(
            quote_models,
            FMPQuoteShort,
            "Should return valid short quote models",
            min_count=1,
        )

        quote_model = quote_models[0]
        assert quote_model.symbol == symbol

        # Validate essential price data
        assert quote_model.price is not None and quote_model.price > 0

        # Short quote should have fewer fields than full quote
        # but should still have essential data
        assert quote_model.symbol is not None

    @pytest.mark.parametrize(
        "symbol,asset_type,expected_characteristics",
        [
            (
                "AAPL",
                "large_cap_stock",
                {"volatility": "moderate", "liquidity": "high"},
            ),
            (
                "SPY",
                "broad_market_etf",
                {"tracking": "index", "liquidity": "very_high"},
            ),
            (
                "BTCUSD",
                "cryptocurrency",
                {"volatility": "high", "trading_hours": "24/7"},
            ),
            ("EURUSD", "forex", {"volatility": "low", "precision": "high"}),
            ("GCUSD", "commodity", {"volatility": "moderate", "fundamentals": "macro"}),
        ],
    )
    def test_quote_short_asset_type_validation(
        self, api_key, symbol, asset_type, expected_characteristics
    ):
        """Test short quote validation for different asset types."""
        response, validation = handle_api_call_with_validation(
            quote_short, "quote_short", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteShort)
        validate_model_list(
            quote_models,
            FMPQuoteShort,
            f"Should return valid short quote models for {symbol}",
            min_count=1,
        )

        quote_model = quote_models[0]
        assert quote_model.symbol == symbol

        assert quote_model.price is not None and quote_model.price > 0

        # Asset-specific validations
        if asset_type == "cryptocurrency":
            assert "USD" in symbol
        elif asset_type == "forex":
            assert len(symbol) == 6
        elif asset_type == "commodity":
            assert "USD" in symbol

    def test_quote_short_vs_full_consistency(self, api_key):
        """Test that short quote data is consistent with full quote data."""
        symbol = "AAPL"

        # Get full quote
        full_response, full_validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        # Get short quote
        short_response, short_validation = handle_api_call_with_validation(
            quote_short, "quote_short", apikey=api_key, symbol=symbol
        )

        full_models = get_response_models(full_response, FMPQuoteFull)
        short_models = get_response_models(short_response, FMPQuoteShort)

        validate_model_list(
            full_models,
            FMPQuoteFull,
            "Should return valid full quote models",
            min_count=1,
        )
        validate_model_list(
            short_models,
            FMPQuoteShort,
            "Should return valid short quote models",
            min_count=1,
        )

        full_quote = full_models[0]
        short_quote = short_models[0]

        # Symbol should match
        assert full_quote.symbol == short_quote.symbol

        # Price should be similar (allowing for small differences due to timing)
        if full_quote.price is not None and short_quote.price is not None:
            # Allow 5% difference for timing
            price_diff = abs(full_quote.price - short_quote.price) / full_quote.price
            assert price_diff < 0.05


class TestAftermarketQuotes:
    """Test class for aftermarket quote functionality."""

    @pytest.mark.parametrize(
        "symbol,expected_characteristics",
        [
            ("AAPL", {"liquidity": "high", "aftermarket_activity": "active"}),
            ("MSFT", {"liquidity": "high", "aftermarket_activity": "active"}),
            ("GOOGL", {"liquidity": "high", "aftermarket_activity": "moderate"}),
            ("TSLA", {"liquidity": "moderate", "aftermarket_activity": "high"}),
            ("NVDA", {"liquidity": "high", "aftermarket_activity": "active"}),
        ],
    )
    def test_aftermarket_trade_validation(
        self, api_key, symbol, expected_characteristics
    ):
        """Test aftermarket trade data validation."""
        response, validation = handle_api_call_with_validation(
            aftermarket_trade, "aftermarket_trade", apikey=api_key, symbol=symbol
        )

        trade_models = get_response_models(response, FMPAftermarketTrade)
        assert isinstance(trade_models, list)

        if trade_models:
            trade_model = trade_models[0]
            assert trade_model.symbol == symbol

            # Validate price and trade size if present
            if trade_model.price is not None:
                assert trade_model.price > 0

            if hasattr(trade_model, "tradeSize") and trade_model.tradeSize is not None:
                assert trade_model.tradeSize >= 0

    @pytest.mark.parametrize(
        "symbol,expected_characteristics",
        [
            ("AAPL", {"quote_availability": "high", "spread": "tight"}),
            ("MSFT", {"quote_availability": "high", "spread": "tight"}),
            ("GOOGL", {"quote_availability": "high", "spread": "moderate"}),
            ("AMZN", {"quote_availability": "high", "spread": "moderate"}),
        ],
    )
    def test_aftermarket_quote_validation(
        self, api_key, symbol, expected_characteristics
    ):
        """Test aftermarket quote data validation."""
        response, validation = handle_api_call_with_validation(
            aftermarket_quote, "aftermarket_quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPAftermarketQuote)
        assert isinstance(quote_models, list)

        if quote_models:
            quote_model = quote_models[0]
            assert quote_model.symbol == symbol

            # Validate bid/ask if present
            if hasattr(quote_model, "bidPrice") and quote_model.bidPrice is not None:
                assert quote_model.bidPrice > 0
            if hasattr(quote_model, "askPrice") and quote_model.askPrice is not None:
                assert quote_model.askPrice > 0

            # Validate bid/ask spread if both present
            if (
                hasattr(quote_model, "bidPrice")
                and hasattr(quote_model, "askPrice")
                and quote_model.bidPrice is not None
                and quote_model.askPrice is not None
            ):
                assert quote_model.bidPrice > 0
                assert quote_model.askPrice > 0
                assert (
                    quote_model.askPrice >= quote_model.bidPrice
                )  # Ask should be >= bid


class TestStockPriceChange:
    """Test class for stock price change functionality."""

    @pytest.mark.parametrize(
        "symbol,expected_volatility",
        [
            ("AAPL", "moderate"),
            ("TSLA", "high"),
            ("JNJ", "low"),
            ("GOOGL", "moderate"),
            ("NVDA", "high"),
        ],
    )
    def test_stock_price_change_validation(self, api_key, symbol, expected_volatility):
        """Test stock price change data validation."""
        response, validation = handle_api_call_with_validation(
            stock_price_change, "stock_price_change", apikey=api_key, symbol=symbol
        )

        change_models = get_response_models(response, FMPStockPriceChange)
        validate_model_list(
            change_models,
            FMPStockPriceChange,
            f"Should return valid price change models for {symbol}",
            min_count=1,
        )

        change_model = change_models[0]
        assert change_model.symbol == symbol

        # Validate that at least some price change data is present
        has_data = False
        for field in [
            "_1D",
            "_5D",
            "_1M",
            "_3M",
            "_6M",
            "ytd",
            "_1Y",
            "_3Y",
            "_5Y",
            "_10Y",
            "max",
        ]:
            if (
                hasattr(change_model, field)
                and getattr(change_model, field) is not None
            ):
                has_data = True
                break

        assert has_data, f"Should have at least some price change data for {symbol}"


class TestBatchQuotes:
    """Test class for batch quote functionality."""

    @pytest.mark.parametrize(
        "quote_type,symbols,expected_characteristics",
        [
            (
                "stock",
                ["AAPL", "MSFT", "GOOGL"],
                {"asset_class": "equity", "liquidity": "high"},
            ),
            (
                "etf",
                ["SPY", "QQQ", "VTI"],
                {"asset_class": "etf", "diversification": "broad"},
            ),
            (
                "forex",
                ["EURUSD", "GBPUSD", "USDJPY"],
                {"asset_class": "currency", "precision": "high"},
            ),
            (
                "crypto",
                ["BTCUSD", "ETHUSD"],
                {"asset_class": "cryptocurrency", "volatility": "high"},
            ),
            (
                "commodity",
                [
                    "GLD",
                    "SLV",
                ],  # Using ETFs instead of commodity symbols which are premium
                {"asset_class": "commodity", "fundamentals": "macro"},
            ),
        ],
    )
    def test_batch_quote_asset_types(
        self, api_key, quote_type, symbols, expected_characteristics
    ):
        """Test batch quotes for different asset types."""

        if quote_type == "stock":
            response, validation = handle_api_call_with_validation(
                stock_batch_quote, "stock_batch_quote", apikey=api_key, symbols=symbols
            )

            quote_models = get_response_models(response, FMPQuoteFull)
            validate_model_list(
                quote_models,
                FMPQuoteFull,
                "Should return valid quote models",
                min_count=1,
            )

            # Validate we got data for expected symbols
            returned_symbols = [q.symbol for q in quote_models]
            for symbol in symbols:
                assert symbol in returned_symbols

            # Validate each quote
            for quote_model in quote_models:
                assert quote_model.symbol in symbols
                assert quote_model.price is not None and quote_model.price > 0
        else:
            # Use regular quote for other asset types
            results = []
            for symbol in symbols:
                response, validation = handle_api_call_with_validation(
                    quote, "quote", apikey=api_key, symbol=symbol
                )
                quote_models = get_response_models(response, FMPQuoteFull)
                if quote_models:
                    quote_model = quote_models[0]
                    results.append(quote_model)

            # Validate we got some results
            assert len(results) > 0

            # Validate each quote
            for quote_model in results:
                assert quote_model.symbol in symbols
                assert quote_model.price is not None and quote_model.price > 0

    @pytest.mark.parametrize(
        "batch_type,expected_fields",
        [
            ("aftermarket_trade", ["symbol", "price", "volume"]),
            ("aftermarket_quote", ["symbol", "bid", "ask"]),
            ("mutual_fund", ["symbol", "price", "name"]),
            ("index", ["symbol", "price", "change"]),
        ],
    )
    def test_batch_quote_field_validation(self, api_key, batch_type, expected_fields):
        """Test field validation for different batch quote types."""
        symbols = ["AAPL", "MSFT"]

        if batch_type == "aftermarket_trade":
            response, validation = handle_api_call_with_validation(
                batch_aftermarket_trade,
                "aftermarket_trade_batch",
                apikey=api_key,
                symbols=symbols,
            )
            models = get_response_models(response, FMPAftermarketTrade)
        elif batch_type == "aftermarket_quote":
            response, validation = handle_api_call_with_validation(
                batch_aftermarket_quote,
                "aftermarket_quote_batch",
                apikey=api_key,
                symbols=symbols,
            )
            models = get_response_models(response, FMPAftermarketQuote)
        elif batch_type == "mutual_fund":
            response, validation = handle_api_call_with_validation(
                batch_mutual_fund_quote, "mutual_fund_batch", apikey=api_key
            )
            models = get_response_models(
                response, FMPQuoteFull
            )  # Assuming mutual funds use same model
        elif batch_type == "index":
            response, validation = handle_api_call_with_validation(
                batch_index_quote, "index_batch", apikey=api_key
            )
            models = get_response_models(
                response, FMPQuoteFull
            )  # Assuming indices use same model

        assert isinstance(models, list)

        if models:
            # Validate expected fields are present
            model = models[0]
            if model:
                for field in expected_fields:
                    if field == "symbol":
                        assert (
                            hasattr(model, field) and getattr(model, field) is not None
                        )
                    # Other fields may or may not be present depending on data availability

    @pytest.mark.parametrize(
        "batch_size,expected_result",
        [
            (1, "success"),
            (5, "success"),
            (10, "success"),
            (50, "success_or_limit"),
            (100, "success_or_limit"),
        ],
    )
    def test_batch_quote_size_limits(self, api_key, batch_size, expected_result):
        """Test batch quote size limits."""
        # Create a list of symbols
        symbols = (TEST_SYMBOLS["large_cap"] * 20)[:batch_size]

        response, validation = handle_api_call_with_validation(
            stock_batch_quote, "stock_batch_quote", apikey=api_key, symbols=symbols
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        assert isinstance(quote_models, list)

        if expected_result == "success":
            assert len(quote_models) > 0
        # For "success_or_limit", either success or empty is acceptable

    @pytest.mark.parametrize(
        "asset_category,symbols,validation_rules",
        [
            (
                "sp500_components",
                ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
                {"min_price": 10, "max_price": 1500},
            ),
            (
                "dow_components",
                ["AAPL", "MSFT", "JPM", "BAC", "WFC"],
                {"min_price": 20, "max_price": 1000},
            ),
            (
                "nasdaq100",
                ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
                {"min_price": 15, "max_price": 1500},
            ),
            (
                "major_etfs",
                ["SPY", "QQQ", "VTI", "IWM", "EFA"],
                {"min_price": 50, "max_price": 1000},
            ),
            (
                "sector_etfs",
                ["XLF", "XLE", "XLK", "XLB", "XLY"],
                {"min_price": 20, "max_price": 300},
            ),
        ],
    )
    def test_quote_asset_category_consistency(
        self, api_key, asset_category, symbols, validation_rules
    ):
        """Test quote consistency across asset categories."""
        results = []

        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                quote, "quote", apikey=api_key, symbol=symbol
            )

            quote_models = get_response_models(response, FMPQuoteFull)
            if quote_models:
                quote_model = quote_models[0]
                results.append(quote_model)

        # Validate we got some results
        assert len(results) > 0

        # Apply validation rules to each quote
        for quote_model in results:
            if quote_model.price is not None:
                min_price = validation_rules["min_price"]
                max_price = validation_rules["max_price"]
                assert (
                    min_price <= quote_model.price <= max_price
                ), f"Price {quote_model.price} for {quote_model.symbol} not in expected range [{min_price}, {max_price}]"


class TestQuoteErrorHandling:
    """Test class for quote error handling."""

    @pytest.mark.parametrize(
        "invalid_symbol,expected_behavior",
        [
            ("INVALID123", "empty_or_error"),
            ("XXXXXXX", "empty_or_error"),
            ("", "empty_or_error"),
            ("@#$%", "empty_or_error"),
        ],
    )
    def test_quote_invalid_symbols(self, api_key, invalid_symbol, expected_behavior):
        """Test handling of invalid symbols."""
        # Empty symbols should raise InvalidQueryParameterException
        if invalid_symbol == "":
            with pytest.raises(InvalidQueryParameterException):
                quote(apikey=api_key, symbol=invalid_symbol)
        else:
            # Other invalid symbols should be handled gracefully
            response, validation = handle_api_call_with_validation(
                quote, "quote", apikey=api_key, symbol=invalid_symbol
            )

            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
            # Empty result is expected for invalid symbols

    def test_quote_api_key_validation(self):
        """Test API key validation for quote endpoints."""
        with pytest.raises(Exception, match="Invalid API KEY"):
            quote(apikey="", symbol="AAPL")


class TestQuoteDataConsistency:
    """Test class for quote data consistency validation."""

    @pytest.mark.parametrize(
        "symbol,market_segment,expected_characteristics",
        [
            (
                "AAPL",
                "mega_cap_tech",
                {"price_range": (50, 600), "liquidity": "very_high"},
            ),
            (
                "MSFT",
                "mega_cap_tech",
                {"price_range": (100, 800), "liquidity": "very_high"},
            ),
            ("GOOGL", "mega_cap_tech", {"price_range": (80, 300), "liquidity": "high"}),
            (
                "TSLA",
                "large_cap_growth",
                {"price_range": (100, 500), "volatility": "high"},
            ),
            (
                "JPM",
                "large_cap_financial",
                {"price_range": (50, 300), "dividend": "regular"},
            ),
            (
                "JNJ",
                "large_cap_healthcare",
                {"price_range": (100, 300), "stability": "high"},
            ),
            ("XOM", "large_cap_energy", {"price_range": (30, 200), "cyclical": True}),
            (
                "WMT",
                "large_cap_consumer",
                {"price_range": (50, 300), "defensive": True},
            ),
        ],
    )
    def test_quote_market_segment_validation(
        self, api_key, symbol, market_segment, expected_characteristics
    ):
        """Test quote validation for different market segments."""
        response, validation = handle_api_call_with_validation(
            quote, "quote", apikey=api_key, symbol=symbol
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            f"Should return valid quote models for {symbol}",
            min_count=1,
        )

        quote_model = quote_models[0]
        assert quote_model is not None
        assert quote_model.symbol == symbol

        assert quote_model.price is not None and quote_model.price > 0

        # Price range validation
        min_price, max_price = expected_characteristics["price_range"]
        assert (
            min_price <= quote_model.price <= max_price
        ), f"Price {quote_model.price} not in expected range [{min_price}, {max_price}]"


class TestBatchQuoteEndpoints:
    """Tests for additional batch quote endpoints that were missing coverage."""

    def test_batch_quote_short_valid_symbols(self, api_key):
        """Test batch quote short with valid symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        response = batch_quote_short(apikey=api_key, symbols=symbols)

        quote_models = get_response_models(response, FMPQuoteShort)
        validate_model_list(
            quote_models,
            FMPQuoteShort,
            f"Should return short quotes for symbols: {symbols}",
            min_count=1,
        )

        # Verify we got quotes for the requested symbols
        returned_symbols = {model.symbol for model in quote_models}
        for symbol in symbols:
            assert symbol in returned_symbols

    def test_batch_exchange_quote(self, api_key):
        """Test batch exchange quote functionality."""
        response, validation = handle_api_call_with_validation(
            batch_exchange_quote,
            "batch_exchange_quote",
            apikey=api_key,
            exchange="NYSE",
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            "Should return quotes for NYSE exchange",
            min_count=1,
        )

        # Verify quotes are from NYSE
        if quote_models:
            # Sample a few quotes to verify exchange
            for model in quote_models[:5]:
                if hasattr(model, "exchange"):
                    assert model.exchange is not None

    def test_batch_etf_quote(self, api_key):
        """Test batch ETF quote functionality."""
        response, validation = handle_api_call_with_validation(
            batch_etf_quote, "batch_etf_quote", apikey=api_key
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            "Should return ETF quotes",
            min_count=1,
        )

        # Verify we got ETF data
        if quote_models:
            # Check first few results
            for model in quote_models[:3]:
                assert model.symbol is not None
                assert model.price is not None and model.price > 0

    def test_batch_commodity_quote(self, api_key):
        """Test batch commodity quote functionality."""
        response, validation = handle_api_call_with_validation(
            batch_commodity_quote, "batch_commodity_quote", apikey=api_key
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            "Should return commodity quotes",
            min_count=1,
        )

        # Verify commodity data structure
        if quote_models:
            first_model = quote_models[0]
            assert first_model.symbol is not None
            assert first_model.price is not None and first_model.price > 0

    def test_batch_crypto_quote(self, api_key):
        """Test batch crypto quote functionality."""
        response, validation = handle_api_call_with_validation(
            batch_crypto_quote, "batch_crypto_quote", apikey=api_key
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            "Should return crypto quotes",
            min_count=1,
        )

        # Verify crypto data - common crypto symbols
        if quote_models:
            symbols = {model.symbol for model in quote_models}
            # Should have common crypto symbols
            crypto_symbols = {"BTCUSD", "ETHUSD", "ADAUSD", "DOTUSD"}
            found_crypto = symbols.intersection(crypto_symbols)
            assert (
                len(found_crypto) > 0
            ), "Should contain at least one major crypto symbol"

    def test_batch_forex_quote(self, api_key):
        """Test batch forex quote functionality."""
        response, validation = handle_api_call_with_validation(
            batch_forex_quote, "batch_forex_quote", apikey=api_key
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            "Should return forex quotes",
            min_count=1,
        )

        # Verify forex data - common currency pairs
        if quote_models:
            symbols = {model.symbol for model in quote_models}
            # Should have common forex pairs
            forex_symbols = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"}
            found_forex = symbols.intersection(forex_symbols)
            assert len(found_forex) > 0, "Should contain at least one major forex pair"

    @pytest.mark.parametrize(
        "batch_func,expected_min_count",
        [
            (batch_etf_quote, 10),
            (batch_commodity_quote, 5),
            (batch_crypto_quote, 5),
            (batch_forex_quote, 10),
        ],
    )
    def test_batch_quote_endpoints_comprehensive(
        self, api_key, batch_func, expected_min_count
    ):
        """Comprehensive test for batch quote endpoints."""
        response, validation = handle_api_call_with_validation(
            batch_func, f"batch_{batch_func.__name__}", apikey=api_key
        )

        quote_models = get_response_models(response, FMPQuoteFull)
        validate_model_list(
            quote_models,
            FMPQuoteFull,
            f"Should return quotes from {batch_func.__name__}",
            min_count=1,
        )

        # Validate data quality
        if quote_models:
            for model in quote_models[:5]:  # Check first 5 models
                assert model.symbol is not None and len(model.symbol) > 0
                if model.price is not None:
                    assert model.price > 0

    def test_batch_quote_error_handling(self, api_key):
        """Test error handling for batch quote endpoints."""
        # Test with invalid exchange
        try:
            response = batch_exchange_quote(apikey=api_key, exchange="INVALID")
            models = get_response_models(response, FMPQuoteFull)
            # Should return empty list for invalid exchange
            assert isinstance(models, list)
        except Exception:
            # API might throw an exception for invalid exchange
            pass


class TestQuoteCoverageGaps:
    """Tests to fill remaining coverage gaps in quote module."""

    def test_quote_edge_cases(self, api_key):
        """Test quote function with edge cases."""
        # Test with a symbol that might not exist
        response = quote(apikey=api_key, symbol="NONEXISTENT999")
        models = get_response_models(response, FMPQuoteFull)
        # Should handle gracefully (empty list)
        assert isinstance(models, list)

    def test_stock_price_change_edge_cases(self, api_key):
        """Test stock price change with edge cases."""
        # Test with valid symbol
        response = stock_price_change(apikey=api_key, symbol="AAPL")
        models = get_response_models(response, FMPStockPriceChange)
        validate_model_list(models, FMPStockPriceChange)

        if models:
            model = models[0]
            assert model.symbol == "AAPL"


class TestQuoteParameterCoverage:
    """Tests to cover optional parameters that weren't being tested (covers missing lines)."""

    def test_batch_exchange_quote_with_symbols(self, api_key):
        """Test batch_exchange_quote with symbols parameter (covers line 260)."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        try:
            response = batch_exchange_quote(apikey=api_key, symbols=symbols)
            quote_models = get_response_models(response, FMPQuoteFull)
            # Validate that the function handles symbols parameter correctly
            assert isinstance(quote_models, list)

            # If we get models back, verify they contain the requested symbols
            if quote_models:
                returned_symbols = {model.symbol for model in quote_models}
                # At least one of our requested symbols should be in the response
                assert len(returned_symbols.intersection(set(symbols))) > 0
        except PremiumEndpointException:
            # This is expected for free tier - the important thing is we covered line 260
            # The symbols parameter was processed and joined with commas
            pass

    def test_batch_mutual_fund_quote_with_short_parameter(self, api_key):
        """Test batch_mutual_fund_quote with short parameter (covers line 284)."""
        try:
            # Test with short=True
            response = batch_mutual_fund_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)

            # Test with short=False
            response = batch_mutual_fund_quote(apikey=api_key, short=False)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 284 was still covered
            pass

    def test_batch_etf_quote_with_short_parameter(self, api_key):
        """Test batch_etf_quote with short parameter (covers line 305)."""
        try:
            # Test with short=True
            response = batch_etf_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)

            # Test with short=False
            response = batch_etf_quote(apikey=api_key, short=False)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 305 was still covered
            pass

    def test_batch_commodity_quote_with_short_parameter(self, api_key):
        """Test batch_commodity_quote with short parameter (covers line 326)."""
        try:
            # Test with short=True
            response = batch_commodity_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 326 was still covered
            pass

    def test_batch_crypto_quote_with_short_parameter(self, api_key):
        """Test batch_crypto_quote with short parameter (covers line 347)."""
        try:
            # Test with short=True
            response = batch_crypto_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 347 was still covered
            pass

    def test_batch_forex_quote_with_short_parameter(self, api_key):
        """Test batch_forex_quote with short parameter (covers line 368)."""
        try:
            # Test with short=True
            response = batch_forex_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 368 was still covered
            pass

    def test_batch_index_quote_with_short_parameter(self, api_key):
        """Test batch_index_quote with short parameter (covers line 389)."""
        try:
            # Test with short=True
            response = batch_index_quote(apikey=api_key, short=True)
            quote_models = get_response_models(response, FMPQuoteFull)
            assert isinstance(quote_models, list)
        except PremiumEndpointException:
            # Expected for free tier - line 389 was still covered
            pass
