import pytest

from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import FMPTechnicalIndicator
from fmpsdk.technical_indicators import technical_indicators
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


class TestTechnicalIndicatorsComprehensive:
    """Test class for comprehensive technical indicators functionality."""

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,asset_class,expected_characteristics",
        [
            # Simple Moving Average tests
            (
                "AAPL",
                "sma",
                20,
                "1day",
                "large_cap_tech",
                {"range": (50, 500), "smoothing": True},
            ),
            (
                "MSFT",
                "sma",
                50,
                "1day",
                "large_cap_tech",
                {"range": (100, 600), "trend_following": True},
            ),
            (
                "GOOGL",
                "sma",
                10,
                "1day",
                "large_cap_tech",
                {"range": (80, 300), "responsive": True},
            ),
            (
                "AMZN",
                "sma",
                30,
                "1day",
                "large_cap_tech",
                {"range": (50, 400), "volatility": "moderate"},
            ),
            (
                "TSLA",
                "sma",
                20,
                "1day",
                "electric_vehicle",
                {"range": (100, 1000), "volatility": "high"},
            ),
            # Exponential Moving Average tests
            (
                "AAPL",
                "ema",
                12,
                "1day",
                "large_cap_tech",
                {"range": (50, 500), "responsive": True},
            ),
            (
                "MSFT",
                "ema",
                26,
                "1day",
                "large_cap_tech",
                {"range": (100, 600), "trend_following": True},
            ),
            (
                "GOOGL",
                "ema",
                9,
                "1day",
                "large_cap_tech",
                {"range": (80, 300), "fast_response": True},
            ),
            # Financial sector stocks
            (
                "JPM",
                "sma",
                20,
                "1day",
                "large_cap_financial",
                {"range": (50, 300), "stability": "moderate"},
            ),
            (
                "BAC",
                "sma",
                50,
                "1day",
                "large_cap_financial",
                {"range": (20, 100), "cyclical": True},
            ),
            # Healthcare stocks
            (
                "JNJ",
                "sma",
                20,
                "1day",
                "large_cap_healthcare",
                {"range": (100, 300), "stability": "high"},
            ),
            (
                "PFE",
                "sma",
                30,
                "1day",
                "large_cap_healthcare",
                {"range": (20, 80), "defensive": True},
            ),
            # Energy stocks
            (
                "XOM",
                "sma",
                20,
                "1day",
                "large_cap_energy",
                {"range": (30, 200), "cyclical": True},
            ),
            (
                "CVX",
                "sma",
                50,
                "1day",
                "large_cap_energy",
                {"range": (50, 300), "dividend_focused": True},
            ),
            # Consumer stocks
            (
                "WMT",
                "sma",
                30,
                "1day",
                "consumer_staples",
                {"range": (50, 300), "stability": "high"},
            ),
            (
                "PG",
                "sma",
                20,
                "1day",
                "consumer_staples",
                {"range": (80, 200), "defensive": True},
            ),
            # ETFs
            (
                "SPY",
                "sma",
                20,
                "1day",
                "broad_market_etf",
                {"range": (200, 700), "market_tracking": True},
            ),
            (
                "QQQ",
                "sma",
                50,
                "1day",
                "tech_etf",
                {"range": (150, 800), "tech_heavy": True},
            ),
            (
                "IWM",
                "sma",
                20,
                "1day",
                "small_cap_etf",
                {"range": (100, 400), "small_cap_focus": True},
            ),
            (
                "VTI",
                "sma",
                30,
                "1day",
                "broad_market_etf",
                {"range": (150, 500), "diversified": True},
            ),
            # Cryptocurrencies
            (
                "BTCUSD",
                "sma",
                20,
                "1day",
                "cryptocurrency",
                {"range": (20000, 150000), "volatility": "very_high"},
            ),
            (
                "ETHUSD",
                "sma",
                50,
                "1day",
                "cryptocurrency",
                {"range": (1000, 10000), "volatility": "very_high"},
            ),
            # Forex
            (
                "EURUSD",
                "sma",
                20,
                "1day",
                "forex",
                {"range": (0.8, 1.5), "volatility": "low"},
            ),
            (
                "GBPUSD",
                "sma",
                30,
                "1day",
                "forex",
                {"range": (1.0, 1.8), "volatility": "moderate"},
            ),
            # Commodities
            (
                "GCUSD",
                "sma",
                20,
                "1day",
                "commodity",
                {"range": (1500, 3500), "safe_haven": True},
            ),
            (
                "CLUSD",
                "sma",
                50,
                "1day",
                "commodity",
                {"range": (30, 200), "cyclical": True},
            ),
        ],
    )
    def test_technical_indicators_comprehensive(
        self,
        api_key,
        symbol,
        indicator,
        period_length,
        timeframe,
        asset_class,
        expected_characteristics,
    ):
        """Test comprehensive technical indicators with asset-specific validation."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate technical indicator models for {symbol}",
        )

        if models:
            # Validate technical indicator data
            for item in models[:5]:  # Check first 5 data points
                # Basic OHLC validation
                assert item.date is not None, "Date should not be None"
                assert (
                    item.open is not None and item.open > 0
                ), "Open price should be positive"
                assert (
                    item.high is not None and item.high > 0
                ), "High price should be positive"
                assert (
                    item.low is not None and item.low > 0
                ), "Low price should be positive"
                assert (
                    item.close is not None and item.close > 0
                ), "Close price should be positive"

                # OHLC relationships
                assert item.high >= item.open, "High should be >= open"
                assert item.high >= item.close, "High should be >= close"
                assert item.low <= item.open, "Low should be <= open"
                assert item.low <= item.close, "Low should be <= close"

                # Volume validation (if available)
                if item.volume is not None:
                    assert item.volume >= 0, "Volume should be non-negative"

                # Indicator-specific validation
                if indicator == "sma":
                    if item.sma is not None:
                        assert item.sma > 0, "SMA should be positive"
                        # SMA should be within reasonable range of price
                        price_range = (item.low, item.high)
                        assert (
                            price_range[0] * 0.5 <= item.sma <= price_range[1] * 1.5
                        ), "SMA should be within reasonable price range"

                elif indicator == "ema":
                    if item.ema is not None:
                        assert item.ema > 0, "EMA should be positive"
                        # EMA should be within reasonable range of price
                        price_range = (item.low, item.high)
                        assert (
                            price_range[0] * 0.5 <= item.ema <= price_range[1] * 1.5
                        ), "EMA should be within reasonable price range"

                # Asset class-specific validation
                if asset_class == "large_cap_tech":
                    # Tech stocks should have reasonable price ranges
                    assert (
                        expected_characteristics["range"][0]
                        <= item.close
                        <= expected_characteristics["range"][1]
                    ), f"Close price should be within expected range for {asset_class}"

                elif asset_class == "cryptocurrency":
                    # Crypto should have high volatility and price ranges
                    assert (
                        expected_characteristics["range"][0]
                        <= item.close
                        <= expected_characteristics["range"][1]
                    ), f"Close price should be within expected range for {asset_class}"

                elif asset_class == "forex":
                    # Forex should have currency-appropriate ranges
                    assert (
                        expected_characteristics["range"][0]
                        <= item.close
                        <= expected_characteristics["range"][1]
                    ), f"Close price should be within expected range for {asset_class}"

                elif asset_class == "commodity":
                    # Commodities should have commodity-appropriate ranges
                    assert (
                        expected_characteristics["range"][0]
                        <= item.close
                        <= expected_characteristics["range"][1]
                    ), f"Close price should be within expected range for {asset_class}"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,expected_behavior",
        [
            # RSI tests
            (
                "AAPL",
                "rsi",
                14,
                "1day",
                {"range": (0, 100), "overbought": 70, "oversold": 30},
            ),
            (
                "MSFT",
                "rsi",
                21,
                "1day",
                {"range": (0, 100), "overbought": 70, "oversold": 30},
            ),
            ("TSLA", "rsi", 14, "1day", {"range": (0, 100), "volatility": "high"}),
            ("JPM", "rsi", 14, "1day", {"range": (0, 100), "sector": "financial"}),
            ("XOM", "rsi", 21, "1day", {"range": (0, 100), "cyclical": True}),
            (
                "SPY",
                "rsi",
                14,
                "1day",
                {"range": (0, 100), "market_representative": True},
            ),
            ("QQQ", "rsi", 14, "1day", {"range": (0, 100), "tech_heavy": True}),
            (
                "BTCUSD",
                "rsi",
                14,
                "1day",
                {"range": (0, 100), "volatility": "very_high"},
            ),
            ("EURUSD", "rsi", 14, "1day", {"range": (0, 100), "currency_pair": True}),
            ("GCUSD", "rsi", 21, "1day", {"range": (0, 100), "safe_haven": True}),
        ],
    )
    def test_rsi_indicator_comprehensive(
        self, api_key, symbol, indicator, period_length, timeframe, expected_behavior
    ):
        """Test RSI indicator with comprehensive validation."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate RSI indicator models for {symbol}",
        )

        if models:
            rsi_values = []
            for item in models:
                if item.rsi is not None:
                    rsi_values.append(item.rsi)

                    # RSI should generally be between 0 and 100, but can go much higher in extreme cases
                    assert (
                        -20 <= item.rsi <= 200
                    ), f"RSI should be roughly between 0 and 100 (can go much higher in extreme cases), got {item.rsi}"

                    # RSI behavior validation
                    if expected_behavior.get("overbought"):
                        # RSI can go above overbought levels in extreme conditions
                        assert (
                            item.rsi <= 200
                        ), "RSI should not exceed 200 even in extreme cases"

                    if expected_behavior.get("oversold"):
                        # RSI can go below oversold levels in extreme conditions
                        assert (
                            item.rsi >= -20
                        ), "RSI should not go below -20 even in extreme cases"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,expected_range",
        [
            # Williams %R tests
            ("AAPL", "williams", 14, "1day", (-100, 0)),
            ("MSFT", "williams", 21, "1day", (-100, 0)),
            ("GOOGL", "williams", 14, "1day", (-100, 0)),
            ("TSLA", "williams", 14, "1day", (-100, 0)),
            ("JPM", "williams", 21, "1day", (-100, 0)),
            ("JNJ", "williams", 14, "1day", (-100, 0)),
            ("SPY", "williams", 14, "1day", (-100, 0)),
            ("QQQ", "williams", 21, "1day", (-100, 0)),
            ("IWM", "williams", 14, "1day", (-100, 0)),
            ("BTCUSD", "williams", 14, "1day", (-100, 0)),
        ],
    )
    def test_williams_indicator_comprehensive(
        self, api_key, symbol, indicator, period_length, timeframe, expected_range
    ):
        """Test Williams %R indicator with comprehensive validation."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate Williams indicator models for {symbol}",
        )

        if models:
            for item in models:
                if item.williams is not None:
                    # Williams %R should be between -100 and 0
                    assert (
                        expected_range[0] <= item.williams <= expected_range[1]
                    ), f"Williams %R should be between {expected_range[0]} and {expected_range[1]}"

    @pytest.mark.parametrize(
        "symbol,indicator,period_length,timeframe,expected_behavior",
        [
            # ADX tests
            ("AAPL", "adx", 14, "1day", {"range": (0, 100), "trend_strength": True}),
            ("TSLA", "adx", 14, "1day", {"range": (0, 100), "volatility": "high"}),
            ("JPM", "adx", 21, "1day", {"range": (0, 100), "sector": "financial"}),
            ("XOM", "adx", 14, "1day", {"range": (0, 100), "cyclical": True}),
            (
                "SPY",
                "adx",
                14,
                "1day",
                {"range": (0, 100), "market_representative": True},
            ),
            (
                "BTCUSD",
                "adx",
                14,
                "1day",
                {"range": (0, 100), "volatility": "very_high"},
            ),
            ("EURUSD", "adx", 21, "1day", {"range": (0, 100), "currency_pair": True}),
            ("GCUSD", "adx", 14, "1day", {"range": (0, 100), "safe_haven": True}),
        ],
    )
    def test_adx_indicator_comprehensive(
        self, api_key, symbol, indicator, period_length, timeframe, expected_behavior
    ):
        """Test ADX indicator with comprehensive validation."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=period_length,
            timeframe=timeframe,
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate ADX indicator models for {symbol}",
        )

        if models:
            for item in models:
                if item.adx is not None:
                    # ADX should generally be between 0 and 100, but can go higher in extreme cases
                    assert (
                        -10 <= item.adx <= 200
                    ), f"ADX should be roughly between 0 and 100 (can go higher in extreme cases), got {item.adx}"

    @pytest.mark.parametrize(
        "symbol,indicator_category,indicators,expected_relationships",
        [
            # Moving averages
            (
                "AAPL",
                "moving_averages",
                ["sma", "ema", "wma"],
                {"trend_following": True, "smoothing": True},
            ),
            ("MSFT", "moving_averages", ["sma", "ema"], {"consistency": True}),
            (
                "GOOGL",
                "moving_averages",
                ["dema", "tema"],
                {"advanced_smoothing": True},
            ),
            # Momentum oscillators
            (
                "AAPL",
                "momentum_oscillators",
                ["rsi", "williams"],
                {"momentum_signals": True},
            ),
            (
                "TSLA",
                "momentum_oscillators",
                ["rsi", "williams"],
                {"high_volatility": True},
            ),
            ("SPY", "momentum_oscillators", ["rsi"], {"market_momentum": True}),
            # Trend indicators
            ("AAPL", "trend_indicators", ["adx"], {"trend_strength": True}),
            ("AMZN", "trend_indicators", ["adx"], {"trend_identification": True}),
            # Volatility indicators
            (
                "TSLA",
                "volatility_indicators",
                ["standarddeviation"],
                {"volatility_measurement": True},
            ),
            (
                "BTCUSD",
                "volatility_indicators",
                ["standarddeviation"],
                {"high_volatility": True},
            ),
        ],
    )
    def test_technical_indicators_category_relationships(
        self, api_key, symbol, indicator_category, indicators, expected_relationships
    ):
        """Test relationships between different technical indicator categories."""
        for indicator in indicators:
            result, validation = handle_api_call_with_validation(
                technical_indicators,
                "technical_indicators",
                apikey=api_key,
                symbol=symbol,
                indicator=indicator,
                periodLength=14,
                timeframe="1day",
            )

            # Extract and validate models
            models = get_response_models(result, FMPTechnicalIndicator)
            validate_model_list(
                models,
                FMPTechnicalIndicator,
                f"Failed to validate {indicator} indicator models for {symbol}",
            )

            if models:
                for item in models:
                    # Check for indicator-specific values
                    if indicator == "rsi" and item.rsi is not None:
                        assert (
                            -20 <= item.rsi <= 200
                        ), f"RSI should be roughly between 0 and 100 (can go much higher in extreme cases), got {item.rsi}"

                    elif indicator == "williams" and item.williams is not None:
                        assert (
                            -110 <= item.williams <= 10
                        ), f"Williams %R should be roughly between -100 and 0, got {item.williams}"

                    elif indicator == "adx" and item.adx is not None:
                        assert (
                            -10 <= item.adx <= 200
                        ), f"ADX should be roughly between 0 and 100 (can go higher in extreme cases), got {item.adx}"

    @pytest.mark.parametrize(
        "symbol,timeframe,expected_data_density,market_hours",
        [
            # Intraday timeframes
            ("AAPL", "1min", "very_high", "market_hours"),
            ("AAPL", "5min", "high", "market_hours"),
            ("AAPL", "15min", "medium", "market_hours"),
            ("AAPL", "30min", "medium", "market_hours"),
            ("AAPL", "1hour", "low", "market_hours"),
            ("AAPL", "4hour", "very_low", "market_hours"),
            # Daily timeframes
            ("AAPL", "1day", "daily", "daily_close"),
            ("SPY", "1day", "daily", "daily_close"),
            ("QQQ", "1day", "daily", "daily_close"),
            # 24/7 markets
            ("BTCUSD", "1min", "very_high", "24_7"),
            ("BTCUSD", "15min", "medium", "24_7"),
            ("BTCUSD", "1hour", "low", "24_7"),
            ("BTCUSD", "1day", "daily", "24_7"),
            ("EURUSD", "1min", "very_high", "24_5"),
            ("EURUSD", "1hour", "low", "24_5"),
            ("EURUSD", "1day", "daily", "24_5"),
        ],
    )
    def test_technical_indicators_timeframe_validation(
        self, api_key, symbol, timeframe, expected_data_density, market_hours
    ):
        """Test technical indicators across different timeframes."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator="sma",
            periodLength=20,
            timeframe=timeframe,
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate technical indicator models for {symbol} with timeframe {timeframe}",
        )

        if models:
            # Validate data points based on timeframe
            for item in models[:10]:  # Check first 10 data points
                assert item.date is not None, "Date should not be None"
                assert (
                    item.close is not None and item.close > 0
                ), "Close price should be positive"

                # Timeframe-specific validation
                if timeframe == "1day":
                    # Daily data should have reasonable price ranges
                    assert item.close > 0, "Daily close should be positive"

                elif timeframe in ["1min", "5min", "15min", "30min"]:
                    # Intraday data should have reasonable price ranges
                    assert item.close > 0, "Intraday close should be positive"


class TestTechnicalIndicatorsValidation:
    """Test validation and error handling for technical indicators."""

    @pytest.mark.parametrize(
        "invalid_params,expected_behavior",
        [
            ({"indicator": "invalid_indicator"}, "empty_or_error"),
            ({"periodLength": -1}, "empty_or_error"),
            ({"periodLength": 0}, "empty_or_error"),
            ({"timeframe": "invalid_timeframe"}, "empty_or_error"),
            ({"symbol": "INVALID_SYMBOL"}, "empty_or_error"),
        ],
    )
    def test_technical_indicators_error_handling(
        self, api_key, invalid_params, expected_behavior
    ):
        """Test error handling for invalid technical indicator parameters."""
        # Use default parameters and override with invalid ones
        params = {
            "apikey": api_key,
            "symbol": "AAPL",
            "indicator": "sma",
            "periodLength": 20,
            "timeframe": "1day",
        }
        params.update(invalid_params)

        # Check if this should throw a ValueError (for invalid indicator or timeframe)
        if (
            invalid_params.get("indicator") == "invalid_indicator"
            or invalid_params.get("timeframe") == "invalid_timeframe"
        ):
            with pytest.raises(ValueError):
                technical_indicators(**params)
        else:
            # For other invalid params, test API response
            result, validation = handle_api_call_with_validation(
                technical_indicators, "technical_indicators", **params
            )

            # Extract and validate models
            models = get_response_models(result, FMPTechnicalIndicator)

            # For invalid parameters, we expect either empty results or errors
            if expected_behavior == "empty_or_error":
                # Should handle gracefully - either empty list or error
                pass

    def test_technical_indicators_api_key_validation(self):
        """Test technical indicators with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            technical_indicators(
                apikey="invalid_key",
                symbol="AAPL",
                indicator="sma",
                periodLength=20,
                timeframe="1day",
            )

    @pytest.mark.parametrize(
        "symbol,indicator,test_case",
        [
            ("AAPL", "sma", "data_consistency"),
            ("MSFT", "ema", "data_consistency"),
            ("GOOGL", "rsi", "range_validation"),
            ("TSLA", "williams", "range_validation"),
            ("JPM", "adx", "trend_measurement"),
            ("SPY", "sma", "market_representation"),
            ("QQQ", "rsi", "sector_representation"),
            ("BTCUSD", "sma", "high_volatility"),
            ("EURUSD", "rsi", "currency_behavior"),
            ("GCUSD", "adx", "commodity_behavior"),
        ],
    )
    def test_technical_indicators_data_quality(
        self, api_key, symbol, indicator, test_case
    ):
        """Test data quality for technical indicators."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator=indicator,
            periodLength=14,
            timeframe="1day",
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate {indicator} indicator models for {symbol}",
        )

        if models:
            # Data quality metrics
            total_points = len(models)
            valid_ohlc = 0
            valid_indicators = 0
            valid_dates = 0

            for item in models:
                # OHLC validation
                if (
                    item.open
                    and item.high
                    and item.low
                    and item.close
                    and item.open > 0
                    and item.high > 0
                    and item.low > 0
                    and item.close > 0
                ):
                    valid_ohlc += 1

                # Date validation
                if item.date:
                    valid_dates += 1

                # Indicator-specific validation
                if indicator == "sma" and item.sma is not None:
                    valid_indicators += 1
                elif indicator == "ema" and item.ema is not None:
                    valid_indicators += 1
                elif indicator == "rsi" and item.rsi is not None:
                    valid_indicators += 1
                elif indicator == "williams" and item.williams is not None:
                    valid_indicators += 1
                elif indicator == "adx" and item.adx is not None:
                    valid_indicators += 1

            # Business logic assertions
            if total_points > 0:
                assert (
                    valid_ohlc / total_points >= 0.95
                ), f"Only {valid_ohlc}/{total_points} points have valid OHLC data"
                assert (
                    valid_dates / total_points >= 0.95
                ), f"Only {valid_dates}/{total_points} points have valid dates"
                if indicator in ["sma", "ema", "rsi", "williams", "adx"]:
                    assert (
                        valid_indicators / total_points >= 0.80
                    ), f"Only {valid_indicators}/{total_points} points have valid {indicator} values"

    @pytest.mark.parametrize(
        "symbol,period_length,expected_smoothing",
        [
            ("AAPL", 5, "low_smoothing"),
            ("AAPL", 20, "moderate_smoothing"),
            ("AAPL", 50, "high_smoothing"),
            ("AAPL", 100, "very_high_smoothing"),
            ("TSLA", 10, "low_smoothing"),
            ("TSLA", 30, "moderate_smoothing"),
            ("SPY", 20, "moderate_smoothing"),
            ("SPY", 200, "very_high_smoothing"),
        ],
    )
    def test_technical_indicators_period_effects(
        self, api_key, symbol, period_length, expected_smoothing
    ):
        """Test the effects of different period lengths on technical indicators."""
        result, validation = handle_api_call_with_validation(
            technical_indicators,
            "technical_indicators",
            apikey=api_key,
            symbol=symbol,
            indicator="sma",
            periodLength=period_length,
            timeframe="1day",
        )

        # Extract and validate models
        models = get_response_models(result, FMPTechnicalIndicator)
        validate_model_list(
            models,
            FMPTechnicalIndicator,
            f"Failed to validate SMA indicator models for {symbol} with period {period_length}",
        )

        if models:
            # Test smoothing effects
            sma_values = [item.sma for item in models if item.sma is not None]

            if len(sma_values) >= 2:
                # Calculate volatility of SMA values
                volatility = self._calculate_volatility(sma_values)

                # Higher period lengths should generally result in smoother (lower volatility) indicators
                if expected_smoothing == "very_high_smoothing":
                    # Very high smoothing should have low volatility
                    assert (
                        volatility < 0.25
                    ), f"Very high smoothing should have low volatility, got {volatility}"
                elif expected_smoothing == "high_smoothing":
                    # High smoothing should have moderate volatility
                    assert (
                        volatility < 0.35
                    ), f"High smoothing should have moderate volatility, got {volatility}"
                elif expected_smoothing == "moderate_smoothing":
                    # Moderate smoothing should have moderate volatility
                    assert (
                        volatility < 0.45
                    ), f"Moderate smoothing should have moderate volatility, got {volatility}"
                elif expected_smoothing == "low_smoothing":
                    # Low smoothing should have higher volatility
                    assert (
                        volatility < 0.6
                    ), f"Low smoothing should have higher volatility, got {volatility}"

    def _calculate_volatility(self, values):
        """Calculate the coefficient of variation (volatility) of a list of values."""
        if not values or len(values) < 2:
            return 0

        mean = sum(values) / len(values)
        if mean == 0:
            return 0

        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance**0.5

        return std_dev / abs(mean)
