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
from tests.conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper function to safely get field value from dict or model."""
    if isinstance(item, dict):
        return item.get(field_name)
    else:
        return getattr(item, field_name, None)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestHistoricalPriceEODLight:
    """Test class for historical EOD light data functionality."""

    def test_historical_price_eod_light_basic(self, api_key):
        """Test basic historical EOD light data retrieval."""
        result = historical_price_eod_light(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first item
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPHistoricalDataPointLight.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.date is not None
        assert validated.price > 0
        assert validated.volume >= 0

    def test_historical_price_eod_light_with_date_range(self, api_key):
        """Test historical EOD light data with specific date range."""
        from_date = "2024-01-01"
        to_date = "2024-01-31"

        result = historical_price_eod_light(
            apikey=api_key, symbol="AAPL", from_date=from_date, to_date=to_date
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate date range
        for item in result_list:
            date_value = get_field_value(item, "date")
            assert from_date <= date_value <= to_date

    def test_historical_price_eod_light_multiple_asset_types(
        self, api_key, test_symbols
    ):
        """Test historical EOD light data for different asset types."""
        test_cases = [
            ("large_cap", "AAPL", "stock"),
            ("etf", "SPY", "ETF"),
            ("crypto", "BTCUSD", "cryptocurrency"),
            ("forex", "EURUSD", "forex pair"),
            ("commodity", "GCUSD", "commodity"),
        ]

        for asset_category, symbol, asset_name in test_cases:
            if symbol in test_symbols[asset_category]:
                result = historical_price_eod_light(apikey=api_key, symbol=symbol)
                result_list = extract_data_list(result)

                assert isinstance(
                    result_list, list
                ), f"Result should be list for {asset_name}"
                assert (
                    len(result_list) > 0
                ), f"Should have data for {asset_name} {symbol}"

                first_item = result_list[0]
                symbol_value = get_field_value(first_item, "symbol")
                price_value = get_field_value(first_item, "price")

                assert symbol_value == symbol, f"Symbol should match for {asset_name}"
                assert price_value > 0, f"Price should be positive for {asset_name}"

    def test_historical_price_eod_light_chronological_order(self, api_key):
        """Test that historical data is returned in chronological order."""
        result = historical_price_eod_light(
            apikey=api_key, symbol="AAPL", from_date="2024-01-01", to_date="2024-01-10"
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 1

        dates = [get_field_value(item, "date") for item in result_list]

        # Check if dates are in order (either ascending or descending)
        is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
        is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

        assert is_ascending or is_descending, "Dates should be in chronological order"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestHistoricalPriceEODFull:
    """Test class for historical EOD full data functionality."""

    def test_historical_price_eod_full_basic(self, api_key):
        """Test basic historical EOD full data retrieval."""
        result = historical_price_eod(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate first item has OHLCV data
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPHistoricalDataPointFull.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == "AAPL"
        assert validated.date is not None
        assert validated.open is not None and validated.open > 0
        assert validated.high is not None and validated.high > 0
        assert validated.low is not None and validated.low > 0
        assert validated.close is not None and validated.close > 0
        assert validated.volume is not None and validated.volume >= 0

        # OHLC relationships should be valid
        assert validated.high >= validated.open
        assert validated.high >= validated.close
        assert validated.low <= validated.open
        assert validated.low <= validated.close

    def test_historical_price_eod_full_vs_light_consistency(self, api_key):
        """Test consistency between full and light historical data."""
        symbol = "AAPL"
        from_date = "2024-01-01"
        to_date = "2024-01-05"

        # Get both full and light data
        full_result = historical_price_eod(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )
        light_result = historical_price_eod_light(
            apikey=api_key, symbol=symbol, from_date=from_date, to_date=to_date
        )

        full_list = extract_data_list(full_result)
        light_list = extract_data_list(light_result)

        assert len(full_list) == len(
            light_list
        ), "Full and light data should have same number of records"

        # Compare first few records
        for i in range(min(3, len(full_list))):
            full_item = full_list[i]
            light_item = light_list[i]

            full_date = get_field_value(full_item, "date")
            light_date = get_field_value(light_item, "date")
            full_close = get_field_value(full_item, "close")
            light_price = get_field_value(light_item, "price")

            assert full_date == light_date, f"Dates should match for record {i}"
            assert (
                abs(full_close - light_price) < 0.01
            ), f"Close price should match light price for record {i}"

    def test_historical_price_eod_full_high_volume_stocks(self, api_key):
        """Test historical EOD data for high volume stocks."""
        high_volume_symbols = ["AAPL", "MSFT", "SPY", "QQQ"]

        for symbol in high_volume_symbols:
            result = historical_price_eod(
                apikey=api_key,
                symbol=symbol,
                from_date="2024-01-01",
                to_date="2024-01-03",
            )

            result_list = extract_data_list(result)
            assert len(result_list) > 0, f"Should have data for {symbol}"

            for item in result_list:
                volume_value = get_field_value(item, "volume")
                close_value = get_field_value(item, "close")

                assert volume_value > 0, f"Volume should be positive for {symbol}"
                assert close_value > 0, f"Close price should be positive for {symbol}"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestHistoricalPriceAdjustments:
    """Test class for price adjustment functionality."""

    def test_historical_price_non_split_adjusted(self, api_key):
        """Test non-split adjusted historical data."""
        # Use a symbol that has had stock splits
        symbol = "AAPL"  # Apple has had multiple stock splits

        result = historical_price_eod_non_split_adjusted(
            apikey=api_key, symbol=symbol, from_date="2020-01-01", to_date="2020-12-31"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate structure
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPHistoricalDataPointFull.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == symbol
        assert validated.date is not None
        # Note: Some adjusted endpoints may return None for OHLC fields
        # Just ensure we have symbol, date, and volume data
        assert validated.volume is not None and validated.volume >= 0

    def test_historical_price_dividend_adjusted(self, api_key):
        """Test dividend adjusted historical data."""
        # Use a symbol that pays regular dividends
        symbol = "KO"  # Coca-Cola pays regular dividends

        result = historical_price_eod_dividend_adjusted(
            apikey=api_key, symbol=symbol, from_date="2024-01-01", to_date="2024-03-31"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        # Validate structure
        first_item = result_list[0]
        if isinstance(first_item, dict):
            validated = FMPHistoricalDataPointFull.model_validate(first_item)
        else:
            validated = first_item

        assert validated.symbol == symbol
        assert validated.date is not None
        # Note: Some adjusted endpoints may return None for OHLC fields
        # Just ensure we have symbol, date, and volume data
        assert validated.volume is not None and validated.volume >= 0

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

        regular_list = extract_data_list(regular_result)
        non_split_list = extract_data_list(non_split_result)

        assert len(regular_list) > 0
        assert len(non_split_list) > 0

        # Both should have data for the same dates
        assert len(regular_list) == len(non_split_list)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestHistoricalChart:
    """Test class for intraday historical chart functionality."""

    def test_historical_chart_valid_intervals(self, api_key):
        """Test historical chart with all valid intervals."""
        valid_intervals = ["1min", "5min", "15min", "30min", "1hour", "4hour"]
        symbol = "AAPL"

        for interval in valid_intervals:
            result = historical_chart(symbol=symbol, interval=interval, apikey=api_key)

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for {interval}"

            # Intraday data might be limited, but structure should be valid
            if len(result_list) > 0:
                first_item = result_list[0]
                if isinstance(first_item, dict):
                    validated = FMPIntradayDataPoint.model_validate(first_item)
                else:
                    validated = first_item

                assert validated.date is not None
                assert validated.open > 0
                assert validated.high > 0
                assert validated.low > 0
                assert validated.close > 0
                assert validated.volume >= 0

                # OHLC relationships should be valid
                assert validated.high >= validated.open
                assert validated.high >= validated.close
                assert validated.low <= validated.open
                assert validated.low <= validated.close

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
            result_list = extract_data_list(result)

            assert isinstance(result_list, list), f"Result should be list for {symbol}"

            # Validate structure if data is available
            if len(result_list) > 0:
                first_item = result_list[0]
                open_value = get_field_value(first_item, "open")
                close_value = get_field_value(first_item, "close")

                assert open_value > 0, f"Open price should be positive for {symbol}"
                assert close_value > 0, f"Close price should be positive for {symbol}"

    def test_historical_chart_data_chronology(self, api_key):
        """Test that intraday data is in chronological order."""
        result = historical_chart(symbol="AAPL", interval="1hour", apikey=api_key)
        result_list = extract_data_list(result)

        if len(result_list) > 1:
            dates = [get_field_value(item, "date") for item in result_list]

            # Check if dates are in order (either ascending or descending)
            is_ascending = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
            is_descending = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

            assert (
                is_ascending or is_descending
            ), "Intraday data should be in chronological order"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestChartErrorHandling:
    """Test class for chart error handling."""

    def test_historical_price_invalid_symbol(self, api_key):
        """Test historical price with invalid symbol."""
        result = historical_price_eod_light(apikey=api_key, symbol="INVALID_XYZ")

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            # Empty list is acceptable for invalid symbols

    def test_historical_price_invalid_api_key(self):
        """Test historical price with invalid API key."""
        result = historical_price_eod_light(apikey="invalid_key", symbol="AAPL")

        # Should return error response
        assert isinstance(result, dict)
        assert "Error Message" in result

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
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

    def test_historical_chart_invalid_symbol(self, api_key):
        """Test historical chart with invalid symbol."""
        result = historical_chart(
            symbol="INVALID_XYZ", interval="1hour", apikey=api_key
        )

        # Should return empty list or error response
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
class TestChartResponseTimes:
    """Test class for chart response time validation."""

    def test_historical_price_response_time(self, api_key, test_config):
        """Test that historical price responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = historical_price_eod_light(apikey=api_key, symbol="AAPL")
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"

    def test_historical_chart_response_time(self, api_key, test_config):
        """Test that historical chart responses are within acceptable time limits."""
        import time

        start_time = time.time()
        result = historical_chart(symbol="AAPL", interval="1hour", apikey=api_key)
        response_time = time.time() - start_time

        assert result is not None
        assert (
            response_time < test_config["max_response_time"]
        ), f"Response time {response_time:.2f}s should be under {test_config['max_response_time']}s"


@pytest.mark.integration
@pytest.mark.requires_api_key
@pytest.mark.live_data
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

        month_list = extract_data_list(one_month_result)
        week_list = extract_data_list(one_week_result)

        assert len(month_list) > len(
            week_list
        ), "Month data should have more records than week data"

        # Week data should be subset of month data
        month_dates = {get_field_value(item, "date") for item in month_list}
        week_dates = {get_field_value(item, "date") for item in week_list}

        assert week_dates.issubset(
            month_dates
        ), "Week dates should be subset of month dates"

    def test_price_data_reasonableness(self, api_key):
        """Test that price data values are reasonable."""
        result = historical_price_eod(
            apikey=api_key, symbol="AAPL", from_date="2024-01-01", to_date="2024-01-05"
        )

        result_list = extract_data_list(result)
        assert len(result_list) > 0

        for item in result_list:
            open_val = get_field_value(item, "open")
            high_val = get_field_value(item, "high")
            low_val = get_field_value(item, "low")
            close_val = get_field_value(item, "close")
            volume_val = get_field_value(item, "volume")

            # Price reasonableness checks
            assert (
                0 < low_val <= high_val
            ), f"Low {low_val} should be positive and <= high {high_val}"
            assert (
                low_val <= open_val <= high_val
            ), f"Open {open_val} should be between low {low_val} and high {high_val}"
            assert (
                low_val <= close_val <= high_val
            ), f"Close {close_val} should be between low {low_val} and high {high_val}"
            assert volume_val >= 0, f"Volume {volume_val} should be non-negative"

            # Daily price movement should be reasonable (less than 50% typically)
            daily_range = (high_val - low_val) / low_val
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

        light_list = extract_data_list(light_result)
        full_list = extract_data_list(full_result)

        if len(light_list) > 0 and len(full_list) > 0:
            light_volume = get_field_value(light_list[0], "volume")
            full_volume = get_field_value(full_list[0], "volume")

            assert (
                light_volume == full_volume
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
            ("CLUSD", 60, 60, "commodity"),  # Oil (trades 24/5)
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

        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), f"Result should be list for {asset_class} asset {symbol}"
        assert (
            len(result_list) > 0
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
            min_expected <= len(result_list) <= max_expected
        ), f"{symbol} ({asset_class}) should have {min_expected}-{max_expected} data points for {date_range_days} days, got {len(result_list)}"

        first_item = result_list[0]
        symbol_value = get_field_value(first_item, "symbol")
        price_value = get_field_value(first_item, "price")
        date_value = get_field_value(first_item, "date")

        assert symbol_value == symbol, f"Symbol should match for {asset_class} asset"
        assert (
            price_value > 0
        ), f"Price should be positive for {asset_class} asset {symbol}"
        assert (
            date_value is not None
        ), f"Date should be present for {asset_class} asset {symbol}"

        # Validate date range
        for item in result_list:
            item_date = get_field_value(item, "date")
            assert (
                from_date <= item_date <= to_date
            ), f"Date should be within range for {symbol}"

        # Asset class specific validations
        if asset_class == "large_cap_tech":
            # Tech stocks should have reasonable price ranges
            assert (
                10 <= price_value <= 1000
            ), f"Tech stock {symbol} price should be reasonable"
        elif asset_class == "cryptocurrency":
            # Crypto should have higher prices typically
            assert (
                price_value > 100
            ), f"Major crypto {symbol} should have substantial price"
        elif asset_class.startswith("etf_"):
            # ETFs should have reasonable price ranges
            assert 10 <= price_value <= 1000, f"ETF {symbol} price should be reasonable"
        elif asset_class == "forex":
            # Forex pairs should be around 0.5-2.0 range typically
            assert (
                0.3 <= price_value <= 5.0
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

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Result should be list for {time_period} period"
            assert (
                len(result_list) > 0
            ), f"Should have data for {symbol} over {time_period}"

            # Validate data point count is reasonable for the time period
            expected_trading_days = expected_patterns["trading_days"]
            min_expected = int(
                expected_trading_days * 0.6
            )  # Account for holidays/weekends
            max_expected = int(expected_trading_days * 1.2)  # Account for variations

            assert (
                min_expected <= len(result_list) <= max_expected
            ), f"{symbol} over {time_period} should have {min_expected}-{max_expected} data points, got {len(result_list)}"

            # Validate chronological ordering
            dates = [get_field_value(item, "date") for item in result_list]
            is_ordered = all(
                dates[i] >= dates[i + 1] for i in range(len(dates) - 1)
            ) or all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
            assert (
                is_ordered
            ), f"Dates should be chronologically ordered for {symbol} over {time_period}"

            # Validate price consistency (no zero or negative prices)
            prices = [get_field_value(item, "price") for item in result_list]
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
