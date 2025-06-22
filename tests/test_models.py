"""
Unit tests for fmpsdk Pydantic models.
"""

from typing import List

import pytest
from pydantic import ValidationError

from fmpsdk.models import (FMPCompanyCIKSearch, FMPCompanyNameSearch,
                           FMPCusipSearch, FMPIsinSearch,
                           FMPStockScreenerResult, FMPSymbolSearch)


class TestStockSymbolSearchModels:
    """Test models for stock symbol search endpoints."""

    def test_stock_symbol_search_item_valid_data(self):
        """Test FMPSymbolSearch with valid data."""
        data = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "currency": "USD",
            "exchangeFullName": "NASDAQ Global Select",
            "exchange": "NASDAQ",
        }

        item = FMPSymbolSearch(**data)

        assert item.symbol == "AAPL"
        assert item.name == "Apple Inc."
        assert item.currency == "USD"
        assert item.exchangeFullName == "NASDAQ Global Select"
        assert item.exchange == "NASDAQ"

    def test_stock_symbol_search_item_missing_required_field(self):
        """Test FMPSymbolSearch validation with missing required field."""
        data = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "currency": "USD",
            "exchangeFullName": "NASDAQ Global Select",
            # Missing 'exchange' field
        }

        with pytest.raises(ValidationError):
            FMPSymbolSearch(**data)

    def test_stock_symbol_search_response_valid_list(self):
        """Test FMPSymbolSearch RootModel with valid list data."""
        from pydantic import RootModel

        data = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "currency": "USD",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "currency": "USD",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
            },
        ]
        response = RootModel[List[FMPSymbolSearch]](data)
        assert len(response.root) == 2
        assert response.root[0].symbol == "AAPL"
        assert response.root[1].symbol == "MSFT"

    def test_stock_symbol_search_response_empty_list(self):
        """Test FMPSymbolSearch RootModel with empty list."""
        from pydantic import RootModel

        data = []
        response = RootModel[List[FMPSymbolSearch]](data)
        assert len(response.root) == 0


class TestCompanyNameSearchModels:
    """Test models for company name search endpoints."""

    def test_company_name_search_item_valid_data(self):
        """Test FMPCompanyNameSearch with valid data."""
        data = {
            "symbol": "TSLA",
            "name": "Tesla, Inc.",
            "currency": "USD",
            "exchangeFullName": "NASDAQ Global Select",
            "exchange": "NASDAQ",
        }

        item = FMPCompanyNameSearch(**data)

        assert item.symbol == "TSLA"
        assert item.name == "Tesla, Inc."
        assert item.currency == "USD"

    def test_company_name_search_response(self):
        """Test FMPCompanyNameSearch RootModel."""
        from pydantic import RootModel

        data = [
            {
                "symbol": "TSLA",
                "name": "Tesla, Inc.",
                "currency": "USD",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
            }
        ]
        response = RootModel[List[FMPCompanyNameSearch]](data)
        assert len(response.root) == 1
        assert response.root[0].symbol == "TSLA"


class TestCikSearchModels:
    """Test models for CIK search endpoints."""

    def test_cik_search_item_valid_data(self):
        """Test FMPCompanyCIKSearch with valid data."""
        data = {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "cik": "0000320193",
            "exchangeFullName": "NASDAQ Global Select",
            "exchange": "NASDAQ",
            "currency": "USD",
        }
        item = FMPCompanyCIKSearch(**data)
        assert item.symbol == "AAPL"
        assert item.companyName == "Apple Inc."
        assert item.cik == "0000320193"
        assert item.currency == "USD"

    def test_cik_search_response(self):
        """Test FMPCompanyCIKSearch RootModel."""
        from pydantic import RootModel

        data = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "cik": "0000320193",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
                "currency": "USD",
            }
        ]
        response = RootModel[List[FMPCompanyCIKSearch]](data)
        assert len(response.root) == 1
        assert response.root[0].cik == "0000320193"


class TestCusipSearchModels:
    """Test models for CUSIP search endpoints."""

    def test_cusip_search_item_valid_data(self):
        """Test FMPCusipSearch with valid data."""
        data = {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "cusip": "037833100",
            "marketCap": 3000000000000.0,
        }
        item = FMPCusipSearch(**data)
        assert item.symbol == "AAPL"
        assert item.companyName == "Apple Inc."
        assert item.cusip == "037833100"
        assert item.marketCap == 3000000000000.0


class TestIsinSearchModels:
    """Test models for ISIN search endpoints."""

    def test_isin_search_item_valid_data(self):
        """Test FMPIsinSearch with valid data."""
        data = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "isin": "US0378331005",
            "marketCap": 3000000000000.0,
        }
        item = FMPIsinSearch(**data)
        assert item.symbol == "AAPL"
        assert item.name == "Apple Inc."
        assert item.isin == "US0378331005"
        assert item.marketCap == 3000000000000.0


class TestStockScreenerModels:
    """Test models for stock screener endpoints."""

    def test_stock_screener_item_valid_data(self):
        """Test FMPStockScreenerResult with valid data."""
        data = {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "marketCap": 3000000000000.0,
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "beta": 1.2,
            "price": 150.0,
            "lastAnnualDividend": 0.88,
            "volume": 50000000,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "country": "US",
            "isEtf": False,
            "isFund": False,
            "isActivelyTrading": True,
        }
        item = FMPStockScreenerResult(**data)
        assert item.symbol == "AAPL"
        assert item.companyName == "Apple Inc."
        assert item.marketCap == 3000000000000.0
        assert item.sector == "Technology"
        assert item.industry == "Consumer Electronics"
        assert item.beta == 1.2
        assert item.price == 150.0
        assert item.isEtf == False
        assert item.isFund == False
        assert item.isActivelyTrading == True
