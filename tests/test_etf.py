import time

from fmpsdk import etf
from fmpsdk.models import (
    FMPFundAssetExposure,
    FMPFundCountryAllocation,
    FMPFundHolding,
    FMPFundInfo,
    FMPFundSectorWeighting,
)

from .conftest import extract_data_list


class TestETFInfo:
    """Test the etf_info function."""

    def test_etf_info_success(self, api_key):
        """Test successful retrieval of ETF info."""
        result = etf.etf_info(apikey=api_key, symbol="SPY")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                fund_info = FMPFundInfo(**first_item)
            else:
                fund_info = first_item
            assert fund_info.symbol, "Symbol should not be empty"

    def test_etf_info_major_etfs(self, api_key):
        """Test ETF info for major ETFs."""
        major_etfs = ["SPY", "QQQ", "VTI", "IWM"]

        for symbol in major_etfs:
            result = etf.etf_info(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"

    def test_etf_info_invalid_symbol(self, api_key):
        """Test ETF info with invalid symbol."""
        result = etf.etf_info(apikey=api_key, symbol="INVALID")
        result_list = extract_data_list(result)
        assert isinstance(
            result_list, list
        ), "Should return a list even with invalid symbol"


class TestETFHoldings:
    """Test the etf_holdings function."""

    def test_etf_holdings_success(self, api_key):
        """Test successful retrieval of ETF holdings."""
        result = etf.etf_holdings(apikey=api_key, symbol="SPY")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                holding = FMPFundHolding(**first_item)
            else:
                holding = first_item
            assert hasattr(holding, "symbol") or hasattr(
                holding, "holdingSymbol"
            ), "Should have symbol field"

    def test_etf_holdings_major_etfs(self, api_key):
        """Test ETF holdings for major ETFs."""
        major_etfs = ["SPY", "QQQ", "VTI"]

        for symbol in major_etfs:
            result = etf.etf_holdings(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"


class TestETFAssetExposure:
    """Test the etf_asset_exposure function."""

    def test_etf_asset_exposure_success(self, api_key):
        """Test successful retrieval of ETF asset exposure."""
        result = etf.etf_asset_exposure(apikey=api_key, symbol="SPY")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                exposure = FMPFundAssetExposure(**first_item)
            else:
                exposure = first_item
            assert hasattr(exposure, "assetType") or hasattr(
                exposure, "exposure"
            ), "Should have asset exposure fields"

    def test_etf_asset_exposure_different_types(self, api_key):
        """Test asset exposure for different ETF types."""
        etf_types = ["SPY", "AGG", "GLD"]  # Equity, Bond, Commodity

        for symbol in etf_types:
            result = etf.etf_asset_exposure(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"


class TestETFCountryWeightings:
    """Test the etf_country_weightings function."""

    def test_etf_country_weightings_success(self, api_key):
        """Test successful retrieval of ETF country weightings."""
        result = etf.etf_country_weightings(apikey=api_key, symbol="SPY")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                country = FMPFundCountryAllocation(**first_item)
            else:
                country = first_item
            assert hasattr(country, "country") or hasattr(
                country, "countryName"
            ), "Should have country field"

    def test_etf_country_weightings_international(self, api_key):
        """Test country weightings for international ETFs."""
        international_etfs = ["VEA", "EFA", "VWO"]

        for symbol in international_etfs:
            result = etf.etf_country_weightings(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"


class TestETFSectorWeightings:
    """Test the etf_sector_weightings function."""

    def test_etf_sector_weightings_success(self, api_key):
        """Test successful retrieval of ETF sector weightings."""
        result = etf.etf_sector_weightings(apikey=api_key, symbol="SPY")
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                sector = FMPFundSectorWeighting(**first_item)
            else:
                sector = first_item
            assert hasattr(sector, "sector") or hasattr(
                sector, "sectorName"
            ), "Should have sector field"

    def test_etf_sector_weightings_broad_market(self, api_key):
        """Test sector weightings for broad market ETFs."""
        broad_market_etfs = ["SPY", "VTI", "QQQ"]

        for symbol in broad_market_etfs:
            result = etf.etf_sector_weightings(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"


class TestETFComprehensive:
    """Comprehensive ETF tests."""

    def test_etf_all_functions_consistency(self, api_key):
        """Test that all ETF functions work consistently for SPY."""
        symbol = "SPY"

        # Test all functions with the same symbol
        info_result = etf.etf_info(apikey=api_key, symbol=symbol)
        holdings_result = etf.etf_holdings(apikey=api_key, symbol=symbol)
        asset_result = etf.etf_asset_exposure(apikey=api_key, symbol=symbol)
        country_result = etf.etf_country_weightings(apikey=api_key, symbol=symbol)
        sector_result = etf.etf_sector_weightings(apikey=api_key, symbol=symbol)

        # All should return lists
        assert isinstance(extract_data_list(info_result), list)
        assert isinstance(extract_data_list(holdings_result), list)
        assert isinstance(extract_data_list(asset_result), list)
        assert isinstance(extract_data_list(country_result), list)
        assert isinstance(extract_data_list(sector_result), list)

    def test_etf_response_times(self, api_key):
        """Test that ETF functions respond within reasonable time."""
        symbol = "SPY"
        functions = [
            etf.etf_info,
            etf.etf_holdings,
            etf.etf_asset_exposure,
            etf.etf_country_weightings,
            etf.etf_sector_weightings,
        ]

        for func in functions:
            start_time = time.time()
            result = func(apikey=api_key, symbol=symbol)
            extract_data_list(result)
            response_time = time.time() - start_time

            assert (
                response_time < 10.0
            ), f"{func.__name__} took {response_time:.2f}s, expected < 10.0s"

    def test_etf_invalid_api_keys(self):
        """Test ETF functions with invalid API keys."""
        symbol = "SPY"
        functions = [
            etf.etf_info,
            etf.etf_holdings,
            etf.etf_asset_exposure,
            etf.etf_country_weightings,
            etf.etf_sector_weightings,
        ]

        for func in functions:
            result = func(apikey="invalid_key", symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"{func.__name__} should return list with invalid key"
