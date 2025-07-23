from datetime import datetime, timedelta

import pytest

from fmpsdk.chart import (
    historical_chart,
    historical_price_eod,
    historical_price_eod_dividend_adjusted,
    historical_price_eod_light,
    historical_price_eod_non_split_adjusted,
)
from fmpsdk.models import (
    FMPHistoricalDataPointFull,
    FMPHistoricalDataPointLight,
    FMPIntradayDataPoint,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


class TestHistoricalPriceEODLight:
    """Test class for historical EOD light data functionality."""

    def test_historical_price_eod_light_basic(self, api_key):
        """Test basic historical EOD light data retrieval."""
        result, validation = handle_api_call_with_validation(
            historical_price_eod_light,
            "historical_price_eod_light",
            apikey=api_key,
            symbol="AAPL",
        )

        data_points = get_response_models(result, FMPHistoricalDataPointLight)
        validate_model_list(data_points, FMPHistoricalDataPointLight)
        assert len(data_points) > 0

        # Validate first item with business logic
        first_point = data_points[0]
        assert first_point.symbol == "AAPL"
        assert first_point.date is not None, "Date should not be None"
        assert first_point.price > 0, "Price should be positive"
        assert first_point.volume >= 0, "Volume should be non-negative"

    def test_historical_price_eod_light_with_date_range(self, api_key):
        """Test historical EOD light data with specific date range."""
        from_date = "2024-01-01"
        to_date = "2024-01-31"

        result, validation = handle_api_call_with_validation(
            historical_price_eod_light,
            "historical_price_eod_light",
            apikey=api_key,
            symbol="AAPL",
            from_date=from_date,
            to_date=to_date,
        )

        data_points = get_response_models(result, FMPHistoricalDataPointLight)
        validate_model_list(data_points, FMPHistoricalDataPointLight)
        assert len(data_points) > 0

        # Validate date range
        for point in data_points:
            assert (
                from_date <= point.date <= to_date
            ), f"Date {point.date} should be within range {from_date} to {to_date}"

    def test_historical_price_eod_light_multiple_asset_types(self, api_key):
        """Test historical EOD light data for different asset types."""
        test_cases = [
            ("large_cap", "AAPL", "stock"),
            ("etf", "SPY", "ETF"),
            ("crypto", "BTCUSD", "cryptocurrency"),
            ("forex", "EURUSD", "forex pair"),
            ("commodity", "GCUSD", "commodity"),
        ]

        for asset_category, symbol, asset_name in test_cases:
            result, validation = handle_api_call_with_validation(
                historical_price_eod_light,
                "historical_price_eod_light",
                apikey=api_key,
                symbol=symbol,
            )
            data_points = get_response_models(result, FMPHistoricalDataPointLight)
            validate_model_list(data_points, FMPHistoricalDataPointLight, min_count=0)

            # Some asset types might not have data available
            if len(data_points) > 0:
                first_point = data_points[0]
                assert (
                    first_point.symbol == symbol
                ), f"Symbol should match for {asset_name}"
                assert (
                    first_point.price > 0
                ), f"Price should be positive for {asset_name}"

    def test_historical_price_eod_light_chronological_order(self, api_key):
        """Test that historical data is returned in chronological order."""
        result, validation = handle_api_call_with_validation(
            historical_price_eod_light,
            "historical_price_eod_light",
            apikey=api_key,
            symbol="AAPL",
            from_date="2024-01-01",
            to_date="2024-01-10",
        )

        data_points = get_response_models(result, FMPHistoricalDataPointLight)
        validate_model_list(data_points, FMPHistoricalDataPointLight)
        assert len(data_points) > 1

        dates = [point.date for point in data_points]

        # Check if dates are in order (either ascending or descending)
        is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
        is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

        assert is_ascending or is_descending, "Dates should be in chronological order"


class TestHistoricalPriceEODFull:
    """Test class for historical EOD full data functionality."""

    def test_historical_price_eod_full_basic(self, api_key):
        """Test basic historical EOD full data retrieval."""
        result, validation = handle_api_call_with_validation(
            historical_price_eod, "historical_price_eod", apikey=api_key, symbol="AAPL"
        )

        data_points = get_response_models(result, FMPHistoricalDataPointFull)
        validate_model_list(data_points, FMPHistoricalDataPointFull)
        assert len(data_points) > 0

        # Validate first item has OHLCV data with business logic
        first_point = data_points[0]
        assert first_point.symbol == "AAPL"
        assert first_point.date is not None, "Date should not be None"
        assert (
            first_point.open is not None and first_point.open > 0
        ), "Open price should be positive"
        assert (
            first_point.high is not None and first_point.high > 0
        ), "High price should be positive"
        assert (
            first_point.low is not None and first_point.low > 0
        ), "Low price should be positive"
        assert (
            first_point.close is not None and first_point.close > 0
        ), "Close price should be positive"
        assert (
            first_point.volume is not None and first_point.volume >= 0
        ), "Volume should be non-negative"

        # OHLC relationships should be valid
        assert first_point.high >= first_point.open, "High should be >= open"
        assert first_point.high >= first_point.close, "High should be >= close"
        assert first_point.low <= first_point.open, "Low should be <= open"
        assert first_point.low <= first_point.close, "Low should be <= close"

    def test_historical_price_eod_full_vs_light_consistency(self, api_key):
        """Test consistency between full and light historical data."""
        symbol = "AAPL"
        from_date = "2024-01-01"
        to_date = "2024-01-05"

        # Get both full and light data
        full_result, validation = handle_api_call_with_validation(
            historical_price_eod,
            "historical_price_eod",
            apikey=api_key,
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
        )
        light_result, validation = handle_api_call_with_validation(
            historical_price_eod_light,
            "historical_price_eod_light",
            apikey=api_key,
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
        )

        full_data = get_response_models(full_result, FMPHistoricalDataPointFull)
        light_data = get_response_models(light_result, FMPHistoricalDataPointLight)
        validate_model_list(full_data, FMPHistoricalDataPointFull)
        validate_model_list(light_data, FMPHistoricalDataPointLight)

        assert len(full_data) == len(
            light_data
        ), "Full and light data should have same number of records"

        # Compare first few records
        for i in range(min(3, len(full_data))):
            full_point = full_data[i]
            light_point = light_data[i]

            assert (
                full_point.date == light_point.date
            ), f"Dates should match for record {i}"
            assert (
                abs(full_point.close - light_point.price) < 0.01
            ), f"Close price should match light price for record {i}"

    def test_historical_price_eod_full_high_volume_stocks(self, api_key):
        """Test historical EOD data for high volume stocks."""
        high_volume_symbols = ["AAPL", "MSFT", "SPY", "QQQ"]

        for symbol in high_volume_symbols:
            result, validation = handle_api_call_with_validation(
                historical_price_eod,
                "historical_price_eod",
                apikey=api_key,
                symbol=symbol,
                from_date="2024-01-01",
                to_date="2024-01-03",
            )

            data_points = get_response_models(result, FMPHistoricalDataPointFull)
            validate_model_list(data_points, FMPHistoricalDataPointFull)
            assert len(data_points) > 0, f"Should have data for {symbol}"

            for point in data_points:
                assert point.volume > 0, f"Volume should be positive for {symbol}"
                assert point.close > 0, f"Close price should be positive for {symbol}"


class TestHistoricalPriceAdjustments:
    """Test class for price adjustment functionality."""

    def test_historical_price_non_split_adjusted(self, api_key):
        """Test non-split adjusted historical data."""
        # Use a symbol that has had stock splits
        symbol = "AAPL"  # Apple has had multiple stock splits

        result = historical_price_eod_non_split_adjusted(
            apikey=api_key, symbol=symbol, from_date="2020-01-01", to_date="2020-12-31"
        )

        data_points = get_response_models(result, FMPHistoricalDataPointFull)
        validate_model_list(data_points, FMPHistoricalDataPointFull)
        assert len(data_points) > 0

        # Validate structure
        first_point = data_points[0]
        assert first_point.symbol == symbol
        assert first_point.date is not None
        # Note: Some adjusted endpoints may return None for OHLC fields
        # Just ensure we have symbol, date, and volume data
        assert first_point.volume is not None and first_point.volume >= 0

    def test_historical_price_dividend_adjusted(self, api_key):
        """Test dividend adjusted historical data."""
        # Use a symbol that pays regular dividends
        symbol = "KO"  # Coca-Cola pays regular dividends

        result = historical_price_eod_dividend_adjusted(
            apikey=api_key, symbol=symbol, from_date="2024-01-01", to_date="2024-03-31"
        )

        data_points = get_response_models(result, FMPHistoricalDataPointFull)
        validate_model_list(data_points, FMPHistoricalDataPointFull)
        assert len(data_points) > 0

        # Validate structure
        first_point = data_points[0]
        assert first_point.symbol == symbol
        assert first_point.date is not None
        # Note: Some adjusted endpoints may return None for OHLC fields
        # Just ensure we have symbol, date, and volume data
        assert first_point.volume is not None and first_point.volume >= 0

    def test_adjustment_comparison(self, api_key):
        """Compare regular vs adjusted prices."""
        symbol = "AAPL"
        from_date = "2023-01-01"
        to_date = "2023-12-31"

        # Get regular and non-split adjusted data
        regular_result = historical_price_eod(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )
        non_split_result = historical_price_eod_non_split_adjusted(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )

        regular_data = get_response_models(regular_result, FMPHistoricalDataPointFull)
        non_split_data = get_response_models(
            non_split_result, FMPHistoricalDataPointFull
        )
        validate_model_list(regular_data, FMPHistoricalDataPointFull)
        validate_model_list(non_split_data, FMPHistoricalDataPointFull)

        assert len(regular_data) > 0
        assert len(non_split_data) > 0

        # Both should have data for the same dates
        assert len(regular_data) == len(non_split_data)


class TestHistoricalChart:
    """Test class for intraday historical chart functionality."""

    def test_historical_chart_valid_intervals(self, api_key):
        """Test historical chart with all valid intervals."""
        valid_intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour"]
        symbol = "AAPL"

        for interval in valid_intervals:
            result = historical_chart(symbol=symbol, interval=interval, apikey=api_key)

            data_points = get_response_models(result, FMPIntradayDataPoint)
            validate_model_list(data_points, FMPIntradayDataPoint)

            # Intraday data might be limited, but structure should be valid
            if len(data_points) > 0:
                first_point = data_points[0]
                assert first_point.date is not None
                assert first_point.open > 0
                assert first_point.high > 0
                assert first_point.low > 0
                assert first_point.close > 0
                assert first_point.volume >= 0

                # OHLC relationships should be valid
                assert first_point.high >= first_point.open
                assert first_point.high >= first_point.close
                assert first_point.low <= first_point.open
                assert first_point.low <= first_point.close

    def test_historical_chart_invalid_interval(self, api_key):
        """Test historical chart with invalid interval."""
        with pytest.raises(ValueError, match="Invalid interval"):
            historical_chart(symbol="AAPL", interval="invalid", apikey=api_key)

    def test_historical_chart_different_symbols(self, api_key):
        """Test historical chart for different types of symbols."""
        test_symbols = ["AAPL", "SPY", "QQQ"]
        interval = "1hour"

        for symbol in test_symbols:
            result = historical_chart(symbol=symbol, interval=interval, apikey=api_key)
            data_points = get_response_models(result, FMPIntradayDataPoint)
            validate_model_list(data_points, FMPIntradayDataPoint)

            # Validate structure if data is available
            if len(data_points) > 0:
                first_point = data_points[0]
                assert (
                    first_point.open > 0
                ), f"Open price should be positive for {symbol}"
                assert (
                    first_point.close > 0
                ), f"Close price should be positive for {symbol}"

    def test_historical_chart_data_chronology(self, api_key):
        """Test that intraday data is in chronological order."""
        result = historical_chart(symbol="AAPL", interval="1hour", apikey=api_key)
        data_points = get_response_models(result, FMPIntradayDataPoint)
        validate_model_list(data_points, FMPIntradayDataPoint)

        if len(data_points) > 1:
            dates = [point.date for point in data_points]

            # Check if dates are in order (either ascending or descending)
            is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
            is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

            assert (
                is_ascending or is_descending
            ), "Intraday data should be in chronological order"


class TestChartErrorHandling:
    """Test class for chart error handling."""

    def test_historical_price_invalid_symbol(self, api_key):
        """Test historical price with invalid symbol."""
        result = historical_price_eod_light(apikey=api_key, symbol="INVALID_XYZ")

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data_points = get_response_models(result, FMPHistoricalDataPointLight)
            validate_model_list(data_points, FMPHistoricalDataPointLight, min_count=0)
            # Empty list is acceptable for invalid symbols

    def test_historical_price_invalid_api_key(self):
        """Test historical price with invalid API key."""
        from fmpsdk.exceptions import InvalidAPIKeyException

        with pytest.raises(InvalidAPIKeyException):
            historical_price_eod_light(apikey="invalid_key", symbol="AAPL")

    def test_historical_price_invalid_date_format(self, api_key):
        """Test historical price with invalid date format."""
        # This should still work or return an error gracefully
        result = historical_price_eod_light(
            apikey=api_key, symbol="AAPL", from_date="invalid-date"
        )

        # Should handle gracefully
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data_points = get_response_models(result, FMPHistoricalDataPointLight)
            validate_model_list(data_points, FMPHistoricalDataPointLight)

    def test_historical_chart_invalid_symbol(self, api_key):
        """Test historical chart with invalid symbol."""
        result = historical_chart(
            symbol="INVALID_XYZ", interval="1hour", apikey=api_key
        )

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data_points = get_response_models(result, FMPIntradayDataPoint)
            validate_model_list(data_points, FMPIntradayDataPoint, min_count=0)


class TestChartDataConsistency:
    """Test class for chart data consistency validation."""

    def test_different_timeframe_consistency(self, api_key):
        """Test consistency across different historical timeframes."""
        symbol = "AAPL"

        # Get 1 month of data
        one_month_result = historical_price_eod_light(
            apikey=api_key, symbol=symbol, from_date="2024-01-01", to_date="2024-01-31"
        )

        # Get 1 week of data within that month
        one_week_result = historical_price_eod_light(
            apikey=api_key, symbol=symbol, from_date="2024-01-15", to_date="2024-01-19"
        )

        month_data = get_response_models(one_month_result, FMPHistoricalDataPointLight)
        week_data = get_response_models(one_week_result, FMPHistoricalDataPointLight)
        validate_model_list(month_data, FMPHistoricalDataPointLight)
        validate_model_list(week_data, FMPHistoricalDataPointLight)

        assert len(month_data) > len(
            week_data
        ), "Month data should have more records than week data"

        # Week data should be subset of month data
        month_dates = {point.date for point in month_data}
        week_dates = {point.date for point in week_data}

        assert week_dates.issubset(
            month_dates
        ), "Week dates should be subset of month dates"

    def test_price_data_reasonableness(self, api_key):
        """Test that price data values are reasonable."""
        result = historical_price_eod(
            apikey=api_key, symbol="AAPL", from_date="2024-01-01", to_date="2024-01-05"
        )

        data_points = get_response_models(result, FMPHistoricalDataPointFull)
        validate_model_list(data_points, FMPHistoricalDataPointFull)
        assert len(data_points) > 0

        for point in data_points:
            # Price reasonableness checks
            assert (
                0 < point.low <= point.high
            ), f"Low {point.low} should be positive and <= high {point.high}"
            assert (
                point.low <= point.open <= point.high
            ), f"Open {point.open} should be between low {point.low} and high {point.high}"
            assert (
                point.low <= point.close <= point.high
            ), f"Close {point.close} should be between low {point.low} and high {point.high}"
            assert point.volume >= 0, f"Volume {point.volume} should be non-negative"

            # Daily price movement should be reasonable (less than 50% typically)
            daily_range = (point.high - point.low) / point.low
            assert (
                daily_range < 0.5
            ), f"Daily price range {daily_range:.2%} seems unreasonably large"

    def test_volume_consistency(self, api_key):
        """Test volume data consistency across endpoints."""
        symbol = "SPY"  # High volume ETF
        from_date = "2024-01-02"
        to_date = "2024-01-02"

        # Get light and full data for same date
        light_result = historical_price_eod_light(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )
        full_result = historical_price_eod(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )

        light_data = get_response_models(light_result, FMPHistoricalDataPointLight)
        full_data = get_response_models(full_result, FMPHistoricalDataPointFull)
        validate_model_list(light_data, FMPHistoricalDataPointLight)
        validate_model_list(full_data, FMPHistoricalDataPointFull)

        if len(light_data) > 0 and len(full_data) > 0:
            assert (
                light_data[0].volume == full_data[0].volume
            ), "Volume should match between light and full data"

    @pytest.mark.parametrize(
        "symbol,date_range_days,data_points_expected,asset_class",
        [
            ("AAPL", 30, 20, "large_cap_tech"),  # ~20 trading days in a month
            ("MSFT", 60, 40, "large_cap_tech"),  # ~40 trading days in 2 months
            ("GOOGL", 90, 60, "large_cap_tech"),  # ~60 trading days in 3 months
            ("JPM", 30, 20, "financial"),  # Major bank
            ("JNJ", 60, 40, "healthcare"),  # Healthcare blue chip
            ("XOM", 90, 60, "energy"),  # Energy sector
            ("WMT", 30, 20, "consumer_staples"),  # Retail
            ("TSLA", 60, 40, "electric_vehicle"),  # High volatility stock
            ("SPY", 30, 20, "etf_broad_market"),  # S&P 500 ETF
            ("QQQ", 60, 40, "etf_tech"),  # NASDAQ ETF
            ("IWM", 90, 60, "etf_small_cap"),  # Russell 2000 ETF
            ("VTI", 30, 20, "etf_total_market"),  # Total stock market ETF
            ("BTCUSD", 30, 30, "cryptocurrency"),  # Bitcoin (trades 24/7)
            ("ETHUSD", 60, 60, "cryptocurrency"),  # Ethereum (trades 24/7)
            ("EURUSD", 30, 30, "forex"),  # Euro/USD (trades 24/5)
            ("GBPUSD", 60, 60, "forex"),  # GBP/USD (trades 24/5)
            ("GCUSD", 30, 30, "commodity"),  # Gold (trades 24/5)
            ("BZUSD", 60, 60, "commodity"),  # Brent Oil (trades 24/5)
        ],
    )
    def test_historical_price_eod_light_comprehensive_assets(
        self, api_key, symbol, date_range_days, data_points_expected, asset_class
    ):
        """Test historical EOD light data across comprehensive asset classes with varying date ranges."""
        from_date = (datetime.now() - timedelta(days=date_range_days)).strftime(
            "%Y-%m-%d"
        )
        to_date = datetime.now().strftime("%Y-%m-%d")

        result = historical_price_eod_light(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )

        data_points = get_response_models(result, FMPHistoricalDataPointLight)
        validate_model_list(data_points, FMPHistoricalDataPointLight)
        assert (
            len(data_points) > 0
        ), f"Should have data for {asset_class} asset {symbol}"

        # Flexible data point validation (markets have holidays, weekends, etc.)
        min_expected = int(data_points_expected * 0.7)  # Allow 30% variance
        max_expected = int(data_points_expected * 1.3)  # Allow 30% variance

        # For 24/7 markets (crypto), expect more data points
        if asset_class == "cryptocurrency":
            min_expected = date_range_days - 5  # Account for potential gaps
        elif asset_class in ["forex", "commodity"]:
            min_expected = int(date_range_days * 0.8)  # Account for weekends

        assert (
            min_expected <= len(data_points) <= max_expected
        ), f"{symbol} ({asset_class}) should have {min_expected}-{max_expected} data points for {date_range_days} days, got {len(data_points)}"

        first_point = data_points[0]
        assert (
            first_point.symbol == symbol
        ), f"Symbol should match for {asset_class} asset"
        assert (
            first_point.price > 0
        ), f"Price should be positive for {asset_class} asset {symbol}"
        assert (
            first_point.date is not None
        ), f"Date should be present for {asset_class} asset {symbol}"

        # Validate date range
        for point in data_points:
            assert (
                from_date <= point.date <= to_date
            ), f"Date should be within range for {symbol}"

        # Asset class specific validations
        if asset_class == "large_cap_tech":
            # Tech stocks should have reasonable price ranges
            assert (
                10 <= first_point.price <= 1000
            ), f"Tech stock {symbol} price should be reasonable"
        elif asset_class == "cryptocurrency":
            # Crypto should have higher prices typically
            assert (
                first_point.price > 100
            ), f"Major crypto {symbol} should have substantial price"
        elif asset_class.startswith("etf_"):
            # ETFs should have reasonable price ranges
            assert (
                10 <= first_point.price <= 1000
            ), f"ETF {symbol} price should be reasonable"
        elif asset_class == "forex":
            # Forex pairs should be around 0.5-2.0 range typically
            assert (
                0.3 <= first_point.price <= 5.0
            ), f"Forex pair {symbol} should be in normal range"

    @pytest.mark.parametrize(
        "time_period,symbol_set,expected_patterns",
        [
            ("1_week", ["AAPL", "SPY"], {"trading_days": 5, "pattern": "recent"}),
            ("1_month", ["MSFT", "QQQ"], {"trading_days": 22, "pattern": "short_term"}),
            (
                "1_quarter",
                ["GOOGL", "IWM"],
                {"trading_days": 65, "pattern": "medium_term"},
            ),
            (
                "6_months",
                ["AMZN", "VTI"],
                {"trading_days": 130, "pattern": "longer_term"},
            ),
            ("1_year", ["TSLA", "SPY"], {"trading_days": 250, "pattern": "annual"}),
            (
                "2_years",
                ["NVDA", "QQQ"],
                {"trading_days": 500, "pattern": "multi_year"},
            ),
        ],
    )
    def test_historical_price_eod_light_time_periods(
        self, api_key, time_period, symbol_set, expected_patterns
    ):
        """Test historical EOD data across different time periods and patterns."""
        # Calculate date ranges based on time period
        period_days = {
            "1_week": 7,
            "1_month": 30,
            "1_quarter": 90,
            "6_months": 180,
            "1_year": 365,
            "2_years": 730,
        }

        days_back = period_days[time_period]
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        for symbol in symbol_set:
            result = historical_price_eod_light(
                apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
            )

            data_points = get_response_models(result, FMPHistoricalDataPointLight)
            validate_model_list(data_points, FMPHistoricalDataPointLight)
            assert (
                len(data_points) > 0
            ), f"Should have data for {symbol} over {time_period}"

            # Validate data point count is reasonable for the time period
            expected_trading_days = expected_patterns["trading_days"]
            min_expected = int(
                expected_trading_days * 0.6
            )  # Account for holidays/weekends
            max_expected = int(expected_trading_days * 1.2)  # Account for variations

            assert (
                min_expected <= len(data_points) <= max_expected
            ), f"{symbol} over {time_period} should have {min_expected}-{max_expected} data points, got {len(data_points)}"

            # Validate chronological ordering
            dates = [point.date for point in data_points]
            is_ordered = all(
                dates[i] >= dates[i + 1] for i in range(len(dates) - 1)
            ) or all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
            assert (
                is_ordered
            ), f"Dates should be chronologically ordered for {symbol} over {time_period}"

            # Validate price consistency (no zero or negative prices)
            prices = [point.price for point in data_points]
            assert all(
                price > 0 for price in prices
            ), f"All prices should be positive for {symbol}"

            # Pattern-specific validations
            if expected_patterns["pattern"] == "recent":
                # Recent data should be very current
                latest_date = max(dates)
                days_old = (
                    datetime.now() - datetime.strptime(latest_date, "%Y-%m-%d")
                ).days
                assert days_old <= 5, f"Recent data for {symbol} should be very current"
            elif expected_patterns["pattern"] == "multi_year":
                # Multi-year data should span significant time
                date_range = (
                    datetime.strptime(max(dates), "%Y-%m-%d")
                    - datetime.strptime(min(dates), "%Y-%m-%d")
                ).days
                assert (
                    date_range >= 600
                ), f"Multi-year data for {symbol} should span significant time"
