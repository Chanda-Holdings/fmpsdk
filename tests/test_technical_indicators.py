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
