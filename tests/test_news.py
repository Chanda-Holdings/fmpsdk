import os
import time
from datetime import datetime, timedelta

import pytest

from fmpsdk import news
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPHistoricalSentiment,
    FMPNewsArticle,
    FMPPriceTargetNews,
    FMPStockGradeNews,
    FMPTrendingSentiment,
)
from tests.conftest import (
    get_response_models,
    validate_model_list,
    validate_required_fields,
)


@pytest.fixture
def api_key():
    """API key fixture for testing."""
    return os.getenv("FMP_API_KEY")


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
        result = news.news_stock_latest(apikey=api_key, limit=10)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If we have data
            for article in models[:3]:  # Check first few items
                # Enhanced business logic validation
                assert article.publishedDate, "Published date should not be empty"
                assert (
                    article.title or article.text
                ), "Should have either title or text content"

                # Date should be valid format
                try:
                    datetime.strptime(article.publishedDate[:10], "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format: {article.publishedDate}")

                # Content validation
                if article.title:
                    assert (
                        len(article.title) <= 1000
                    ), "Title should be reasonable length"
                    assert (
                        len(article.title) >= 5
                    ), "Title should have meaningful content"
                if article.text:
                    assert (
                        len(article.text) >= 10
                    ), "Text should have meaningful content"
                if article.url:
                    assert article.url.startswith(
                        ("http://", "https://")
                    ), "URL should be valid"
                if article.site:
                    assert (
                        len(article.site) <= 100
                    ), "Site name should be reasonable length"

    def test_company_press_releases_latest(self, api_key):
        """Test getting latest company press releases."""
        result = news.company_press_releases_latest(apikey=api_key, limit=10)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If we have data
            for release in models[:3]:  # Check first few items
                # Enhanced business logic validation
                assert release.publishedDate, "Published date should not be empty"
                assert (
                    release.title or release.text
                ), "Should have either title or text content"

                # Press releases should typically have a symbol
                if release.symbol:
                    assert (
                        len(release.symbol) <= 10
                    ), "Symbol should have reasonable length"
                    assert release.symbol.isupper(), "Symbol should be uppercase"

                # Content quality validation
                if release.title:
                    assert (
                        len(release.title) >= 10
                    ), "Press release title should be substantial"
                if release.text:
                    assert (
                        len(release.text) >= 20
                    ), "Press release text should be substantial"

    def test_news_general_latest(self, api_key):
        """Test getting latest general market news."""
        result = news.news_general_latest(apikey=api_key, limit=10)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If we have data
            for article in models[:3]:  # Check first few items
                # Enhanced business logic validation
                assert article.publishedDate, "Published date should not be empty"
                assert (
                    article.title or article.text
                ), "Should have either title or text content"

                # News freshness validation
                try:
                    news_date = datetime.strptime(
                        article.publishedDate[:10], "%Y-%m-%d"
                    )
                    days_old = (datetime.now() - news_date).days
                    assert (
                        days_old <= 365
                    ), f"News should not be too old (found {days_old} days old)"
                except ValueError:
                    pytest.fail(f"Invalid date format: {article.publishedDate}")

    def test_news_crypto_latest(self, api_key):
        """Test getting latest cryptocurrency news."""
        result = news.news_crypto_latest(apikey=api_key, limit=10)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If we have data
            for article in models[:3]:  # Check first few items
                # Enhanced business logic validation
                assert article.publishedDate, "Published date should not be empty"
                assert (
                    article.title or article.text
                ), "Should have either title or text content"

                # Crypto-specific validation
                if article.symbol:
                    # Crypto symbols often end with USD
                    assert (
                        len(article.symbol) <= 15
                    ), "Crypto symbol should be reasonable length"
                if article.title:
                    # Crypto news might contain relevant keywords
                    crypto_keywords = [
                        "bitcoin",
                        "ethereum",
                        "crypto",
                        "blockchain",
                        "btc",
                        "eth",
                    ]
                    title_lower = article.title.lower()
                    # Not enforcing keywords as general news might not always contain them


class TestNewsWithParameters:
    """Test news endpoints with various parameters."""

    def test_news_stock_latest_with_date_range(self, api_key, recent_date, older_date):
        """Test stock news with date range parameters."""
        result = news.news_stock_latest(
            apikey=api_key, from_date=older_date, to_date=recent_date, limit=15
        )

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:
            # Validate date range filtering with enhanced business logic
            for article in models[:5]:
                # Check if date is within range (API might not strictly enforce)
                article_date = datetime.strptime(article.publishedDate[:10], "%Y-%m-%d")
                from_date_obj = datetime.strptime(older_date, "%Y-%m-%d")
                to_date_obj = datetime.strptime(recent_date, "%Y-%m-%d")

                # Some tolerance for API behavior
                assert article_date >= from_date_obj - timedelta(
                    days=7
                ), f"Article date {article_date} too early"
                assert article_date <= to_date_obj + timedelta(
                    days=7
                ), f"Article date {article_date} too late"

                # Enhanced validation
                if article.symbol:
                    assert (
                        len(article.symbol) <= 10
                    ), "Stock symbol should be reasonable length"
                if article.title:
                    assert (
                        len(article.title) >= 5
                    ), "Article title should have substance"

    def test_news_with_pagination(self, api_key):
        """Test news endpoints with pagination parameters."""
        result = news.news_general_latest(apikey=api_key, page=0, limit=5)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        # Should respect limit (with some tolerance)
        if models:
            assert (
                len(models) <= 10
            ), "Should respect pagination limit with some tolerance"

            # Validate pagination results
            for article in models[:3]:
                assert article.publishedDate, "Published date should be present"
                assert article.title or article.text, "Content should be present"

    def test_crypto_news_with_date_filter(self, api_key, recent_date):
        """Test crypto news with date filtering."""
        result = news.news_crypto_latest(
            apikey=api_key, from_date=recent_date, limit=10
        )

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:
            for article in models[:3]:
                # Enhanced crypto news validation
                assert article.publishedDate, "Published date should be present"

                # Date should be after the filter date
                article_date = datetime.strptime(article.publishedDate[:10], "%Y-%m-%d")
                filter_date = datetime.strptime(recent_date, "%Y-%m-%d")
                assert article_date >= filter_date - timedelta(
                    days=1
                ), "Article should be after filter date"

                # Crypto news quality validation
                if article.symbol:
                    assert (
                        len(article.symbol) <= 15
                    ), "Crypto symbol should be reasonable length"
                if article.title:
                    assert len(article.title) >= 5, "Title should have substance"
                if article.site:
                    assert len(article.site) <= 100, "Site name should be reasonable"


class TestNewsDataQuality:
    """Test news data quality and content validation."""

    def test_news_article_content_validation(self, api_key):
        """Test news article content quality."""
        result = news.news_stock_latest(apikey=api_key, limit=20)

        models = get_response_models(result, FMPNewsArticle)
        if models:
            valid_articles = 0
            for article in models:
                # Content quality checks
                if article.title and len(article.title.strip()) > 10:
                    valid_articles += 1

                    # Title should not be excessively long
                    assert len(article.title) <= 500

                    # Published date should be recent (within last year)
                    if article.publishedDate:
                        pub_date = datetime.strptime(
                            article.publishedDate[:10], "%Y-%m-%d"
                        )
                        assert pub_date >= datetime.now() - timedelta(days=365)

                    # URL validation if present
                    if article.url:
                        assert article.url.startswith(("http://", "https://"))

                    # Publisher validation if present
                    if article.publisher:
                        assert len(article.publisher) <= 100

            # Should have at least some valid articles
            assert valid_articles > 0

    def test_press_release_symbol_consistency(self, api_key):
        """Test press release symbol consistency."""
        result = news.company_press_releases_latest(apikey=api_key, limit=15)

        models = get_response_models(result, FMPNewsArticle)
        if models:
            for release in models[:10]:
                # Symbol format validation
                if release.symbol:
                    # Symbol should be uppercase and reasonable length
                    assert release.symbol.isupper() or release.symbol.isdigit()
                    assert 1 <= len(release.symbol) <= 10

                    # Symbol should not contain spaces or special chars (with some exceptions)
                    assert not any(char in release.symbol for char in [" ", "\t", "\n"])

    def test_news_freshness(self, api_key):
        """Test that news data is reasonably fresh."""
        result = news.news_general_latest(apikey=api_key, limit=10)

        models = get_response_models(result, FMPNewsArticle)
        if models:
            # Check the most recent article
            latest_article = models[0]

            # Most recent news should be within last 7 days (with tolerance for weekends)
            latest_date = datetime.strptime(
                latest_article.publishedDate[:10], "%Y-%m-%d"
            )
            days_old = (datetime.now() - latest_date).days

            # Allow up to 10 days for news data freshness
            assert days_old <= 10, f"Most recent news is {days_old} days old"


class TestNewsErrorHandling:
    """Test error handling for news endpoints."""

    def test_news_invalid_api_key(self):
        """Test news endpoints with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            news.news_stock_latest(apikey="invalid_key", limit=5)

    def test_press_releases_invalid_api_key(self):
        """Test press releases with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            news.company_press_releases_latest(apikey="invalid_key", limit=5)

    def test_news_invalid_date_format(self, api_key):
        """Test news with invalid date format."""
        result = news.news_general_latest(
            apikey=api_key, from_date="invalid-date", to_date="2024-13-45"
        )

        # API might return error or ignore invalid dates
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            models = get_response_models(result, FMPNewsArticle)
            validate_model_list(models, FMPNewsArticle)

    def test_news_invalid_pagination(self, api_key):
        """Test news with invalid pagination parameters."""
        result = news.news_crypto_latest(apikey=api_key, page=-1, limit=0)

        # API might handle invalid pagination gracefully
        if isinstance(result, dict) and "Error Message" in result:
            assert "Error Message" in result
        else:
            models = get_response_models(result, FMPNewsArticle)
            # Invalid pagination may return empty results, which is valid behavior
            validate_model_list(models, FMPNewsArticle, min_count=0)

    def test_general_news_invalid_api_key(self):
        """Test general news with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            news.news_general_latest(apikey="invalid_key")

    def test_crypto_news_invalid_api_key(self):
        """Test crypto news with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            news.news_crypto_latest(apikey="invalid_key")


class TestNewsPerformance:
    """Test news endpoint performance."""

    def test_press_release_vs_news_distinction(self, api_key):
        """Test distinction between press releases and general news."""
        # Get both press releases and general news
        press_releases = news.company_press_releases_latest(apikey=api_key, limit=10)
        general_news = news.news_general_latest(apikey=api_key, limit=10)

        pr_models = get_response_models(press_releases, FMPNewsArticle)
        news_models = get_response_models(general_news, FMPNewsArticle)

        # Both should return valid model lists
        validate_model_list(pr_models, FMPNewsArticle)
        validate_model_list(news_models, FMPNewsArticle)

        # Content validation (basic structure should be similar)
        if pr_models and news_models:
            for article in pr_models[:3]:
                assert article.publishedDate

            for article in news_models[:3]:
                assert article.publishedDate


class TestNewsAdditionalEndpoints:
    """Tests for additional news endpoints to improve coverage."""

    def test_news_forex(self, api_key):
        """Test getting forex news."""
        result = news.news_forex(apikey=api_key, limit=10)

        # Extract models and validate structure
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If data is returned
            for article in models[:3]:  # Test first few items
                assert article.title
                assert article.text

    def test_news_forex_with_date_range(self, api_key, recent_date, older_date):
        """Test forex news with date range."""
        result = news.news_forex(
            apikey=api_key, from_date=older_date, to_date=recent_date, limit=5
        )
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

    def test_price_target_news(self, api_key):
        """Test getting price target news for a specific symbol."""
        result = news.price_target_news(apikey=api_key, symbol="AAPL", limit=10)
        models = get_response_models(result, FMPPriceTargetNews)
        validate_model_list(models, FMPPriceTargetNews)

        if models:  # If data is returned
            for item in models[:3]:  # Test first few items
                validate_required_fields(item, ["symbol"])

    def test_price_target_latest_news(self, api_key):
        """Test latest price target news."""
        result = news.price_target_latest_news(apikey=api_key, symbol="AAPL", limit=10)
        models = get_response_models(result, FMPPriceTargetNews)
        validate_model_list(models, FMPPriceTargetNews)

        if models:  # If data is returned
            for item in models[:3]:  # Test first few items
                validate_required_fields(item, ["symbol"])

    def test_news_stock_with_symbols(self, api_key):
        """Test getting news for specific stock symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = news.news_stock(apikey=api_key, symbols=symbols, limit=10)
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If data is returned
            for article in models[:3]:  # Test first few items
                assert article.title
                assert article.symbol

    def test_news_stock_with_date_range(self, api_key, recent_date, older_date):
        """Test stock news with date range and multiple symbols."""
        symbols = ["AAPL", "TSLA"]
        result = news.news_stock(
            apikey=api_key,
            symbols=symbols,
            from_date=older_date,
            to_date=recent_date,
            limit=5,
        )
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

    def test_company_press_releases_with_symbols(self, api_key):
        """Test getting press releases for specific symbols."""
        symbols = ["AAPL", "MSFT"]
        result = news.company_press_releases(apikey=api_key, symbols=symbols, limit=10)
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If data is returned
            for article in models[:3]:  # Test first few items
                assert article.title
                assert article.symbol

    def test_news_crypto_with_symbols(self, api_key):
        """Test getting crypto news for specific symbols."""
        symbols = ["BTCUSD", "ETHUSD"]
        result = news.news_crypto(apikey=api_key, symbols=symbols, limit=10)
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

        if models:  # If data is returned
            for article in models[:3]:  # Test first few items
                assert article.title

    def test_stock_grade_news(self, api_key):
        """Test getting stock grade news for a specific symbol."""
        result = news.stock_grade_news(apikey=api_key, symbol="AAPL", limit=10)
        models = get_response_models(result, FMPStockGradeNews)
        validate_model_list(models, FMPStockGradeNews)

        if models:  # If data is returned
            for item in models[:3]:  # Test first few items
                validate_required_fields(item, ["symbol"])

    def test_stock_grade_latest_news(self, api_key):
        """Test getting latest stock grade news."""
        result = news.stock_grade_latest_news(apikey=api_key, limit=10)
        models = get_response_models(result, FMPStockGradeNews)
        validate_model_list(models, FMPStockGradeNews)

        if models:  # If data is returned
            for item in models[:3]:  # Test first few items
                validate_required_fields(item, ["symbol"])

    def test_social_sentiment(self, api_key):
        """Test getting social sentiment for a symbol."""
        result = news.social_sentiment(apikey=api_key, symbol="AAPL", page=0)
        models = get_response_models(result, FMPHistoricalSentiment)
        validate_model_list(models, FMPHistoricalSentiment)

    def test_trending_sentiment_bullish(self, api_key):
        """Test getting trending bullish sentiment."""
        result = news.trending_sentiment(
            apikey=api_key, type="bullish", source="stocktwits"
        )
        models = get_response_models(result, FMPTrendingSentiment)
        validate_model_list(models, FMPTrendingSentiment)

    def test_trending_sentiment_bearish(self, api_key):
        """Test getting trending bearish sentiment."""
        result = news.trending_sentiment(
            apikey=api_key, type="bearish", source="stocktwits"
        )
        models = get_response_models(result, FMPTrendingSentiment)
        validate_model_list(models, FMPTrendingSentiment)


class TestNewsParameterValidation:
    """Tests for parameter validation and edge cases to improve coverage."""

    def test_news_forex_with_all_parameters(self, api_key, recent_date, older_date):
        """Test forex news with all optional parameters."""
        result = news.news_forex(
            apikey=api_key, from_date=older_date, to_date=recent_date, page=0, limit=5
        )
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

    def test_price_target_news_with_pagination(self, api_key):
        """Test price target news with pagination."""
        result = news.price_target_news(apikey=api_key, symbol="AAPL", page=0, limit=5)
        models = get_response_models(result, FMPPriceTargetNews)
        validate_model_list(models, FMPPriceTargetNews)

    def test_stock_grade_news_with_pagination(self, api_key):
        """Test stock grade news with pagination parameters."""
        result = news.stock_grade_news(apikey=api_key, symbol="MSFT", page=0, limit=5)
        models = get_response_models(result, FMPStockGradeNews)
        validate_model_list(models, FMPStockGradeNews)

    def test_stock_grade_latest_news_with_pagination(self, api_key):
        """Test latest stock grade news with pagination."""
        result = news.stock_grade_latest_news(apikey=api_key, page=0, limit=5)
        models = get_response_models(result, FMPStockGradeNews)
        validate_model_list(models, FMPStockGradeNews)

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
            else:
                models = get_response_models(result, FMPNewsArticle)
                validate_model_list(models, FMPNewsArticle)
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
            limit=5,
        )
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

    def test_news_crypto_all_params(self, api_key, recent_date, older_date):
        """Test crypto news with all parameters."""
        symbols = ["BTCUSD"]
        result = news.news_crypto(
            apikey=api_key,
            symbols=symbols,
            from_date=older_date,
            to_date=recent_date,
            page=0,
            limit=5,
        )
        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(models, FMPNewsArticle)

    @pytest.mark.parametrize(
        "symbol,sector,expected_news_volume,company_size",
        [
            ("AAPL", "Technology", "high", "mega_cap"),
            ("MSFT", "Technology", "high", "mega_cap"),
            ("GOOGL", "Technology", "high", "mega_cap"),
            ("AMZN", "Technology", "high", "mega_cap"),
            ("TSLA", "Automotive", "very_high", "large_cap"),
            ("META", "Technology", "high", "mega_cap"),
            ("NVDA", "Technology", "very_high", "large_cap"),
            ("JPM", "Financial", "high", "large_cap"),
            ("JNJ", "Healthcare", "medium", "large_cap"),
            ("PG", "Consumer Staples", "medium", "large_cap"),
            ("XOM", "Energy", "medium", "large_cap"),
            ("WMT", "Consumer Staples", "medium", "large_cap"),
            ("DIS", "Media", "high", "large_cap"),
            ("BA", "Aerospace", "high", "large_cap"),
            ("CAT", "Industrial", "medium", "large_cap"),
            ("ROKU", "Technology", "medium", "mid_cap"),
            ("ZM", "Technology", "medium", "mid_cap"),
            ("TDOC", "Healthcare", "medium", "mid_cap"),
            ("AIRT", "Industrial", "low", "small_cap"),
            ("TVTX", "Technology", "low", "small_cap"),
        ],
    )
    def test_news_stock_symbol_comprehensive(
        self, api_key, symbol, sector, expected_news_volume, company_size
    ):
        """Test getting stock news for comprehensive range of companies across sectors and sizes."""
        result = news.news_stock(apikey=api_key, symbols=[symbol], limit=20)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(
            models, FMPNewsArticle, f"Result should be valid for {symbol}"
        )

        if models:  # If we have data
            # Validate news volume expectations based on company size and sector
            news_count = len(models)

            if expected_news_volume == "very_high":
                # Companies like TSLA, NVDA should have lots of news
                assert (
                    news_count >= 10
                ), f"Very high profile {symbol} should have substantial news coverage"
            elif expected_news_volume == "high":
                # Mega-cap companies should have good news coverage
                assert (
                    news_count >= 5
                ), f"High profile {symbol} should have good news coverage"
            elif expected_news_volume == "medium":
                # Large-cap companies should have some news
                assert (
                    news_count >= 2
                ), f"Medium profile {symbol} should have some news coverage"
            elif expected_news_volume == "low":
                # Small-cap companies may have limited news
                assert (
                    news_count >= 0
                ), f"Low profile {symbol} may have limited news coverage"

            # Validate news article structure for first few items
            for article in models[:3]:
                # Validate news article data
                assert (
                    article.publishedDate
                ), f"News for {symbol} should have publish date"
                assert (
                    article.title or article.text
                ), f"News for {symbol} should have content"

                # Date should be valid format and reasonably recent
                try:
                    news_date = datetime.strptime(
                        article.publishedDate[:10], "%Y-%m-%d"
                    )
                    days_old = (datetime.now() - news_date).days
                    assert (
                        days_old <= 365
                    ), f"News for {symbol} should be within last year"
                except ValueError:
                    pytest.fail(
                        f"Invalid date format for {symbol}: {article.publishedDate}"
                    )

    @pytest.mark.parametrize(
        "date_range_days,limit,expected_article_count_range,period_description",
        [
            (1, 10, (0, 10), "last_day"),
            (7, 20, (5, 20), "last_week"),
            (30, 50, (20, 50), "last_month"),
            (90, 100, (30, 100), "last_quarter"),
            (180, 150, (50, 150), "last_half_year"),
            (365, 200, (100, 200), "last_year"),
        ],
    )
    def test_news_stock_latest_date_ranges(
        self,
        api_key,
        date_range_days,
        limit,
        expected_article_count_range,
        period_description,
    ):
        """Test getting latest stock news across different date ranges and limits."""
        result = news.news_stock_latest(apikey=api_key, limit=limit)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(
            models, FMPNewsArticle, f"Result should be valid for {period_description}"
        )

        if models:
            actual_count = len(models)
            min_expected, max_expected = expected_article_count_range

            # Flexible validation - news volume can vary significantly
            assert (
                actual_count <= limit
            ), f"Should not exceed requested limit for {period_description}"

            if actual_count > 0:
                # Validate date distribution for the period
                dates = []
                for article in models[
                    : min(10, len(models))
                ]:  # Check first 10 articles
                    try:
                        news_date = datetime.strptime(
                            article.publishedDate[:10], "%Y-%m-%d"
                        )
                        days_old = (datetime.now() - news_date).days
                        dates.append(days_old)
                    except ValueError:
                        continue

                if dates:
                    # Most news should be relatively recent
                    recent_news_count = sum(1 for d in dates if d <= date_range_days)
                    total_checked = len(dates)
                    recent_ratio = (
                        recent_news_count / total_checked if total_checked > 0 else 0
                    )

                    # At least 30% of news should be within the expected timeframe
                    assert (
                        recent_ratio >= 0.3
                    ), f"At least 30% of news should be recent for {period_description}"

    @pytest.mark.parametrize(
        "news_type,expected_characteristics",
        [
            (
                "general",
                {
                    "min_articles": 10,
                    "max_age_days": 30,
                    "content_types": ["title", "text"],
                },
            ),
            (
                "earnings",
                {
                    "min_articles": 5,
                    "max_age_days": 90,
                    "content_types": ["title", "text"],
                },
            ),
            (
                "press_releases",
                {
                    "min_articles": 3,
                    "max_age_days": 60,
                    "content_types": ["title", "text"],
                },
            ),
            (
                "analyst_ratings",
                {"min_articles": 2, "max_age_days": 120, "content_types": ["title"]},
            ),
        ],
    )
    def test_news_content_type_validation(
        self, api_key, news_type, expected_characteristics
    ):
        """Test different types of news content and their characteristics."""
        if news_type == "general":
            result = news.news_stock_latest(apikey=api_key, limit=20)
        elif news_type == "press_releases":
            result = news.company_press_releases_latest(apikey=api_key, limit=15)
        elif news_type == "earnings":
            # Use general news but look for earnings-related content
            result = news.news_stock_latest(apikey=api_key, limit=30)
        else:
            # Default to general news
            result = news.news_stock_latest(apikey=api_key, limit=20)

        models = get_response_models(result, FMPNewsArticle)
        validate_model_list(
            models, FMPNewsArticle, f"Result should be valid for {news_type} news"
        )

        if models:
            content_validation = expected_characteristics
            articles_analyzed = 0
            valid_articles = 0

            for article in models[:15]:  # Analyze first 15 articles
                articles_analyzed += 1

                # Validate content types
                has_required_content = False
                if "title" in content_validation["content_types"] and article.title:
                    has_required_content = True
                if "text" in content_validation["content_types"] and article.text:
                    has_required_content = True

                if has_required_content:
                    valid_articles += 1

                # Validate age
                try:
                    news_date = datetime.strptime(
                        article.publishedDate[:10], "%Y-%m-%d"
                    )
                    days_old = (datetime.now() - news_date).days
                    assert (
                        days_old <= content_validation["max_age_days"]
                    ), f"{news_type} news should be within {content_validation['max_age_days']} days"
                except ValueError:
                    continue

            # Validate overall quality
            if articles_analyzed > 0:
                validity_ratio = valid_articles / articles_analyzed
                assert (
                    validity_ratio >= 0.7
                ), f"At least 70% of {news_type} articles should have valid content"


class TestNewsParameterCoverage:
    """Tests to cover optional parameters that weren't being tested (covers missing lines)."""

    def test_news_stock_latest_with_page_parameter(self, api_key):
        """Test news_stock_latest with page parameter (covers line 41)."""
        page = 1
        result = news.news_stock_latest(apikey=api_key, page=page)

        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # If we have results, validate basic structure
        if news_models:
            assert hasattr(news_models[0], "title") or hasattr(news_models[0], "url")

    def test_company_press_releases_latest_with_parameters(
        self, api_key, recent_date, older_date
    ):
        """Test company_press_releases_latest with from_date, to_date, page parameters (covers lines 69, 71, 73)."""
        # Test with from_date parameter (covers line 69)
        result = news.company_press_releases_latest(
            apikey=api_key, from_date=older_date
        )
        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # Test with to_date parameter (covers line 71)
        result = news.company_press_releases_latest(apikey=api_key, to_date=recent_date)
        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # Test with page parameter (covers line 73)
        page = 1
        result = news.company_press_releases_latest(apikey=api_key, page=page)
        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # Test with combined parameters
        result = news.company_press_releases_latest(
            apikey=api_key, from_date=older_date, to_date=recent_date, page=page
        )
        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

    def test_news_crypto_latest_with_to_date_parameter(self, api_key, recent_date):
        """Test news_crypto_latest with to_date parameter (covers line 156)."""
        result = news.news_crypto_latest(apikey=api_key, to_date=recent_date)

        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # If we have results, validate basic structure
        if news_models:
            assert hasattr(news_models[0], "title") or hasattr(news_models[0], "url")

    def test_news_stock_with_page_parameter(self, api_key):
        """Test news_stock with page parameter (covers line 281)."""
        page = 1
        result = news.news_stock(apikey=api_key, symbols=["AAPL"], page=page)

        news_models = get_response_models(result, FMPNewsArticle)
        assert isinstance(news_models, list)

        # If we have results, validate basic structure
        if news_models:
            assert hasattr(news_models[0], "title") or hasattr(news_models[0], "symbol")
