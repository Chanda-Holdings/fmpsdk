from datetime import datetime, timedelta
from typing import Dict

from fmpsdk import insider_trades
from fmpsdk.models import (
    FMPAcquisitionOwnership,
    FMPInsiderTrade,
    FMPInsiderTradeStatistics,
    FMPInsiderTransactionType,
)
from tests.conftest import extract_data_list


class TestInsiderTrading:
    """Test the main insider trading search endpoint."""

    def test_insider_trading_basic(self, api_key):
        """Test basic insider trading search."""
        result = insider_trades.insider_trading(apikey=api_key, symbol="AAPL", limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:  # If data is available
            assert len(result_list) <= 10

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "symbol" in first_item
                assert "filingDate" in first_item
                assert "transactionDate" in first_item
                assert "reportingCik" in first_item
                assert "companyCik" in first_item
                assert "transactionType" in first_item

                # Test Pydantic model validation
                trade = FMPInsiderTrade(**first_item)
                assert trade.symbol == first_item["symbol"]
                assert trade.filingDate == first_item["filingDate"]
                assert trade.transactionDate == first_item["transactionDate"]
            else:
                # Already a Pydantic model
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "transactionDate")

    def test_insider_trading_with_filters(self, api_key):
        """Test insider trading with various filters."""
        result = insider_trades.insider_trading(
            apikey=api_key, symbol="TSLA", transactionType="P-Purchase", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            assert len(result_list) <= 5
            for item in result_list[:3]:  # Check first few items
                if isinstance(item, dict):
                    assert item["symbol"] == "TSLA"
                    # Note: transactionType filter may not be strictly enforced by API
                else:
                    assert item.symbol == "TSLA"

    def test_insider_trading_by_cik(self, api_key):
        """Test insider trading search by company CIK."""
        # Apple's CIK
        result = insider_trades.insider_trading(
            apikey=api_key, companyCik="320193", limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # API returns padded CIK (e.g., "0000320193")
                    assert item["companyCik"].endswith("320193")
                else:
                    assert item.companyCik.endswith("320193")

    def test_insider_trading_pagination(self, api_key):
        """Test pagination in insider trading search."""
        result_page1 = insider_trades.insider_trading(
            apikey=api_key, symbol="MSFT", page=0, limit=5
        )

        result_page2 = insider_trades.insider_trading(
            apikey=api_key, symbol="MSFT", page=1, limit=5
        )

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

        # If both pages have data, they should be different
        if result_list1 and result_list2:
            # Compare transaction dates or filing dates to ensure different results
            page1_dates = set()
            page2_dates = set()

            for item in result_list1:
                if isinstance(item, dict):
                    page1_dates.add(item.get("filingDate", ""))
                else:
                    page1_dates.add(item.filingDate)

            for item in result_list2:
                if isinstance(item, dict):
                    page2_dates.add(item.get("filingDate", ""))
                else:
                    page2_dates.add(item.filingDate)

            # Some items should be different between pages
            assert len(page1_dates.intersection(page2_dates)) < max(
                len(page1_dates), len(page2_dates)
            )

    def test_insider_trading_invalid_symbol(self, api_key):
        """Test insider trading with invalid symbol."""
        result = insider_trades.insider_trading(
            apikey=api_key, symbol="INVALID_SYMBOL_XYZ", limit=5
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid symbol
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_insider_trading_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.insider_trading(apikey=invalid_api_key, symbol="AAPL")

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestInsiderTradingLatest:
    """Test the latest insider trading endpoint."""

    def test_insider_trading_latest_basic(self, api_key):
        """Test basic latest insider trading data."""
        result = insider_trades.insider_trading_latest(apikey=api_key, limit=10)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            assert len(result_list) <= 10

            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "symbol" in first_item
                assert "filingDate" in first_item
                assert "transactionDate" in first_item

                # Test Pydantic model validation
                trade = FMPInsiderTrade(**first_item)
                assert trade.symbol == first_item["symbol"]
            else:
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "filingDate")

    def test_insider_trading_latest_with_date(self, api_key):
        """Test latest insider trading with date filter."""
        # Use recent date
        recent_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = insider_trades.insider_trading_latest(
            apikey=api_key, date=recent_date, limit=5
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        # Note: Results may be empty if no trades on specific date

    def test_insider_trading_latest_pagination(self, api_key):
        """Test pagination in latest insider trading."""
        result_page1 = insider_trades.insider_trading_latest(
            apikey=api_key, page=0, limit=5
        )

        result_page2 = insider_trades.insider_trading_latest(
            apikey=api_key, page=1, limit=5
        )

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_insider_trading_latest_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.insider_trading_latest(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestInsiderTradingReportingName:
    """Test the insider trading by reporting name endpoint."""

    def test_insider_trading_reporting_name_basic(self, api_key):
        """Test insider trading by reporting name."""
        # Use a common executive name
        result = insider_trades.insider_trading_reporting_name(
            apikey=api_key, name="COOK TIMOTHY D"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            # Check that results contain the reporting name
            for item in result_list[:3]:
                if isinstance(item, dict):
                    reporting_name = item.get("reportingName", "").upper()
                    assert "COOK" in reporting_name or "TIMOTHY" in reporting_name
                else:
                    reporting_name = getattr(item, "reportingName", "").upper()
                    assert "COOK" in reporting_name or "TIMOTHY" in reporting_name

    def test_insider_trading_reporting_name_invalid(self, api_key):
        """Test insider trading with invalid reporting name."""
        result = insider_trades.insider_trading_reporting_name(
            apikey=api_key, name="INVALID_PERSON_NAME_XYZ"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid name
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_insider_trading_reporting_name_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.insider_trading_reporting_name(
            apikey=invalid_api_key, name="COOK TIMOTHY D"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestInsiderTradingTransactionType:
    """Test the insider trading transaction types endpoint."""

    def test_insider_trading_transaction_type_basic(self, api_key):
        """Test getting insider trading transaction types."""
        result = insider_trades.insider_trading_transaction_type(apikey=api_key)

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                assert "transactionType" in first_item

                # Test Pydantic model validation
                transaction_type = FMPInsiderTransactionType(**first_item)
                assert transaction_type.transactionType == first_item["transactionType"]
            else:
                assert hasattr(first_item, "transactionType")

            # Check for common transaction types
            transaction_types = []
            for item in result_list:
                if isinstance(item, dict):
                    transaction_types.append(item["transactionType"])
                else:
                    transaction_types.append(item.transactionType)

            # Should contain common transaction types
            common_types = ["P-Purchase", "S-Sale", "A-Award", "J-Other"]
            found_types = [
                t for t in common_types if any(ct in transaction_types for ct in [t])
            ]
            assert len(found_types) > 0  # At least one common type should be found

    def test_insider_trading_transaction_type_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.insider_trading_transaction_type(apikey=invalid_api_key)

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestInsiderTradingStatistics:
    """Test the insider trading statistics endpoint."""

    def test_insider_trading_statistics_basic(self, api_key):
        """Test insider trading statistics for a symbol."""
        result = insider_trades.insider_trading_statistics(
            apikey=api_key, symbol="AAPL"
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "symbol" in first_item
                assert "cik" in first_item
                assert "year" in first_item
                assert "quarter" in first_item

                # Test Pydantic model validation
                stats = FMPInsiderTradeStatistics(**first_item)
                assert stats.symbol == first_item["symbol"]
                assert stats.cik == first_item["cik"]
            else:
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "year")
                assert hasattr(first_item, "quarter")

    def test_insider_trading_statistics_multiple_symbols(self, api_key):
        """Test insider trading statistics for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            result = insider_trades.insider_trading_statistics(
                apikey=api_key, symbol=symbol
            )

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            if result_list:
                for item in result_list[:2]:  # Check first few items
                    if isinstance(item, dict):
                        assert item["symbol"] == symbol
                    else:
                        assert item.symbol == symbol

    def test_insider_trading_statistics_invalid_symbol(self, api_key):
        """Test insider trading statistics with invalid symbol."""
        result = insider_trades.insider_trading_statistics(
            apikey=api_key, symbol="INVALID_SYMBOL_XYZ"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid symbol
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_insider_trading_statistics_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.insider_trading_statistics(
            apikey=invalid_api_key, symbol="AAPL"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestAcquisitionOwnership:
    """Test the acquisition of beneficial ownership endpoint."""

    def test_acquisition_ownership_basic(self, api_key):
        """Test acquisition of beneficial ownership data."""
        result = insider_trades.acquisition_ownership(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            # Test first item structure
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Validate required fields
                assert "cik" in first_item
                assert "symbol" in first_item
                assert "filingDate" in first_item
                assert "nameOfReportingPerson" in first_item

                # Test Pydantic model validation
                ownership = FMPAcquisitionOwnership(**first_item)
                assert ownership.symbol == first_item["symbol"]
                assert ownership.cik == first_item["cik"]
            else:
                assert hasattr(first_item, "symbol")
                assert hasattr(first_item, "cik")
                assert hasattr(first_item, "filingDate")
                assert hasattr(first_item, "nameOfReportingPerson")

    def test_acquisition_ownership_pagination(self, api_key):
        """Test pagination in acquisition ownership."""
        result_page1 = insider_trades.acquisition_ownership(
            apikey=api_key, symbol="MSFT", page=0
        )

        result_page2 = insider_trades.acquisition_ownership(
            apikey=api_key, symbol="MSFT", page=1
        )

        result_list1 = extract_data_list(result_page1)
        result_list2 = extract_data_list(result_page2)
        assert isinstance(result_list1, list)
        assert isinstance(result_list2, list)

    def test_acquisition_ownership_multiple_symbols(self, api_key):
        """Test acquisition ownership for multiple symbols."""
        symbols = ["AAPL", "TSLA", "GOOGL"]

        for symbol in symbols:
            result = insider_trades.acquisition_ownership(apikey=api_key, symbol=symbol)

            result_list = extract_data_list(result)
            assert isinstance(result_list, list)
            if result_list:
                for item in result_list[:2]:  # Check first few items
                    if isinstance(item, dict):
                        assert item["symbol"] == symbol
                    else:
                        assert item.symbol == symbol

    def test_acquisition_ownership_invalid_symbol(self, api_key):
        """Test acquisition ownership with invalid symbol."""
        result = insider_trades.acquisition_ownership(
            apikey=api_key, symbol="INVALID_SYMBOL_XYZ"
        )

        result_list = extract_data_list(result)
        # Should return empty list for invalid symbol
        assert isinstance(result_list, list)
        assert len(result_list) == 0

    def test_acquisition_ownership_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        invalid_api_key = "invalid_key_123"
        result = insider_trades.acquisition_ownership(
            apikey=invalid_api_key, symbol="AAPL"
        )

        # API returns error dict instead of raising exception
        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "Invalid API KEY" in result["Error Message"]


class TestInsiderTradesDataQuality:
    """Test data quality and business logic validation."""

    def test_insider_trading_data_consistency(self, api_key):
        """Test data consistency in insider trading records."""
        result = insider_trades.insider_trading(apikey=api_key, symbol="AAPL", limit=10)

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:5]:
                if isinstance(item, dict):
                    # Check date formats
                    assert len(item["filingDate"]) >= 10  # YYYY-MM-DD format
                    assert len(item["transactionDate"]) >= 10

                    # Check numeric fields
                    assert isinstance(item["securitiesOwned"], (int, float))
                    assert isinstance(item["securitiesTransacted"], (int, float))
                    assert isinstance(item["price"], (int, float))

                    # Check that price is positive
                    assert item["price"] >= 0

                    # Check transaction type is not empty
                    assert len(item["transactionType"]) > 0
                else:
                    # Pydantic model
                    assert len(item.filingDate) >= 10
                    assert len(item.transactionDate) >= 10
                    assert isinstance(item.securitiesOwned, (int, float))
                    assert isinstance(item.securitiesTransacted, (int, float))
                    assert isinstance(item.price, (int, float))
                    assert item.price >= 0
                    assert len(item.transactionType) > 0

    def test_insider_trading_statistics_calculations(self, api_key):
        """Test that insider trading statistics have logical values."""
        result = insider_trades.insider_trading_statistics(
            apikey=api_key, symbol="AAPL"
        )

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check that counts are non-negative
                    assert item["acquiredTransactions"] >= 0
                    assert item["disposedTransactions"] >= 0
                    assert item["totalPurchases"] >= 0
                    assert item["totalSales"] >= 0

                    # Check that ratio calculations make sense
                    if item["disposedTransactions"] > 0:
                        expected_ratio = (
                            item["acquiredTransactions"] / item["disposedTransactions"]
                        )
                        assert (
                            abs(item["acquiredDisposedRatio"] - expected_ratio) < 0.01
                        )

                    # Check that averages are positive when there are transactions
                    if item["acquiredTransactions"] > 0:
                        assert item["averageAcquired"] > 0
                    if item["disposedTransactions"] > 0:
                        assert item["averageDisposed"] > 0
                else:
                    # Pydantic model
                    assert item.acquiredTransactions >= 0
                    assert item.disposedTransactions >= 0
                    assert item.totalPurchases >= 0
                    assert item.totalSales >= 0

    def test_acquisition_ownership_data_quality(self, api_key):
        """Test data quality in acquisition ownership records."""
        result = insider_trades.acquisition_ownership(apikey=api_key, symbol="AAPL")

        result_list = extract_data_list(result)
        if result_list:
            for item in result_list[:3]:
                if isinstance(item, dict):
                    # Check that required fields are not empty
                    assert len(item["nameOfReportingPerson"]) > 0
                    assert len(item["cusip"]) > 0
                    assert len(item["filingDate"]) >= 10

                    # Check that ownership percentage is reasonable
                    percent_str = item["percentOfClass"]
                    if percent_str and percent_str != "":
                        try:
                            percent = float(percent_str.replace("%", ""))
                            assert 0 <= percent <= 100
                        except (ValueError, AttributeError):
                            # Some entries might have non-numeric values
                            pass
                else:
                    # Pydantic model
                    assert len(item.nameOfReportingPerson) > 0
                    assert len(item.cusip) > 0
                    assert len(item.filingDate) >= 10


class TestInsiderTradesPremiumEndpoints:
    """Test endpoints that may require premium access."""

    def test_premium_insider_trading_advanced_search(self, api_key):
        """Test advanced insider trading search features."""
        result = insider_trades.insider_trading(
            apikey=api_key, symbol="AAPL", transactionType="P-Purchase", limit=100
        )

        result_list = extract_data_list(result)
        assert isinstance(result_list, list)
        if result_list:
            # Premium endpoint might return more detailed data
            first_item = result_list[0]
            if isinstance(first_item, dict):
                # Check for additional premium fields
                premium_fields = ["url", "securityName", "typeOfOwner"]
                for field in premium_fields:
                    if field in first_item:
                        assert first_item[field] is not None

    def test_premium_insider_trading_bulk_data(self, api_key):
        """Test bulk insider trading data access."""
        result = insider_trades.insider_trading_latest(
            apikey=api_key, limit=1000  # Large limit might be premium feature
        )

        # Result should be a RootModel with a list in the root attribute
        assert hasattr(result, "root")
        assert isinstance(result.root, list)
        # Premium might allow larger result sets
        if len(result.root) > 100:
            assert True  # Successfully retrieved large dataset


# Additional test utilities
def validate_insider_trade_model(data: Dict) -> bool:
    """Validate that data conforms to FMPInsiderTrade model."""
    try:
        FMPInsiderTrade(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False


def validate_acquisition_ownership_model(data: Dict) -> bool:
    """Validate that data conforms to FMPAcquisitionOwnership model."""
    try:
        FMPAcquisitionOwnership(**data)
        return True
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False
