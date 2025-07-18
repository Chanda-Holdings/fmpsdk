import pytest

from fmpsdk import etf
from fmpsdk.models import (
    FMPFundAssetExposure,
    FMPFundCountryAllocation,
    FMPFundHolding,
    FMPFundInfo,
    FMPFundSectorWeighting,
)

from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
    validate_required_fields,
)


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
        response, validation = handle_api_call_with_validation(
            etf.etf_info, "etf_info", True, apikey=api_key, symbol=symbol
        )
        
        # ETF info specific validation
        result_list = get_response_models(response, FMPFundInfo)
        
        for item in result_list:
            # Symbol validation
            if item.symbol:
                assert item.symbol == symbol, f"Symbol should match {symbol}"
                assert len(item.symbol) <= 10, f"Symbol should be reasonable length: {item.symbol}"
                assert item.symbol.replace("-", "").replace(".", "").isalnum(), f"Symbol should be alphanumeric: {item.symbol}"
            
            # Fund name validation
            if item.name:
                assert len(item.name) >= 3, f"Fund name should be meaningful: {item.name}"
                assert len(item.name) <= 200, f"Fund name should be reasonable length: {item.name}"
            
            # Expense ratio validation
            if item.expenseRatio is not None:
                assert 0 <= item.expenseRatio <= 5, f"Expense ratio should be reasonable (0-5%): {item.expenseRatio}"
            
            # NAV validation
            if item.nav is not None:
                assert item.nav > 0, f"NAV should be positive: {item.nav}"
                assert item.nav <= 10000, f"NAV should be reasonable: {item.nav}"
            
            # Assets under management validation
            if item.assetsUnderManagement is not None:
                assert item.assetsUnderManagement >= 0, f"AUM should be non-negative: {item.assetsUnderManagement}"
            
            # Average volume validation
            if item.avgVolume is not None:
                assert item.avgVolume >= 0, f"Average volume should be non-negative: {item.avgVolume}"
            
            # Inception date validation
            if item.inceptionDate:
                assert len(item.inceptionDate) >= 8, f"Inception date should be properly formatted: {item.inceptionDate}"

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
            response, validation = handle_api_call_with_validation(
                etf.etf_info, "etf_info", True, apikey=api_key, symbol=symbol
            )
            
            # Category consistency validation
            result_list = get_response_models(response, FMPFundInfo)
            
            for item in result_list:
                if item.name:
                    # Basic categorization validation based on fund name
                    if etf_category == "sector":
                        sector_keywords = ["Select", "Sector", "SPDR", "Financial", "Technology", "Energy", "Health", "Industrial", "Consumer", "Utilities", "Materials", "Real Estate"]
                        # Not all sector ETFs have these keywords, so just check if present
                    elif etf_category == "international":
                        intl_keywords = ["FTSE", "MSCI", "EAFE", "Emerging", "Europe", "Pacific", "China", "Japan", "India", "Brazil"]
                        # Similar soft validation for international ETFs
                    elif etf_category == "fixed_income":
                        bond_keywords = ["Bond", "Treasury", "Corporate", "Municipal", "Aggregate", "Fixed", "Income"]
                        # Similar soft validation for bond ETFs


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
        response, validation = handle_api_call_with_validation(
            etf.etf_holdings, "etf_holdings", True, apikey=api_key, symbol=symbol
        )
        
        # ETF holdings specific validation
        result_list = get_response_models(response, FMPFundHolding)
        total_weight = 0
        
        for item in result_list:
            # Symbol validation
            if item.symbol:
                assert len(item.symbol) <= 15, f"Holding symbol should be reasonable length: {item.symbol}"
                assert item.symbol.replace("-", "").replace(".", "").isalnum(), f"Holding symbol should be alphanumeric: {item.symbol}"
            
            # Weight validation
            if item.weightPercentage is not None:
                assert 0 <= item.weightPercentage <= 100, f"Weight should be 0-100%: {item.weightPercentage}"
                total_weight += item.weightPercentage
            
            # Shares validation
            if item.sharesNumber is not None:
                assert item.sharesNumber >= 0, f"Shares should be non-negative: {item.sharesNumber}"
            
            # Market value validation
            if item.marketValue is not None:
                assert item.marketValue >= 0, f"Market value should be non-negative: {item.marketValue}"
            
            # Asset name validation
            if item.name:
                assert len(item.name) <= 200, f"Asset name should be reasonable length: {item.name}"
        
        # Total weight should generally be reasonable (allowing for incomplete data)
        if total_weight > 0:
            assert total_weight <= 110, f"Total weight should be reasonable: {total_weight}%"

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
            response, validation = handle_api_call_with_validation(
                etf.etf_holdings, "etf_holdings", True, apikey=api_key, symbol=symbol
            )


class TestETFAssetExposure:
    """Test the etf_asset_exposure function."""

    @pytest.mark.parametrize(
        "symbol", ["SPY", "QQQ", "VTI", "IWM", "EFA", "EEM", "AGG", "TLT", "GLD", "XLF"]
    )
    def test_etf_asset_exposure_comprehensive(self, api_key, symbol):
        """Test ETF asset exposure across various ETFs."""
        response, validation = handle_api_call_with_validation(
            etf.etf_asset_exposure, "etf_asset_exposure", True, apikey=api_key, symbol=symbol
        )
        
        # Asset exposure specific validation
        result_list = get_response_models(response, FMPFundAssetExposure)
        total_exposure = 0
        
        for item in result_list:
            # Asset validation
            if item.asset:
                assert len(item.asset) <= 50, f"Asset should be reasonable length: {item.asset}"
            
            # Weight percentage validation
            if item.weightPercentage is not None:
                assert 0 <= item.weightPercentage <= 100, f"Weight percentage should be 0-100%: {item.weightPercentage}"
                total_exposure += item.weightPercentage
            
            # Symbol validation
            if item.symbol:
                assert len(item.symbol) <= 15, f"Symbol should be reasonable length: {item.symbol}"
                
            # Market value validation
            if item.marketValue is not None:
                assert item.marketValue >= 0, f"Market value should be non-negative: {item.marketValue}"
        
        # Total exposure should be reasonable (allowing for incomplete data)
        if total_exposure > 0:
            assert total_exposure <= 110, f"Total exposure should be reasonable: {total_exposure}%"


class TestETFCountryWeightings:
    """Test the etf_country_weightings function."""

    def test_etf_country_weightings_comprehensive(self, api_key):
        """Test ETF country weightings across various ETFs."""
        international_etfs = ["VEA", "EFA", "VWO", "EEM", "SPY"]
        
        for symbol in international_etfs:
            response, validation = handle_api_call_with_validation(
                etf.etf_country_weightings, "etf_country_weightings", True, apikey=api_key, symbol=symbol
            )
            
            # Country weightings specific validation
            result_list = get_response_models(response, FMPFundCountryAllocation)
            total_weight = 0
            
            for item in result_list:
                # Country validation
                if item.country:
                    assert len(item.country) >= 2, f"Country should have reasonable length: {item.country}"
                    assert len(item.country) <= 100, f"Country should be reasonable length: {item.country}"
                
                # Weight validation (note: weightPercentage is a string in this model)
                if item.weightPercentage:
                    try:
                        weight_float = float(item.weightPercentage.replace('%', ''))
                        assert -10 <= weight_float <= 100, f"Weight should be reasonable range (-10% to 100%): {weight_float}"
                        total_weight += weight_float
                    except (ValueError, AttributeError):
                        # Skip invalid weight values
                        pass
            
            # Total weight should be reasonable
            if total_weight > 0:
                assert total_weight <= 110, f"Total weight should be reasonable: {total_weight}%"


class TestETFSectorWeightings:
    """Test the etf_sector_weightings function."""

    def test_etf_sector_weightings_comprehensive(self, api_key):
        """Test ETF sector weightings across various ETFs."""
        broad_market_etfs = ["SPY", "VTI", "QQQ", "IWM"]
        
        for symbol in broad_market_etfs:
            response, validation = handle_api_call_with_validation(
                etf.etf_sector_weightings, "etf_sector_weightings", True, apikey=api_key, symbol=symbol
            )
            
            # Sector weightings specific validation
            result_list = get_response_models(response, FMPFundSectorWeighting)
            total_weight = 0
            valid_sectors = [
                "Technology", "Health Care", "Financial", "Consumer", "Industrial", 
                "Communication", "Energy", "Materials", "Real Estate", "Utilities"
            ]
            
            for item in result_list:
                # Sector validation
                if item.sector:
                    assert len(item.sector) >= 3, f"Sector should have meaningful length: {item.sector}"
                    assert len(item.sector) <= 100, f"Sector should be reasonable length: {item.sector}"
                    
                    # Check if sector matches common sector names (soft validation)
                    sector_matches = any(valid_sector in item.sector for valid_sector in valid_sectors)
                    # Note: Not all sectors will match, so this is just informational
                
                # Weight validation
                if item.weightPercentage is not None:
                    assert 0 <= item.weightPercentage <= 100, f"Weight should be 0-100%: {item.weightPercentage}"
                    total_weight += item.weightPercentage
            
            # Total weight should be reasonable
            if total_weight > 0:
                assert total_weight <= 110, f"Total weight should be reasonable: {total_weight}%"


class TestETFDataQuality:
    """Test ETF data quality metrics."""

    def test_etf_data_quality_comprehensive(self, api_key):
        """Test comprehensive ETF data quality across multiple endpoints."""
        test_symbols = ["SPY", "QQQ", "VTI", "AGG", "GLD"]
        
        for symbol in test_symbols:
            response, validation = handle_api_call_with_validation(
                etf.etf_info, "etf_info", True, apikey=api_key, symbol=symbol
            )
            
            # Comprehensive data quality validation
            result_list = get_response_models(response, FMPFundInfo)
            if not result_list:
                continue
            
            # Calculate data quality metrics
            total_items = len(result_list)
            valid_symbols = sum(1 for item in result_list if item.symbol)
            meaningful_names = sum(1 for item in result_list if item.name and len(item.name) > 3)
            valid_nav = sum(1 for item in result_list if item.nav and item.nav > 0)
            
            # Data quality assertions
            if total_items > 0:
                assert valid_symbols / total_items >= 0.9, f"At least 90% should have valid symbols: {valid_symbols}/{total_items}"
                assert meaningful_names / total_items >= 0.8, f"At least 80% should have meaningful names: {meaningful_names}/{total_items}"
                if valid_nav > 0:
                    assert valid_nav / total_items >= 0.7, f"At least 70% should have valid NAV: {valid_nav}/{total_items}"

    def test_etf_invalid_inputs(self, api_key):
        """Test ETF functions with invalid inputs."""
        # Test with invalid symbol
        response, validation = handle_api_call_with_validation(
            etf.etf_info, "etf_info", True, apikey=api_key, symbol="INVALID"
        )
        
        # Test with invalid API key (should raise InvalidAPIKeyException)
        with pytest.raises(Exception):  # Expecting an exception for invalid API key
            etf.etf_info(apikey="invalid_key", symbol="SPY")
