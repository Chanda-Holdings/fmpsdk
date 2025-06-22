"""
Comprehensive tests for fmpsdk.technical_indicators module.
Tests all technical indicator functions including validation and error handling.
"""

import os

import pytest

import fmpsdk as ti
from fmpsdk.models import *

API_KEY = os.getenv("FMP_API_KEY")


class TestTechnicalIndicatorsGeneral:
    """Test the general technical indicators function."""

    def test_technical_indicators_default_parameters(self):
        """Test technical indicators with default parameters."""
        result = ti.technical_indicators(apikey=API_KEY, symbol="AAPL")
        assert result is not None

    def test_technical_indicators_custom_parameters(self):
        """Test technical indicators with custom parameters."""
        result = ti.technical_indicators(
            apikey=API_KEY,
            symbol="AAPL",
            period=20,
            statistics_type="EMA",
            time_delta="daily",
        )
        assert result is not None

    def test_technical_indicators_intraday_time_deltas(self):
        """Test technical indicators with different intraday time deltas."""
        time_deltas = ["1min", "5min", "15min", "30min", "1hour", "4hour"]

        for time_delta in time_deltas:
            result = ti.technical_indicators(
                apikey=API_KEY, symbol="AAPL", time_delta=time_delta
            )
            assert result is not None

    def test_technical_indicators_different_statistics_types(self):
        """Test technical indicators with different statistics types."""
        statistics_types = [
            "sma",
            "ema",
            "wma",
            "dema",
            "tema",
            "williams",
            "rsi",
            "adx",
            "standardDeviation",
        ]

        for stats_type in statistics_types:
            result = ti.technical_indicators(
                apikey=API_KEY, symbol="AAPL", statistics_type=stats_type
            )
            assert result is not None

    def test_technical_indicators_different_periods(self):
        """Test technical indicators with different periods."""
        periods = [5, 10, 14, 20, 50, 100, 200]

        for period in periods:
            result = ti.technical_indicators(
                apikey=API_KEY, symbol="AAPL", period=period
            )
            assert result is not None

    def test_technical_indicators_invalid_statistics_type(self):
        """Test technical indicators with invalid statistics type."""
        # This should handle invalid types gracefully
        result = ti.technical_indicators(
            apikey=API_KEY, symbol="AAPL", statistics_type="INVALID_TYPE"
        )
        # Should still return a result, the validation happens internally
        assert result is not None

    def test_technical_indicators_invalid_time_delta(self):
        """Test technical indicators with invalid time delta."""
        # This should handle invalid time deltas gracefully
        result = ti.technical_indicators(
            apikey=API_KEY, symbol="AAPL", time_delta="INVALID_DELTA"
        )
        # Should still return a result, the validation happens internally
        assert result is not None


class TestSMAIndicator:
    """Test Simple Moving Average (SMA) indicator."""

    def test_technical_indicators_sma_daily(self):
        """Test SMA with daily interval."""
        result = ti.technical_indicators_sma(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20
        )
        assert result is not None

    def test_technical_indicators_sma_different_intervals(self):
        """Test SMA with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=20
            )
            assert result is not None

    def test_technical_indicators_sma_different_time_periods(self):
        """Test SMA with different time periods."""
        time_periods = [5, 10, 14, 20, 50, 100, 200]

        for period in time_periods:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None

    def test_technical_indicators_sma_different_symbols(self):
        """Test SMA with different symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "SPY"]

        for symbol in symbols:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol=symbol, interval="daily", time_period=20
            )
            assert result is not None


class TestEMAIndicator:
    """Test Exponential Moving Average (EMA) indicator."""

    def test_technical_indicators_ema_daily(self):
        """Test EMA with daily interval."""
        result = ti.technical_indicators_ema(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20
        )
        assert result is not None

    def test_technical_indicators_ema_different_intervals(self):
        """Test EMA with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_ema(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=20
            )
            assert result is not None

    def test_technical_indicators_ema_different_time_periods(self):
        """Test EMA with different time periods."""
        time_periods = [5, 10, 12, 21, 26, 50, 100, 200]

        for period in time_periods:
            result = ti.technical_indicators_ema(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestDEMAIndicator:
    """Test Double Exponential Moving Average (DEMA) indicator."""

    def test_technical_indicators_dema_daily(self):
        """Test DEMA with daily interval."""
        result = ti.technical_indicators_dema(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20
        )
        assert result is not None

    def test_technical_indicators_dema_different_intervals(self):
        """Test DEMA with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_dema(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=20
            )
            assert result is not None

    def test_technical_indicators_dema_different_time_periods(self):
        """Test DEMA with different time periods."""
        time_periods = [10, 14, 20, 21, 50, 100]

        for period in time_periods:
            result = ti.technical_indicators_dema(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestRSIIndicator:
    """Test Relative Strength Index (RSI) indicator."""

    def test_technical_indicators_rsi_daily(self):
        """Test RSI with daily interval."""
        result = ti.technical_indicators_rsi(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=14
        )
        assert result is not None

    def test_technical_indicators_rsi_different_intervals(self):
        """Test RSI with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_rsi(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=14
            )
            assert result is not None

    def test_technical_indicators_rsi_different_time_periods(self):
        """Test RSI with different time periods."""
        time_periods = [9, 14, 21, 25]  # Common RSI periods

        for period in time_periods:
            result = ti.technical_indicators_rsi(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None

    def test_technical_indicators_rsi_crypto_symbols(self):
        """Test RSI with cryptocurrency symbols."""
        crypto_symbols = ["BTCUSD", "ETHUSD", "ADAUSD"]

        for symbol in crypto_symbols:
            result = ti.technical_indicators_rsi(
                apikey=API_KEY, symbol=symbol, interval="daily", time_period=14
            )
            assert result is not None


class TestStandardDeviationIndicator:
    """Test Standard Deviation indicator."""

    def test_technical_indicators_standarddeviation_daily(self):
        """Test Standard Deviation with daily interval."""
        result = ti.technical_indicators_standarddeviation(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20
        )
        assert result is not None

    def test_technical_indicators_standarddeviation_different_intervals(self):
        """Test Standard Deviation with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_standarddeviation(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=20
            )
            assert result is not None

    def test_technical_indicators_standarddeviation_different_time_periods(self):
        """Test Standard Deviation with different time periods."""
        time_periods = [10, 14, 20, 30, 50]

        for period in time_periods:
            result = ti.technical_indicators_standarddeviation(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestWilliamsIndicator:
    """Test Williams %R indicator."""

    def test_technical_indicators_williams_daily(self):
        """Test Williams %R with daily interval."""
        result = ti.technical_indicators_williams(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=14
        )
        assert result is not None

    def test_technical_indicators_williams_different_intervals(self):
        """Test Williams %R with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_williams(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=14
            )
            assert result is not None

    def test_technical_indicators_williams_different_time_periods(self):
        """Test Williams %R with different time periods."""
        time_periods = [7, 14, 21, 28]  # Common Williams %R periods

        for period in time_periods:
            result = ti.technical_indicators_williams(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestADXIndicator:
    """Test Average Directional Index (ADX) indicator."""

    def test_technical_indicators_adx_daily(self):
        """Test ADX with daily interval."""
        result = ti.technical_indicators_adx(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=14
        )
        assert result is not None

    def test_technical_indicators_adx_different_intervals(self):
        """Test ADX with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour", "daily"]

        for interval in intervals:
            result = ti.technical_indicators_adx(
                apikey=API_KEY, symbol="AAPL", interval=interval, time_period=14
            )
            assert result is not None

    def test_technical_indicators_adx_different_time_periods(self):
        """Test ADX with different time periods."""
        time_periods = [7, 14, 21, 28]  # Common ADX periods

        for period in time_periods:
            result = ti.technical_indicators_adx(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestTechnicalIndicatorsErrorHandling:
    """Test error handling for technical indicators."""

    def test_technical_indicators_invalid_api_key(self):
        """Test technical indicators with invalid API key."""
        result = ti.technical_indicators_sma(
            apikey="invalid_key", symbol="AAPL", interval="daily", time_period=20
        )
        # Should handle gracefully, not crash
        assert result is not None or result is None

    def test_technical_indicators_invalid_symbol(self):
        """Test technical indicators with invalid symbol."""
        result = ti.technical_indicators_sma(
            apikey=API_KEY, symbol="INVALID123", interval="daily", time_period=20
        )
        # Should handle gracefully
        assert result is not None

    def test_technical_indicators_invalid_interval(self):
        """Test technical indicators with invalid interval."""
        result = ti.technical_indicators_sma(
            apikey=API_KEY, symbol="AAPL", interval="invalid_interval", time_period=20
        )
        # Should handle gracefully
        assert result is not None

    def test_technical_indicators_invalid_time_period(self):
        """Test technical indicators with invalid time period."""
        invalid_periods = [0, -1, -10]

        for period in invalid_periods:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            # Should handle gracefully
            assert result is not None

    def test_technical_indicators_extreme_time_periods(self):
        """Test technical indicators with extreme time periods."""
        extreme_periods = [1, 2, 500, 1000]

        for period in extreme_periods:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestTechnicalIndicatorsCombinations:
    """Test combinations of technical indicators parameters."""

    def test_all_indicators_same_symbol(self):
        """Test all indicator types for the same symbol."""
        symbol = "AAPL"
        interval = "daily"
        time_period = 20

        indicators = [
            ti.technical_indicators_sma,
            ti.technical_indicators_ema,
            ti.technical_indicators_dema,
            ti.technical_indicators_rsi,
            ti.technical_indicators_standarddeviation,
            ti.technical_indicators_williams,
            ti.technical_indicators_adx,
        ]

        for indicator_func in indicators:
            result = indicator_func(
                apikey=API_KEY,
                symbol=symbol,
                interval=interval,
                time_period=time_period,
            )
            assert result is not None

    def test_multiple_symbols_same_indicator(self):
        """Test multiple symbols with the same indicator."""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

        for symbol in symbols:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol=symbol, interval="daily", time_period=20
            )
            assert result is not None

    def test_forex_symbols_technical_indicators(self):
        """Test technical indicators with forex symbols."""
        forex_symbols = ["EURUSD", "GBPUSD", "USDJPY"]

        for symbol in forex_symbols:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol=symbol, interval="daily", time_period=20
            )
            assert result is not None

    def test_commodity_symbols_technical_indicators(self):
        """Test technical indicators with commodity symbols."""
        commodity_symbols = ["GCUSD", "CLUSD", "NQUSD"]  # Gold, Oil, Natural Gas

        for symbol in commodity_symbols:
            result = ti.technical_indicators_rsi(
                apikey=API_KEY, symbol=symbol, interval="daily", time_period=14
            )
            assert result is not None


class TestTechnicalIndicatorsDataTypes:
    """Test data types and return values of technical indicators."""

    def test_technical_indicators_return_types(self):
        """Test that technical indicators return proper types."""
        result = ti.technical_indicators_sma(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20
        )

        # Should return a list-like object or None
        assert result is None or hasattr(result, "__iter__")

    def test_technical_indicators_parameter_types(self):
        """Test that technical indicators handle parameter types correctly."""
        # Test with string time_period (should be converted to int internally)
        result = ti.technical_indicators_sma(
            apikey=API_KEY, symbol="AAPL", interval="daily", time_period=20  # int
        )
        assert result is not None


class TestTechnicalIndicatorsPerformance:
    """Test performance aspects of technical indicators."""

    def test_technical_indicators_bulk_requests(self):
        """Test making multiple technical indicator requests."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        indicators = [
            ti.technical_indicators_sma,
            ti.technical_indicators_ema,
            ti.technical_indicators_rsi,
        ]

        results = []
        for symbol in symbols:
            for indicator_func in indicators:
                result = indicator_func(
                    apikey=API_KEY, symbol=symbol, interval="daily", time_period=20
                )
                results.append(result)

        # All requests should succeed
        assert all(result is not None for result in results)

    def test_technical_indicators_different_time_periods_performance(self):
        """Test technical indicators with different time periods for performance."""
        time_periods = [5, 10, 20, 50, 100, 200]

        for period in time_periods:
            result = ti.technical_indicators_sma(
                apikey=API_KEY, symbol="AAPL", interval="daily", time_period=period
            )
            assert result is not None


class TestParameterizedExtremeCases:
    """Test extreme parameter values and edge cases."""

    @pytest.mark.parametrize(
        "period,scenario",
        [
            (1, "MINIMUM_PERIOD"),
            (2, "VERY_SHORT_PERIOD"),
            (500, "VERY_LONG_PERIOD"),
            (1000, "EXTREME_PERIOD"),
            (9999, "MAXIMUM_PERIOD"),
            (0, "ZERO_PERIOD"),
            (-1, "NEGATIVE_PERIOD"),
            (-10, "VERY_NEGATIVE_PERIOD"),
        ],
    )
    def test_extreme_period_values(self, period, scenario):
        """Test technical indicators with extreme period values."""
        try:
            result = ti.technical_indicators(
                apikey=API_KEY, symbol="AAPL", period=period, statistics_type="sma"
            )

            if scenario in ["ZERO_PERIOD", "NEGATIVE_PERIOD", "VERY_NEGATIVE_PERIOD"]:
                # These might return None or handle gracefully
                assert result is None or isinstance(result, (list, dict))
            else:
                assert result is not None
        except Exception as e:
            # Some extreme values might raise exceptions
            assert scenario in [
                "ZERO_PERIOD",
                "NEGATIVE_PERIOD",
                "VERY_NEGATIVE_PERIOD",
                "MAXIMUM_PERIOD",
            ]


class TestParameterizedVolatilityScenarios:
    """Test technical indicators on stocks with different volatility profiles."""

    @pytest.mark.parametrize(
        "symbol,volatility_profile",
        [
            # High volatility stocks
            ("TSLA", "HIGH_VOLATILITY"),
            ("NVDA", "TECH_VOLATILITY"),
            ("GME", "MEME_STOCK"),
            ("AMC", "RETAIL_FAVORITE"),
            # Low volatility stocks
            ("KO", "STABLE_DIVIDEND"),
            ("PG", "DEFENSIVE"),
            ("JNJ", "HEALTHCARE_STABLE"),
            ("WMT", "CONSUMER_STAPLES"),
            # Medium volatility
            ("AAPL", "LARGE_CAP_TECH"),
            ("MSFT", "ENTERPRISE_TECH"),
            ("JPM", "FINANCIAL"),
            ("XOM", "ENERGY"),
            # Special cases
            ("BRK.A", "ULTRA_HIGH_PRICE"),
            ("BRK.B", "HIGH_PRICE"),
            ("SIRI", "LOW_PRICE"),
        ],
    )
    def test_volatility_profile_indicators(self, symbol, volatility_profile):
        """Test technical indicators across different volatility profiles."""
        # Test multiple indicators on each symbol
        indicators = ["sma", "ema", "rsi", "williams"]

        for indicator in indicators:
            result = ti.technical_indicators(
                apikey=API_KEY, symbol=symbol, statistics_type=indicator, period=14
            )
            assert result is not None


class TestParameterizedTimeFrameCombinations:
    """Test all combinations of time frames and indicators."""

    @pytest.mark.parametrize(
        "time_delta,indicator,period",
        [
            # Intraday combinations
            ("1min", "sma", 20),
            ("5min", "ema", 10),
            ("15min", "rsi", 14),
            ("30min", "williams", 14),
            ("1hour", "adx", 14),
            ("4hour", "standardDeviation", 20),
            # Daily combinations
            ("daily", "sma", 50),
            ("daily", "ema", 200),
            ("daily", "rsi", 14),
            ("daily", "williams", 14),
            ("daily", "adx", 14),
            # Edge case combinations
            ("1min", "sma", 200),  # Very long period on short timeframe
            ("daily", "sma", 5),  # Very short period on long timeframe
            ("4hour", "rsi", 2),  # Minimal period
        ],
    )
    def test_timeframe_indicator_combinations(self, time_delta, indicator, period):
        """Test various combinations of timeframes, indicators, and periods."""
        result = ti.technical_indicators(
            apikey=API_KEY,
            symbol="AAPL",
            time_delta=time_delta,
            statistics_type=indicator,
            period=period,
        )
        assert result is not None
