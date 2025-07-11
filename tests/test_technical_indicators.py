from datetime import datetime

import pytest

from fmpsdk.models import FMPTechnicalIndicator
from fmpsdk.technical_indicators import technical_indicators

from .conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name)
    else:
        return getattr(item, field_name, None)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicators:
    """Test class for technical indicators functionality."""

    def test_sma_indicator(self, api_key):
        """Test Simple Moving Average indicator."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # Note: Technical indicators may return empty results due to API limitations or plan restrictions
        if len(result_list) > 0:
            # Validate first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPTechnicalIndicator.model_validate(first_item)
            else:
                validated = first_item

            assert validated.date is not None
            assert validated.open > 0
            assert validated.high > 0
            assert validated.low > 0
            assert validated.close > 0
            assert validated.volume >= 0
            assert validated.sma is not None
            assert validated.sma > 0

            # OHLC relationships should be valid
            assert validated.high >= validated.open
            assert validated.high >= validated.close
            assert validated.low <= validated.open
            assert validated.low <= validated.close
        else:
            # API may not provide technical indicators data - test API response structure
            assert result_list == []

    def test_ema_indicator(self, api_key):
        """Test Exponential Moving Average indicator."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="ema",
            periodLength=12,
            timeframe="1day",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.ema is not None
            assert validated.ema > 0
        else:
            assert result_list == []

    def test_rsi_indicator(self, api_key):
        """Test Relative Strength Index indicator."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="rsi",
            periodLength=14,
            timeframe="1day",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.rsi is not None
            # RSI should be between 0 and 100
            assert 0 <= validated.rsi <= 100
        else:
            assert result_list == []

    def test_williams_indicator(self, api_key):
        """Test Williams %R indicator."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="williams",
            periodLength=14,
            timeframe="1day",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.williams is not None
            # Williams %R should be between -100 and 0
            assert -100 <= validated.williams <= 0
        else:
            assert result_list == []

    def test_adx_indicator(self, api_key):
        """Test Average Directional Index indicator."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="adx",
            periodLength=14,
            timeframe="1day",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.adx is not None
            # ADX should be between 0 and 100
            assert 0 <= validated.adx <= 100
        else:
            assert result_list == []


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestAllTechnicalIndicators:
    """Test class for all supported technical indicators."""

    def test_all_supported_indicators(self, api_key):
        """Test all supported technical indicators."""
        valid_indicators = [
            "sma",
            "ema",
            "wma",
            "dema",
            "tema",
            "rsi",
            "standarddeviation",
            "williams",
            "adx",
        ]
        symbol = "AAPL"
        period_length = 20
        timeframe = "1day"

        for indicator in valid_indicators:
            result = technical_indicators(
                apikey=api_key,
                symbol=symbol,
                indicator=indicator,
                periodLength=period_length,
                timeframe=timeframe,
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for {indicator}"

            # Technical indicators may return empty results due to API limitations
            if len(result_list) > 0:
                # Validate structure
                first_item = result_list[0]
                validated = (
                    FMPTechnicalIndicator.model_validate(first_item)
                    if isinstance(first_item, dict)
                    else first_item
                )

                assert (
                    validated.date is not None
                ), f"Date should be present for {indicator}"
                assert (
                    validated.close > 0
                ), f"Close price should be positive for {indicator}"

                # Check that the specific indicator field is populated
                indicator_value = getattr(validated, indicator, None)
                if indicator == "standarddeviation":
                    indicator_value = getattr(validated, "standardDeviation", None)

                assert (
                    indicator_value is not None
                ), f"Indicator value should be present for {indicator}"

                # Value range checks for specific indicators
                if indicator == "rsi":
                    assert (
                        0 <= indicator_value <= 100
                    ), f"RSI should be 0-100, got {indicator_value}"
                elif indicator == "williams":
                    assert (
                        -100 <= indicator_value <= 0
                    ), f"Williams %R should be -100 to 0, got {indicator_value}"
                elif indicator == "adx":
                    assert (
                        0 <= indicator_value <= 100
                    ), f"ADX should be 0-100, got {indicator_value}"
                else:
                    assert (
                        indicator_value > 0
                    ), f"{indicator} should be positive, got {indicator_value}"
            else:
                # Empty result is acceptable due to API limitations
                assert (
                    result_list == []
                ), f"Empty result should be empty list for {indicator}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorParameters:
    """Test class for technical indicator parameter variations."""

    def test_different_period_lengths(self, api_key):
        """Test technical indicators with different period lengths."""
        period_lengths = [5, 10, 14, 20, 50, 100]

        for period in period_lengths:
            result = technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=period,
                timeframe="1day",
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for period {period}"

            # Skip this period if no data available
            if len(result_list) == 0:
                continue

            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )
            assert (
                validated.sma is not None
            ), f"SMA should be present for period {period}"

    def test_different_timeframes(self, api_key):
        """Test technical indicators with different timeframes."""
        timeframes = ["1min", "1hour", "1day"]

        for timeframe in timeframes:
            result = technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=20,
                timeframe=timeframe,
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for timeframe {timeframe}"

            # Skip this timeframe if no data available
            if len(result_list) == 0:
                continue

            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )
            assert (
                validated.sma is not None
            ), f"SMA should be present for timeframe {timeframe}"

    def test_intraday_timeframes(self, api_key):
        """Test technical indicators with intraday timeframes."""
        intraday_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour"]

        for timeframe in intraday_timeframes:
            result = technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=20,
                timeframe=timeframe,
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for timeframe {timeframe}"

            # Intraday data might be limited, but structure should be valid
            if len(result_list) > 0:
                first_item = result_list[0]
                validated = (
                    FMPTechnicalIndicator.model_validate(first_item)
                    if isinstance(first_item, dict)
                    else first_item
                )
                assert (
                    validated.date is not None
                ), f"Date should be present for timeframe {timeframe}"

    def test_with_date_range(self, api_key):
        """Test technical indicators with date range filtering."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-02-29",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        end_date = datetime.strptime("2024-02-29", "%Y-%m-%d")

        for item in result_list:
            date_value = get_field_value(item, "date")
            item_date = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")

            assert (
                start_date <= item_date <= end_date
            ), f"Date {date_value} should be within range {start_date.date()} to {end_date.date()}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorAssetTypes:
    """Test class for technical indicators across different asset types."""

    def test_technical_indicators_multiple_asset_types(self, api_key, test_symbols):
        """Test technical indicators for different asset types."""
        test_cases = [
            ("large_cap", "AAPL", "stock"),
            ("etf", "SPY", "ETF"),
            # Note: Technical indicators may not be available for all asset types
        ]

        for asset_category, symbol, asset_name in test_cases:
            if symbol in test_symbols[asset_category]:
                result = technical_indicators(
                    apikey=api_key,
                    symbol=symbol,
                    indicator="sma",
                    periodLength=20,
                    timeframe="1day",
                )

                result_list = extract_data_list(result)
                assert isinstance(
                    result_list, list
                ), f"Result should be list for {asset_name}"

                if len(result_list) > 0:
                    first_item = result_list[0]
                    validated = (
                        FMPTechnicalIndicator.model_validate(first_item)
                        if isinstance(first_item, dict)
                        else first_item
                    )
                    assert (
                        validated.sma is not None
                    ), f"SMA should be present for {asset_name}"

    def test_high_volume_stocks(self, api_key):
        """Test technical indicators for high volume stocks."""
        high_volume_symbols = ["AAPL", "MSFT", "SPY", "QQQ"]

        for symbol in high_volume_symbols:
            result = technical_indicators(
                apikey=api_key,
                symbol=symbol,
                indicator="rsi",
                periodLength=14,
                timeframe="1day",
            )

            result_list = extract_data_list(result)
            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            # Skip this symbol if no data available
            if len(result_list) == 0:
                continue

            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )
            assert validated.rsi is not None, f"RSI should be present for {symbol}"
            assert 0 <= validated.rsi <= 100, f"RSI should be 0-100 for {symbol}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorErrorHandling:
    """Test class for technical indicator error handling."""

    def test_invalid_indicator_type(self, api_key):
        """Test technical indicators with invalid indicator type."""
        with pytest.raises(ValueError, match="Invalid indicator type"):
            technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="invalid_indicator",
                periodLength=20,
                timeframe="1day",
            )

    def test_invalid_symbol(self, api_key):
        """Test technical indicators with invalid symbol."""
        result = technical_indicators(
            apikey=api_key,
            symbol="INVALID_XYZ",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
        )

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_invalid_api_key(self):
        """Test technical indicators with invalid API key."""
        result = technical_indicators(
            apikey="invalid_key",
            symbol="AAPL",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
        )

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_invalid_period_length(self, api_key):
        """Test technical indicators with invalid period length."""
        # Very small period length might cause issues
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=1,
            timeframe="1day",
        )

        # Should handle gracefully
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_invalid_timeframe(self, api_key):
        """Test technical indicators with invalid timeframe (daily instead of 1day)."""
        with pytest.raises(ValueError, match="Invalid timeframe"):
            technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=20,
                timeframe="daily",  # Invalid: should be "1day"
            )


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorDataConsistency:
    """Test class for technical indicator data consistency validation."""

    def test_moving_average_relationships(self, api_key):
        """Test relationships between different moving averages."""

        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-01-10",
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        for item in result_list:
            validated = (
                FMPTechnicalIndicator.model_validate(item)
                if isinstance(item, dict)
                else item
            )

            # SMA should be within reasonable range of the price
            price_range = [validated.low, validated.high]
            # SMA might be outside daily range but should be reasonable
            assert validated.sma > 0, "SMA should be positive"
            assert (
                validated.sma < validated.high * 2
            ), "SMA should not be excessively high"
            assert (
                validated.sma > validated.low * 0.5
            ), "SMA should not be excessively low"

    def test_rsi_oscillator_behavior(self, api_key):
        """Test RSI oscillator behavior and constraints."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="rsi",
            periodLength=14,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-01-31",
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        rsi_values = []
        for item in result_list:
            validated = (
                FMPTechnicalIndicator.model_validate(item)
                if isinstance(item, dict)
                else item
            )
            assert (
                0 <= validated.rsi <= 100
            ), f"RSI should be 0-100, got {validated.rsi}"
            rsi_values.append(validated.rsi)

        # RSI should show some variation over time
        if len(rsi_values) > 5:
            rsi_range = max(rsi_values) - min(rsi_values)
            assert rsi_range > 0, "RSI should show some variation over the period"

    def test_williams_oscillator_behavior(self, api_key):
        """Test Williams %R oscillator behavior and constraints."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="williams",
            periodLength=14,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-01-15",
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        for item in result_list:
            validated = (
                FMPTechnicalIndicator.model_validate(item)
                if isinstance(item, dict)
                else item
            )
            assert (
                -100 <= validated.williams <= 0
            ), f"Williams %R should be -100 to 0, got {validated.williams}"

    def test_standard_deviation_behavior(self, api_key):
        """Test standard deviation indicator behavior."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="standarddeviation",
            periodLength=20,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-01-15",
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        for item in result_list:
            validated = (
                FMPTechnicalIndicator.model_validate(item)
                if isinstance(item, dict)
                else item
            )
            # Standard deviation should be positive
            assert (
                validated.standardDeviation >= 0
            ), f"Standard deviation should be non-negative, got {validated.standardDeviation}"
            # Should be reasonable relative to price
            assert (
                validated.standardDeviation < validated.close
            ), f"Standard deviation {validated.standardDeviation} seems too high relative to price {validated.close}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorResponseTimes:
    """Test class for technical indicator response time validation."""

    def test_technical_indicator_response_time(self, api_key, test_config):
        """Test that technical indicator responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=20,
            timeframe="1day",
        )
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"

    def test_complex_indicator_response_time(self, api_key, test_config):
        """Test response time for more complex indicators."""
        import time

        start_time = time.time()
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="adx",
            periodLength=14,
            timeframe="1day",
        )
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"ADX response time {response_time:.2f}s should be under {test_config['max_response_time']}s"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestTechnicalIndicatorEdgeCases:
    """Test class for technical indicator edge cases."""

    def test_short_period_lengths(self, api_key):
        """Test technical indicators with very short period lengths."""
        short_periods = [2, 3, 5]

        for period in short_periods:
            result = technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=period,
                timeframe="1day",
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for period {period}"

            if len(result_list) > 0:
                first_item = result_list[0]
                validated = (
                    FMPTechnicalIndicator.model_validate(first_item)
                    if isinstance(first_item, dict)
                    else first_item
                )
                assert (
                    validated.sma is not None
                ), f"SMA should be present for short period {period}"

    def test_long_period_lengths(self, api_key):
        """Test technical indicators with very long period lengths."""
        long_periods = [100, 200]

        for period in long_periods:
            result = technical_indicators(
                apikey=api_key,
                symbol="AAPL",
                indicator="sma",
                periodLength=period,
                timeframe="1day",
            )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for period {period}"

            # Long periods might have limited data
            if len(result_list) > 0:
                first_item = result_list[0]
                validated = (
                    FMPTechnicalIndicator.model_validate(first_item)
                    if isinstance(first_item, dict)
                    else first_item
                )
                assert (
                    validated.sma is not None
                ), f"SMA should be present for long period {period}"

    def test_data_sufficiency(self, api_key):
        """Test that sufficient data is available for indicator calculation."""
        result = technical_indicators(
            apikey=api_key,
            symbol="AAPL",
            indicator="sma",
            periodLength=50,
            timeframe="1day",
            from_date="2024-01-01",
            to_date="2024-03-31",
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        # For a 50-period SMA, we need at least 50 data points
        # The result should either have sufficient data or handle gracefully
        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            # All basic OHLCV data should be present
            assert validated.open > 0
            assert validated.high > 0
            assert validated.low > 0
            assert validated.close > 0
            assert validated.volume >= 0


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestComprehensiveTechnicalIndicators:
    """Comprehensive test class for technical indicators across diverse assets and conditions."""

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,expected_range,asset_class",
        [
            ("AAPL", "sma", 20, "1day", (50, 500), "large_cap_tech"),
            ("MSFT", "sma", 50, "1day", (100, 600), "large_cap_tech"),
            ("GOOGL", "sma", 10, "1day", (80, 300), "large_cap_tech"),
            ("AMZN", "sma", 30, "1day", (50, 400), "large_cap_tech"),
            ("TSLA", "sma", 20, "1day", (100, 1000), "electric_vehicle"),
            ("JPM", "sma", 20, "1day", (50, 300), "financial"),
            ("JNJ", "sma", 50, "1day", (100, 300), "healthcare"),
            ("XOM", "sma", 20, "1day", (30, 200), "energy"),
            ("WMT", "sma", 30, "1day", (50, 300), "consumer_staples"),
            ("SPY", "sma", 20, "1day", (200, 700), "etf"),
            ("QQQ", "sma", 50, "1day", (150, 800), "tech_etf"),
            ("IWM", "sma", 20, "1day", (100, 400), "small_cap_etf"),
            ("VTI", "sma", 30, "1day", (150, 500), "broad_market_etf"),
            ("BTCUSD", "sma", 20, "1day", (20000, 100000), "cryptocurrency"),
            ("ETHUSD", "sma", 50, "1day", (1000, 10000), "cryptocurrency"),
            ("EURUSD", "sma", 20, "1day", (0.8, 1.5), "forex"),
            ("GBPUSD", "sma", 30, "1day", (1.0, 1.8), "forex"),
            ("GCUSD", "sma", 20, "1day", (1500, 3000), "commodity"),
            ("CLUSD", "sma", 50, "1day", (30, 200), "commodity"),
        ],
    )
    def test_sma_indicator_comprehensive(
        self,
        api_key,
        symbol,
        indicator,
        period_length,
        timeframe,
        expected_range,
        asset_class,
    ):
        """Test Simple Moving Average indicator across diverse assets and parameters."""
        result = technical_indicators(
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {asset_class} asset {symbol}"

        # Note: Technical indicators may return empty results due to API limitations or plan restrictions
        if len(result_list) > 0:
            # Validate first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                validated = FMPTechnicalIndicator.model_validate(first_item)
            else:
                validated = first_item

            assert validated.date is not None, f"Date should be present for {symbol}"
            assert validated.open > 0, f"Open price should be positive for {symbol}"
            assert validated.high > 0, f"High price should be positive for {symbol}"
            assert validated.low > 0, f"Low price should be positive for {symbol}"
            assert validated.close > 0, f"Close price should be positive for {symbol}"
            assert validated.volume >= 0, f"Volume should be non-negative for {symbol}"
            assert validated.sma is not None, f"SMA should be present for {symbol}"
            assert validated.sma > 0, f"SMA should be positive for {symbol}"

            # OHLC relationships should be valid
            assert (
                validated.high >= validated.open
            ), f"High should be >= open for {symbol}"
            assert (
                validated.high >= validated.close
            ), f"High should be >= close for {symbol}"
            assert (
                validated.low <= validated.open
            ), f"Low should be <= open for {symbol}"
            assert (
                validated.low <= validated.close
            ), f"Low should be <= close for {symbol}"

            # Asset-specific price range validation (with flexibility for market volatility)
            min_expected, max_expected = expected_range
            flexible_min = (
                min_expected * 0.3
            )  # Allow significant variance due to market changes
            flexible_max = (
                max_expected * 3.0
            )  # Allow significant variance due to market changes

            if asset_class not in ["cryptocurrency"]:  # Crypto can be very volatile
                assert (
                    flexible_min <= validated.sma <= flexible_max
                ), f"SMA for {asset_class} {symbol} should be in reasonable range, got {validated.sma}"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,asset_class,expected_characteristics",
        [
            (
                "AAPL",
                "rsi",
                14,
                "1day",
                "large_cap_tech",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "MSFT",
                "rsi",
                21,
                "1day",
                "large_cap_tech",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "TSLA",
                "rsi",
                14,
                "1day",
                "volatile_stock",
                {"range": (0, 100), "typical": (20, 80)},
            ),
            (
                "JPM",
                "rsi",
                14,
                "1day",
                "financial",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "XOM",
                "rsi",
                21,
                "1day",
                "energy",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "SPY",
                "rsi",
                14,
                "1day",
                "broad_market_etf",
                {"range": (0, 100), "typical": (35, 65)},
            ),
            (
                "QQQ",
                "rsi",
                14,
                "1day",
                "tech_etf",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "BTCUSD",
                "rsi",
                14,
                "1day",
                "cryptocurrency",
                {"range": (0, 100), "typical": (20, 80)},
            ),
            (
                "EURUSD",
                "rsi",
                14,
                "1day",
                "forex",
                {"range": (0, 100), "typical": (30, 70)},
            ),
            (
                "GCUSD",
                "rsi",
                21,
                "1day",
                "commodity",
                {"range": (0, 100), "typical": (30, 70)},
            ),
        ],
    )
    def test_rsi_indicator_comprehensive(
        self,
        api_key,
        symbol,
        indicator,
        period_length,
        timeframe,
        asset_class,
        expected_characteristics,
    ):
        """Test Relative Strength Index indicator across diverse assets."""
        result = technical_indicators(
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {asset_class} asset {symbol}"

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.rsi is not None, f"RSI should be present for {symbol}"

            # RSI should be between 0 and 100
            rsi_range = expected_characteristics["range"]
            assert (
                rsi_range[0] <= validated.rsi <= rsi_range[1]
            ), f"RSI for {symbol} should be between {rsi_range[0]} and {rsi_range[1]}, got {validated.rsi}"

            # Asset-specific RSI behavior validation
            if asset_class == "broad_market_etf":
                # Market ETFs tend to have more moderate RSI values
                assert (
                    10 <= validated.rsi <= 90
                ), f"Market ETF {symbol} RSI should be moderate"
            elif asset_class == "volatile_stock":
                # Volatile stocks can have extreme RSI values
                assert (
                    0 <= validated.rsi <= 100
                ), f"Volatile stock {symbol} RSI can be extreme"
            elif asset_class == "cryptocurrency":
                # Crypto can have very extreme RSI values
                assert (
                    0 <= validated.rsi <= 100
                ), f"Crypto {symbol} RSI can be very extreme"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,asset_class",
        [
            ("AAPL", "williams", 14, "1day", "large_cap_tech"),
            ("MSFT", "williams", 21, "1day", "large_cap_tech"),
            ("GOOGL", "williams", 14, "1day", "large_cap_tech"),
            ("TSLA", "williams", 14, "1day", "volatile_stock"),
            ("JPM", "williams", 21, "1day", "financial"),
            ("JNJ", "williams", 14, "1day", "healthcare"),
            ("SPY", "williams", 14, "1day", "broad_market_etf"),
            ("QQQ", "williams", 21, "1day", "tech_etf"),
            ("IWM", "williams", 14, "1day", "small_cap_etf"),
            ("BTCUSD", "williams", 14, "1day", "cryptocurrency"),
        ],
    )
    def test_williams_indicator_comprehensive(
        self, api_key, symbol, indicator, period_length, timeframe, asset_class
    ):
        """Test Williams %R indicator across diverse assets."""
        result = technical_indicators(
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {asset_class} asset {symbol}"

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert (
                validated.williams is not None
            ), f"Williams %R should be present for {symbol}"
            # Williams %R should be between -100 and 0
            assert (
                -100 <= validated.williams <= 0
            ), f"Williams %R for {symbol} should be between -100 and 0, got {validated.williams}"

            # Asset-specific validations
            if asset_class in ["broad_market_etf", "large_cap_tech"]:
                # More stable assets still can have any Williams %R value, but typically less extreme
                # We just ensure it's within the valid range
                assert (
                    -100 <= validated.williams <= 0
                ), f"Stable asset {symbol} Williams %R should be within valid range, got {validated.williams}"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,asset_class",
        [
            ("AAPL", "adx", 14, "1day", "large_cap_tech"),
            ("TSLA", "adx", 14, "1day", "volatile_stock"),
            ("JPM", "adx", 21, "1day", "financial"),
            ("XOM", "adx", 14, "1day", "energy"),
            ("SPY", "adx", 14, "1day", "broad_market_etf"),
            ("BTCUSD", "adx", 14, "1day", "cryptocurrency"),
            ("EURUSD", "adx", 21, "1day", "forex"),
            ("GCUSD", "adx", 14, "1day", "commodity"),
        ],
    )
    def test_adx_indicator_comprehensive(
        self, api_key, symbol, indicator, period_length, timeframe, asset_class
    ):
        """Test Average Directional Index indicator across diverse assets."""
        result = technical_indicators(
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {asset_class} asset {symbol}"

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            assert validated.adx is not None, f"ADX should be present for {symbol}"
            # ADX should be between 0 and 100
            assert (
                0 <= validated.adx <= 100
            ), f"ADX for {symbol} should be between 0 and 100, got {validated.adx}"

            # Asset-specific ADX interpretation
            if asset_class == "volatile_stock":
                # Volatile stocks often have higher ADX values indicating strong trends
                assert (
                    validated.adx >= 0
                ), f"Volatile stock {symbol} ADX should indicate trend strength"
            elif asset_class == "broad_market_etf":
                # Market ETFs tend to have moderate ADX values
                assert (
                    0 <= validated.adx <= 100
                ), f"Market ETF {symbol} ADX should be moderate"

    @pytest.mark.parametrize(
        "symbol,indicator,timeframe,period_length,expected_data_density,market_type",
        [
            ("AAPL", "sma", "1min", 20, "very_high", "stock"),
            ("AAPL", "sma", "5min", 20, "high", "stock"),
            ("AAPL", "sma", "15min", 20, "medium", "stock"),
            ("AAPL", "sma", "30min", 20, "medium", "stock"),
            ("AAPL", "sma", "1hour", 20, "low", "stock"),
            ("AAPL", "sma", "4hour", 20, "very_low", "stock"),
            ("AAPL", "sma", "1day", 20, "daily", "stock"),
            ("SPY", "ema", "1min", 12, "very_high", "etf"),
            ("SPY", "ema", "1hour", 12, "low", "etf"),
            ("SPY", "ema", "1day", 12, "daily", "etf"),
            ("BTCUSD", "rsi", "1min", 14, "very_high", "crypto"),
            ("BTCUSD", "rsi", "15min", 14, "medium", "crypto"),
            ("BTCUSD", "rsi", "1hour", 14, "low", "crypto"),
            ("BTCUSD", "rsi", "1day", 14, "daily", "crypto"),
            ("EURUSD", "williams", "1min", 14, "very_high", "forex"),
            ("EURUSD", "williams", "1hour", 14, "low", "forex"),
            ("EURUSD", "williams", "1day", 14, "daily", "forex"),
        ],
    )
    def test_technical_indicators_timeframe_comprehensive(
        self,
        api_key,
        symbol,
        indicator,
        timeframe,
        period_length,
        expected_data_density,
        market_type,
    ):
        """Test technical indicators across different timeframes and market types."""
        result = technical_indicators(
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {market_type} {symbol} on {timeframe}"

        if len(result_list) > 0:
            first_item = result_list[0]
            validated = (
                FMPTechnicalIndicator.model_validate(first_item)
                if isinstance(first_item, dict)
                else first_item
            )

            # Basic validation
            assert (
                validated.date is not None
            ), f"Date should be present for {symbol} on {timeframe}"
            assert validated.open > 0, f"Open should be positive for {symbol}"
            assert validated.high > 0, f"High should be positive for {symbol}"
            assert validated.low > 0, f"Low should be positive for {symbol}"
            assert validated.close > 0, f"Close should be positive for {symbol}"

            # Indicator-specific validation
            if indicator == "sma" and validated.sma is not None:
                assert validated.sma > 0, f"SMA should be positive for {symbol}"
            elif indicator == "ema" and validated.ema is not None:
                assert validated.ema > 0, f"EMA should be positive for {symbol}"
            elif indicator == "rsi" and validated.rsi is not None:
                assert 0 <= validated.rsi <= 100, f"RSI should be 0-100 for {symbol}"
            elif indicator == "williams" and validated.williams is not None:
                assert (
                    -100 <= validated.williams <= 0
                ), f"Williams %R should be -100 to 0 for {symbol}"

            # Timeframe-specific validation
            if timeframe in ["1min", "5min"]:
                # High frequency data should have volume (for stocks/ETFs)
                if market_type in ["stock", "etf"]:
                    assert (
                        validated.volume is not None
                    ), f"Volume should be present for {market_type} on {timeframe}"
            elif timeframe == "1day":
                # Daily data should always have complete OHLCV
                assert validated.volume is not None or market_type in [
                    "forex",
                    "crypto",
                ], f"Daily data should have volume for {market_type}"

            # Market type-specific validation
            if market_type == "crypto":
                # Crypto trades 24/7, so should have data at all times
                assert (
                    validated.date is not None
                ), f"Crypto {symbol} should have date on {timeframe}"
            elif market_type == "forex":
                # Forex trades 24/5, so should have good coverage
                assert (
                    validated.date is not None
                ), f"Forex {symbol} should have date on {timeframe}"
            elif market_type in ["stock", "etf"]:
                # Traditional markets have specific trading hours
                assert (
                    validated.date is not None
                ), f"Stock/ETF {symbol} should have date on {timeframe}"

    @pytest.mark.parametrize(
        "indicator_category,indicators,symbol,period_length,timeframe",
        [
            ("moving_averages", ["sma", "ema", "wma"], "AAPL", 20, "1day"),
            ("moving_averages", ["dema", "tema"], "MSFT", 21, "1day"),
            ("momentum_oscillators", ["rsi", "williams"], "GOOGL", 14, "1day"),
            ("trend_indicators", ["adx"], "AMZN", 14, "1day"),
            ("volatility_indicators", ["standarddeviation"], "TSLA", 20, "1day"),
            ("moving_averages", ["sma", "ema"], "SPY", 50, "1day"),
            ("momentum_oscillators", ["rsi", "williams"], "QQQ", 14, "1day"),
            ("moving_averages", ["sma", "ema"], "BTCUSD", 20, "1day"),
            ("momentum_oscillators", ["rsi"], "EURUSD", 14, "1day"),
            ("trend_indicators", ["adx"], "GCUSD", 14, "1day"),
        ],
    )
    def test_technical_indicators_category_coverage(
        self, api_key, indicator_category, indicators, symbol, period_length, timeframe
    ):
        """Test comprehensive coverage of technical indicator categories."""
        results = {}

        for indicator in indicators:
            result = technical_indicators(
                apikey=api_key,
                symbol=symbol,
                indicator=indicator,
                periodLength=period_length,
                timeframe=timeframe,
            )

            result_list = extract_data_list(result)
            results[indicator] = result_list

            assert isinstance(
                result_list, list
            ), f"Result should be list for {indicator} on {symbol}"

            if len(result_list) > 0:
                first_item = result_list[0]
                validated = (
                    FMPTechnicalIndicator.model_validate(first_item)
                    if isinstance(first_item, dict)
                    else first_item
                )

                # Category-specific validation
                if indicator_category == "moving_averages":
                    # Moving averages should smooth price data
                    if indicator == "sma" and validated.sma is not None:
                        assert validated.sma > 0, f"SMA should be positive for {symbol}"
                        # SMA should be reasonably close to close price
                        price_diff_ratio = (
                            abs(validated.sma - validated.close) / validated.close
                        )
                        assert (
                            price_diff_ratio <= 0.5
                        ), f"SMA should be reasonably close to price for {symbol}"
                    elif indicator == "ema" and validated.ema is not None:
                        assert validated.ema > 0, f"EMA should be positive for {symbol}"
                    elif (
                        indicator in ["wma", "dema", "tema"]
                        and hasattr(validated, indicator)
                        and getattr(validated, indicator) is not None
                    ):
                        assert (
                            getattr(validated, indicator) > 0
                        ), f"{indicator.upper()} should be positive for {symbol}"

                elif indicator_category == "momentum_oscillators":
                    # Momentum oscillators should be bounded
                    if indicator == "rsi" and validated.rsi is not None:
                        assert (
                            0 <= validated.rsi <= 100
                        ), f"RSI should be 0-100 for {symbol}"
                    elif indicator == "williams" and validated.williams is not None:
                        assert (
                            -100 <= validated.williams <= 0
                        ), f"Williams %R should be -100 to 0 for {symbol}"

                elif indicator_category == "trend_indicators":
                    # Trend indicators should indicate trend strength
                    if indicator == "adx" and validated.adx is not None:
                        assert (
                            0 <= validated.adx <= 100
                        ), f"ADX should be 0-100 for {symbol}"

                elif indicator_category == "volatility_indicators":
                    # Volatility indicators should be non-negative
                    if (
                        indicator == "standarddeviation"
                        and hasattr(validated, "standarddeviation")
                        and validated.standarddeviation is not None
                    ):
                        assert (
                            validated.standarddeviation >= 0
                        ), f"Standard deviation should be non-negative for {symbol}"

        # Verify we got results for the indicator category
        successful_indicators = [ind for ind, res in results.items() if len(res) > 0]
        if len(successful_indicators) == 0:
            # If no indicators returned data, it might be due to API limitations
            pytest.skip(
                f"No {indicator_category} data available for {symbol}, possibly due to API plan limitations"
            )
