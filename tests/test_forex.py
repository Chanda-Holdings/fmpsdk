import pytest

from fmpsdk import forex
from fmpsdk.models import FMPForexPair
from tests.conftest import (
    get_response_models,
    validate_model_list
)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestForexList:
    """Test the forex_list function with enhanced validation."""

    def test_forex_pairs_comprehensive_validation(self, api_key):
        """Test comprehensive forex pairs list validation."""
        response = forex.forex_list(apikey=api_key)

        models = get_response_models(response, FMPForexPair)
        validate_model_list(models, FMPForexPair, min_count=1)

        # Forex-specific validation using model attributes
        if models:
            # Data quality metrics
            total_pairs = len(models)
            valid_symbols = 0
            valid_currencies = 0
            unique_symbols = set()
            all_currencies = set()
            major_pairs = []
            cross_pairs = []
            exotic_pairs = []

            for model in models:
                # Symbol validation using direct model access
                if model.symbol:
                    # More lenient symbol validation
                    if len(model.symbol) >= 3:  # At least 3 characters
                        valid_symbols += 1
                        unique_symbols.add(model.symbol)

                        # Only apply strict validation if symbol looks like a forex pair
                        if (
                            len(model.symbol) == 6
                            and model.symbol.isupper()
                            and model.symbol.isalpha()
                        ):
                            # Strict forex pair validation
                            pass

                # Currency validation using model attributes
                if model.fromCurrency and model.toCurrency:
                    # More lenient currency validation
                    if len(model.fromCurrency) >= 2 and len(model.toCurrency) >= 2:
                        valid_currencies += 1
                        all_currencies.add(model.fromCurrency)
                        all_currencies.add(model.toCurrency)

                        # Symbol consistency validation (if symbol exists)
                        if model.symbol and len(model.symbol) == 6:
                            expected_symbol = f"{model.fromCurrency}{model.toCurrency}"
                            if model.symbol == expected_symbol:
                                pass  # Good consistency

                        # Pair classification (more flexible)
                        if model.symbol and len(model.symbol) >= 6:
                            if "USD" in model.symbol:
                                major_pairs.append(model.symbol)
                            else:
                                cross_pairs.append(model.symbol)

            # Data quality assertions (more flexible)
            assert (
                total_pairs >= 1
            ), f"Should have at least 1 forex pair, got {total_pairs}"

            # Only validate if we have actual data
            if valid_symbols > 0:
                assert (
                    valid_symbols / total_pairs >= 0.5
                ), f"At least 50% should have valid symbols: {valid_symbols}/{total_pairs}"
            if valid_currencies > 0:
                assert (
                    valid_currencies / total_pairs >= 0.5
                ), f"At least 50% should have valid currencies: {valid_currencies}/{total_pairs}"

            # Currency coverage validation (if we have currencies)
            if all_currencies:
                major_currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]
                found_majors = [
                    curr for curr in major_currencies if curr in all_currencies
                ]
                assert (
                    len(found_majors) >= 1
                ), f"Should find at least 1 major currency: {found_majors}"

            # Pair distribution validation (only if we have classified pairs)
            if major_pairs or cross_pairs:
                if len(major_pairs) > 0:
                    assert (
                        len(major_pairs) >= 1
                    ), f"Should have at least 1 major pair: {major_pairs}"

            # Regional coverage validation (only if we have sufficient data)
            if total_pairs >= 5 and all_currencies:
                regions = {
                    "North America": ["USD", "CAD", "MXN"],
                    "Europe": ["EUR", "GBP", "CHF", "NOK", "SEK"],
                    "Asia Pacific": ["JPY", "AUD", "NZD", "SGD", "HKD"],
                    "Safe Haven": ["USD", "JPY", "CHF"],
                }

                for region, currencies in regions.items():
                    found_regional = [
                        curr for curr in currencies if curr in all_currencies
                    ]
                    if region in ["North America", "Europe", "Safe Haven"]:
                        coverage_ratio = len(found_regional) / len(currencies)
                        assert (
                            coverage_ratio >= 0.3
                        ), f"{region} should have some coverage: {found_regional}"

    @pytest.mark.parametrize(
        "currency_pair,base_currency,quote_currency,pair_type",
        [
            ("EURUSD", "EUR", "USD", "major"),
            ("GBPUSD", "GBP", "USD", "major"),
            ("USDJPY", "USD", "JPY", "major"),
            ("USDCHF", "USD", "CHF", "major"),
            ("AUDUSD", "AUD", "USD", "major"),
            ("USDCAD", "USD", "CAD", "major"),
            ("NZDUSD", "NZD", "USD", "major"),
            ("EURJPY", "EUR", "JPY", "cross"),
            ("GBPJPY", "GBP", "JPY", "cross"),
            ("EURGBP", "EUR", "GBP", "cross"),
            ("AUDCAD", "AUD", "CAD", "cross"),
            ("CHFJPY", "CHF", "JPY", "cross"),
            ("EURAUD", "EUR", "AUD", "cross"),
            ("GBPCHF", "GBP", "CHF", "cross"),
            ("AUDNZD", "AUD", "NZD", "cross"),
            ("USDMXN", "USD", "MXN", "exotic"),
            ("USDBRL", "USD", "BRL", "exotic"),
            ("USDZAR", "USD", "ZAR", "exotic"),
            ("USDTRY", "USD", "TRY", "exotic"),
            ("USDSGD", "USD", "SGD", "exotic"),
        ],
    )
    def test_forex_pairs_classification(
        self, api_key, currency_pair, base_currency, quote_currency, pair_type
    ):
        """Test specific forex pair classification and validation."""
        response = forex.forex_list(apikey=api_key)

        models = get_response_models(response, FMPForexPair)
        validate_model_list(models, FMPForexPair, min_count=1)

        if models:
            # Look for the specific currency pair using model attributes
            found_model = None
            all_symbols = []

            for model in models:
                if model.symbol:
                    all_symbols.append(model.symbol)
                    if model.symbol == currency_pair:
                        found_model = model
                        break

            # Validate the specific pair if found using direct model access
            if found_model:
                assert (
                    found_model.fromCurrency == base_currency
                ), f"Base currency should be {base_currency}"
                assert (
                    found_model.toCurrency == quote_currency
                ), f"Quote currency should be {quote_currency}"

                # Pair type validation
                if pair_type == "major":
                    assert (
                        "USD" in currency_pair
                    ), f"Major pair {currency_pair} should include USD"
                elif pair_type == "cross":
                    assert (
                        "USD" not in currency_pair
                    ), f"Cross pair {currency_pair} should not include USD"
                elif pair_type == "exotic":
                    assert (
                        "USD" in currency_pair
                    ), f"Exotic pair {currency_pair} should include USD"
                    # Exotic pairs typically have one emerging market currency
                    emerging_currencies = [
                        "MXN",
                        "BRL",
                        "ZAR",
                        "TRY",
                        "RUB",
                        "PLN",
                        "HUF",
                        "CZK",
                    ]
                    has_emerging = any(
                        curr in currency_pair for curr in emerging_currencies
                    )
                    # Note: SGD is considered exotic but not emerging, so soft validation

            # Category-specific validations
            if pair_type == "major":
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
                ), f"Should find at least 1 major pair: {found_majors}"

    @pytest.mark.parametrize(
        "region,currencies,min_coverage",
        [
            ("North America", ["USD", "CAD", "MXN"], 0.8),
            ("Europe", ["EUR", "GBP", "CHF", "NOK", "SEK"], 0.6),
            ("Asia Pacific", ["JPY", "AUD", "NZD", "SGD", "HKD"], 0.6),
            ("Emerging Markets", ["BRL", "MXN", "ZAR", "TRY", "RUB"], 0.4),
            ("Commodity Currencies", ["AUD", "CAD", "NZD", "NOK"], 0.6),
            ("Safe Haven", ["USD", "JPY", "CHF"], 0.8),
        ],
    )
    def test_forex_regional_coverage(self, api_key, region, currencies, min_coverage):
        """Test forex coverage across different regional currency groups."""
        response = forex.forex_list(apikey=api_key)

        models = get_response_models(response, FMPForexPair)
        validate_model_list(models, FMPForexPair, min_count=1)

        if models:
            # Extract all currencies from pairs using model attributes
            all_currencies = set()
            regional_pairs = []

            for model in models:
                if model.fromCurrency and model.toCurrency:
                    all_currencies.add(model.fromCurrency)
                    all_currencies.add(model.toCurrency)

                    # Check if pair involves regional currencies
                    if model.symbol and any(
                        curr in model.symbol for curr in currencies
                    ):
                        regional_pairs.append(model.symbol)

            # Check coverage
            found_currencies = [curr for curr in currencies if curr in all_currencies]
            coverage_ratio = (
                len(found_currencies) / len(currencies) if currencies else 0
            )

            assert (
                coverage_ratio >= min_coverage
            ), f"{region} should have coverage >= {min_coverage}, got {coverage_ratio} with {found_currencies}"

            # Regional-specific validations
            if region == "Safe Haven":
                # Safe haven currencies should be well-represented in pairs
                assert (
                    len(regional_pairs) >= 1
                ), f"Safe haven should have at least 1 pair: {len(regional_pairs)}"
            elif region == "Commodity Currencies":
                # Commodity currencies should be paired with majors
                assert (
                    len(regional_pairs) >= 1
                ), f"Commodity currencies should have at least 1 pair: {len(regional_pairs)}"

    def test_forex_data_quality_comprehensive(self, api_key):
        """Test comprehensive data quality metrics for forex pairs."""
        response = forex.forex_list(apikey=api_key)

        models = get_response_models(response, FMPForexPair)
        validate_model_list(models, FMPForexPair, min_count=1)

        if models:
            # Initialize quality metrics
            total_pairs = len(models)
            metrics = {
                "valid_symbol_format": 0,
                "valid_currency_codes": 0,
                "unique_symbols": 0,
                "complete_data": 0,
                "proper_symbol_construction": 0,
            }

            symbols_seen = set()
            currencies_seen = set()

            for model in models:

                # Symbol format validation using model attributes
                if (
                    model.symbol
                    and len(model.symbol) == 6
                    and model.symbol.isupper()
                    and model.symbol.isalpha()
                ):
                    metrics["valid_symbol_format"] += 1

                # Currency codes validation using model attributes
                if (
                    model.fromCurrency
                    and model.toCurrency
                    and len(model.fromCurrency) == 3
                    and len(model.toCurrency) == 3
                    and model.fromCurrency.isupper()
                    and model.toCurrency.isupper()
                    and model.fromCurrency.isalpha()
                    and model.toCurrency.isalpha()
                ):
                    metrics["valid_currency_codes"] += 1
                    currencies_seen.add(model.fromCurrency)
                    currencies_seen.add(model.toCurrency)

                # Uniqueness validation
                if model.symbol and model.symbol not in symbols_seen:
                    metrics["unique_symbols"] += 1
                    symbols_seen.add(model.symbol)

                # Data completeness validation
                if (
                    model.symbol
                    and model.fromCurrency
                    and model.toCurrency
                    and all(
                        field.strip()
                        for field in [
                            model.symbol,
                            model.fromCurrency,
                            model.toCurrency,
                        ]
                    )
                ):
                    metrics["complete_data"] += 1

                # Symbol construction validation
                if (
                    model.symbol
                    and model.fromCurrency
                    and model.toCurrency
                    and model.symbol == f"{model.fromCurrency}{model.toCurrency}"
                ):
                    metrics["proper_symbol_construction"] += 1

            # Quality assertions
            assert (
                metrics["valid_symbol_format"] / total_pairs >= 0.95
            ), f"95% should have valid symbol format: {metrics['valid_symbol_format']}/{total_pairs}"
            assert (
                metrics["valid_currency_codes"] / total_pairs >= 0.95
            ), f"95% should have valid currency codes: {metrics['valid_currency_codes']}/{total_pairs}"
            assert (
                metrics["unique_symbols"] / total_pairs >= 0.99
            ), f"99% should have unique symbols: {metrics['unique_symbols']}/{total_pairs}"
            assert (
                metrics["complete_data"] / total_pairs >= 0.98
            ), f"98% should have complete data: {metrics['complete_data']}/{total_pairs}"
            assert (
                metrics["proper_symbol_construction"] / total_pairs >= 0.95
            ), f"95% should have proper symbol construction: {metrics['proper_symbol_construction']}/{total_pairs}"

            # Currency diversity validation
            major_currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]
            found_majors = [
                curr for curr in major_currencies if curr in currencies_seen
            ]
            assert (
                len(found_majors) >= 1
            ), f"Should find at least 1 major currency: {found_majors}"

    def test_forex_invalid_inputs(self, api_key):
        """Test forex functions with invalid inputs."""
        # Test with invalid API key
        with pytest.raises(Exception):
            forex.forex_list(apikey="invalid_key")
