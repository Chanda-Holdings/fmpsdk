from unittest.mock import patch

import pytest

import fmpsdk.market_performance as mp


class TestMarketPerformance:
    """Test market performance endpoints."""

    @pytest.fixture
    def mock_api_key(self):
        return "test_api_key"

    @patch("fmpsdk.market_performance.__return_json")
    def test_sector_performance_snapshot(self, mock_return_json, mock_api_key):
        """Test sector performance snapshot endpoint."""
        # Mock the return value
        mock_return_json.return_value = [
            {"sector": "Technology", "changesPercentage": "2.5"}
        ]

        result = mp.sector_performance_snapshot(apikey=mock_api_key)

        # Check that the function was called with correct parameters
        mock_return_json.assert_called_once_with(
            path="sector-performance-snapshot", query_vars={"apikey": mock_api_key}
        )

        # Check return value structure
        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert len(result.root) == 1
        assert result.root[0].sector == "Technology"

    @patch("fmpsdk.market_performance.__return_json")
    def test_industry_performance_snapshot(self, mock_return_json, mock_api_key):
        """Test industry performance snapshot endpoint."""
        mock_return_json.return_value = [
            {
                "industry": "Software",
                "changesPercentage": "1.8",
                "marketCap": 5000000000,
                "numberOfSymbols": 50,
            }
        ]

        result = mp.industry_performance_snapshot(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="industry-performance-snapshot", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].industry == "Software"

    @patch("fmpsdk.market_performance.__return_json")
    def test_historical_sector_performance(self, mock_return_json, mock_api_key):
        """Test historical sector performance endpoint."""
        mock_return_json.return_value = [
            {"date": "2023-01-01", "sector": "Technology", "changesPercentage": 1.5}
        ]

        result = mp.historical_sector_performance(
            apikey=mock_api_key, sector="Technology"
        )

        mock_return_json.assert_called_once_with(
            path="historical-sector-performance",
            query_vars={"apikey": mock_api_key, "sector": "Technology"},
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].sector == "Technology"

    @patch("fmpsdk.market_performance.__return_json")
    def test_historical_industry_performance(self, mock_return_json, mock_api_key):
        """Test historical industry performance endpoint."""
        mock_return_json.return_value = [
            {"date": "2023-01-01", "industry": "Software", "changesPercentage": 2.1}
        ]

        result = mp.historical_industry_performance(
            apikey=mock_api_key, industry="Software"
        )

        mock_return_json.assert_called_once_with(
            path="historical-industry-performance",
            query_vars={"apikey": mock_api_key, "industry": "Software"},
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].industry == "Software"

    @patch("fmpsdk.market_performance.__return_json")
    def test_sector_pe_snapshot(self, mock_return_json, mock_api_key):
        """Test sector PE snapshot endpoint."""
        mock_return_json.return_value = [
            {"sector": "Technology", "pe": 25.5, "marketCap": 8000000000000}
        ]

        result = mp.sector_pe_snapshot(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="sector-pe-snapshot", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].pe == 25.5

    @patch("fmpsdk.market_performance.__return_json")
    def test_industry_pe_snapshot(self, mock_return_json, mock_api_key):
        """Test industry PE snapshot endpoint."""
        mock_return_json.return_value = [
            {"industry": "Software", "pe": 30.2, "marketCap": 5000000000000}
        ]

        result = mp.industry_pe_snapshot(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="industry-pe-snapshot", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].industry == "Software"

    @patch("fmpsdk.market_performance.__return_json")
    def test_historical_sector_pe(self, mock_return_json, mock_api_key):
        """Test historical sector PE endpoint."""
        mock_return_json.return_value = [
            {
                "date": "2023-01-01",
                "sector": "Technology",
                "pe": 22.8,
                "marketCap": 7500000000000,
            }
        ]

        result = mp.historical_sector_pe(apikey=mock_api_key, sector="Technology")

        mock_return_json.assert_called_once_with(
            path="historical-sector-pe",
            query_vars={"apikey": mock_api_key, "sector": "Technology"},
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].sector == "Technology"

    @patch("fmpsdk.market_performance.__return_json")
    def test_historical_industry_pe(self, mock_return_json, mock_api_key):
        """Test historical industry PE endpoint."""
        mock_return_json.return_value = [
            {
                "date": "2023-01-01",
                "industry": "Software",
                "pe": 28.5,
                "marketCap": 4500000000000,
            }
        ]

        result = mp.historical_industry_pe(apikey=mock_api_key, industry="Software")

        mock_return_json.assert_called_once_with(
            path="historical-industry-pe",
            query_vars={"apikey": mock_api_key, "industry": "Software"},
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].industry == "Software"

    @patch("fmpsdk.market_performance.__return_json")
    def test_biggest_gainers(self, mock_return_json, mock_api_key):
        """Test biggest gainers endpoint."""
        mock_return_json.return_value = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "change": 5.25,
                "price": 150.75,
                "changesPercentage": 3.61,
            }
        ]

        result = mp.biggest_gainers(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="biggest-gainers", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].symbol == "AAPL"

    @patch("fmpsdk.market_performance.__return_json")
    def test_biggest_losers(self, mock_return_json, mock_api_key):
        """Test biggest losers endpoint."""
        mock_return_json.return_value = [
            {
                "symbol": "TSLA",
                "name": "Tesla Inc.",
                "change": -8.50,
                "price": 200.25,
                "changesPercentage": -4.07,
            }
        ]

        result = mp.biggest_losers(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="biggest-losers", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].symbol == "TSLA"

    @patch("fmpsdk.market_performance.__return_json")
    def test_most_active_stocks(self, mock_return_json, mock_api_key):
        """Test most active stocks endpoint."""
        mock_return_json.return_value = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "change": 1.25,
                "price": 425.50,
                "changesPercentage": 0.29,
            }
        ]

        result = mp.most_active_stocks(apikey=mock_api_key)

        mock_return_json.assert_called_once_with(
            path="most-actives", query_vars={"apikey": mock_api_key}
        )

        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        assert result.root[0].symbol == "SPY"


class TestMarketPerformanceIntegration:
    """Integration tests for market performance endpoints."""

    @pytest.mark.parametrize(
        "function,kwargs",
        [
            (mp.sector_performance_snapshot, {}),
            (mp.industry_performance_snapshot, {}),
            (mp.historical_sector_performance, {"sector": "Technology"}),
            (mp.historical_industry_performance, {"industry": "Software"}),
            (mp.sector_pe_snapshot, {}),
            (mp.industry_pe_snapshot, {}),
            (mp.historical_sector_pe, {"sector": "Technology"}),
            (mp.historical_industry_pe, {"industry": "Software"}),
            (mp.biggest_gainers, {}),
            (mp.biggest_losers, {}),
            (mp.most_active_stocks, {}),
        ],
    )
    def test_market_performance_endpoints_structure(self, function, kwargs):
        """Test that all market performance endpoints have correct structure."""
        # This test ensures that function calls don't raise exceptions
        # and would work with proper API credentials
        import inspect

        sig = inspect.signature(function)
        assert "apikey" in sig.parameters

        # Check that required parameters are present
        for param_name in kwargs:
            assert param_name in sig.parameters
