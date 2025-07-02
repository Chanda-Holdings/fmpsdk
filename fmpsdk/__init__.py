import logging

# Import all functions from alternative_data
from .alternative_data import (
    commitment_of_traders_report,
    commitment_of_traders_report_analysis,
    commitment_of_traders_report_list,
    crowdfunding_offerings,
    crowdfunding_offerings_latest,
    crowdfunding_offerings_search,
    fundraising,
    fundraising_latest,
    fundraising_search,
)

# Import all functions from bulk
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

# Import all functions from calendar_module
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

# Import all functions from commodities
from .commodities import (
    batch_commodity_quotes,
    commodities_quote,
    commodities_quote_short,
)

# Import all functions from company_valuation
from .company_valuation import (
    analyst_estimates,
)
from .company_valuation import available_industries as company_available_industries
from .company_valuation import (
    available_traded_list,
    balance_sheet_statement,
    balance_sheet_statement_as_reported,
    balance_sheet_statement_growth,
    batch_earning_call_transcript,
    cash_flow_statement,
    cash_flow_statement_as_reported,
    cash_flow_statement_growth,
    company_notes,
    company_profile,
    company_profile_cik,
    custom_discounted_cash_flow,
    custom_levered_discounted_cash_flow,
    delisted_companies,
    discounted_cash_flow,
    earning_call_transcript,
    earning_call_transcripts_available_dates,
    earnings,
    earnings_surprises,
    employee_count,
    enterprise_values,
    esg_benchmark,
    esg_disclosures,
    esg_ratings,
    etf_list,
    financial_growth,
    financial_ratios,
    financial_ratios_ttm,
    financial_reports_xlsx,
    financial_statement_full_as_reported,
    financial_statement_symbol_lists,
    historical_daily_discounted_cash_flow,
    historical_discounted_cash_flow,
    historical_employee_count,
    historical_market_capitalization,
    historical_rating,
    historical_stock_grades,
    income_statement,
    income_statement_as_reported,
    income_statement_growth,
    key_metrics,
    key_metrics_ttm,
    levered_discounted_cash_flow,
    market_capitalization,
    market_capitalization_batch,
    price_target_consensus,
    price_target_news,
    price_target_summary,
    rating,
    ratings_historical,
    ratings_snapshot,
    sec_filings,
    social_sentiment,
    stock_grade_latest_news,
    stock_grade_news,
    stock_grades,
    stock_grades_summary,
    stock_peers,
    stock_screener,
    symbols_list,
    trending_sentiment,
    upgrades_downgrades_consensus,
)

# Import all functions from cryptocurrencies
from .cryptocurrencies import (
    available_cryptocurrencies,
    cryptocurrencies_list,
    cryptocurrency_list,
    last_crypto_price,
)

# Import all functions from economic_indicators
from .economic_indicators import (
    economic_indicators,
    treasury_rates,
)

# Import all functions from etf
from .etf import (
    available_etfs,
    etf_asset_exposure,
    etf_holdings,
    etf_info,
    etf_price_realtime,
    etf_sector_weightings,
)

# Import all functions from forex
from .forex import (
    available_forex,
    batch_forex_quotes,
    forex,
    forex_list,
    forex_quote,
    forex_quote_short,
)

# Import all functions from general
from .general import (
    actively_trading_list,
    available_countries,
    available_exchanges,
    available_indexes,
    available_industries,
    available_sectors,
    cik_list,
    company_screener,
    earnings_transcript_list,
)
from .general import etf_list as general_etf_list
from .general import (
    financial_statement_symbol_list,
    quote,
    search_cik,
    search_cusip,
    search_exchange_variants,
    search_isin,
)
from .general import search_name
from .general import search_name as search_ticker
from .general import search_symbol
from .general import search_symbol as search
from .general import (
    stock_list,
    symbol_change,
)

# Import all functions from insider_trading
from .insider_trading import (
    acquisition_ownership,
    insider_trading_search,
    insider_trading_latest,
    insider_trading_reporting_name,
    insider_trading_statistics,
    insider_trading_transaction_type,
)

# Import all functions from institutional_fund
from .institutional_fund import (
    institutional_ownership_by_symbol,
    institutional_ownership_dates,
    institutional_ownership_extract,
    institutional_ownership_holder_industry_breakdown,
    institutional_ownership_holdings_new_positions,
    institutional_ownership_holdings_overview,
    institutional_ownership_holdings_portfolio_changes,
    institutional_ownership_holdings_sold_out_positions,
    institutional_ownership_holdings_summary,
    institutional_ownership_industry_summary,
    institutional_ownership_latest,
    sec_filings_8k,
    sec_filings_company_search_cik,
    sec_filings_company_search_name,
    sec_filings_company_search_symbol,
    sec_filings_financials,
    sec_filings_search_form_type,
    sec_filings_search_symbol,
    sec_profile,
    sec_rss_feeds,
)

# Import all functions from market_indexes
from .market_indexes import (
    all_exchange_market_hours,
)
from .market_indexes import available_sectors as market_available_sectors
from .market_indexes import (
    index_list,
    index_quote_short,
    indexes,
)

# Import all functions from market_performance
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

# Import all functions from mutual_funds
from .mutual_funds import (
    funds_disclosure,
    funds_disclosure_dates,
    funds_disclosure_holders_latest,
    funds_disclosure_holders_search,
    mutual_fund_holdings,
    mutual_fund_list,
)

# Import all functions from news
from .news import (
    company_news,
    company_press_releases,
    news_crypto,
    news_forex,
    news_general,
    price_target_latest_news,
)

# Import all functions from senate
from .senate import (
    house_latest,
    house_trades,
    house_trades_by_name,
    house_trades_by_symbol,
    senate_latest,
    senate_trades,
    senate_trades_by_name,
    senate_trades_by_symbol,
)

# Import all functions from shares_float
from .shares_float import (
    shares_float,
    shares_float_all,
)

# Import all functions from stock_time_series
from .stock_time_series import (
    exchange_realtime,
    historical_chart,
    historical_chart_1hour,
    historical_chart_1min,
    historical_chart_4hour,
    historical_chart_5min,
    historical_chart_15min,
    historical_chart_30min,
    historical_price_eod_dividend_adjusted,
    historical_price_eod_full,
    historical_price_eod_light,
    historical_price_eod_non_split_adjusted,
    historical_stock_dividend,
    historical_stock_split,
    historical_survivorship_bias_free_eod,
    live_full_price,
    quote_short,
)

# Import all functions from technical_indicators
from .technical_indicators import (
    technical_indicators,
    technical_indicators_adx,
    technical_indicators_dema,
    technical_indicators_ema,
    technical_indicators_rsi,
    technical_indicators_sma,
    technical_indicators_standarddeviation,
    technical_indicators_williams,
)

# Import all functions from tsx
from .tsx import (
    tsx_list,
)

# Import utility functions
from .utils import iterate_over_pages, parse_response

attribution: str = "Data provided by Financial Modeling Prep"
logging.info(attribution)

__all__ = [
    # alternative_data
    "commitment_of_traders_report",
    "commitment_of_traders_report_analysis",
    "commitment_of_traders_report_list",
    "crowdfunding_offerings_latest",
    "crowdfunding_offerings_search",
    "crowdfunding_offerings",
    "fundraising_latest",
    "fundraising_search",
    "fundraising",
    # bulk
    "bulk_profiles",
    "scores_bulk",
    "upgrades_downgrades_consensus_bulk",
    "profile_bulk",
    "rating_bulk",
    "dcf_bulk",
    "price_target_summary_bulk",
    "etf_holder_bulk",
    "key_metrics_ttm_bulk",
    "ratios_ttm_bulk",
    "peers_bulk",
    "earnings_surprises_bulk",
    "income_statement_bulk",
    "income_statement_growth_bulk",
    "balance_sheet_statement_bulk",
    "balance_sheet_statement_growth_bulk",
    "cash_flow_statement_bulk",
    "cash_flow_statement_growth_bulk",
    "eod_bulk",
    # calendar_module
    "dividends",
    "dividends_calendar",
    "earnings_calendar",
    "ipos_calendar",
    "ipos_disclosure",
    "ipos_prospectus",
    "splits",
    "splits_calendar",
    # commodities
    "commodities_quote",
    "commodities_quote_short",
    "batch_commodity_quotes",
    # company_valuation
    "company_profile",
    "company_profile_cik",
    "stock_peers",
    "delisted_companies",
    "employee_count",
    "historical_employee_count",
    "income_statement",
    "balance_sheet_statement",
    "cash_flow_statement",
    "income_statement_as_reported",
    "balance_sheet_statement_as_reported",
    "cash_flow_statement_as_reported",
    "financial_statement_full_as_reported",
    "financial_statement_symbol_lists",
    "income_statement_growth",
    "balance_sheet_statement_growth",
    "cash_flow_statement_growth",
    "financial_ratios_ttm",
    "financial_ratios",
    "enterprise_values",
    "key_metrics_ttm",
    "key_metrics",
    "financial_growth",
    "rating",
    "historical_rating",
    "discounted_cash_flow",
    "levered_discounted_cash_flow",
    "custom_discounted_cash_flow",
    "custom_levered_discounted_cash_flow",
    "historical_discounted_cash_flow",
    "historical_daily_discounted_cash_flow",
    "market_capitalization",
    "historical_market_capitalization",
    "symbols_list",
    "etf_list",
    "available_traded_list",
    "stock_screener",
    "stock_news",
    "earnings_surprises",
    "earning_call_transcript",
    "batch_earning_call_transcript",
    "earning_call_transcripts_available_dates",
    "sec_filings",
    "social_sentiment",
    "trending_sentiment",
    "analyst_estimates",
    "ratings_snapshot",
    "ratings_historical",
    "price_target_summary",
    "price_target_consensus",
    "price_target_news",
    "price_target_latest_news",
    "stock_grades",
    "historical_stock_grades",
    "stock_grades_summary",
    "stock_grade_news",
    "stock_grade_latest_news",
    "financial_reports_xlsx",
    "company_available_industries",
    "upgrades_downgrades_consensus",
    "esg_disclosures",
    "esg_ratings",
    "esg_benchmark",
    "earnings",
    "company_notes",
    "market_capitalization_batch",
    # cryptocurrencies
    "available_cryptocurrencies",
    "cryptocurrencies_list",
    "cryptocurrency_list",
    "last_crypto_price",
    # economic_indicators
    "treasury_rates",
    "economic_indicators",
    # etf
    "available_etfs",
    "etf_price_realtime",
    "etf_info",
    "etf_holdings",
    "etf_asset_exposure",
    "etf_sector_weightings",
    # euronext
    "euronext_list",
    # forex
    "forex",
    "forex_list",
    "available_forex",
    "forex_news",
    "forex_quote",
    "forex_quote_short",
    "batch_forex_quotes",
    # general
    "quote",
    "search_symbol",
    "search_name",
    "search_cik",
    "search_cusip",
    "search_isin",
    "company_screener",
    "search_exchange_variants",
    "stock_list",
    "financial_statement_symbol_list",
    "cik_list",
    "symbol_change",
    "general_etf_list",
    "actively_trading_list",
    "earnings_transcript_list",
    "available_exchanges",
    "available_sectors",
    "available_industries",
    "available_countries",
    "available_indexes",
    "search_ticker",
    "search",
    # insider_trading
    "insider_trading_search",
    "insider_trading_latest",
    "insider_trading_reporting_name",
    "insider_trading_transaction_type",
    "insider_trading_statistics",
    "acquisition_ownership",
    # institutional_fund
    "sec_rss_feeds",
    "institutional_ownership_latest",
    "institutional_ownership_extract",
    "institutional_ownership_dates",
    "institutional_ownership_holder_industry_breakdown",
    "institutional_ownership_industry_summary",
    "institutional_ownership_holdings_portfolio_changes",
    "institutional_ownership_holdings_new_positions",
    "institutional_ownership_holdings_summary",
    "institutional_ownership_holdings_overview",
    "institutional_ownership_holdings_sold_out_positions",
    "institutional_ownership_by_symbol",
    "sec_filings_8k",
    "sec_filings_financials",
    "sec_filings_search_form_type",
    "sec_filings_search_symbol",
    "sec_filings_company_search_name",
    "sec_filings_company_search_symbol",
    "sec_filings_company_search_cik",
    "sec_profile",
    # market_indexes
    "indexes",
    "market_available_sectors",
    "all_exchange_market_hours",
    "index_list",
    "index_quote_short",
    # market_performance
    "sector_performance_snapshot",
    "industry_performance_snapshot",
    "historical_sector_performance",
    "historical_industry_performance",
    "sector_pe_snapshot",
    "industry_pe_snapshot",
    "historical_sector_pe",
    "historical_industry_pe",
    "biggest_gainers",
    "biggest_losers",
    "most_active_stocks",
    # mutual_funds
    "mutual_fund_list",
    "funds_disclosure_holders_latest",
    "funds_disclosure",
    "funds_disclosure_holders_search",
    "funds_disclosure_dates",
    "mutual_fund_holdings",
    # news
    "company_news",
    "company_press_releases",
    "news_crypto",
    "news_forex",
    "news_general",
    "price_target_latest_news",
    # senate
    "senate_latest",
    "house_latest",
    "senate_trades",
    "senate_trades_by_name",
    "house_trades",
    "house_trades_by_name",
    "senate_trades_by_symbol",
    "house_trades_by_symbol",
    # shares_float
    "shares_float",
    "shares_float_all",
    # stock_time_series
    "quote_short",
    "exchange_realtime",
    "historical_stock_dividend",
    "historical_stock_split",
    "historical_survivorship_bias_free_eod",
    "live_full_price",
    "historical_price_eod_light",
    "historical_price_eod_full",
    "historical_price_eod_non_split_adjusted",
    "historical_price_eod_dividend_adjusted",
    "historical_chart",
    "historical_chart_1min",
    "historical_chart_5min",
    "historical_chart_15min",
    "historical_chart_30min",
    "historical_chart_1hour",
    "historical_chart_4hour",
    # technical_indicators
    "technical_indicators",
    "technical_indicators_adx",
    "technical_indicators_dema",
    "technical_indicators_ema",
    "technical_indicators_rsi",
    "technical_indicators_sma",
    "technical_indicators_standarddeviation",
    "technical_indicators_williams",
    # tsx
    "tsx_list",
    # utils
    "iterate_over_pages",
    "parse_response",
]
