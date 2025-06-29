"""
Integration tests for company_valuation endpoints.
Requires a valid FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest

import fmpsdk.company_valuation as cv

API_KEY = os.getenv("FMP_API_KEY")


@pytest.mark.parametrize(
    "func,kwargs",
    [
        (cv.company_profile, {"symbol": "AAPL"}),
        (cv.company_profile_cik, {"cik": "0000320193"}),
        (cv.stock_peers, {"symbol": "AAPL"}),
        (cv.delisted_companies, {}),
        (cv.employee_count, {"symbol": "AAPL"}),
        (cv.historical_employee_count, {"symbol": "AAPL"}),
        (cv.income_statement, {"symbol": "AAPL"}),
        (cv.balance_sheet_statement, {"symbol": "AAPL"}),
        (cv.cash_flow_statement, {"symbol": "AAPL"}),
        (cv.financial_statement_symbol_lists, {}),
        (cv.income_statement_growth, {"symbol": "AAPL"}),
        (cv.balance_sheet_statement_growth, {"symbol": "AAPL"}),
        (cv.cash_flow_statement_growth, {"symbol": "AAPL"}),
        (cv.income_statement_as_reported, {"symbol": "AAPL"}),
        (cv.balance_sheet_statement_as_reported, {"symbol": "AAPL"}),
        (cv.cash_flow_statement_as_reported, {"symbol": "AAPL"}),
        (cv.financial_statement_full_as_reported, {"symbol": "AAPL"}),
        (cv.financial_ratios_ttm, {"symbol": "AAPL"}),
        (cv.financial_ratios, {"symbol": "AAPL"}),
        (cv.enterprise_values, {"symbol": "AAPL"}),
        (cv.key_metrics_ttm, {"symbol": "AAPL"}),
        (cv.key_metrics, {"symbol": "AAPL"}),
        (cv.financial_growth, {"symbol": "AAPL"}),
        (cv.rating, {"symbol": "AAPL"}),
        (cv.historical_rating, {"symbol": "AAPL"}),
        (cv.upgrades_downgrades_consensus, {"symbol": "AAPL"}),
        (cv.discounted_cash_flow, {"symbol": "AAPL"}),
        (cv.historical_discounted_cash_flow, {"symbol": "AAPL"}),
        (cv.historical_daily_discounted_cash_flow, {"symbol": "AAPL"}),
        (cv.market_capitalization, {"symbol": "AAPL"}),
        (cv.historical_market_capitalization, {"symbol": "AAPL"}),
        (cv.analyst_estimates, {"symbol": "AAPL"}),
        (cv.ratings_snapshot, {"symbol": "AAPL"}),
        (cv.ratings_historical, {"symbol": "AAPL"}),
        (cv.price_target_summary, {"symbol": "AAPL"}),
        (cv.price_target_consensus, {"symbol": "AAPL"}),
        (cv.price_target_news, {"symbol": "AAPL"}),
        (cv.esg_disclosures, {"symbol": "AAPL"}),
        (cv.esg_ratings, {"symbol": "AAPL"}),
        (cv.esg_benchmark, {"symbol": "AAPL"}),
        (cv.earnings, {"symbol": "AAPL"}),
        (cv.company_notes, {"symbol": "AAPL"}),
        (cv.market_capitalization_batch, {"symbols": "AAPL,MSFT"}),
        (cv.stock_grades, {"symbol": "AAPL"}),
        (cv.historical_stock_grades, {"symbol": "AAPL"}),
        (cv.stock_grades_summary, {"symbol": "AAPL"}),
        (cv.stock_grade_news, {"symbol": "AAPL"}),
        (cv.stock_grade_latest_news, {}),
        (cv.financial_reports_xlsx, {"symbol": "AAPL", "year": 2023}),
    ],
)
def test_company_valuation_endpoints(func, kwargs):
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)
    assert result is not None, f"{func.__name__} returned None"


def test_financial_statements_with_periods():
    """Test financial statements with different periods (annual vs quarterly)."""
    # Test annual data
    result = cv.income_statement(
        apikey=API_KEY, symbol="AAPL", period="annual", limit=5
    )
    assert result is not None

    # Test quarterly data
    result = cv.income_statement(
        apikey=API_KEY, symbol="AAPL", period="quarter", limit=5
    )
    assert result is not None

    # Test balance sheet quarterly
    result = cv.balance_sheet_statement(
        apikey=API_KEY, symbol="AAPL", period="quarter", limit=5
    )
    assert result is not None

    # Test cash flow quarterly
    result = cv.cash_flow_statement(
        apikey=API_KEY, symbol="AAPL", period="quarter", limit=5
    )
    assert result is not None


def test_financial_ratios_and_metrics():
    """Test various financial ratios and metrics endpoints."""
    # Test TTM ratios
    result = cv.financial_ratios_ttm(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test annual ratios
    result = cv.financial_ratios(
        apikey=API_KEY, symbol="AAPL", period="annual", limit=5
    )
    assert result is not None

    # Test quarterly ratios
    result = cv.financial_ratios(
        apikey=API_KEY, symbol="AAPL", period="quarter", limit=5
    )
    assert result is not None

    # Test enterprise values
    result = cv.enterprise_values(
        apikey=API_KEY, symbol="AAPL", period="annual", limit=5
    )
    assert result is not None


def test_valuation_models():
    """Test various valuation model endpoints."""
    # Test basic DCF
    result = cv.discounted_cash_flow(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test levered DCF
    result = cv.levered_discounted_cash_flow(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test custom DCF models
    result = cv.custom_discounted_cash_flow(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    result = cv.custom_levered_discounted_cash_flow(apikey=API_KEY, symbol="AAPL")
    assert result is not None


def test_historical_data_with_date_ranges():
    """Test historical data endpoints with date ranges."""
    # Test historical market cap with date range
    result = cv.historical_market_capitalization(
        apikey=API_KEY,
        symbol="AAPL",
        from_date="2024-01-01",
        to_date="2024-03-31",
        limit=10,
    )
    assert result is not None

    # Test historical DCF
    result = cv.historical_discounted_cash_flow(
        apikey=API_KEY, symbol="AAPL", period="annual", limit=5
    )
    assert result is not None

    # Test historical daily DCF
    result = cv.historical_daily_discounted_cash_flow(
        apikey=API_KEY, symbol="AAPL", limit=30
    )
    assert result is not None


def test_analyst_coverage():
    """Test analyst-related endpoints."""
    # Test analyst estimates
    result = cv.analyst_estimates(
        apikey=API_KEY, symbol="AAPL", period="annual", limit=5
    )
    assert result is not None

    # Test quarterly estimates
    result = cv.analyst_estimates(
        apikey=API_KEY, symbol="AAPL", period="quarter", limit=5
    )
    assert result is not None

    # Test ratings snapshot
    result = cv.ratings_snapshot(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test historical ratings
    result = cv.ratings_historical(
        apikey=API_KEY, symbol="AAPL", from_date="2024-01-01", to_date="2024-12-31"
    )
    assert result is not None


def test_price_targets():
    """Test price target related endpoints."""
    # Test price target summary
    result = cv.price_target_summary(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test price target consensus
    result = cv.price_target_consensus(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test price target news
    result = cv.price_target_news(apikey=API_KEY, symbol="AAPL", limit=10)
    assert result is not None


def test_esg_data():
    """Test ESG (Environmental, Social, Governance) endpoints."""
    # Test ESG disclosures
    result = cv.esg_disclosures(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test ESG ratings
    result = cv.esg_ratings(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test ESG benchmark
    result = cv.esg_benchmark(apikey=API_KEY, symbol="AAPL")
    assert result is not None


def test_screener_functionality():
    """Test stock screener with various parameters."""
    # Test basic screener
    result = cv.stock_screener(apikey=API_KEY, limit=10)
    assert result is not None

    # Test screener with market cap filter
    result = cv.stock_screener(
        apikey=API_KEY,
        market_cap_more_than=1000000000,  # $1B+
        market_cap_lower_than=1000000000000,  # $1T-
        limit=10,
    )
    assert result is not None

    # Test screener with sector filter
    result = cv.stock_screener(apikey=API_KEY, sector="Technology", limit=10)
    assert result is not None

    # Test screener with multiple filters
    result = cv.stock_screener(
        apikey=API_KEY,
        market_cap_more_than=10000000000,  # $10B+
        beta_more_than=0.5,
        beta_lower_than=2.0,
        limit=5,
    )
    assert result is not None


def test_multiple_symbols_batch():
    """Test endpoints that support multiple symbols."""
    symbols = ["AAPL", "MSFT", "GOOGL"]

    # Test market cap batch
    result = cv.market_capitalization_batch(apikey=API_KEY, symbols=symbols)
    assert result is not None


def test_earnings_and_transcripts():
    """Test earnings and transcript related endpoints."""
    # Test earnings surprises
    result = cv.earnings_surprises(apikey=API_KEY, symbol="AAPL")
    assert result is not None

    # Test earning call transcript (recent quarter)
    result = cv.earning_call_transcript(
        apikey=API_KEY, symbol="AAPL", year=2024, quarter=1
    )
    assert result is not None

    # Test batch transcript
    result = cv.batch_earning_call_transcript(apikey=API_KEY, symbol="AAPL", year=2024)
    assert result is not None

    # Test available transcript dates
    result = cv.earning_call_transcripts_available_dates(apikey=API_KEY, symbol="AAPL")
    assert result is not None


def test_sec_filings():
    """Test SEC filings endpoint."""
    # Test general SEC filings
    result = cv.sec_filings(apikey=API_KEY, symbol="AAPL", limit=10)
    assert result is not None

    # Test specific filing type
    result = cv.sec_filings(apikey=API_KEY, symbol="AAPL", filing_type="10-K", limit=5)
    assert result is not None


def test_different_company_types():
    """Test endpoints with different types of companies."""
    test_symbols = [
        "AAPL",  # Large cap tech
        "TSLA",  # Growth stock
        "BRK.A",  # Berkshire Hathaway (different structure)
        "JNJ",  # Healthcare/Dividend aristocrat
        "XOM",  # Energy sector
    ]

    for symbol in test_symbols:
        # Test basic profile
        result = cv.company_profile(apikey=API_KEY, symbol=symbol)
        assert result is not None, f"Profile failed for {symbol}"

        # Test financial data
        result = cv.income_statement(apikey=API_KEY, symbol=symbol, limit=1)
        assert result is not None, f"Income statement failed for {symbol}"

        # Test market cap
        result = cv.market_capitalization(apikey=API_KEY, symbol=symbol)
        assert result is not None, f"Market cap failed for {symbol}"
