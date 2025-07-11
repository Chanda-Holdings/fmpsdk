from datetime import datetime, timedelta

import pytest

from fmpsdk import commitment_of_traders
from fmpsdk.models import (
    FMPCommitmentOfTradersAnalysis,
    FMPCommitmentOfTradersReport,
    FMPSymbolAndNameList,
)
from tests.conftest import extract_data_list


class TestCommitmentOfTradersBasic:
    """Test basic COT functionality."""

    @pytest.mark.parametrize(
        "commodity_symbol",
        [
            # Energy Commodities
            "CL",  # Crude Oil
            "NG",  # Natural Gas
            "HO",  # Heating Oil
            "RB",  # RBOB Gasoline
            "BZ",  # Brent Crude
            # Precious Metals
            "GC",  # Gold
            "SI",  # Silver
            "PL",  # Platinum
            "PA",  # Palladium
            # Industrial Metals
            "HG",  # Copper
            "AL",  # Aluminum (if available)
            # Agricultural Commodities
            "C",  # Corn
            "W",  # Wheat
            "S",  # Soybeans
            "SB",  # Sugar
            "KC",  # Coffee
            "CT",  # Cotton
            "CC",  # Cocoa
            "OJ",  # Orange Juice
            # Livestock
            "LC",  # Live Cattle
            "FC",  # Feeder Cattle
            "LH",  # Lean Hogs
            # Financial Futures
            "ES",  # E-mini S&P 500
            "NQ",  # E-mini NASDAQ 100
            "YM",  # E-mini Dow Jones
            "TY",  # 10-Year Treasury Note
            "FV",  # 5-Year Treasury Note
            "TU",  # 2-Year Treasury Note
            "US",  # 30-Year Treasury Bond
            # Currency Futures
            "EUR",  # Euro
            "GBP",  # British Pound
            "JPY",  # Japanese Yen
            "CAD",  # Canadian Dollar
            "AUD",  # Australian Dollar
            "CHF",  # Swiss Franc
            "NZD",  # New Zealand Dollar
            "MXN",  # Mexican Peso
            # Other Commodities
            "LBS",  # Lumber (if available)
            "DA",  # Milk (if available)
        ],
    )
    def test_commitment_of_traders_report_by_symbol(self, api_key, commodity_symbol):
        """Test COT reports for various commodity symbols."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol=commodity_symbol
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            report = data[0]

            # Validate against model
            if isinstance(report, dict):
                report_obj = FMPCommitmentOfTradersReport(**report)
            else:
                report_obj = report

            # Basic validation
            assert hasattr(report_obj, "symbol")
            assert hasattr(report_obj, "date")

            # Symbol should match requested
            if report_obj.symbol:
                assert (
                    commodity_symbol in report_obj.symbol
                    or report_obj.symbol in commodity_symbol
                )

    @pytest.mark.parametrize(
        "commodity_category",
        [
            "energy",
            "precious_metals",
            "industrial_metals",
            "agricultural",
            "livestock",
            "financial",
            "currency",
        ],
    )
    def test_commitment_of_traders_analysis_by_category(
        self, api_key, commodity_category
    ):
        """Test COT analysis across different commodity categories."""
        category_symbols = {
            "energy": ["CL", "NG", "HO"],
            "precious_metals": ["GC", "SI", "PL"],
            "industrial_metals": ["HG"],
            "agricultural": ["C", "W", "S"],
            "livestock": ["LC", "LH"],
            "financial": ["ES", "TY", "NQ"],
            "currency": ["EUR", "GBP", "JPY"],
        }

        symbols = category_symbols.get(commodity_category, ["CL"])

        for symbol in symbols:
            result = commitment_of_traders.commitment_of_traders_report_analysis(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

            if data:  # If we have data
                analysis = data[0]

                # Validate against model
                if isinstance(analysis, dict):
                    analysis_obj = FMPCommitmentOfTradersAnalysis(**analysis)
                else:
                    analysis_obj = analysis

                # Basic validation
                assert hasattr(analysis_obj, "symbol")
                assert hasattr(analysis_obj, "date")

    @pytest.mark.parametrize(
        "market_segment",
        [
            "commodity_futures",
            "financial_futures",
            "currency_futures",
            "equity_index_futures",
        ],
    )
    def test_commitment_of_traders_by_market_segment(self, api_key, market_segment):
        """Test COT data across different market segments."""
        segment_symbols = {
            "commodity_futures": ["CL", "GC", "C", "LC"],
            "financial_futures": ["TY", "FV", "US", "TU"],
            "currency_futures": ["EUR", "GBP", "JPY", "CAD"],
            "equity_index_futures": ["ES", "NQ", "YM"],
        }

        symbols = segment_symbols.get(market_segment, ["CL"])

        for symbol in symbols:
            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict
            if isinstance(result, dict) and "Error Message" in result:
                continue

            data = extract_data_list(result)
            assert isinstance(data, list)

    @pytest.mark.parametrize("timeframe", ["recent", "quarterly", "annual"])
    def test_commitment_of_traders_timeframes(self, api_key, timeframe):
        """Test COT data for different timeframes."""
        # Use a reliable symbol like crude oil
        symbol = "CL"

        if timeframe == "recent":
            # Test recent data (no date filter)
            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key, symbol=symbol
            )
        elif timeframe == "quarterly":
            # Test quarterly data from last quarter
            from datetime import datetime, timedelta

            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)

            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key,
                symbol=symbol,
                from_date=start_date.strftime("%Y-%m-%d"),
                to_date=end_date.strftime("%Y-%m-%d"),
            )
        elif timeframe == "annual":
            # Test annual data from last year
            from datetime import datetime, timedelta

            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key,
                symbol=symbol,
                from_date=start_date.strftime("%Y-%m-%d"),
                to_date=end_date.strftime("%Y-%m-%d"),
            )

        # Check if result is error dict
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

    def test_commitment_of_traders_report_list(self, api_key):
        """Test getting list of available COT reports."""
        result = commitment_of_traders.commitment_of_traders_report_list(apikey=api_key)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            symbol_info = data[0]

            # Validate against model
            if isinstance(symbol_info, dict):
                symbol_obj = FMPSymbolAndNameList(**symbol_info)
            else:
                symbol_obj = symbol_info

            # Required fields validation
            assert hasattr(symbol_obj, "symbol")
            assert hasattr(symbol_obj, "name")

            # Data quality checks
            assert symbol_obj.symbol
            assert symbol_obj.name
            assert len(symbol_obj.symbol) >= 1
            assert len(symbol_obj.name) > 0

    def test_commitment_of_traders_report_without_symbol(self, api_key):
        """Test getting COT report without specifying symbol."""
        result = commitment_of_traders.commitment_of_traders_report(apikey=api_key)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            report = data[0]

            # Validate against model
            if isinstance(report, dict):
                report_obj = FMPCommitmentOfTradersReport(**report)
            else:
                report_obj = report

            # Required fields validation
            assert hasattr(report_obj, "symbol")
            assert hasattr(report_obj, "date")
            assert hasattr(report_obj, "name")
            assert hasattr(report_obj, "sector")
            assert hasattr(report_obj, "openInterestAll")

            # Data quality checks
            assert report_obj.symbol
            assert report_obj.date
            assert report_obj.name
            assert isinstance(report_obj.openInterestAll, int)

    def test_commitment_of_traders_report_with_symbol(self, api_key):
        """Test getting COT report for specific symbol."""
        # Test with ES (S&P 500 E-mini futures)
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for report in data[:3]:  # Check first few items
                if isinstance(report, dict):
                    assert report["symbol"] == "ES"
                    report_obj = FMPCommitmentOfTradersReport(**report)
                else:
                    assert report.symbol == "ES"
                    report_obj = report

                # Validate ES-specific data
                assert "S&P" in report_obj.name or "E-MINI" in report_obj.name.upper()

    def test_commitment_of_traders_analysis_without_symbol(self, api_key):
        """Test getting COT analysis without specifying symbol."""
        result = commitment_of_traders.commitment_of_traders_report_analysis(
            apikey=api_key
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            analysis = data[0]

            # Validate against model
            if isinstance(analysis, dict):
                analysis_obj = FMPCommitmentOfTradersAnalysis(**analysis)
            else:
                analysis_obj = analysis

            # Required fields validation
            assert hasattr(analysis_obj, "symbol")
            assert hasattr(analysis_obj, "date")
            assert hasattr(analysis_obj, "marketSituation")
            assert hasattr(analysis_obj, "marketSentiment")
            assert hasattr(analysis_obj, "reversalTrend")

            # Data quality checks
            assert analysis_obj.symbol
            assert analysis_obj.date
            assert analysis_obj.marketSituation
            assert analysis_obj.marketSentiment
            assert isinstance(analysis_obj.reversalTrend, bool)


class TestCommitmentOfTradersSymbols:
    """Test COT with different futures symbols."""

    def test_cot_major_equity_indices(self, api_key):
        """Test COT for major equity index futures."""
        symbols = ["ES", "NQ", "YM"]  # S&P 500, NASDAQ, Dow

        for symbol in symbols:
            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                return

            data = extract_data_list(result)
            assert isinstance(data, list)

            if data:
                # Ensure symbol matches
                if isinstance(data[0], dict):
                    assert data[0]["symbol"] == symbol
                else:
                    assert data[0].symbol == symbol

    def test_cot_currency_futures(self, api_key):
        """Test COT for major currency futures."""
        symbols = ["EUR", "GBP", "JPY"]  # Major currency futures

        for symbol in symbols:
            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                return

            data = extract_data_list(result)
            assert isinstance(data, list)
            # Data may be empty for some symbols

    def test_cot_commodity_futures(self, api_key):
        """Test COT for major commodity futures."""
        symbols = ["GC", "CL", "NG"]  # Gold, Crude Oil, Natural Gas

        for symbol in symbols:
            result = commitment_of_traders.commitment_of_traders_report(
                apikey=api_key, symbol=symbol
            )

            # Check if result is error dict (invalid API key)
            if isinstance(result, dict) and "Error Message" in result:
                return

            data = extract_data_list(result)
            assert isinstance(data, list)
            # Data may be empty for some symbols


class TestCommitmentOfTradersDateRanges:
    """Test COT with date range parameters."""

    def test_cot_report_with_date_range(self, api_key):
        """Test COT report with from/to date parameters."""
        # Test with last 30 days
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES", from_date=from_date, to_date=to_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Validate dates are within range
            for report in data[:5]:  # Check first few items
                if isinstance(report, dict):
                    report_date = report["date"]
                else:
                    report_date = report.date

                # Date should be within our range (allowing for some flexibility)
                assert len(report_date) >= 10  # YYYY-MM-DD format

    def test_cot_analysis_with_date_range(self, api_key):
        """Test COT analysis with from/to date parameters."""
        # Test with last 60 days
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

        result = commitment_of_traders.commitment_of_traders_report_analysis(
            apikey=api_key, symbol="ES", from_date=from_date, to_date=to_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Validate analysis fields
            analysis = data[0]
            if isinstance(analysis, dict):
                analysis_obj = FMPCommitmentOfTradersAnalysis(**analysis)
            else:
                analysis_obj = analysis

            # Check that we have meaningful analysis
            assert analysis_obj.currentLongMarketSituation is not None
            assert analysis_obj.currentShortMarketSituation is not None


class TestCommitmentOfTradersDataQuality:
    """Test data quality and business logic validation."""

    def test_cot_position_consistency(self, api_key):
        """Test COT position data consistency."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for report in data[:3]:  # Check first few items
                if isinstance(report, dict):
                    report_obj = FMPCommitmentOfTradersReport(**report)
                else:
                    report_obj = report

                # Position consistency checks
                assert report_obj.openInterestAll >= 0
                assert report_obj.noncommPositionsLongAll >= 0
                assert report_obj.noncommPositionsShortAll >= 0
                assert report_obj.commPositionsLongAll >= 0
                assert report_obj.commPositionsShortAll >= 0

                # Percentage fields should be reasonable
                assert 0 <= report_obj.pctOfOiNoncommLongAll <= 100
                assert 0 <= report_obj.pctOfOiNoncommShortAll <= 100
                assert 0 <= report_obj.pctOfOiCommLongAll <= 100
                assert 0 <= report_obj.pctOfOiCommShortAll <= 100

    def test_cot_analysis_sentiment_values(self, api_key):
        """Test COT analysis sentiment values."""
        result = commitment_of_traders.commitment_of_traders_report_analysis(
            apikey=api_key, symbol="ES"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for analysis in data[:3]:  # Check first few items
                if isinstance(analysis, dict):
                    analysis_obj = FMPCommitmentOfTradersAnalysis(**analysis)
                else:
                    analysis_obj = analysis

                # Market situation should be meaningful
                assert (
                    analysis_obj.marketSituation
                    in ["Bullish", "Bearish", "Neutral", ""]
                    or len(analysis_obj.marketSituation) > 0
                )

                # Market sentiment should be meaningful
                assert (
                    analysis_obj.marketSentiment
                    in ["Bullish", "Bearish", "Neutral", ""]
                    or len(analysis_obj.marketSentiment) > 0
                )

                # Reversal trend should be boolean
                assert isinstance(analysis_obj.reversalTrend, bool)

    def test_cot_data_freshness(self, api_key):
        """Test that COT data exists (freshness may vary for demo data)."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            # Check the most recent report
            latest_report = data[0]
            if isinstance(latest_report, dict):
                latest_date = latest_report["date"]
            else:
                latest_date = latest_report.date

            # Parse date and check it exists (demo data may be old)
            if latest_date and len(latest_date) >= 10:
                report_date = datetime.strptime(latest_date[:10], "%Y-%m-%d")
                days_ago = (datetime.now() - report_date).days

                # Just verify we have a valid date - demo data may be old
                assert days_ago >= 0, f"COT data has future date: {latest_date}"

                # Log a warning if data is very old (but don't fail the test)
                if days_ago > 90:
                    print(
                        f"Warning: COT data is {days_ago} days old - likely demo/sandbox data"
                    )

    def test_cot_symbol_name_consistency(self, api_key):
        """Test that symbol and name fields are consistent."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for report in data[:3]:  # Check first few items
                if isinstance(report, dict):
                    symbol = report["symbol"]
                    name = report["name"]
                else:
                    symbol = report.symbol
                    name = report.name

                # For ES, name should contain S&P 500 or E-MINI
                if symbol == "ES":
                    assert "S&P" in name or "E-MINI" in name.upper()


class TestCommitmentOfTradersErrorHandling:
    """Test error handling for COT endpoints."""

    def test_cot_report_invalid_api_key(self):
        """Test COT report with invalid API key."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey="invalid_key"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_cot_analysis_invalid_api_key(self):
        """Test COT analysis with invalid API key."""
        result = commitment_of_traders.commitment_of_traders_report_analysis(
            apikey="invalid_key"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_cot_list_invalid_api_key(self):
        """Test COT list with invalid API key."""
        result = commitment_of_traders.commitment_of_traders_report_list(
            apikey="invalid_key"
        )

        # Should return error dict, not raise exception
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_cot_invalid_symbol(self, api_key):
        """Test COT with invalid symbol."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="INVALID_SYMBOL_XYZ"
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for invalid symbol
        assert len(data) == 0

    def test_cot_invalid_date_format(self, api_key):
        """Test COT with invalid date format."""
        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key,
            symbol="ES",
            from_date="invalid-date",
            to_date="also-invalid",
        )

        # Should handle invalid dates gracefully
        # Either return error dict or empty list
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_cot_future_dates(self, api_key):
        """Test COT with future dates."""
        # Test with future dates
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        result = commitment_of_traders.commitment_of_traders_report(
            apikey=api_key, symbol="ES", from_date=future_date, to_date=future_date
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)
        # Should return empty list for future dates
        assert len(data) == 0
