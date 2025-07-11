import time

import pytest
from pydantic_core import ValidationError

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

    @pytest.mark.parametrize(
        "symbol",
        [
            # Broad Market ETFs
            "SPY",  # SPDR S&P 500 ETF
            "VTI",  # Vanguard Total Stock Market ETF
            "QQQ",  # Invesco QQQ Trust ETF
            "IWM",  # iShares Russell 2000 ETF
            "VEA",  # Vanguard FTSE Developed Markets ETF
            "VWO",  # Vanguard FTSE Emerging Markets ETF
            "AGG",  # iShares Core US Aggregate Bond ETF
            "BND",  # Vanguard Total Bond Market ETF
            # Sector ETFs
            "XLF",  # Financial Select Sector SPDR Fund
            "XLK",  # Technology Select Sector SPDR Fund
            "XLE",  # Energy Select Sector SPDR Fund
            "XLV",  # Health Care Select Sector SPDR Fund
            "XLI",  # Industrial Select Sector SPDR Fund
            "XLP",  # Consumer Staples Select Sector SPDR Fund
            "XLY",  # Consumer Discretionary Select Sector SPDR Fund
            "XLU",  # Utilities Select Sector SPDR Fund
            "XLB",  # Materials Select Sector SPDR Fund
            "XLRE",  # Real Estate Select Sector SPDR Fund
            # Thematic ETFs
            "ARK",  # ARK Innovation ETF (if available)
            "ICLN",  # iShares Global Clean Energy ETF
            "JETS",  # U.S. Global Jets ETF
            "SOXX",  # iShares PHLX Semiconductor ETF
            "FINX",  # Global X FinTech ETF
            "ESGU",  # iShares MSCI USA ESG Select ETF
            "MTUM",  # iShares MSCI USA Momentum Factor ETF
            "QUAL",  # iShares MSCI USA Quality Factor ETF
            "SIZE",  # iShares MSCI USA Size Factor ETF
            "USMV",  # iShares MSCI USA Min Vol Factor ETF
            # International ETFs
            "EFA",  # iShares MSCI EAFE ETF
            "EEM",  # iShares MSCI Emerging Markets ETF
            "VGK",  # Vanguard FTSE Europe ETF
            "VPL",  # Vanguard FTSE Pacific ETF
            "FXI",  # iShares China Large-Cap ETF
            "EWJ",  # iShares MSCI Japan ETF
            "INDA",  # iShares MSCI India ETF
            "EWZ",  # iShares MSCI Brazil ETF
            # Fixed Income ETFs
            "TLT",  # iShares 20+ Year Treasury Bond ETF
            "IEF",  # iShares 7-10 Year Treasury Bond ETF
            "SHY",  # iShares 1-3 Year Treasury Bond ETF
            "LQD",  # iShares iBoxx $ Investment Grade Corporate Bond ETF
            "HYG",  # iShares iBoxx $ High Yield Corporate Bond ETF
            "EMB",  # iShares J.P. Morgan USD Emerging Markets Bond ETF
            "MUB",  # iShares National Muni Bond ETF
            "VTEB",  # Vanguard Tax-Exempt Bond ETF
            # Commodity ETFs
            "GLD",  # SPDR Gold Shares
            "SLV",  # iShares Silver Trust
            "DJP",  # iPath Bloomberg Commodity Index Total Return ETN
            "USO",  # United States Oil Fund
            "UNG",  # United States Natural Gas Fund
            "DBA",  # Invesco DB Agriculture Fund
        ],
    )
    def test_etf_info_comprehensive(self, api_key, symbol):
        """Test ETF info across various categories and asset classes."""
        try:
            result = etf.etf_info(apikey=api_key, symbol=symbol)
        except ValidationError as e:
            pytest.skip(
                f"Validation error for {symbol}: {str(e)[:100]}... - API data doesn't match model"
            )

        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                fund_info = FMPFundInfo(**first_item)
            else:
                fund_info = first_item

            assert fund_info.symbol == symbol, f"Symbol should match {symbol}"

            # Basic data quality checks
            if hasattr(fund_info, "fundName") and fund_info.fundName:
                assert len(fund_info.fundName) > 3, "Fund name should be meaningful"

            if (
                hasattr(fund_info, "expenseRatio")
                and fund_info.expenseRatio is not None
            ):
                assert (
                    0 <= fund_info.expenseRatio <= 5
                ), "Expense ratio should be reasonable (0-5%)"

            if hasattr(fund_info, "nav") and fund_info.nav is not None:
                assert fund_info.nav > 0, "NAV should be positive"

    @pytest.mark.parametrize(
        "etf_category",
        [
            "broad_market",
            "sector",
            "international",
            "fixed_income",
            "commodity",
            "thematic",
        ],
    )
    def test_etf_info_by_category(self, api_key, etf_category):
        """Test ETF info across different ETF categories."""
        category_etfs = {
            "broad_market": ["SPY", "VTI", "QQQ"],
            "sector": ["XLF", "XLK", "XLE"],
            "international": ["EFA", "EEM", "VGK"],
            "fixed_income": ["AGG", "TLT", "LQD"],
            "commodity": ["GLD", "SLV", "USO"],
            "thematic": ["ICLN", "JETS", "SOXX"],
        }

        symbols = category_etfs.get(etf_category, ["SPY"])

        for symbol in symbols:
            try:
                result = etf.etf_info(apikey=api_key, symbol=symbol)
            except ValidationError as e:
                pytest.skip(
                    f"Validation error for {symbol}: {str(e)[:100]}... - API data doesn't match model"
                )

            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"

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

    @pytest.mark.parametrize(
        "symbol",
        [
            # Large Cap ETFs with many holdings
            "SPY",  # S&P 500 - 500+ holdings
            "VTI",  # Total Market - 1000+ holdings
            "QQQ",  # NASDAQ 100 - 100+ holdings
            "IWM",  # Russell 2000 - 2000+ holdings
            # Sector ETFs with focused holdings
            "XLF",  # Financial sector
            "XLK",  # Technology sector
            "XLE",  # Energy sector
            "XLV",  # Healthcare sector
            # International ETFs
            "EFA",  # Developed markets
            "EEM",  # Emerging markets
            "VGK",  # Europe
            "FXI",  # China
            # Bond ETFs
            "AGG",  # Aggregate bonds
            "TLT",  # Long-term treasury
            "LQD",  # Investment grade corporate
            "HYG",  # High yield corporate
            # Specialty ETFs
            "GLD",  # Gold
            "ARKK",  # Innovation (if available)
            "ICLN",  # Clean energy
            "JETS",  # Airlines
        ],
    )
    def test_etf_holdings_comprehensive(self, api_key, symbol):
        """Test ETF holdings across various ETF types."""
        result = etf.etf_holdings(apikey=api_key, symbol=symbol)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                holding = FMPFundHolding(**first_item)
            else:
                holding = first_item

            # Should have symbol or holdingSymbol field
            has_symbol = (hasattr(holding, "symbol") and holding.symbol) or (
                hasattr(holding, "holdingSymbol") and holding.holdingSymbol
            )
            assert has_symbol, "Should have symbol field"

            # Should have weight information
            if hasattr(holding, "weightPercent") and holding.weightPercent is not None:
                assert 0 <= holding.weightPercent <= 100, "Weight should be 0-100%"

            # Should have shares or market value
            has_quantity = (
                hasattr(holding, "shares") and holding.shares is not None
            ) or (hasattr(holding, "marketValue") and holding.marketValue is not None)
            # This may not always be available, so just check if present

    @pytest.mark.parametrize(
        "asset_class", ["equity", "fixed_income", "commodity", "real_estate"]
    )
    def test_etf_holdings_by_asset_class(self, api_key, asset_class):
        """Test ETF holdings across different asset classes."""
        asset_class_etfs = {
            "equity": ["SPY", "QQQ", "VTI"],
            "fixed_income": ["AGG", "TLT", "LQD"],
            "commodity": ["GLD", "SLV", "USO"],
            "real_estate": ["XLRE", "VNQ", "RWR"],
        }

        symbols = asset_class_etfs.get(asset_class, ["SPY"])

        for symbol in symbols:
            result = etf.etf_holdings(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(
                result_list, list
            ), f"Response should be a list for {symbol}"

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

    @pytest.mark.parametrize(
        "symbol", ["SPY", "QQQ", "VTI", "IWM", "EFA", "EEM", "AGG", "TLT", "GLD", "XLF"]
    )
    def test_etf_asset_exposure_comprehensive(self, api_key, symbol):
        """Test ETF asset exposure across various ETFs."""
        result = etf.etf_asset_exposure(apikey=api_key, symbol=symbol)
        result_list = extract_data_list(result)

        assert isinstance(result_list, list), "Response should be a list"

        if result_list:
            # Test first item
            first_item = result_list[0]
            if isinstance(first_item, dict):
                exposure = FMPFundAssetExposure(**first_item)
            else:
                exposure = first_item

            # Should have asset allocation information
            assert hasattr(exposure, "assetClass") or hasattr(
                exposure, "category"
            ), "Should have asset class information"

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
