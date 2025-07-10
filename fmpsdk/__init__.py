"""
FMP Python SDK - Financial Modeling Prep API Python SDK

A comprehensive Python SDK for the Financial Modeling Prep (FMP) API.
This package provides easy access to financial data including company profiles,
financial statements, market data, and more.

Usage:
    from fmpsdk import company_profile, financial_ratios

    # Get company profile
    profile = company_profile(apikey="your_api_key", symbol="AAPL")

    # Get financial ratios
    ratios = financial_ratios(apikey="your_api_key", symbol="AAPL")
"""

# Analyst functions
from .analyst import (
    analyst_estimates,
    historical_stock_grades,
    price_target_consensus,
    price_target_summary,
    ratings_historical,
    ratings_snapshot,
    stock_grades,
    stock_grades_summary,
)

# Bulk data functions
from .bulk import (
    balance_sheet_statement_bulk,
    balance_sheet_statement_growth_bulk,
    bulk_profiles,
    cash_flow_statement_bulk,
    cash_flow_statement_growth_bulk,
    dcf_bulk,
    earnings_surprises_bulk,
    eod_bulk,
    etf_holder_bulk,
    income_statement_bulk,
    income_statement_growth_bulk,
    key_metrics_ttm_bulk,
    peers_bulk,
    price_target_summary_bulk,
    profile_bulk,
    rating_bulk,
    ratios_ttm_bulk,
    scores_bulk,
    upgrades_downgrades_consensus_bulk,
)

# Calendar functions
from .calendar_module import (
    dividends,
    dividends_calendar,
    earnings_calendar,
    ipos_calendar,
    ipos_disclosure,
    ipos_prospectus,
    splits,
    splits_calendar,
)

# Chart functions
from .chart import (
    historical_chart,
    historical_price_eod,
    historical_price_eod_dividend_adjusted,
    historical_price_eod_light,
    historical_price_eod_non_split_adjusted,
)

# Commitment of Traders functions
from .commitment_of_traders import (
    commitment_of_traders_report,
    commitment_of_traders_report_analysis,
    commitment_of_traders_report_list,
)

# Commodity functions
from .commodity import commodity_list

# Company functions
from .company import (
    company_notes,
    company_profile,
    company_profile_cik,
    delisted_companies,
    employee_count,
    executive_compensation_benchmark,
    historical_employee_count,
    historical_market_capitalization,
    key_executives,
    key_executives_compensation,
    market_capitalization,
    market_capitalization_batch,
    mergers_acquisitions,
    mergers_acquisitions_search,
    shares_float,
    shares_float_all,
    stock_peers,
)

# Cryptocurrency functions
from .crypto import cryptocurrency_list

# Directory functions
from .directory import (
    actively_trading_list,
    available_countries,
    available_exchanges,
    available_indexes,
    available_industries,
    available_sectors,
    cik_list,
    etf_list,
    financial_statement_symbol_list,
    stock_list,
    symbol_change,
)

# Discounted Cash Flow functions
from .discounted_cash_flow import (
    discounted_cash_flow_custom,
    discounted_cash_flow_custom_levered,
    discounted_cash_flow_levered,
    discounted_cash_flow_valuation,
)

# Earnings functions
from .earnings_transcript import (
    earnings_transcript,
    earnings_transcript_by_symbol,
    earnings_transcript_latest,
    earnings_transcript_list,
)

# Economics functions
from .economics import (
    economic_calendar,
    economic_indicators,
    market_risk_premium,
    treasury_rates,
)

# ESG functions
from .esg import (
    esg_benchmark,
    esg_disclosures,
    esg_ratings,
)

# ETF functions
from .etf import (
    etf_asset_exposure,
    etf_country_weightings,
    etf_holdings,
    etf_info,
    etf_sector_weightings,
)

# Forex functions
from .forex import forex_list

# Form 13F functions
from .form13f import (
    institutional_ownership_dates,
    institutional_ownership_extract,
    institutional_ownership_extract_analytics_by_holder,
    institutional_ownership_holder_industry_breakdown,
    institutional_ownership_holder_performance_summary,
    institutional_ownership_industry_summary,
    institutional_ownership_latest,
    institutional_ownership_positions_summary,
)

# Fundraising functions
from .fundraising import (
    crowdfunding_offerings,
    crowdfunding_offerings_latest,
    crowdfunding_offerings_search,
    fundraising,
    fundraising_latest,
    fundraising_search,
)

# Indexes functions
from .indexes import (
    index_constituents,
    index_constituents_historical,
    index_list,
)

# Insider trades functions
from .insider_trades import (
    acquisition_ownership,
    insider_trading,
    insider_trading_latest,
    insider_trading_reporting_name,
    insider_trading_statistics,
    insider_trading_transaction_type,
)

# Market hours functions
from .market_hours import (
    all_exchange_market_hours,
    exchange_market_hours,
    holidays_by_exchange,
)

# Market performance functions
from .market_performance import (
    biggest_gainers,
    biggest_losers,
    historical_industry_pe,
    historical_industry_performance,
    historical_sector_pe,
    historical_sector_performance,
    industry_pe_snapshot,
    industry_performance_snapshot,
    most_active_stocks,
    sector_pe_snapshot,
    sector_performance_snapshot,
)

# Mutual funds functions
from .mutual_funds import (
    funds_disclosure,
    funds_disclosure_dates,
    funds_disclosure_holders_latest,
    funds_disclosure_holders_search,
)

# News functions
from .news import (
    company_press_releases,
    company_press_releases_latest,
    news_crypto,
    news_crypto_latest,
    news_forex,
    news_general_latest,
    news_stock,
    news_stock_latest,
    price_target_latest_news,
    price_target_news,
    social_sentiment,
    stock_grade_latest_news,
    stock_grade_news,
    trending_sentiment,
)

# Quote functions
from .quote import (
    aftermarket_quote,
    aftermarket_trade,
    batch_aftermarket_quote,
    batch_aftermarket_trade,
    batch_commodity_quote,
    batch_crypto_quote,
    batch_etf_quote,
    batch_exchange_quote,
    batch_forex_quote,
    batch_index_quote,
    batch_mutual_fund_quote,
    batch_quote_short,
    quote,
    quote_short,
    stock_batch_quote,
    stock_price_change,
)

# Search functions
from .search import (
    company_screener,
    search_cik,
    search_cusip,
    search_exchange_variants,
    search_isin,
    search_name,
    search_symbol,
)

# SEC filings functions
from .sec_filings import (
    industry_classification_all,
    industry_classification_list,
    industry_classification_search,
    sec_filings_8k,
    sec_filings_company_search_cik,
    sec_filings_company_search_name,
    sec_filings_company_search_symbol,
    sec_filings_financials,
    sec_filings_search_cik,
    sec_filings_search_form_type,
    sec_filings_search_symbol,
    sec_profile,
    sec_rss_feeds,
)

# Senate trades functions
from .senate import (
    house_latest,
    house_trades,
    house_trades_by_name,
    senate_latest,
    senate_trades,
    senate_trades_by_name,
)

# Financial statements functions
from .statements import (
    balance_sheet_statement,
    balance_sheet_statement_as_reported,
    balance_sheet_statement_growth,
    balance_sheet_statements_ttm,
    cash_flow_statement,
    cash_flow_statement_as_reported,
    cash_flow_statement_growth,
    cashflow_statements_ttm,
    enterprise_values,
    financial_growth,
    financial_ratios,
    financial_ratios_ttm,
    financial_reports_dates,
    financial_reports_json,
    financial_scores,
    financial_statement_full_as_reported,
    financial_statements_latest,
    income_statement,
    income_statement_as_reported,
    income_statement_growth,
    income_statement_ttm,
    key_metrics,
    key_metrics_ttm,
    owner_earnings,
    revenue_geographic_segmentation,
    revenue_product_segmentation,
)

# Technical indicators functions
from .technical_indicators import technical_indicators

# Utility functions
from .utils import iterate_over_pages, to_dataframe, to_dict_list

# Make all functions available at package level
__all__ = [
    # Analyst
    "analyst_estimates",
    "historical_stock_grades",
    "price_target_consensus",
    "price_target_summary",
    "ratings_historical",
    "ratings_snapshot",
    "stock_grades",
    "stock_grades_summary",
    # Bulk
    "balance_sheet_statement_bulk",
    "balance_sheet_statement_growth_bulk",
    "bulk_profiles",
    "cash_flow_statement_bulk",
    "cash_flow_statement_growth_bulk",
    "dcf_bulk",
    "earnings_surprises_bulk",
    "eod_bulk",
    "etf_holder_bulk",
    "income_statement_bulk",
    "income_statement_growth_bulk",
    "key_metrics_ttm_bulk",
    "peers_bulk",
    "price_target_summary_bulk",
    "profile_bulk",
    "rating_bulk",
    "ratios_ttm_bulk",
    "scores_bulk",
    "upgrades_downgrades_consensus_bulk",
    # Calendar
    "dividends",
    "dividends_calendar",
    "earnings_calendar",
    "ipos_calendar",
    "ipos_disclosure",
    "ipos_prospectus",
    "splits",
    "splits_calendar",
    # Chart
    "historical_chart",
    "historical_price_eod",
    "historical_price_eod_dividend_adjusted",
    "historical_price_eod_light",
    "historical_price_eod_non_split_adjusted",
    # Commitment of Traders
    "commitment_of_traders_report",
    "commitment_of_traders_report_analysis",
    "commitment_of_traders_report_list",
    # Commodity
    "commodity_list",
    # Company
    "company_notes",
    "company_profile",
    "company_profile_cik",
    "delisted_companies",
    "employee_count",
    "executive_compensation_benchmark",
    "historical_employee_count",
    "historical_market_capitalization",
    "key_executives",
    "key_executives_compensation",
    "market_capitalization",
    "market_capitalization_batch",
    "mergers_acquisitions",
    "mergers_acquisitions_search",
    "shares_float",
    "shares_float_all",
    "stock_peers",
    # Crypto
    "cryptocurrency_list",
    # Directory
    "actively_trading_list",
    "available_countries",
    "available_exchanges",
    "available_indexes",
    "available_industries",
    "available_sectors",
    "cik_list",
    "etf_list",
    "financial_statement_symbol_list",
    "stock_list",
    "symbol_change",
    # DCF
    "discounted_cash_flow_custom",
    "discounted_cash_flow_custom_levered",
    "discounted_cash_flow_levered",
    "discounted_cash_flow_valuation",
    # Earnings
    "earnings_transcript_latest",
    "earnings_transcript",
    "earnings_transcript_by_symbol",
    "earnings_transcript_list",
    # Economics
    "economic_calendar",
    "economic_indicators",
    "market_risk_premium",
    "treasury_rates",
    # ESG
    "esg_benchmark",
    "esg_disclosures",
    "esg_ratings",
    # ETF
    "etf_asset_exposure",
    "etf_country_weightings",
    "etf_holdings",
    "etf_info",
    "etf_sector_weightings",
    # Forex
    "forex_list",
    # Form 13F
    "institutional_ownership_dates",
    "institutional_ownership_extract",
    "institutional_ownership_extract_analytics_by_holder",
    "institutional_ownership_holder_industry_breakdown",
    "institutional_ownership_holder_performance_summary",
    "institutional_ownership_industry_summary",
    "institutional_ownership_latest",
    "institutional_ownership_positions_summary",
    # Fundraising
    "crowdfunding_offerings",
    "crowdfunding_offerings_latest",
    "crowdfunding_offerings_search",
    "fundraising",
    "fundraising_latest",
    "fundraising_search",
    # Indexes
    "index_constituents",
    "index_constituents_historical",
    "index_list",
    # Insider Trades
    "acquisition_ownership",
    "insider_trading",
    "insider_trading_latest",
    "insider_trading_reporting_name",
    "insider_trading_statistics",
    "insider_trading_transaction_type",
    # Market Hours
    "all_exchange_market_hours",
    "exchange_market_hours",
    "holidays_by_exchange",
    # Market Performance
    "biggest_gainers",
    "biggest_losers",
    "historical_industry_pe",
    "historical_industry_performance",
    "historical_sector_pe",
    "historical_sector_performance",
    "industry_pe_snapshot",
    "industry_performance_snapshot",
    "most_active_stocks",
    "sector_pe_snapshot",
    "sector_performance_snapshot",
    # Mutual Funds
    "funds_disclosure",
    "funds_disclosure_dates",
    "funds_disclosure_holders_latest",
    "funds_disclosure_holders_search",
    # News
    "company_press_releases",
    "company_press_releases_latest",
    "news_crypto",
    "news_crypto_latest",
    "news_forex",
    "news_general_latest",
    "news_stock",
    "news_stock_latest",
    "price_target_latest_news",
    "price_target_news",
    "stock_grade_latest_news",
    "stock_grade_news",
    "social_sentiment",
    "trending_sentiment",
    # Quote
    "aftermarket_quote",
    "aftermarket_trade",
    "batch_aftermarket_quote",
    "batch_aftermarket_trade",
    "batch_commodity_quote",
    "batch_crypto_quote",
    "batch_etf_quote",
    "batch_exchange_quote",
    "batch_forex_quote",
    "batch_index_quote",
    "batch_mutual_fund_quote",
    "batch_quote_short",
    "quote",
    "quote_short",
    "stock_batch_quote",
    "stock_price_change",
    # Search
    "company_screener",
    "search_cik",
    "search_cusip",
    "search_exchange_variants",
    "search_isin",
    "search_name",
    "search_symbol",
    # SEC Filings
    "industry_classification_all",
    "industry_classification_list",
    "industry_classification_search",
    "sec_filings_8k",
    "sec_filings_company_search_cik",
    "sec_filings_company_search_name",
    "sec_filings_company_search_symbol",
    "sec_filings_financials",
    "sec_filings_search_cik",
    "sec_filings_search_form_type",
    "sec_filings_search_symbol",
    "sec_profile",
    "sec_rss_feeds",
    # Senate
    "house_latest",
    "house_trades",
    "house_trades_by_name",
    "senate_latest",
    "senate_trades",
    "senate_trades_by_name",
    # Statements
    "balance_sheet_statement",
    "balance_sheet_statement_as_reported",
    "balance_sheet_statement_growth",
    "balance_sheet_statements_ttm",
    "cash_flow_statement",
    "cash_flow_statement_as_reported",
    "cash_flow_statement_growth",
    "cashflow_statements_ttm",
    "enterprise_values",
    "financial_growth",
    "financial_ratios",
    "financial_ratios_ttm",
    "financial_reports_dates",
    "financial_reports_json",
    "financial_scores",
    "financial_statement_full_as_reported",
    "financial_statements_latest",
    "income_statement",
    "income_statement_as_reported",
    "income_statement_growth",
    "income_statement_ttm",
    "key_metrics",
    "key_metrics_ttm",
    "owner_earnings",
    "revenue_geographic_segmentation",
    "revenue_product_segmentation",
    # Technical Indicators
    "technical_indicators",
    # Utils
    "iterate_over_pages",
    "to_dataframe",
    "to_dict_list",
    "to_list",
]
