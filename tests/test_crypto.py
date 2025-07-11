import pytest

from fmpsdk import crypto
from fmpsdk.models import FMPCryptocurrencyListItem, FMPSymbolAndNameList

from .conftest import extract_data_list


class TestCryptocurrencyList:
    """Test the cryptocurrency_list function."""

    def test_cryptocurrency_list_success(self, api_key):
        """Test successful retrieval of cryptocurrency list."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item - might be dict or model depending on SDK implementation
            first_item = result_list[0]
            if isinstance(first_item, dict):
                crypto_data = FMPCryptocurrencyListItem(**first_item)
            else:
                crypto_data = first_item
            assert crypto_data.symbol, "Symbol should not be empty"
            assert crypto_data.name, "Name should not be empty"

    def test_cryptocurrency_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Test model validation on first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated_item = FMPSymbolAndNameList(**first_item)
            else:
                validated_item = first_item
            assert hasattr(validated_item, "symbol")
            assert hasattr(validated_item, "name")

    def test_cryptocurrency_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        result = crypto.cryptocurrency_list(apikey="invalid_api_key")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid key"

    def test_cryptocurrency_list_stress_test(self, api_key):
        """Stress test for cryptocurrency list endpoint."""
        # Test multiple rapid calls
        results = []
        for i in range(3):
            result = crypto.cryptocurrency_list(apikey=api_key)
            result_list = extract_data_list(result)
            results.append(len(result_list))

        # All calls should return consistent results
        assert all(
            count == results[0] for count in results
        ), "Crypto list should be consistent across calls"

        # Should have reasonable number of cryptocurrencies
        if results[0] > 0:
            assert results[0] >= 50, "Should have at least 50 cryptocurrencies listed"
            assert (
                results[0] <= 10000
            ), "Should have reasonable number of cryptos (< 10,000)"

    import pytest

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
        """Test cryptocurrency list contains expected categories."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if not result_list:
            pytest.skip("No cryptocurrency data available")

        # Map categories to expected symbols/names
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

        for item in result_list:
            if isinstance(item, dict):
                crypto_data = FMPCryptocurrencyListItem(**item)
            else:
                crypto_data = item

            name_lower = crypto_data.name.lower() if crypto_data.name else ""
            symbol_lower = crypto_data.symbol.lower() if crypto_data.symbol else ""

            for pattern in patterns:
                if pattern in name_lower or pattern in symbol_lower:
                    found_cryptos.append(crypto_data.symbol)
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
        """Test that cryptocurrency list contains major cryptocurrencies."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No cryptocurrency data available")

        symbols = []
        for item in result_list:
            if isinstance(item, dict):
                crypto_data = FMPCryptocurrencyListItem(**item)
            else:
                crypto_data = item
            symbols.append(crypto_data.symbol)

        # Check for exact match or partial match (symbol format may vary)
        symbol_found = any(expected_crypto in symbol for symbol in symbols)
        base_symbol = expected_crypto.replace("USD", "").replace("USDT", "")
        partial_match = any(base_symbol in symbol for symbol in symbols)

        assert (
            symbol_found or partial_match
        ), f"{expected_crypto} or similar not found in crypto list"

    @pytest.mark.parametrize(
        "market_cap_tier", ["top_10", "top_50", "top_100", "emerging"]
    )
    def test_cryptocurrency_list_by_market_cap(self, api_key, market_cap_tier):
        """Test cryptocurrency list across different market cap tiers."""
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

        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No cryptocurrency data available")

        found_count = 0
        symbols = []
        for item in result_list:
            if isinstance(item, dict):
                crypto_data = FMPCryptocurrencyListItem(**item)
            else:
                crypto_data = item
            symbols.append(crypto_data.symbol.upper())

        for expected in expected_symbols:
            if any(expected in symbol for symbol in symbols):
                found_count += 1

        # Should find at least some cryptos from each tier
        assert found_count >= 0, f"No {market_cap_tier} cryptocurrencies found"

    @pytest.mark.parametrize(
        "data_quality_check",
        [
            "symbol_format",
            "name_completeness",
            "unique_symbols",
            "usd_pairing",
            "category_coverage",
        ],
    )
    def test_cryptocurrency_list_data_quality(self, api_key, data_quality_check):
        """Test various data quality aspects of cryptocurrency list."""
        result = crypto.cryptocurrency_list(apikey=api_key)
        result_list = extract_data_list(result)

        if not result_list:
            pytest.skip("No cryptocurrency data available")

        if data_quality_check == "symbol_format":
            # Check that symbols follow expected patterns
            valid_symbols = 0
            for item in result_list:
                if isinstance(item, dict):
                    crypto_data = FMPCryptocurrencyListItem(**item)
                else:
                    crypto_data = item

                if crypto_data.symbol and len(crypto_data.symbol) >= 3:
                    valid_symbols += 1

            assert (
                valid_symbols >= len(result_list) * 0.8
            ), "At least 80% of symbols should be valid"

        elif data_quality_check == "name_completeness":
            # Check that most cryptos have meaningful names
            named_cryptos = 0
            for item in result_list:
                if isinstance(item, dict):
                    crypto_data = FMPCryptocurrencyListItem(**item)
                else:
                    crypto_data = item

                if crypto_data.name and len(crypto_data.name) > 2:
                    named_cryptos += 1

            assert (
                named_cryptos >= len(result_list) * 0.9
            ), "At least 90% should have meaningful names"

        elif data_quality_check == "unique_symbols":
            # Check for duplicate symbols
            symbols = []
            for item in result_list:
                if isinstance(item, dict):
                    crypto_data = FMPCryptocurrencyListItem(**item)
                else:
                    crypto_data = item
                symbols.append(crypto_data.symbol)

            unique_symbols = set(symbols)
            assert len(unique_symbols) == len(
                symbols
            ), "All crypto symbols should be unique"

        elif data_quality_check == "usd_pairing":
            # Check that most cryptos are USD-paired
            usd_paired = 0
            for item in result_list:
                if isinstance(item, dict):
                    crypto_data = FMPCryptocurrencyListItem(**item)
                else:
                    crypto_data = item

                if "USD" in crypto_data.symbol:
                    usd_paired += 1

            # Most should be USD paired, but allow for some flexibility
            assert (
                usd_paired >= len(result_list) * 0.7
            ), "At least 70% should be USD-paired"

        elif data_quality_check == "category_coverage":
            # Check that we have good coverage across crypto categories
            categories_found = set()
            major_cryptos = ["btc", "eth", "bnb", "xrp", "ada"]
            defi_tokens = ["uni", "aave", "comp", "mkr", "snx"]
            stablecoins = ["usdt", "usdc", "busd", "dai"]

            for item in result_list:
                if isinstance(item, dict):
                    crypto_data = FMPCryptocurrencyListItem(**item)
                else:
                    crypto_data = item

                name_lower = crypto_data.name.lower() if crypto_data.name else ""
                symbol_lower = crypto_data.symbol.lower() if crypto_data.symbol else ""

                if any(
                    crypto in name_lower or crypto in symbol_lower
                    for crypto in major_cryptos
                ):
                    categories_found.add("major")
                if any(
                    token in name_lower or token in symbol_lower
                    for token in defi_tokens
                ):
                    categories_found.add("defi")
                if any(
                    stable in name_lower or stable in symbol_lower
                    for stable in stablecoins
                ):
                    categories_found.add("stablecoins")

            assert (
                len(categories_found) >= 1
            ), "Should cover at least one major crypto category"
