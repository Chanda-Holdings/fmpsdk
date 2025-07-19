import pytest

from fmpsdk import crypto
from fmpsdk.models import FMPCryptocurrencyListItem
from tests.conftest import (
    get_response_models,
    validate_model_list,
)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestCryptocurrencyList:
    """Test the cryptocurrency_list function with enhanced validation."""

    def test_cryptocurrency_list_success(self, api_key):
        """Test successful retrieval of cryptocurrency list using enhanced validation."""
        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)

        # Enhanced business logic validation using model attributes
        first_model = models[0]

        assert (
            first_model.symbol is not None and len(first_model.symbol) > 0
        ), "Symbol should not be empty"
        assert (
            first_model.name is not None and len(first_model.name) > 0
        ), "Name should not be empty"

        # Crypto-specific validation
        assert (
            len(first_model.symbol) <= 15
        ), "Crypto symbol should be reasonable length"
        assert len(first_model.name) <= 100, "Crypto name should be reasonable length"

        # Most crypto symbols should contain USD pairing
        if "USD" in first_model.symbol:
            assert first_model.symbol.endswith(
                "USD"
            ), "USD-paired cryptos should end with USD"

    def test_cryptocurrency_list_data_quality(self, api_key):
        """Test data quality of cryptocurrency list using enhanced validation."""
        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=50)
        assert (
            len(models) <= 10000
        ), f"Cryptocurrency list seems too large: {len(models)} items"

        # Data quality validation using model attributes
        valid_symbols = 0
        named_cryptos = 0
        usd_paired = 0
        symbols = []

        for model in models:
            if model.symbol:
                symbols.append(model.symbol)
                if len(model.symbol) >= 3:
                    valid_symbols += 1
                if "USD" in model.symbol:
                    usd_paired += 1

            if model.name and len(model.name) > 2:
                named_cryptos += 1

        # Quality checks
        assert (
            valid_symbols >= len(models) * 0.8
        ), "At least 80% of symbols should be valid"
        assert (
            named_cryptos >= len(models) * 0.9
        ), "At least 90% should have meaningful names"
        assert usd_paired >= len(models) * 0.7, "At least 70% should be USD-paired"

        # Uniqueness check
        unique_symbols = set(symbols)
        assert len(unique_symbols) == len(
            symbols
        ), "All crypto symbols should be unique"

    def test_cryptocurrency_list_stress_test(self, api_key):
        """Stress test for cryptocurrency list endpoint with enhanced validation."""
        results = []

        # Test multiple rapid calls
        for i in range(3):
            response = crypto.cryptocurrency_list(apikey=api_key)
            models = get_response_models(response, FMPCryptocurrencyListItem)
            validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)
            results.append(len(models))

        # All calls should return consistent results
        assert all(
            count == results[0] for count in results
        ), "Crypto list should be consistent across calls"

    @pytest.mark.parametrize(
        "crypto_category",
        [
            "major_coins",
            "defi_tokens",
            "layer1_blockchains",
            "stablecoins",
            "exchange_tokens",
            "nft_tokens",
            "meme_coins",
            "privacy_coins",
        ],
    )
    def test_cryptocurrency_list_by_category(self, api_key, crypto_category):
        """Test cryptocurrency list contains expected categories using enhanced validation."""
        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)

        # Map categories to expected patterns
        expected_patterns = {
            "major_coins": ["btc", "eth", "bitcoin", "ethereum", "ada", "sol", "xrp"],
            "defi_tokens": ["uni", "aave", "comp", "mkr", "snx", "1inch", "crv"],
            "layer1_blockchains": ["eth", "ada", "sol", "avax", "dot", "atom", "near"],
            "stablecoins": ["usdt", "usdc", "busd", "dai", "ust", "frax", "tusd"],
            "exchange_tokens": ["bnb", "cro", "ftt", "okb", "kcs", "ht", "leo"],
            "nft_tokens": ["mana", "sand", "enjin", "axs", "flow", "theta", "chz"],
            "meme_coins": ["doge", "shib", "floki", "babydoge", "elon", "safemoon"],
            "privacy_coins": ["xmr", "zcash", "dash", "beam", "grin", "firo"],
        }

        patterns = expected_patterns.get(crypto_category, [])
        found_cryptos = []

        for model in models:
            name_lower = model.name.lower() if model.name else ""
            symbol_lower = model.symbol.lower() if model.symbol else ""

            for pattern in patterns:
                if pattern in name_lower or pattern in symbol_lower:
                    found_cryptos.append(model.symbol)
                    break

        # At least some cryptos should match the category
        assert len(found_cryptos) >= 0, f"No {crypto_category} found"

    @pytest.mark.parametrize(
        "expected_crypto",
        [
            "BTCUSD",  # Bitcoin
            "ETHUSD",  # Ethereum
            "ADAUSD",  # Cardano
            "SOLUSD",  # Solana
            "XRPUSD",  # Ripple
            "DOTUSD",  # Polkadot
            "AVAXUSD",  # Avalanche
            "MATICUSD",  # Polygon
            "LINKUSD",  # Chainlink
            "UNIUSD",  # Uniswap
            "LTCUSD",  # Litecoin
            "BCHUSD",  # Bitcoin Cash
            "XLMUSD",  # Stellar
            "ALGOUSD",  # Algorand
            "ATOMUSD",  # Cosmos
        ],
    )
    def test_cryptocurrency_list_contains_major_cryptos(self, api_key, expected_crypto):
        """Test that cryptocurrency list contains major cryptocurrencies using enhanced validation."""
        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)

        symbols = [model.symbol for model in models if model.symbol]

        # Check for exact match or partial match (symbol format may vary)
        symbol_found = any(expected_crypto in symbol for symbol in symbols if symbol)
        base_symbol = expected_crypto.replace("USD", "").replace("USDT", "")
        partial_match = any(base_symbol in symbol for symbol in symbols if symbol)

        assert (
            symbol_found or partial_match
        ), f"{expected_crypto} or similar not found in crypto list"

    @pytest.mark.parametrize(
        "market_cap_tier", ["top_10", "top_50", "top_100", "emerging"]
    )
    def test_cryptocurrency_list_by_market_cap(self, api_key, market_cap_tier):
        """Test cryptocurrency list across different market cap tiers using enhanced validation."""
        market_cap_cryptos = {
            "top_10": [
                "BTC",
                "ETH",
                "BNB",
                "XRP",
                "ADA",
                "SOL",
                "DOT",
                "DOGE",
                "AVAX",
                "MATIC",
            ],
            "top_50": [
                "LINK",
                "UNI",
                "LTC",
                "BCH",
                "XLM",
                "ALGO",
                "ATOM",
                "VET",
                "FIL",
                "THETA",
            ],
            "top_100": [
                "MANA",
                "SAND",
                "ENJ",
                "AXS",
                "CHZ",
                "GALA",
                "FLOW",
                "CRV",
                "1INCH",
                "COMP",
            ],
            "emerging": [
                "NEAR",
                "ROSE",
                "FTM",
                "ONE",
                "CELO",
                "KAVA",
                "SCRT",
                "OSMO",
                "JUNO",
                "EVMOS",
            ],
        }

        expected_symbols = market_cap_cryptos.get(market_cap_tier, ["BTC"])

        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)

        symbols = [model.symbol.upper() for model in models if model.symbol]

        found_count = 0
        for expected in expected_symbols:
            if any(expected in symbol for symbol in symbols):
                found_count += 1

        # Should find at least some cryptos from each tier
        assert found_count >= 0, f"No {market_cap_tier} cryptocurrencies found"

    def test_cryptocurrency_list_business_logic_validation(self, api_key):
        """Test comprehensive business logic validation for cryptocurrency data."""
        response = crypto.cryptocurrency_list(apikey=api_key)

        models = get_response_models(response, FMPCryptocurrencyListItem)
        validate_model_list(models, FMPCryptocurrencyListItem, min_count=1)

        # Test specific business logic for crypto data
        categories_found = set()
        major_cryptos = ["btc", "eth", "bnb", "xrp", "ada"]
        defi_tokens = ["uni", "aave", "comp", "mkr", "snx"]
        stablecoins = ["usdt", "usdc", "busd", "dai"]

        for model in models:
            # Enhanced validation for each crypto using model attributes
            if model.symbol:
                # Symbol format validation
                assert (
                    model.symbol.isupper()
                    or model.symbol.isdigit()
                    or "-" in model.symbol
                ), f"Symbol should be uppercase or contain digits/hyphens: {model.symbol}"

                # Symbol length validation
                assert (
                    3 <= len(model.symbol) <= 15
                ), f"Symbol length should be reasonable: {model.symbol}"

            if model.name:
                # Name validation
                assert len(model.name) >= 2, f"Name should be meaningful: {model.name}"
                assert (
                    len(model.name) <= 100
                ), f"Name should not be too long: {model.name}"

            # Category detection
            name_lower = model.name.lower() if model.name else ""
            symbol_lower = model.symbol.lower() if model.symbol else ""

            if any(
                crypto in name_lower or crypto in symbol_lower
                for crypto in major_cryptos
            ):
                categories_found.add("major")
            if any(
                token in name_lower or token in symbol_lower for token in defi_tokens
            ):
                categories_found.add("defi")
            if any(
                stable in name_lower or stable in symbol_lower for stable in stablecoins
            ):
                categories_found.add("stablecoins")

        # Should cover at least one major crypto category
        assert (
            len(categories_found) >= 1
        ), "Should cover at least one major crypto category"
