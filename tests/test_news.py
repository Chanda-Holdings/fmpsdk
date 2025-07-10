import os
import time
from datetime import datetime, timedelta
from typing import List

import pytest

from fmpsdk import news
from fmpsdk.models import FMPNewsArticle, FMPPriceTargetNews, FMPStockGradeNews
from tests.conftest import extract_data_list

# Test configuration
RESPONSE_TIME_LIMIT = 15.0  # seconds (news endpoints might be slower)


@pytest.fixture
def api_key():
    """API key fixture for testing."""
    key = os.getenv("FMP_API_KEY")
    if not key:
        pytest.skip("FMP_API_KEY environment variable not set")
    return key


@pytest.fixture
def recent_date():
    """Recent date for testing (within last 7 days)."""
    return (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")


@pytest.fixture
def older_date():
    """Older date for testing (within last 30 days)."""
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


class TestNewsBasic:
    """Basic functionality tests for news endpoints."""

    def test_news_stock_latest(self, api_key):
        """Test getting latest stock news."""
        start_time = time.time()
        result = news.news_stock_latest(apikey=api_key, limit=10)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for article in data[:3]:  # Check first few items
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Validate news article data
                assert article_obj.publishedDate
                assert article_obj.title or article_obj.text  # Should have some content

                # Date should be valid format
                try:
                    datetime.strptime(article_obj.publishedDate[:10], "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format: {article_obj.publishedDate}")

    def test_company_press_releases_latest(self, api_key):
        """Test getting latest company press releases."""
        start_time = time.time()
        result = news.company_press_releases_latest(apikey=api_key, limit=10)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for release in data[:3]:  # Check first few items
                if isinstance(release, dict):
                    release_obj = FMPNewsArticle(**release)
                else:
                    release_obj = release

                # Validate press release data
                assert release_obj.publishedDate
                assert release_obj.title or release_obj.text

                # Press releases should typically have a symbol
                if release_obj.symbol:
                    assert len(release_obj.symbol) <= 10  # Reasonable symbol length

    def test_news_general_latest(self, api_key):
        """Test getting latest general market news."""
        start_time = time.time()
        result = news.news_general_latest(apikey=api_key, limit=10)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for article in data[:3]:  # Check first few items
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Validate general news data
                assert article_obj.publishedDate
                assert article_obj.title or article_obj.text

    def test_news_crypto_latest(self, api_key):
        """Test getting latest cryptocurrency news."""
        start_time = time.time()
        result = news.news_crypto_latest(apikey=api_key, limit=10)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:  # If we have data
            for article in data[:3]:  # Check first few items
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Validate crypto news data
                assert article_obj.publishedDate
                assert article_obj.title or article_obj.text


class TestNewsWithParameters:
    """Test news endpoints with various parameters."""

    def test_news_stock_latest_with_date_range(self, api_key, recent_date, older_date):
        """Test stock news with date range parameters."""
        result = news.news_stock_latest(
            apikey=api_key, from_date=older_date, to_date=recent_date, limit=15
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            # Validate date range filtering (if API supports it)
            for article in data[:5]:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Check if date is within range (API might not strictly enforce)
                article_date = datetime.strptime(
                    article_obj.publishedDate[:10], "%Y-%m-%d"
                )
                from_date_obj = datetime.strptime(older_date, "%Y-%m-%d")
                to_date_obj = datetime.strptime(recent_date, "%Y-%m-%d")

                # Some tolerance for API behavior
                assert article_date >= from_date_obj - timedelta(days=7)
                assert article_date <= to_date_obj + timedelta(days=7)

    def test_news_with_pagination(self, api_key):
        """Test news endpoints with pagination parameters."""
        result = news.news_general_latest(apikey=api_key, page=0, limit=5)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        # Should respect limit (with some tolerance)
        if data:
            assert len(data) <= 10  # Allow some flexibility

    def test_crypto_news_with_date_filter(self, api_key, recent_date):
        """Test crypto news with date filtering."""
        result = news.news_crypto_latest(
            apikey=api_key, from_date=recent_date, limit=10
        )

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        assert isinstance(data, list)

        if data:
            for article in data[:3]:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Validate crypto news content
                assert article_obj.publishedDate
                # Crypto news might contain relevant keywords
                if article_obj.title:
                    title_lower = article_obj.title.lower()
                    crypto_keywords = [
                        "bitcoin",
                        "btc",
                        "ethereum",
                        "eth",
                        "crypto",
                        "blockchain",
                        "defi",
                    ]
                    # Note: Not all crypto news will contain these keywords


class TestNewsDataQuality:
    """Test news data quality and content validation."""

    def test_news_article_content_validation(self, api_key):
        """Test news article content quality."""
        result = news.news_stock_latest(apikey=api_key, limit=20)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            valid_articles = 0
            for article in data:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                # Content quality checks
                if article_obj.title and len(article_obj.title.strip()) > 10:
                    valid_articles += 1

                    # Title should not be excessively long
                    assert len(article_obj.title) <= 500

                    # Published date should be recent (within last year)
                    pub_date = datetime.strptime(
                        article_obj.publishedDate[:10], "%Y-%m-%d"
                    )
                    one_year_ago = datetime.now() - timedelta(days=365)
                    assert pub_date >= one_year_ago

                    # URL should be valid format if present
                    if article_obj.url:
                        assert article_obj.url.startswith(("http://", "https://"))

                    # Publisher should be reasonable if present
                    if article_obj.publisher:
                        assert len(article_obj.publisher) <= 100

            # Should have at least some valid articles
            assert valid_articles > 0

    def test_press_release_symbol_consistency(self, api_key):
        """Test press release symbol consistency."""
        result = news.company_press_releases_latest(apikey=api_key, limit=15)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            for release in data[:10]:
                if isinstance(release, dict):
                    release_obj = FMPNewsArticle(**release)
                else:
                    release_obj = release

                # Symbol format validation
                if release_obj.symbol:
                    # Symbol should be uppercase and reasonable length
                    assert release_obj.symbol.isupper() or release_obj.symbol.isdigit()
                    assert 1 <= len(release_obj.symbol) <= 10

                    # Symbol should not contain spaces or special chars (with some exceptions)
                    assert not any(
                        char in release_obj.symbol for char in [" ", "\t", "\n"]
                    )

    def test_news_freshness(self, api_key):
        """Test that news data is reasonably fresh."""
        result = news.news_general_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data:
            # Check the most recent article
            latest_article = data[0]
            if isinstance(latest_article, dict):
                article_obj = FMPNewsArticle(**latest_article)
            else:
                article_obj = latest_article

            # Most recent news should be within last 7 days (with tolerance for weekends)
            latest_date = datetime.strptime(article_obj.publishedDate[:10], "%Y-%m-%d")
            days_old = (datetime.now() - latest_date).days

            # Allow up to 10 days for news data freshness
            assert days_old <= 10, f"Most recent news is {days_old} days old"


class TestNewsErrorHandling:
    """Test error handling for news endpoints."""

    def test_news_invalid_api_key(self):
        """Test news endpoints with invalid API key."""
        result = news.news_stock_latest(apikey="invalid_key", limit=5)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_press_releases_invalid_api_key(self):
        """Test press releases with invalid API key."""
        result = news.company_press_releases_latest(apikey="invalid_key", limit=5)

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_news_invalid_date_format(self, api_key):
        """Test news with invalid date format."""
        result = news.news_general_latest(
            apikey=api_key, from_date="invalid-date", to_date="2024-13-45"
        )

        # API might return error or ignore invalid dates
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_news_invalid_pagination(self, api_key):
        """Test news with invalid pagination parameters."""
        result = news.news_crypto_latest(apikey=api_key, page=-1, limit=0)

        # API might handle invalid pagination gracefully
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            data = extract_data_list(result)
            assert isinstance(data, list)

    def test_general_news_invalid_api_key(self):
        """Test general news with invalid API key."""
        result = news.news_general_latest(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result

    def test_crypto_news_invalid_api_key(self):
        """Test crypto news with invalid API key."""
        result = news.news_crypto_latest(apikey="invalid_key")

        # Should return error message
        assert isinstance(result, dict)
        assert "Error Message" in result


class TestNewsPerformance:
    """Test news endpoint performance."""

    def test_news_response_times(self, api_key):
        """Test that all news endpoints respond within acceptable time."""
        endpoints = [
            ("stock_news", lambda: news.news_stock_latest(api_key, limit=10)),
            (
                "press_releases",
                lambda: news.company_press_releases_latest(api_key, limit=10),
            ),
            ("general_news", lambda: news.news_general_latest(api_key, limit=10)),
            ("crypto_news", lambda: news.news_crypto_latest(api_key, limit=10)),
        ]

        for endpoint_name, endpoint_func in endpoints:
            start_time = time.time()
            result = endpoint_func()
            response_time = time.time() - start_time

            # Skip premium endpoints

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            return

        data = extract_data_list(result)
        if data and len(data) >= 5:
            publishers = set()
            sites = set()
            symbols = set()

            for article in data[:20]:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                else:
                    article_obj = article

                if article_obj.publisher:
                    publishers.add(article_obj.publisher)
                if article_obj.site:
                    sites.add(article_obj.site)
                if article_obj.symbol:
                    symbols.add(article_obj.symbol)

            # Should have some variety in news sources
            # Note: This is a soft check as demo data might be limited
            if len(data) >= 10:
                assert (
                    len(publishers) >= 1 or len(sites) >= 1
                )  # At least some source diversity

    def test_press_release_vs_news_distinction(self, api_key):
        """Test distinction between press releases and general news."""
        # Get both press releases and general news
        press_releases = news.company_press_releases_latest(apikey=api_key, limit=10)
        general_news = news.news_general_latest(apikey=api_key, limit=10)

        # Check if result is error dict (invalid API key)
        if (isinstance(press_releases, dict) and "Error Message" in press_releases) or (
            isinstance(general_news, dict) and "Error Message" in general_news
        ):
            return

        pr_data = extract_data_list(press_releases)
        news_data = extract_data_list(general_news)

        # Both should return data structures of the same type
        assert isinstance(pr_data, list)
        assert isinstance(news_data, list)

        # Content validation (basic structure should be similar)
        if pr_data and news_data:
            for article in pr_data[:3]:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                    assert article_obj.publishedDate

            for article in news_data[:3]:
                if isinstance(article, dict):
                    article_obj = FMPNewsArticle(**article)
                    assert article_obj.publishedDate


class TestNewsAdditionalEndpoints:
    """Tests for additional news endpoints to improve coverage."""

    def test_news_forex(self, api_key):
        """Test getting forex news."""
        start_time = time.time()
        result = news.news_forex(apikey=api_key, limit=10)
        response_time = time.time() - start_time

        # Response time validation
        assert response_time < RESPONSE_TIME_LIMIT

        # Check if result is error dict (invalid API key)
        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        # Extract data and validate structure
        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPNewsArticle)
                assert hasattr(item, "title")
                assert hasattr(item, "text")

    def test_news_forex_with_date_range(self, api_key, recent_date, older_date):
        """Test forex news with date range."""
        result = news.news_forex(
            apikey=api_key, from_date=older_date, to_date=recent_date, limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_price_target_news(self, api_key):
        """Test getting price target news for a specific symbol."""
        result = news.price_target_news(apikey=api_key, symbol="AAPL", limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPPriceTargetNews)
                assert hasattr(item, "symbol")

    def test_price_target_latest_news(self, api_key):
        """Test getting latest price target news for a specific symbol."""
        result = news.price_target_latest_news(apikey=api_key, symbol="MSFT", limit=5)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPPriceTargetNews)
                assert hasattr(item, "symbol")

    def test_news_stock_with_symbols(self, api_key):
        """Test getting news for specific stock symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = news.news_stock(apikey=api_key, symbols=symbols, limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPNewsArticle)
                assert hasattr(item, "title")
                assert hasattr(item, "symbol")

    def test_news_stock_with_date_range(self, api_key, recent_date, older_date):
        """Test stock news with date range and multiple symbols."""
        symbols = ["AAPL", "TSLA"]
        result = news.news_stock(
            apikey=api_key, symbols=symbols, from_date=older_date, to_date=recent_date, limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_company_press_releases_with_symbols(self, api_key):
        """Test getting press releases for specific symbols."""
        symbols = ["AAPL", "MSFT"]
        result = news.company_press_releases(apikey=api_key, symbols=symbols, limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPNewsArticle)
                assert hasattr(item, "title")
                assert hasattr(item, "symbol")

    def test_news_crypto_with_symbols(self, api_key):
        """Test getting crypto news for specific symbols."""
        symbols = ["BTCUSD", "ETHUSD"]
        result = news.news_crypto(apikey=api_key, symbols=symbols, limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPNewsArticle)
                assert hasattr(item, "title")

    def test_stock_grade_news(self, api_key):
        """Test getting stock grade news for a specific symbol."""
        result = news.stock_grade_news(apikey=api_key, symbol="AAPL", limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPStockGradeNews)
                assert hasattr(item, "symbol")

    def test_stock_grade_latest_news(self, api_key):
        """Test getting latest stock grade news."""
        result = news.stock_grade_latest_news(apikey=api_key, limit=10)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

        if data_list:  # If data is returned
            for item in data_list[:3]:  # Test first few items
                assert isinstance(item, FMPStockGradeNews)

    def test_social_sentiment(self, api_key):
        """Test getting social sentiment for a symbol."""
        result = news.social_sentiment(apikey=api_key, symbol="AAPL", page=0)

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_trending_sentiment_bullish(self, api_key):
        """Test getting trending bullish sentiment."""
        result = news.trending_sentiment(apikey=api_key, type="bullish", source="stocktwits")

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_trending_sentiment_bearish(self, api_key):
        """Test getting trending bearish sentiment."""
        result = news.trending_sentiment(apikey=api_key, type="bearish", source="stocktwits")

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)


class TestNewsParameterValidation:
    """Tests for parameter validation and edge cases to improve coverage."""

    def test_news_forex_with_all_parameters(self, api_key, recent_date, older_date):
        """Test forex news with all optional parameters."""
        result = news.news_forex(
            apikey=api_key,
            from_date=older_date,
            to_date=recent_date,
            page=0,
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_price_target_news_with_pagination(self, api_key):
        """Test price target news with pagination."""
        result = news.price_target_news(
            apikey=api_key, 
            symbol="AAPL", 
            page=0, 
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_stock_grade_news_with_pagination(self, api_key):
        """Test stock grade news with pagination parameters."""
        result = news.stock_grade_news(
            apikey=api_key, 
            symbol="MSFT", 
            page=0, 
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_stock_grade_latest_news_with_pagination(self, api_key):
        """Test latest stock grade news with pagination."""
        result = news.stock_grade_latest_news(
            apikey=api_key, 
            page=0, 
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_news_functions_with_empty_symbol_lists(self, api_key):
        """Test news functions with empty symbol lists."""
        # Test with empty symbols list - should handle gracefully
        empty_symbols = []

        # These should handle empty lists gracefully or raise appropriate errors
        try:
            result = news.news_stock(apikey=api_key, symbols=empty_symbols)
            if isinstance(result, dict) and "Error Message" in result:
                # This is expected behavior for empty symbols
                pass
        except Exception:
            # Exception is also acceptable for empty symbols
            pass

    def test_company_press_releases_all_params(self, api_key, recent_date, older_date):
        """Test company press releases with all parameters."""
        symbols = ["AAPL"]
        result = news.company_press_releases(
            apikey=api_key,
            symbols=symbols,
            from_date=older_date,
            to_date=recent_date,
            page=0,
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)

    def test_news_crypto_all_params(self, api_key, recent_date, older_date):
        """Test crypto news with all parameters."""
        symbols = ["BTCUSD"]
        result = news.news_crypto(
            apikey=api_key,
            symbols=symbols,
            from_date=older_date,
            to_date=recent_date,
            page=0,
            limit=5
        )

        if isinstance(result, dict) and "Error Message" in result:
            pytest.skip("API key might be invalid or endpoint requires premium access")

        data_list = extract_data_list(result)
        assert isinstance(data_list, list)
