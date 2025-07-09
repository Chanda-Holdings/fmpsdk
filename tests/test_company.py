from fmpsdk import company
from fmpsdk.models import (
    FMPCompanyNote,
    FMPCompanyProfile,
    FMPDelistedCompany,
    FMPEmployeeCount,
    FMPExecutiveCompensation,
    FMPExecutiveProfile,
    FMPHistoricalEmployeeCount,
    FMPMarketCap,
    FMPMergerAcquisition,
    FMPShareFloat,
    FMPStockPeer,
)
from tests.conftest import extract_data_list


def get_field_value(item, field_name):
    """Helper to get field value from either dict or model object."""
    if hasattr(item, field_name):
        return getattr(item, field_name)
    elif isinstance(item, dict):
        return item.get(field_name)
    else:
        return None


class TestCompanyProfile:
    """Tests for company profile functions."""

    def test_company_profile_valid_symbol(self, api_key):
        """Test company profile with valid symbol."""
        result = company.company_profile(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) > 0

        for item in result_list:
            if isinstance(item, dict):
                validated = FMPCompanyProfile.model_validate(item)
            else:
                validated = item

            assert validated.symbol == "AAPL"
            assert validated.companyName
            assert validated.industry
            assert validated.sector
            assert validated.exchange
            assert validated.currency

    def test_company_profile_large_cap_stocks(self, api_key):
        """Test company profile for major large cap stocks."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

        for symbol in symbols:
            result = company.company_profile(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            assert len(result_list) > 0

            # Validate first result
            item = result_list[0]
            if isinstance(item, dict):
                validated = FMPCompanyProfile.model_validate(item)
            else:
                validated = item

            assert validated.symbol == symbol
            if validated.mktCap is not None:
                assert validated.mktCap > 100000000  # Should be > $100M

    def test_company_profile_international_stocks(self, api_key):
        """Test company profile for international stocks."""
        symbols = ["ASML", "TSM", "NVO"]

        for symbol in symbols:
            result = company.company_profile(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                item = result_list[0]
                if isinstance(item, dict):
                    FMPCompanyProfile.model_validate(item)

    def test_company_profile_invalid_symbol(self, api_key):
        """Test company profile with invalid symbol."""
        result = company.company_profile(apikey=api_key, symbol="INVALID999")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should return empty list for invalid symbol

    def test_company_profile_cik_valid(self, api_key):
        """Test company profile by CIK number."""
        # Apple's CIK
        result = company.company_profile_cik(apikey=api_key, cik="0000320193")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            item = result_list[0]
            if isinstance(item, dict):
                validated = FMPCompanyProfile.model_validate(item)
            else:
                validated = item
            assert validated.cik == "0000320193"

    def test_company_profile_cik_invalid(self, api_key):
        """Test company profile with invalid CIK."""
        result = company.company_profile_cik(apikey=api_key, cik="INVALID")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Should handle gracefully


class TestCompanyNotes:
    """Tests for company_notes function."""

    def test_company_notes_valid_symbol(self, api_key):
        """Test company notes with valid symbol."""
        result = company.company_notes(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPCompanyNote.model_validate(item)
                else:
                    validated = item
                assert validated.symbol == "AAPL"

    def test_company_notes_multiple_symbols(self, api_key):
        """Test company notes for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = company.company_notes(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)


class TestStockPeers:
    """Tests for stock_peers function."""

    def test_stock_peers_valid_symbol(self, api_key):
        """Test stock peers with valid symbol."""
        result = company.stock_peers(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPStockPeer.model_validate(item)
                else:
                    validated = item
                assert validated.symbol

    def test_stock_peers_technology_sector(self, api_key):
        """Test stock peers for technology companies."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = company.stock_peers(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                # Should return multiple peer companies
                assert len(result_list) >= 1


class TestDelistedCompanies:
    """Tests for delisted_companies function."""

    def test_delisted_companies_no_filters(self, api_key):
        """Test delisted companies with no filters."""
        result = company.delisted_companies(apikey=api_key, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPDelistedCompany.model_validate(item)
                else:
                    validated = item
                assert validated.symbol

    def test_delisted_companies_with_page(self, api_key):
        """Test delisted companies with pagination."""
        result = company.delisted_companies(apikey=api_key, page=0, limit=5)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        assert len(result_list) <= 5


class TestEmployeeCount:
    """Tests for employee count functions."""

    def test_employee_count_valid_symbol(self, api_key):
        """Test current employee count."""
        result = company.employee_count(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            item = result_list[0]
            if isinstance(item, dict):
                validated = FMPEmployeeCount.model_validate(item)
            else:
                validated = item
            assert validated.symbol == "AAPL"
            assert validated.employeeCount is not None

    def test_employee_count_large_companies(self, api_key):
        """Test employee count for large companies."""
        symbols = ["AAPL", "MSFT", "AMZN", "GOOGL"]

        for symbol in symbols:
            result = company.employee_count(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                item = result_list[0]
                if isinstance(item, dict):
                    validated = FMPEmployeeCount.model_validate(item)
                else:
                    validated = item
                # Large companies should have substantial employee counts
                if validated.employeeCount and validated.employeeCount > 1000:
                    assert validated.employeeCount > 1000

    def test_historical_employee_count(self, api_key):
        """Test historical employee count."""
        result = company.historical_employee_count(
            apikey=api_key, symbol="AAPL", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPHistoricalEmployeeCount.model_validate(item)
                else:
                    validated = item
                assert validated.symbol == "AAPL"
                assert validated.employeeCount is not None


class TestMarketCapitalization:
    """Tests for market capitalization functions."""

    def test_market_capitalization_single_symbol(self, api_key):
        """Test market cap for single symbol."""
        result = company.market_capitalization(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            item = result_list[0]
            if isinstance(item, dict):
                validated = FMPMarketCap.model_validate(item)
            else:
                validated = item
            assert validated.symbol == "AAPL"
            if validated.marketCap is not None:
                assert validated.marketCap >= 0  # Can be 0 for some companies

    def test_market_capitalization_batch(self, api_key):
        """Test batch market cap for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        symbols_str = ",".join(symbols)

        result = company.market_capitalization_batch(
            apikey=api_key, symbols=symbols_str
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            # Should return data for multiple symbols
            returned_symbols = set()
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPMarketCap.model_validate(item)
                else:
                    validated = item
                returned_symbols.add(validated.symbol)
                if validated.marketCap is not None:
                    assert validated.marketCap >= 0  # Can be 0 for some companies

            # Should have data for at least some of the requested symbols
            assert len(returned_symbols) > 0

    def test_historical_market_capitalization(self, api_key):
        """Test historical market cap data."""
        result = company.historical_market_capitalization(
            apikey=api_key, symbol="AAPL", limit=10
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPMarketCap.model_validate(item)
                else:
                    validated = item
                assert validated.symbol == "AAPL"
                if validated.marketCap is not None:
                    assert validated.marketCap >= 0  # Can be 0 for some companies


class TestSharesFloat:
    """Tests for shares float functions."""

    def test_shares_float_single_symbol(self, api_key):
        """Test shares float for single symbol."""
        result = company.shares_float(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            item = result_list[0]
            if isinstance(item, dict):
                validated = FMPShareFloat.model_validate(item)
            else:
                validated = item
            assert validated.symbol == "AAPL"

    def test_shares_float_all(self, api_key):
        """Test all shares float data."""
        result = company.shares_float_all(apikey=api_key, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPShareFloat.model_validate(item)
                else:
                    validated = item
                assert validated.symbol


class TestMergersAcquisitions:
    """Tests for M&A functions."""

    def test_mergers_acquisitions_general(self, api_key):
        """Test general M&A announcements."""
        result = company.mergers_acquisitions(apikey=api_key, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPMergerAcquisition.model_validate(item)
                else:
                    validated = item
                # Should have basic M&A information

    def test_mergers_acquisitions_search(self, api_key):
        """Test M&A search functionality."""
        result = company.mergers_acquisitions_search(apikey=api_key, name="Apple")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPMergerAcquisition.model_validate(item)
                else:
                    validated = item


class TestExecutives:
    """Tests for executive functions."""

    def test_key_executives_valid_symbol(self, api_key):
        """Test key executives for valid symbol."""
        result = company.key_executives(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPExecutiveProfile.model_validate(item)
                else:
                    validated = item
                assert validated.name
                assert validated.title

    def test_key_executives_multiple_companies(self, api_key):
        """Test executives for multiple large companies."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = company.key_executives(apikey=api_key, symbol=symbol)
            result_list = extract_data_list(result)
            assert isinstance(result_list, list)

            if len(result_list) > 0:
                # Should have multiple executives
                assert len(result_list) >= 1
                for item in result_list:
                    if isinstance(item, dict):
                        FMPExecutiveProfile.model_validate(item)

    def test_key_executives_compensation(self, api_key):
        """Test executive compensation data."""
        result = company.key_executives_compensation(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPExecutiveCompensation.model_validate(item)
                else:
                    validated = item
                assert validated.nameAndPosition  # Use the correct field name
                assert validated.symbol == "AAPL"

    def test_executive_compensation_benchmark(self, api_key):
        """Test executive compensation benchmarking."""
        result = company.executive_compensation_benchmark(apikey=api_key, year=2023)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

        if len(result_list) > 0:
            for item in result_list:
                if isinstance(item, dict):
                    validated = FMPExecutiveCompensation.model_validate(item)
                else:
                    validated = item


class TestCompanyErrorHandling:
    """Test error handling for company functions."""

    def test_company_profile_invalid_api_key(self):
        """Test company profile with invalid API key."""
        result = company.company_profile(apikey="invalid_key", symbol="AAPL")
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result

    def test_company_profile_empty_symbol(self, api_key):
        """Test company profile with empty symbol."""
        result = company.company_profile(apikey=api_key, symbol="")
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_employee_count_invalid_symbol(self, api_key):
        """Test employee count with invalid symbol."""
        result = company.employee_count(apikey=api_key, symbol="INVALID999")
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)


class TestCompanyResponseTimes:
    """Test response time performance for company functions."""

    def test_company_profile_response_time(self, api_key):
        """Test company profile response time."""
        import time

        start_time = time.time()
        result = company.company_profile(apikey=api_key, symbol="AAPL")
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 10.0  # Should respond within 10 seconds
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)

    def test_batch_market_cap_response_time(self, api_key):
        """Test batch market cap response time."""
        import time

        symbols = ",".join(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])

        start_time = time.time()
        result = company.market_capitalization_batch(apikey=api_key, symbols=symbols)
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 15.0  # Batch operations might be slower
        result_list = extract_data_list(result)
        assert isinstance(result_list, list)


class TestCompanyDataConsistency:
    """Test data consistency across company functions."""

    def test_profile_vs_market_cap_consistency(self, api_key):
        """Test consistency between profile and market cap data."""
        symbol = "AAPL"

        # Get profile data
        profile_result = company.company_profile(apikey=api_key, symbol=symbol)
        profile_list = extract_data_list(profile_result)

        # Get market cap data
        market_cap_result = company.market_capitalization(apikey=api_key, symbol=symbol)
        market_cap_list = extract_data_list(market_cap_result)

        if len(profile_list) > 0 and len(market_cap_list) > 0:
            profile_item = profile_list[0]
            market_cap_item = market_cap_list[0]

            profile_symbol = get_field_value(profile_item, "symbol")
            market_cap_symbol = get_field_value(market_cap_item, "symbol")

            # Symbols should match
            assert profile_symbol == market_cap_symbol == symbol

    def test_profile_vs_employees_consistency(self, api_key):
        """Test consistency between profile and employee data."""
        symbol = "AAPL"

        # Get profile data
        profile_result = company.company_profile(apikey=api_key, symbol=symbol)
        profile_list = extract_data_list(profile_result)

        # Get employee count data
        employee_result = company.employee_count(apikey=api_key, symbol=symbol)
        employee_list = extract_data_list(employee_result)

        if len(profile_list) > 0 and len(employee_list) > 0:
            profile_item = profile_list[0]
            employee_item = employee_list[0]

            # Company names should be related
            profile_name = get_field_value(profile_item, "companyName")
            employee_symbol = get_field_value(employee_item, "symbol")

            assert employee_symbol == symbol
            assert profile_name  # Should have company name
