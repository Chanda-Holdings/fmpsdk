import pytest

from fmpsdk import forex
from fmpsdk.models import FMPForexPair

from .conftest import extract_data_list


class TestForexList:
    """Test the forex_list function."""

    def test_forex_list_success(self, api_key):
        """Test successful retrieval of forex pairs list."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item - might be dict or model depending on SDK implementation
            first_item = result_list[0]
            if isinstance(first_item, dict):
                forex_data = FMPForexPair(**first_item)
            else:
                forex_data = first_item
            assert forex_data.symbol, "Symbol should not be empty"
            assert forex_data.fromCurrency, "From currency should not be empty"
            assert forex_data.toCurrency, "To currency should not be empty"

    def test_forex_list_model_validation(self, api_key):
        """Test that returned data validates against the Pydantic model."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        if result_list:
            # Test model validation on first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated_item = FMPForexPair(**first_item)
            else:
                validated_item = first_item
            assert hasattr(validated_item, "symbol")
            assert hasattr(validated_item, "fromCurrency")

    def test_forex_list_invalid_api_key(self):
        """Test handling of invalid API key."""
        result = forex.forex_list(apikey="invalid_api_key")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid key"

    @pytest.mark.parametrize(
        "currency_pair,base_currency,quote_currency,pair_type,volatility_level,trading_volume",
        [
            ("EURUSD", "EUR", "USD", "major", "low", "very_high"),
            ("GBPUSD", "GBP", "USD", "major", "medium", "very_high"),
            ("USDJPY", "USD", "JPY", "major", "medium", "very_high"),
            ("USDCHF", "USD", "CHF", "major", "low", "high"),
            ("AUDUSD", "AUD", "USD", "major", "medium", "high"),
            ("USDCAD", "USD", "CAD", "major", "low", "high"),
            ("NZDUSD", "NZD", "USD", "major", "medium", "medium"),
            ("EURJPY", "EUR", "JPY", "cross", "medium", "high"),
            ("GBPJPY", "GBP", "JPY", "cross", "high", "medium"),
            ("EURGBP", "EUR", "GBP", "cross", "medium", "high"),
            ("AUDCAD", "AUD", "CAD", "cross", "medium", "medium"),
            ("CHFJPY", "CHF", "JPY", "cross", "medium", "medium"),
            ("EURAUD", "EUR", "AUD", "cross", "medium", "medium"),
            ("GBPCHF", "GBP", "CHF", "cross", "medium", "medium"),
            ("AUDNZD", "AUD", "NZD", "cross", "medium", "low"),
            ("USDMXN", "USD", "MXN", "exotic", "high", "medium"),
            ("USDBRL", "USD", "BRL", "exotic", "high", "medium"),
            ("USDZAR", "USD", "ZAR", "exotic", "very_high", "low"),
            ("USDTRY", "USD", "TRY", "exotic", "very_high", "medium"),
            ("USDSGD", "USD", "SGD", "exotic", "low", "medium"),
        ],
    )
    def test_forex_list_comprehensive_pairs(
        self,
        api_key,
        currency_pair,
        base_currency,
        quote_currency,
        pair_type,
        volatility_level,
        trading_volume,
    ):
        """Test forex list contains comprehensive range of currency pairs across different categories."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(
            result_list, list
        ), f"Response should be a list for {pair_type} pairs"

        if result_list:
            # Look for the specific currency pair in the list
            found_pair = None
            all_symbols = []

            for item in result_list:
                if isinstance(item, dict):
                    forex_data = FMPForexPair(**item)
                else:
                    forex_data = item

                all_symbols.append(forex_data.symbol)

                if forex_data.symbol == currency_pair:
                    found_pair = forex_data
                    break

            # Validate the specific pair if found
            if found_pair:
                assert (
                    found_pair.symbol == currency_pair
                ), f"Symbol should match for {currency_pair}"
                assert (
                    found_pair.fromCurrency == base_currency
                ), f"Base currency should be {base_currency} for {currency_pair}"
                assert (
                    found_pair.toCurrency == quote_currency
                ), f"Quote currency should be {quote_currency} for {currency_pair}"

                # Additional validations based on pair type
                if pair_type == "major":
                    # Major pairs should always include USD
                    assert (
                        "USD" in currency_pair
                    ), f"Major pair {currency_pair} should include USD"
                elif pair_type == "cross":
                    # Cross pairs should not include USD
                    assert (
                        "USD" not in currency_pair
                    ), f"Cross pair {currency_pair} should not include USD"
                elif pair_type == "exotic":
                    # Exotic pairs should include USD and one emerging market currency
                    assert (
                        "USD" in currency_pair
                    ), f"Exotic pair {currency_pair} should include USD"

            # Category-specific validations
            if pair_type == "major":
                # Should find several major pairs
                major_pairs = [
                    "EURUSD",
                    "GBPUSD",
                    "USDJPY",
                    "USDCHF",
                    "AUDUSD",
                    "USDCAD",
                ]
                found_majors = [pair for pair in major_pairs if pair in all_symbols]
                assert (
                    len(found_majors) >= 1
                ), f"Should find at least 1 major pair, found: {found_majors}"

            # General forex list validation
            assert (
                len(result_list) >= 20
            ), "Should have at least 20 forex pairs available"

            # Validate first few items structure
            for item in result_list[:5]:
                if isinstance(item, dict):
                    forex_data = FMPForexPair(**item)
                else:
                    forex_data = item

                assert forex_data.symbol, "Symbol should not be empty"
                assert forex_data.fromCurrency, "From currency should not be empty"
                assert forex_data.toCurrency, "To currency should not be empty"
                assert (
                    len(forex_data.symbol) == 6
                ), f"Forex symbol should be 6 characters, got {forex_data.symbol}"
                assert (
                    len(forex_data.fromCurrency) == 3
                ), f"From currency should be 3 characters, got {forex_data.fromCurrency}"
                assert (
                    len(forex_data.toCurrency) == 3
                ), f"To currency should be 3 characters, got {forex_data.toCurrency}"

    @pytest.mark.parametrize(
        "region,currencies,economic_characteristics",
        [
            (
                "North America",
                ["USD", "CAD", "MXN"],
                {"stability": "high", "liquidity": "very_high"},
            ),
            (
                "Europe",
                ["EUR", "GBP", "CHF", "NOK", "SEK"],
                {"stability": "high", "liquidity": "high"},
            ),
            (
                "Asia Pacific",
                ["JPY", "AUD", "NZD", "SGD", "HKD"],
                {"stability": "medium", "liquidity": "medium"},
            ),
            (
                "Emerging Markets",
                ["BRL", "MXN", "ZAR", "TRY", "RUB"],
                {"stability": "low", "liquidity": "low"},
            ),
            (
                "Commodity Currencies",
                ["AUD", "CAD", "NZD", "NOK"],
                {"stability": "medium", "liquidity": "medium"},
            ),
            (
                "Safe Haven",
                ["USD", "JPY", "CHF"],
                {"stability": "very_high", "liquidity": "very_high"},
            ),
        ],
    )
    def test_forex_list_regional_coverage(
        self, api_key, region, currencies, economic_characteristics
    ):
        """Test forex list coverage across different regional currency groups."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(
            result_list, list
        ), f"Response should be a list for {region} currencies"

        if result_list:
            # Extract all currencies from the forex pairs
            all_currencies = set()
            for item in result_list:
                if isinstance(item, dict):
                    forex_data = FMPForexPair(**item)
                else:
                    forex_data = item

                all_currencies.add(forex_data.fromCurrency)
                all_currencies.add(forex_data.toCurrency)

            # Check coverage of regional currencies
            found_currencies = [curr for curr in currencies if curr in all_currencies]
            coverage_ratio = len(found_currencies) / len(currencies)

            if region in ["North America", "Europe", "Safe Haven"]:
                # These regions should have excellent coverage
                assert (
                    coverage_ratio >= 0.8
                ), f"{region} should have high currency coverage, found {found_currencies}"
            elif region in ["Asia Pacific", "Commodity Currencies"]:
                # These should have good coverage
                assert (
                    coverage_ratio >= 0.6
                ), f"{region} should have good currency coverage, found {found_currencies}"
            elif region == "Emerging Markets":
                # Emerging markets may have limited coverage
                assert (
                    coverage_ratio >= 0.4
                ), f"{region} should have some currency coverage, found {found_currencies}"

            # Regional-specific validations
            if region == "Safe Haven":
                # Safe haven currencies should be well-represented
                safe_haven_pairs = []
                for item in result_list:
                    if isinstance(item, dict):
                        symbol = item.get("symbol", "")
                    else:
                        symbol = getattr(item, "symbol", "")

                    if any(curr in symbol for curr in ["USD", "JPY", "CHF"]):
                        safe_haven_pairs.append(symbol)

                assert (
                    len(safe_haven_pairs) >= 10
                ), f"Should have many safe haven currency pairs"

            elif region == "Commodity Currencies":
                # Commodity currencies should be paired with major currencies
                commodity_pairs = []
                for item in result_list:
                    if isinstance(item, dict):
                        symbol = item.get("symbol", "")
                    else:
                        symbol = getattr(item, "symbol", "")

                    if any(curr in symbol for curr in ["AUD", "CAD", "NZD", "NOK"]):
                        commodity_pairs.append(symbol)

                assert (
                    len(commodity_pairs) >= 5
                ), f"Should have several commodity currency pairs"

    @pytest.mark.parametrize(
        "validation_type,expected_characteristics",
        [
            (
                "symbol_format",
                {"length": 6, "pattern": "uppercase", "structure": "from_to"},
            ),
            (
                "currency_codes",
                {"length": 3, "pattern": "uppercase", "standard": "iso_4217"},
            ),
            ("pair_uniqueness", {"unique_symbols": True, "bidirectional": False}),
            (
                "data_completeness",
                {"required_fields": ["symbol", "fromCurrency", "toCurrency"]},
            ),
        ],
    )
    def test_forex_list_data_quality(
        self, api_key, validation_type, expected_characteristics
    ):
        """Test comprehensive data quality aspects of forex list."""
        result = forex.forex_list(apikey=api_key)
        result_list = extract_data_list(result)

        assert isinstance(
            result_list, list
        ), f"Response should be a list for {validation_type} validation"

        if result_list:
            symbols_seen = set()
            currencies_seen = set()

            for item in result_list:
                if isinstance(item, dict):
                    forex_data = FMPForexPair(**item)
                else:
                    forex_data = item

                if validation_type == "symbol_format":
                    # Validate symbol format
                    assert (
                        len(forex_data.symbol) == expected_characteristics["length"]
                    ), f"Symbol {forex_data.symbol} should be {expected_characteristics['length']} characters"
                    assert (
                        forex_data.symbol.isupper()
                    ), f"Symbol {forex_data.symbol} should be uppercase"
                    assert (
                        forex_data.symbol
                        == f"{forex_data.fromCurrency}{forex_data.toCurrency}"
                    ), f"Symbol should be concatenation of from and to currencies"

                elif validation_type == "currency_codes":
                    # Validate currency codes
                    for currency in [forex_data.fromCurrency, forex_data.toCurrency]:
                        assert (
                            len(currency) == expected_characteristics["length"]
                        ), f"Currency {currency} should be {expected_characteristics['length']} characters"
                        assert (
                            currency.isupper()
                        ), f"Currency {currency} should be uppercase"
                        assert (
                            currency.isalpha()
                        ), f"Currency {currency} should be alphabetic"
                        currencies_seen.add(currency)

                elif validation_type == "pair_uniqueness":
                    # Validate pair uniqueness
                    assert (
                        forex_data.symbol not in symbols_seen
                    ), f"Symbol {forex_data.symbol} should be unique"
                    symbols_seen.add(forex_data.symbol)

                elif validation_type == "data_completeness":
                    # Validate data completeness
                    for field in expected_characteristics["required_fields"]:
                        field_value = getattr(forex_data, field)
                        assert (
                            field_value
                        ), f"Field {field} should not be empty for {forex_data.symbol}"
                        assert (
                            field_value.strip()
                        ), f"Field {field} should not be whitespace for {forex_data.symbol}"

            # Additional validation after processing all items
            if validation_type == "currency_codes":
                # Should have major world currencies
                major_currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]
                found_majors = [
                    curr for curr in major_currencies if curr in currencies_seen
                ]
                assert (
                    len(found_majors) >= 5
                ), f"Should find most major currencies, found: {found_majors}"

            elif validation_type == "pair_uniqueness":
                # Should have unique symbols
                assert len(symbols_seen) == len(
                    result_list
                ), "All symbols should be unique"
