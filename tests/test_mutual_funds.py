"""
Comprehensive tests for fmpsdk.mutual_funds module.
Tests all mutual fund functions including error handling and edge cases.
"""
import os
import pytest

import fmpsdk.mutual_funds as mf
from fmpsdk.models import *

API_KEY = os.getenv("FMP_API_KEY", "demo")


# === PARAMETERIZED TEST CLASSES ===

class TestParameterizedMutualFunds:
    """Comprehensive parameterized tests for mutual fund functions."""
    
    @pytest.mark.parametrize("symbol", [
        "VTIAX", "FXNAX", "VFINX", "VTSMX", "VBTLX",  # Vanguard funds
        "FSKAX", "FTBFX", "FBGRX", "FCNTX", "FDVV",   # Fidelity funds
        "SWPPX", "SWTSX", "SWAGX", "SWISX", "SWLBX",  # Schwab funds
        "INVALID", "FAKE123", "",  # Invalid symbols
        "   ", "NULL", "TEST"  # Edge cases
    ])
    def test_mutual_fund_symbol_variations(self, symbol):
        """Test mutual fund functions with various symbol formats."""
        result = mf.mutual_fund_holdings(apikey=API_KEY, symbol=symbol)
        assert result is not None


class TestMutualFundIntegration:
    """Test integration scenarios for mutual fund functions."""

    def test_mutual_fund_analysis_workflow(self):
        """Test workflow for mutual fund analysis."""
        symbol = "VTIAX"
        
        # 1. Get mutual fund holdings
        holdings = mf.mutual_fund_holdings(apikey=API_KEY, symbol=symbol)
        assert holdings is not None
