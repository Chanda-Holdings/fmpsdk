# FMP SDK Integration Testing Plan

## Overview
This document outlines the comprehensive integration testing strategy for the fmpsdk library. The tests will validate live API endpoints against expected schemas, ensuring data integrity and proper error handling.

## Key Requirements
1. **Schema Validation**: Each endpoint must return data matching the expected schema from `fmp_api_schemas.json`
2. **Negative Testing**: Test error conditions and invalid inputs
3. **Non-Empty Data**: Ensure endpoints return meaningful data for valid inputs
4. **Parameterized Testing**: Test with diverse inputs (high/low market cap stocks, different timeframes, etc.)

## Current State Assessment

### Issues Identified
- **model_registry.py**: Needs to be corrected to properly map API endpoints to their corresponding schemas
- **Schema Mapping**: Need to establish proper mapping between API functions and JSON schemas
- **Test Infrastructure**: No existing test files in `tests/` directory

## Test File Mapping
Each module in `fmpsdk/` will have a corresponding test file:

### 📊 **Core Data Modules**

#### 1. `test_quote.py` (from `quote.py`) - ✅ **COMPLETED**
**Functions tested:**
- ✅ `quote()` - Full quote data for single symbol
- ✅ `stock_batch_quote()` - Multiple full quotes in single request
- ✅ `quote_short()` - Short quote data for single symbol  
- ✅ `aftermarket_trade()` - After-market trading data
- ✅ `aftermarket_quote()` - After-market quote data
- ✅ `stock_price_change()` - Price change percentages over multiple timeframes
- ✅ `batch_quote_short()` - Multiple short quotes in single request
- ✅ `batch_aftermarket_trade()` - Multiple after-market trades
- ✅ `batch_aftermarket_quote()` - Multiple after-market quotes
- ✅ `batch_exchange_quote()` - Batch quotes for multiple symbols
- ✅ `batch_mutual_fund_quote()` - Multiple mutual fund quotes
- ✅ `batch_etf_quote()` - Multiple ETF quotes
- ✅ `batch_commodity_quote()` - Multiple commodity quotes
- ✅ `batch_crypto_quote()` - Multiple cryptocurrency quotes
- ✅ `batch_forex_quote()` - Multiple forex pair quotes
- ✅ `batch_index_quote()` - Multiple index quotes

**Comprehensive testing implemented:**
- ✅ All 16 quote endpoints fully tested and validated
- ✅ All asset types: Stocks, ETFs, Crypto, Forex, Commodities, Indices
- ✅ Schema validation for all asset types with proper Pydantic models
- ✅ Error handling and invalid symbols/API keys
- ✅ Response time validation and performance testing
- ✅ Data consistency checks across related endpoints
- ✅ Batch vs individual quote comparisons and consistency validation
- ✅ Aftermarket data handling with proper model fixes
- ✅ Stock price change validation across multiple timeframes
- ✅ Asset-specific field validation and formatting
- ✅ 49 comprehensive test cases covering all quote functionality

**Models Fixed:**
- ✅ FMPAftermarketTrade: Made tradeSize field optional to handle None values
- ✅ FMPStockPriceChange: Made all price change fields optional for flexibility
- ✅ Fixed API parameter handling for batch endpoints (list vs string)

**Test Parameters:**
- High market cap: AAPL, MSFT, GOOGL, AMZN, TSLA
- Mid market cap: AMD, NVDA, CRM, NFLX
- Low market cap: Small-cap stocks from Russell 2000
- International stocks: ASML, TSM, SAP
- ETFs: SPY, QQQ, VTI, IWM, EFA
- Indices: ^GSPC, ^IXIC, ^DJI, ^RUT
- Forex pairs: EURUSD, GBPUSD, USDJPY, AUDUSD
- Cryptocurrencies: BTCUSD, ETHUSD, ADAUSD
- Commodities: GCUSD (Gold), CLUSD (Oil), NGUSD (Natural Gas)
- Edge cases: Delisted stocks, new IPOs, penny stocks

#### 2. `test_analyst.py` (from `analyst.py`) - ✅ **COMPLETED**
**Functions tested:**
- ✅ `analyst_estimates()` - Analyst estimates with periods (annual/quarter)
- ✅ `ratings_snapshot()` - Current analyst ratings snapshot
- ✅ `ratings_historical()` - Historical analyst ratings over time
- ✅ `price_target_summary()` - Price target summary data
- ✅ `price_target_consensus()` - Consensus price targets from analysts
- ✅ `stock_grades()` - Current stock grades and recommendations
- ✅ `historical_stock_grades()` - Historical stock grade changes
- ✅ `stock_grades_summary()` - Summary of stock grade consensus

**Comprehensive testing implemented:**
- ✅ All analyst estimate periods (annual, quarterly) with schema validation
- ✅ Ratings snapshot and historical data with date ranges
- ✅ Price target summary and consensus validation
- ✅ Stock grades current, historical, and summary data
- ✅ Error handling for invalid symbols, API keys, and parameters
- ✅ Response time validation for all endpoints
- ✅ Data consistency checks between related analyst endpoints
- ✅ Multiple symbol validation and high-coverage stock testing
- ✅ Limit and pagination parameter validation
- ✅ 27 test cases covering all analyst functionality

**Test Parameters:**
- Periods: 'annual', 'quarter'
- High analyst coverage: AAPL, MSFT, GOOGL, AMZN, TSLA
- Medium analyst coverage: Regional banks, mid-cap tech
- Low analyst coverage: Small-cap stocks, recent IPOs
- No analyst coverage: Micro-cap stocks, OTC stocks
- Different sectors: Tech, Finance, Healthcare, Energy, Consumer
- International stocks with analyst coverage
- Limit and page parameters for pagination testing

#### 3. `test_company.py` (from `company.py`) - ✅ **COMPLETED**
**Functions tested:**
- ✅ `company_profile()` - Complete company profile by symbol
- ✅ `company_profile_cik()` - Company profile by CIK number
- ✅ `company_notes()` - Company notes and updates
- ✅ `stock_peers()` - Company peer comparisons
- ✅ `delisted_companies()` - Information on delisted companies
- ✅ `employee_count()` - Current employee count data
- ✅ `historical_employee_count()` - Historical employee count trends
- ✅ `market_capitalization()` - Current market cap data
- ✅ `market_capitalization_batch()` - Batch market cap for multiple symbols
- ✅ `historical_market_capitalization()` - Historical market cap data
- ✅ `shares_float()` - Current shares float information
- ✅ `shares_float_all()` - All shares float data
- ✅ `mergers_acquisitions()` - M&A announcements and data
- ✅ `mergers_acquisitions_search()` - Search M&A transactions
- ✅ `key_executives()` - Company executive information
- ✅ `key_executives_compensation()` - Executive compensation data
- ✅ `executive_compensation_benchmark()` - Executive comp benchmarking

**Comprehensive testing implemented:**
- ✅ All company profile endpoints with various asset types
- ✅ Schema validation for all company data models
- ✅ Error handling and invalid symbols/CIKs
- ✅ Response time validation
- ✅ Data consistency checks between related endpoints
- ✅ Batch processing validation
- ✅ Historical data validation
- ✅ Employee and market cap trend analysis
- ✅ M&A data validation with search functionality
- ✅ Executive data and compensation analysis
- ✅ 33 test cases covering all company functionality

**Test Parameters:**
- Large cap companies: AAPL, MSFT, GOOGL, AMZN
- Mid cap companies: Regional banks, specialty retailers
- Small cap companies: Emerging growth companies
- International companies: ASML, TSM, NVO, UL
- Different sectors: Technology, Healthcare, Finance, Energy, Consumer
- Companies with recent M&A activity
- Companies with executive changes
- Companies with employee count variations
- Different exchange listings: NYSE, NASDAQ, AMEX
- Companies with/without float data
- CIK number validation tests

**Models Fixed:**
- ✅ FMPShareFloat: Made date field optional to handle None values
- ✅ FMPExecutiveProfile: Updated active field to handle int/bool values
- ✅ FMPExecutiveCompensation: Made compensation fields optional
- ✅ FMPMergerAcquisition: Made targeted company fields optional

#### 4. `test_statements.py` (from `statements.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `income_statement()` - Income statements (annual/quarter)
- `balance_sheet_statement()` - Balance sheet statements
- `cash_flow_statement()` - Cash flow statements
- `financial_statements_latest()` - Most recent financial statements
- `income_statement_ttm()` - TTM income statement data
- `balance_sheet_statements_ttm()` - TTM balance sheet data
- `cashflow_statements_ttm()` - TTM cash flow data
- `key_metrics()` - Key financial metrics and ratios
- `financial_ratios()` - Comprehensive financial ratios
- `key_metrics_ttm()` - TTM key metrics
- `financial_ratios_ttm()` - TTM financial ratios
- `financial_scores()` - Financial health scores
- `owner_earnings()` - Owner earnings calculations
- `enterprise_values()` - Enterprise value metrics
- `income_statement_growth()` - Income statement growth rates
- `balance_sheet_statement_growth()` - Balance sheet growth rates
- `cash_flow_statement_growth()` - Cash flow growth rates
- `financial_growth()` - Overall financial growth metrics
- `financial_reports_dates()` - Available financial report dates
- `financial_reports_json()` - Financial reports in JSON format
- `financial_reports_xlsx()` - Financial reports in Excel format
- `revenue_product_segmentation()` - Revenue by product segments
- `revenue_geographic_segmentation()` - Revenue by geography
- `income_statement_as_reported()` - As-reported income statements
- `balance_sheet_statement_as_reported()` - As-reported balance sheets
- `cash_flow_statement_as_reported()` - As-reported cash flows
- `financial_statement_full_as_reported()` - Complete as-reported statements

**Test Parameters:**
- Periods: 'annual', 'quarter'
- Large cap stocks: AAPL, MSFT, GOOGL, AMZN with complete data
- International stocks: Different accounting standards (GAAP vs IFRS)
- Different fiscal year ends: Calendar year vs non-calendar year
- Banking/Financial: Different statement structures
- Real Estate: REIT-specific metrics
- Utilities: Regulated utility financials
- Growth companies: High-growth vs mature companies
- Distressed companies: Companies with financial difficulties
- Limit and page parameters for historical data
- Year ranges: Recent years, historical data availability
- Companies with segment reporting
- Companies with geographic diversification

### 📈 **Chart and Technical Analysis**

#### 5. `test_chart.py` (from `chart.py`) - ✅ **COMPLETED**
**Functions tested:**
- ✅ `historical_price_eod_light()` - Light historical price data (date, price, volume)
- ✅ `historical_price_eod()` - Full historical OHLCV data
- ✅ `historical_price_eod_non_split_adjusted()` - Non-split adjusted historical data
- ✅ `historical_price_eod_dividend_adjusted()` - Dividend adjusted historical data
- ✅ `historical_chart()` - Intraday historical chart data with all intervals

**Comprehensive testing implemented:**
- ✅ All 5 chart endpoints fully tested and validated
- ✅ Historical EOD data with light and full OHLCV formats
- ✅ Date range filtering and chronological order validation
- ✅ Multiple asset types: Stocks, ETFs, Crypto, Forex, Commodities
- ✅ Price adjustment handling (split and dividend adjusted)
- ✅ Intraday chart data with all valid intervals (1min, 5min, 15min, 30min, 1hour, 4hour)
- ✅ Data consistency validation between light and full endpoints
- ✅ OHLC relationship validation and price reasonableness checks
- ✅ Volume consistency across endpoints
- ✅ Error handling for invalid symbols, API keys, and parameters
- ✅ Response time validation and performance testing
- ✅ Chronological data ordering verification
- ✅ High volume stocks and different timeframe testing
- ✅ 23 comprehensive test cases covering all chart functionality

**Models Validated:**
- ✅ FMPHistoricalDataPointLight: Basic price and volume data
- ✅ FMPHistoricalDataPointFull: Complete OHLCV data with optional fields
- ✅ FMPIntradayDataPoint: Intraday chart data with OHLCV structure

**Test Parameters:**
- Timeframes for intraday: 1min, 5min, 15min, 30min, 1hour, 4hour
- Date ranges: 1D, 1W, 1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, max
- High volume stocks: AAPL, MSFT, SPY for complete data availability
- Low volume stocks: Small-cap stocks with limited data
- Different asset types: Stocks, ETFs, indices, forex, crypto
- Stocks with stock splits: Testing split-adjusted vs non-adjusted
- Stocks with dividends: Testing dividend adjustments
- International stocks: Different market hours and holidays
- Newly listed stocks: Limited historical data availability
- Delisted stocks: Historical data up to delisting date
- Market holidays: Data gaps and handling
- After-hours and pre-market data availability

#### 6. `test_technical_indicators.py` (from `technical_indicators.py`) - ✅ **COMPLETED**
**Functions to test:**
- `technical_indicators()` - Generic technical indicator function supporting:
  - `sma` - Simple Moving Average
  - `ema` - Exponential Moving Average
  - `wma` - Weighted Moving Average
  - `dema` - Double Exponential Moving Average
  - `tema` - Triple Exponential Moving Average
  - `rsi` - Relative Strength Index
  - `standarddeviation` - Standard Deviation
  - `williams` - Williams %R
  - `adx` - Average Directional Index

**Test Coverage (26 tests total):**
- ✅ All 9 technical indicator types with validation
- ✅ Parameter variations (period lengths, timeframes, date ranges)
- ✅ Intraday and daily/weekly/monthly timeframes
- ✅ Multiple asset types (stocks, ETFs where available)
- ✅ Error handling (invalid indicators, symbols, API keys)
- ✅ Data consistency and oscillator behavior validation
- ✅ Response time testing
- ✅ Edge cases (short/long periods, data sufficiency)

**Coverage Notes:**
- Tests handle API plan limitations gracefully (technical indicators may return empty data)
- Validates all supported indicator types and parameter combinations
- Tests oscillator constraints (RSI: 0-100, Williams: -100 to 0, ADX: 0-100)
- Includes comprehensive error handling and boundary condition testing
- Tests pass/skip appropriately based on data availability

### 📅 **Calendar and Events**

#### 7. `test_calendar_module.py` (from `calendar_module.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `dividends()` - Historical dividend payments for individual stocks
- `dividends_calendar()` - Upcoming dividend calendar events
- `earnings_calendar()` - Upcoming earnings announcement calendar
- `ipos_calendar()` - Upcoming IPO calendar
- `ipos_disclosure()` - IPO disclosure filings
- `ipos_prospectus()` - IPO prospectus documents
- `splits()` - Historical stock split data
- `splits_calendar()` - Upcoming stock split calendar

**Test Parameters:**
- Date ranges: Past events, current week, next month, quarterly ranges
- Dividend-paying stocks: AAPL, MSFT, JNJ, KO with regular dividends
- High-dividend stocks: REITs, utilities, dividend aristocrats
- Growth stocks: Companies with no dividends vs special dividends
- Earnings timing: Before market, after market, during market hours
- Different sectors: Tech earnings clusters, financial earnings seasons
- IPO activity: High activity periods, quiet periods
- Stock splits: Recent splits, stock dividends, reverse splits
- International calendars: ADR dividend schedules
- Holiday adjustments: Dividend/earnings dates around holidays
- Market-specific events: NYSE vs NASDAQ specific events

### 🔍 **Search and Discovery**

#### 8. `test_search.py` (from `search.py`) - ✅ **COMPLETED**
**Functions to test:**
- `search_symbol()` - Search by ticker symbol with partial matching ✅
- `search_name()` - Search by company name with partial matching ✅
- `search_cik()` - Search by SEC CIK number ✅
- `search_cusip()` - Search by CUSIP identifier ✅
- `search_isin()` - Search by ISIN identifier ✅
- `company_screener()` - Advanced stock screening with multiple criteria ✅
- `search_exchange_variants()` - Search for alternative exchange listings ✅

**Test Coverage:**
- ✅ All 7 search functions fully tested
- ✅ 40 comprehensive test cases covering:
  - Symbol/name exact and partial matching
  - CIK, CUSIP, ISIN identifier searches
  - Company screener with multiple filter combinations (market cap, price, sector, exchange, beta, ETF, etc.)
  - Exchange variants for multi-listed companies
  - Error handling with invalid API keys and parameters
  - Response time performance testing
  - Data consistency validation across endpoints
- ✅ Schema validation with Pydantic models
- ✅ Edge cases: empty results, invalid formats, international symbols
- ✅ Parameter testing: limits, filters, exchanges

**Test Parameters:**
- Partial symbol searches: "AA" (multiple matches), "AAPL" (exact match) ✅
- Company name searches: "Apple" (multiple companies), exact names ✅
- International symbols: ADRs, foreign exchanges ✅
- Different asset types: Stocks, ETFs, indices, bonds ✅
- CIK searches: Valid CIK numbers, invalid formats ✅
- CUSIP searches: Valid CUSIP identifiers, format validation ✅
- ISIN searches: US and international ISINs ✅
- Screener criteria combinations: ✅
  - Market cap ranges: Micro, small, mid, large cap
  - Sector filtering: All 11 GICS sectors
  - Industry filtering: Detailed industry breakdowns
  - Price ranges: Penny stocks to high-priced stocks
  - Volume criteria: High volume, low volume thresholds
  - Beta ranges: Low beta (defensive) to high beta (volatile)
  - Dividend yield ranges: Non-dividend to high yield
  - P/E ratio ranges: Value to growth characteristics
  - Country filtering: US, international markets
  - Exchange filtering: NYSE, NASDAQ, AMEX, OTC
- Exchange variants: Companies listed on multiple exchanges ✅
- Edge cases: Delisted companies, recent IPOs, name changes

### 💰 **Alternative Assets**

#### 9. `test_crypto.py` (from `crypto.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `cryptocurrency_list()` - List all available cryptocurrencies

**Test Parameters:**
- Major cryptocurrencies: BTC, ETH, ADA, DOT, SOL
- Stablecoins: USDT, USDC, BUSD, DAI
- DeFi tokens: UNI, AAVE, COMP, MKR
- Layer 2 tokens: MATIC, AVAX, FTM
- Meme coins: DOGE, SHIB (if available)
- Exchange tokens: BNB, CRO, FTT
- Privacy coins: XMR, ZEC (if available)
- Cross-chain tokens: LINK, DOT
- Newly listed cryptocurrencies
- Delisted or deprecated cryptocurrencies
- Symbol format validation: BTCUSD format (no slash patterns)

#### 10. `test_forex.py` (from `forex.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `forex_list()` - List all available forex pairs

**Test Parameters:**
- Major currency pairs: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- Minor currency pairs: EURGBP, EURJPY, GBPJPY, CHFJPY, EURCHF, AUDJPY
- Exotic currency pairs: USDTRY, USDZAR, USDMXN, EURTRY, USDSGD
- Commodity currencies: AUD, CAD, NZD pairs
- Safe haven currencies: JPY, CHF pairs
- Emerging market currencies: MXN, TRY, ZAR, BRL
- Currency pair format validation: EURUSD format (no slash)
- Cross-currency pairs: Non-USD base currencies
- Regional currency pairs: European, Asian, Americas
- Cryptocurrency forex pairs: BTCUSD, ETHUSD (if available)

#### 11. `test_commodity.py` (from `commodity.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `commodity_list()` - List all available commodities

**Test Parameters:**
- Precious metals: Gold (GCUSD), Silver (SIUSD), Platinum (PLUSD), Palladium (PAUSD)
- Energy commodities: Crude Oil (CLUSD), Natural Gas (NGUSD), Heating Oil, Gasoline
- Agricultural commodities: Wheat, Corn, Soybeans, Coffee, Sugar, Cotton
- Base metals: Copper, Aluminum, Nickel, Zinc, Lead
- Livestock: Live Cattle, Lean Hogs, Feeder Cattle
- Soft commodities: Cocoa, Orange Juice, Lumber
- Futures contracts: Different expiration months and years
- Commodity symbol formats: GCUSD format (no slash patterns)
- Seasonal commodities: Agricultural seasonal patterns
- Regional variations: Different market specifications
- Currency denominations: USD, EUR based pricing

#### 12. `test_etf.py` (from `etf.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `etf_info()` - ETF information and basic details
- `etf_holdings()` - ETF holdings and portfolio composition
- `etf_asset_exposure()` - ETF asset class exposure breakdown
- `etf_country_weightings()` - ETF geographic exposure by country
- `etf_sector_weightings()` - ETF sector allocation weightings

**Test Parameters:**
- Large broad market ETFs: SPY, VOO, VTI, IVV (S&P 500 trackers)
- Technology ETFs: QQQ, VGT, XLK, FTEC
- Sector-specific ETFs: XLF (Financial), XLE (Energy), XLV (Healthcare)
- International ETFs: VEA (Developed), VWO (Emerging), EFA (EAFE)
- Bond ETFs: AGG, BND, TLT, LQD
- Commodity ETFs: GLD (Gold), SLV (Silver), USO (Oil)
- Inverse ETFs: SH, PSQ, SQQQ
- Leveraged ETFs: UPRO, TQQQ, SPXL
- Thematic ETFs: ARKK (Innovation), ICLN (Clean Energy)
- Smart beta ETFs: MTUM (Momentum), QUAL (Quality), USMV (Low Vol)
- Currency ETFs: UUP (Dollar), FXE (Euro)
- Real Estate ETFs: VNQ, SCHH, RWR
- Dividend ETFs: VYM, DVY, SCHD
- Small/Mid cap ETFs: IWM (Russell 2000), MDY (S&P 400)
- International sector ETFs: Regional and sector combinations
- Holdings analysis: Top holdings, concentration ratios
- Expense ratio validation: Management fees and costs

### 📊 **Market Data and Performance**

#### 13. `test_market_performance.py` (from `market_performance.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `sector_performance_snapshot()` - Current sector performance overview
- `industry_performance_snapshot()` - Current industry performance overview
- `historical_sector_performance()` - Historical sector performance trends
- `historical_industry_performance()` - Historical industry performance trends
- `sector_pe_snapshot()` - Current sector P/E ratio snapshot
- `industry_pe_snapshot()` - Current industry P/E ratio snapshot
- `historical_sector_pe()` - Historical sector P/E ratio trends
- `historical_industry_pe()` - Historical industry P/E ratio trends
- `biggest_gainers()` - Top performing stocks of the day
- `biggest_losers()` - Worst performing stocks of the day
- `most_active_stocks()` - Most actively traded stocks

**Test Parameters:**
- All 11 GICS sectors: Technology, Healthcare, Financials, Communication Services, Consumer Discretionary, Consumer Staples, Industrials, Energy, Utilities, Real Estate, Materials
- Industry breakdowns: Detailed industry classifications within sectors
- Time periods: Daily, weekly, monthly, quarterly, yearly performance
- Market conditions: Bull market, bear market, volatile periods
- Sector rotation analysis: Cyclical vs defensive performance
- Market cap segments: Large, mid, small cap performance differences
- Geographic performance: US vs International sectors
- Performance metrics: Price return, total return, volatility
- P/E ratio analysis: Valuation trends across sectors/industries
- Gainers/losers criteria: Percentage thresholds, volume requirements
- Market hours: Regular hours vs extended hours performance

#### 14. `test_indexes.py` (from `indexes.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `index_list()` - List all available market indices
- `available_sectors()` - List available sectors (duplicate from directory module)
- `index_constituents()` - Current index constituent stocks
- `index_constituents_historical()` - Historical index constituent changes

**Test Parameters:**
- Major US indices: ^GSPC (S&P 500), ^IXIC (NASDAQ), ^DJI (Dow Jones), ^RUT (Russell 2000)
- Sector indices: S&P 500 sector indices, NASDAQ sector indices
- International indices: ^FTSE (FTSE 100), ^GDAXI (DAX), ^N225 (Nikkei 225), ^HSI (Hang Seng), ^FCHI (CAC 40)
- Bond indices: Bloomberg Aggregate Bond Index, Treasury indices
- Commodity indices: CRB Index, Gold/Silver indices
- Volatility indices: ^VIX, ^VXN, ^RVX
- Real Estate indices: REIT indices, Real Estate sector indices
- Emerging market indices: MSCI Emerging Markets, regional indices
- Style indices: Growth vs Value, Large vs Small cap
- ESG indices: Sustainable investing indices
- Constituent analysis: Index membership, weightings, market caps
- Historical changes: Additions, deletions, rebalancing events
- Index methodology: Cap-weighted, equal-weighted, fundamental-weighted
- Currency hedged indices: International indices with currency hedging

#### 15. `test_market_hours.py` (from `market_hours.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `exchange_market_hours()` - Market hours for specific exchange
- `holidays_by_exchange()` - Holiday calendar for specific exchange
- `all_exchange_market_hours()` - Market hours for all exchanges

**Test Parameters:**
- Major US exchanges: NYSE, NASDAQ, AMEX, CBOE
- International exchanges: LSE, TSE, HKEX, FSE, Euronext, TSX
- Market sessions: Regular hours, pre-market, after-hours
- Time zones: EST, PST, GMT, JST, CET handling
- Daylight saving time: DST transitions and schedule changes
- Holiday calendars: US federal holidays, international holidays
- Trading halts: Circuit breaker schedules, emergency closures
- Special trading sessions: Shortened trading days, holiday schedules
- Weekend trading: Forex and crypto 24/7 markets
- Market closure events: Weather, technical issues, special circumstances
- Regional variations: Different holiday schedules by country/region

### 📋 **Regulatory and Compliance**

#### 16. `test_sec_filings.py` (from `sec_filings.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `sec_rss_feeds()` - SEC RSS feed data
- `sec_filings_8k()` - SEC 8-K filings search
- `sec_filings_financials()` - SEC financial statement filings
- `sec_filings_search_form_type()` - Search filings by form type
- `sec_filings_search_symbol()` - Search filings by stock symbol
- `sec_filings_search_cik()` - Search filings by CIK number
- `sec_filings_company_search_name()` - Search company filings by name
- `sec_filings_company_search_symbol()` - Search company filings by symbol
- `sec_filings_company_search_cik()` - Search company filings by CIK
- `sec_profile()` - SEC company profile information
- `industry_classification_list()` - List industry classifications
- `industry_classification_search()` - Search industry classifications
- `industry_classification_all()` - All industry classification data

**Test Parameters:**
- Form types: 10-K, 10-Q, 8-K, 20-F, DEF 14A, S-1, S-3, 13F, 4, 3, SC 13G, SC 13D
- Large cap filers: AAPL, MSFT, GOOGL with extensive filing history
- Foreign filers: 20-F forms, international companies
- Date ranges: Recent filings, historical archives, quarterly periods
- CIK validation: Valid CIK formats, leading zeros handling
- Company name searches: Exact matches, partial matches, name changes
- Filing status: Live filings, amended filings, superseded filings
- Industry classifications: SIC codes, NAICS codes, sector mappings
- RSS feed types: Recent filings, specific form types
- Filing content: Financial statements, exhibits, correspondence
- Search pagination: Large result sets, limit parameters
- Filing amendments: Original vs amended filing relationships

#### 17. `test_insider_trades.py` (from `insider_trades.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `insider_trading()` - Insider trading transactions for specific symbol
- `insider_trading_latest()` - Latest insider trading activity across market
- `insider_trading_reporting_name()` - Insider trades by reporting person name
- `insider_trading_transaction_type()` - Filter trades by transaction type
- `insider_trading_statistics()` - Insider trading statistics and summaries
- `acquisition_ownership()` - Beneficial ownership disclosures

**Test Parameters:**
- High insider activity stocks: Companies with frequent insider transactions
- Transaction types: Purchase, Sale, Gift, Exercise of Options, Award/Grant
- Insider roles: CEO, CFO, Director, 10% Owner, Other Officers
- Transaction sizes: Small personal trades, large institutional transactions
- Date ranges: Recent activity, historical patterns, quarterly analysis
- Reporting requirements: Form 4, Form 3, Form 5 filings
- Company sizes: Large cap vs small cap insider activity patterns
- Sectors: Technology, biotech with high option activity
- Ownership thresholds: 5%, 10% beneficial ownership triggers
- Transaction timing: Earnings blackout periods, open window trading
- Statistical analysis: Insider sentiment, buy/sell ratios
- Name searches: Exact matches, common name variations

#### 18. `test_form13f.py` (from `form13f.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `institutional_ownership_latest()` - Latest 13F institutional holdings
- `institutional_ownership_extract()` - Extract specific 13F holdings data
- `institutional_ownership_dates()` - Available 13F filing dates
- `institutional_ownership_extract_analytics_by_holder()` - Extract analytics by holder for symbol
- `institutional_ownership_holder_performance_summary()` - Holder performance summary by CIK
- `institutional_ownership_holder_industry_breakdown()` - Industry breakdown by CIK
- `institutional_ownership_positions_summary()` - Symbol positions summary
- `institutional_ownership_industry_summary()` - Overall industry summary
- `institutional_ownership_extract_analytics_by_holder()` - Analytics data by institutional holder
- `institutional_ownership_holder_performance_summary()` - Institutional holder performance summaries
- `institutional_ownership_holder_industry_breakdown()` - Industry breakdown by institutional holder (both CIK and symbol versions)
- `institutional_ownership_industry_summary()` - Overall industry summary for institutional ownership

**Test Parameters:**
- Major institutional investors: Berkshire Hathaway, Vanguard, BlackRock, State Street
- CIK numbers: Validate major institutional CIK identifiers
- Filing dates: Quarterly 13F filing deadlines (45 days after quarter end)
- Portfolio sizes: Large institutions with extensive holdings
- Holding types: Stocks, ETFs, ADRs reported in 13F
- Position sizes: Large positions, small positions, new positions, sold positions
- Quarter comparisons: Q-over-Q changes in institutional holdings
- Concentration analysis: Top holdings, portfolio diversification
- Market impact: Large institutional position changes
- Filing compliance: On-time vs late filings
- Amendment filings: Original vs amended 13F filings
- Threshold requirements: $100M+ assets under management requirement
- Analytics testing: Extract analytics by holder for specific symbols
- Performance analysis: Holder performance summaries and tracking
- Industry breakdown: Sector allocation analysis by institutional holders
- Symbol-specific analysis: Position summaries for individual stocks
- Industry summaries: Market-wide institutional ownership by sector

#### 19. `test_senate.py` (from `senate.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `senate_latest()` - Latest Senate trading disclosures
- `house_latest()` - Latest House of Representatives trading disclosures
- `senate_trades()` - Historical Senate trading transactions by symbol
- `senate_trades_by_name()` - Senate trades filtered by politician name
- `house_trades()` - Historical House trading transactions by symbol
- `house_trades_by_name()` - House trades filtered by politician name

**Test Parameters:**
- Congressional members: Active senators and representatives
- Trade types: Stock purchases, sales, options, bonds, funds
- Disclosure timing: 30-day and 45-day reporting requirements
- Transaction sizes: $1,001-$15,000, $15,001-$50,000, $50,001-$100,000, etc.
- Asset classes: Individual stocks, mutual funds, ETFs, bonds, derivatives
- Committee oversight: Members on relevant committees (Banking, Finance, etc.)
- Political parties: Republican, Democratic, Independent members
- Date ranges: Recent disclosures, annual patterns, election cycles
- High-activity stocks: Commonly traded stocks by politicians
- Conflict analysis: Committee assignment vs trading activity
- Family member trades: Spouse and dependent transactions
- Compliance monitoring: Late filings, missing disclosures

### 🏢 **Institutional and ESG**

#### 20. `test_mutual_funds.py` (from `mutual_funds.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `funds_disclosure_holders_latest()` - Latest mutual fund disclosure holders
- `funds_disclosure()` - Historical mutual fund disclosure data
- `funds_disclosure_holders_search()` - Search fund holders by criteria
- `funds_disclosure_dates()` - Available fund disclosure filing dates

**Test Parameters:**
- Major fund families: Vanguard, Fidelity, American Funds, T. Rowe Price
- Fund types: Equity funds, bond funds, balanced funds, index funds
- Fund categories: Large cap, small cap, international, sector-specific
- CIK validation: Fund company CIK identifiers
- Filing schedules: N-Q, N-CSR, N-CSRS quarterly and annual filings
- Holdings disclosure: Top holdings, sector allocations, geographic exposure
- Share class variations: Class A, Class C, Institutional shares
- Fund performance: Expense ratios, turnover rates, benchmark tracking
- Shareholder base: Institutional vs retail ownership patterns
- Date ranges: Current holdings vs historical portfolio changes
- Search criteria: Asset size, fund category, investment style
- Regulatory compliance: SEC filing requirements and deadlines

#### 21. `test_esg.py` (from `esg.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `esg_disclosures()` - ESG disclosure filings and reports
- `esg_ratings()` - ESG ratings and scores for companies
- `esg_benchmark()` - ESG benchmark comparisons and sector analysis

**Test Parameters:**
- Large cap companies with ESG focus: AAPL, MSFT, GOOGL, JNJ
- ESG leaders: Companies with high ESG ratings across sectors
- ESG laggards: Companies with poor ESG performance
- Sector analysis: Technology, healthcare vs energy, materials ESG scores
- Rating agencies: Different ESG rating methodologies and scales
- ESG criteria: Environmental, Social, Governance component scores
- Benchmark comparisons: Peer group ESG performance analysis
- International companies: Global ESG standards and reporting
- ESG disclosure types: Sustainability reports, CSR reports, CDP submissions
- Materiality assessments: Industry-specific ESG factors
- ESG controversy tracking: Environmental incidents, social issues
- Sustainable investing: ESG-focused portfolio construction data

#### 22. `test_fundraising.py` (from `fundraising.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `crowdfunding_offerings_latest()` - Latest crowdfunding offerings and campaigns
- `crowdfunding_offerings_search()` - Search crowdfunding offerings by criteria
- `crowdfunding_offerings()` - Historical crowdfunding offering data
- `fundraising_latest()` - Latest venture capital and private equity fundraising
- `fundraising_search()` - Search VC/PE fundraising by criteria
- `fundraising()` - Historical fundraising data by CIK

**Test Parameters:**
- Crowdfunding platforms: Regulation CF, Regulation A+ offerings
- Offering types: Equity crowdfunding, debt crowdfunding, revenue-based
- Industry focus: Technology, healthcare, consumer products, real estate
- Funding stages: Pre-seed, seed, Series A, B, C, later stage rounds
- Geographic distribution: US regions, international fundraising
- Investment minimums: Retail vs accredited investor thresholds
- Funding targets: Small campaigns vs large institutional rounds
- Success rates: Fully funded vs partially funded campaigns
- CIK validation: Private company CIK identifiers
- Regulatory compliance: SEC filing requirements for fundraising
- Date ranges: Recent activity, seasonal fundraising patterns
- Search criteria: Industry, funding amount, geographic location

### 📊 **Bulk and Specialized Data**

#### 23. `test_bulk.py` (from `bulk.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `bulk_profiles()` - Bulk company profiles download by part
- `scores_bulk()` - Bulk financial scores for multiple symbols
- `upgrades_downgrades_consensus_bulk()` - Bulk analyst upgrade/downgrade data
- `profile_bulk()` - Bulk company profiles for symbol list
- `rating_bulk()` - Bulk analyst ratings for symbol list
- `dcf_bulk()` - Bulk discounted cash flow valuations
- `price_target_summary_bulk()` - Bulk price target summaries
- `etf_holder_bulk()` - Bulk ETF holdings data
- `key_metrics_ttm_bulk()` - Bulk TTM key metrics
- `ratios_ttm_bulk()` - Bulk TTM financial ratios
- `peers_bulk()` - Bulk peer comparison data
- `earnings_surprises_bulk()` - Bulk earnings surprise data by year
- `income_statement_bulk()` - Bulk income statements by year/period
- `income_statement_growth_bulk()` - Bulk income statement growth rates
- `balance_sheet_statement_bulk()` - Bulk balance sheet statements
- `balance_sheet_statement_growth_bulk()` - Bulk balance sheet growth rates
- `cash_flow_statement_bulk()` - Bulk cash flow statements
- `cash_flow_statement_growth_bulk()` - Bulk cash flow growth rates
- `eod_bulk()` - Bulk end-of-day price data by date

**Test Parameters:**
- Bulk download parts: Different partition segments for large datasets
- Symbol lists: 10, 50, 100, 500+ symbols for batch processing
- Large cap universe: S&P 500 constituents for comprehensive data
- Date parameters: Recent years, historical data availability
- Period combinations: Annual, quarterly data for financial statements
- Growth rate calculations: YoY, QoQ growth metrics validation
- Data completeness: Handling missing data, partial results
- Performance testing: Large bulk request response times
- Rate limiting: Bulk request frequency limitations
- Memory efficiency: Large dataset handling and processing
- Error handling: Invalid symbols in bulk requests
- Data consistency: Bulk vs individual endpoint result comparison

#### 24. `test_commitment_of_traders.py` (from `commitment_of_traders.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `commitment_of_traders_report()` - COT reports for futures positions
- `commitment_of_traders_report_analysis()` - COT analysis and insights
- `commitment_of_traders_report_list()` - Available COT report symbols

**Test Parameters:**
- Major futures contracts: ES (S&P 500), NQ (NASDAQ), YM (Dow), TY (10-Year Treasury)
- Currency futures: EUR, GBP, JPY, CHF, CAD, AUD futures
- Commodity futures: GC (Gold), SI (Silver), CL (Crude Oil), NG (Natural Gas)
- Agricultural futures: C (Corn), S (Soybeans), W (Wheat), CC (Cocoa)
- Interest rate futures: Fed Funds, Eurodollar, Treasury bond futures
- Date ranges: Weekly COT reports, historical trends, seasonal patterns
- Trader categories: Commercial hedgers, large speculators, small traders
- Position analysis: Long vs short positions, net positioning
- Market sentiment: Contrarian indicators, positioning extremes
- Report timing: Tuesday afternoon release schedule
- Data completeness: All available COT symbols and contracts
- Analysis metrics: Position changes, concentration ratios, market impact

#### 25. `test_economics.py` (from `economics.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `treasury_rates()` - US Treasury yield curve data
- `economic_indicators()` - Economic indicator data (GDP, inflation, unemployment)
- `economic_calendar()` - Economic event calendar and releases
- `market_risk_premium()` - Market risk premium calculations

**Test Parameters:**
- Treasury maturities: 1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y yields
- Economic indicators: GDP, CPI, PPI, unemployment rate, retail sales, housing
- Calendar events: FOMC meetings, employment reports, inflation data, GDP releases
- Release timing: Pre-market, during market, after market releases
- Market impact: High impact vs low impact economic releases
- Frequency: Daily, weekly, monthly, quarterly economic data
- Historical data: Long-term economic trends, recession periods
- International data: US vs global economic indicators
- Fed policy: Interest rate decisions, monetary policy statements
- Inflation measures: Core vs headline inflation, PCE vs CPI
- Employment data: Nonfarm payrolls, unemployment rate, labor participation
- Risk premium: Equity risk premium calculations and historical trends

#### 26. `test_discounted_cash_flow.py` (from `discounted_cash_flow.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `discounted_cash_flow_valuation()` - Standard DCF valuation models
- `discounted_cash_flow_levered()` - Levered DCF with debt considerations
- `discounted_cash_flow_custom()` - Custom DCF with user-defined parameters
- `discounted_cash_flow_custom_levered()` - Custom levered DCF models

**Test Parameters:**
- Stable growth companies: Mature companies with predictable cash flows
- High-growth companies: Technology, biotech with variable growth rates
- Cyclical companies: Automotive, industrials with cyclical patterns
- Capital-intensive companies: Utilities, railroads with high capex
- Financial companies: Banks, insurance with different DCF approaches
- REIT companies: Real estate with FFO-based valuations
- Discount rate variations: Different WACC assumptions and ranges
- Growth rate scenarios: Conservative, base case, optimistic projections
- Terminal value: Perpetual growth vs exit multiple approaches
- Cash flow adjustments: Working capital, capex, depreciation impacts
- Sensitivity analysis: Key assumption sensitivity testing
- Valuation comparison: DCF vs market price, peer multiples

#### 27. `test_news.py` (from `news.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `news_stock_latest()` - Latest stock-specific news articles
- `company_press_releases_latest()` - Latest company press releases
- `news_general_latest()` - Latest general market news
- `news_crypto_latest()` - Latest cryptocurrency news
- `news_forex()` - Forex market news (latest and historical versions)
  - Latest forex news (general market)
  - Historical forex news by specific symbols
- `price_target_news()` - Price target related news
- `price_target_latest_news()` - Latest price target news
- `news_stock()` - Historical stock-specific news
- `company_press_releases()` - Historical company press releases
- `news_crypto()` - Historical cryptocurrency news
- `stock_grade_news()` - Stock grade and rating news
- `stock_grade_latest_news()` - Latest stock grade news

**Test Parameters:**
- High-news stocks: AAPL, TSLA, AMZN with frequent news coverage
- Sectors: Technology, healthcare, energy news patterns
- News sources: Multiple news providers and wire services
- Article types: Breaking news, earnings, analyst reports, press releases
- Time ranges: Real-time, daily, weekly, monthly news archives
- Cryptocurrency news: BTC, ETH, DeFi, regulation news
- Forex news: Central bank announcements, economic policy news
- Sentiment analysis: Positive, negative, neutral news sentiment
- Market impact: High-impact vs routine news events
- Language: English language news content validation
- Article metadata: Publication date, source, headlines, content
- News frequency: High-frequency vs low-frequency news stocks

#### 28. `test_directory.py` (from `directory.py`) - ⚪ **NOT STARTED**
**Functions to test:**
- `stock_list()` - Complete list of available stocks
- `financial_statement_symbol_list()` - Stocks with financial statement data
- `cik_list()` - List of companies with CIK numbers
- `symbol_change()` - Historical symbol changes and ticker updates
- `etf_list()` - Complete list of available ETFs
- `actively_trading_list()` - Currently actively trading securities
- `earnings_transcript_list()` - Companies with earnings transcripts
- `available_exchanges()` - List of supported exchanges
- `available_sectors()` - List of available market sectors
- `available_industries()` - List of available industries
- `available_countries()` - List of supported countries
- `available_indexes()` - List of available market indices

**Test Parameters:**
- Exchange coverage: NYSE, NASDAQ, AMEX, OTC, international exchanges
- Asset types: Stocks, ETFs, REITs, ADRs, preferred shares
- Market cap ranges: Large, mid, small, micro-cap coverage
- Sector distribution: All 11 GICS sectors representation
- Geographic coverage: US domestic, international, emerging markets
- Symbol formats: Standard tickers, complex symbols with suffixes
- Status validation: Active vs inactive, trading vs suspended
- Data completeness: Symbols with full vs partial data coverage
- Historical changes: Mergers, acquisitions, spin-offs, bankruptcies
- CIK validation: Proper CIK format and SEC registration
- Industry classification: SIC codes, NAICS codes, GICS standards
- Index membership: Major index constituents and compositions

## Test Infrastructure Setup

### Required Components

#### 1. **Configuration Management** - ⚪ **NOT STARTED**
- Environment variables for API keys
- Test configuration settings
- Rate limiting management

#### 2. **Schema Validation Framework** - ⚪ **NOT STARTED**
- Pydantic model validation
- JSON schema comparison
- Custom validation functions

#### 3. **Test Data Management** - ⚪ **NOT STARTED**
- Parameterized test data sets
- Edge case scenarios
- Mock data for offline testing

#### 4. **Error Handling Tests** - ⚪ **NOT STARTED**
- Invalid API keys
- Rate limiting scenarios
- Network timeouts
- Invalid parameters

#### 5. **Performance Testing** - ⚪ **NOT STARTED**
- Response time benchmarks
- Rate limit compliance
- Concurrent request handling

## Next Steps

### Phase 1: Foundation (Priority 1)
1. **Fix model_registry.py** - Map all functions to correct schemas
2. **Create base test classes** - Common testing patterns
3. **Set up test environment** - API keys, configuration
4. **Implement schema validation** - Core validation logic

### Phase 2: Core Modules (Priority 2)
1. **test_quote.py** - Most fundamental endpoint
2. **test_search.py** - Basic search functionality
3. **test_company.py** - Company data validation
4. **test_analyst.py** - Analyst data validation

### Phase 3: Specialized Modules (Priority 3)
1. **Financial statements** - Income, balance sheet, cash flow
2. **Calendar events** - Earnings, dividends, economics
3. **Technical analysis** - Charts and indicators
4. **Alternative assets** - Crypto, forex, commodities

### Phase 4: Advanced Features (Priority 4)
1. **Regulatory data** - SEC filings, insider trades
2. **ESG and specialized data**
3. **Bulk operations**
4. **Performance optimization**

## Success Criteria

### For Each Test File:
- ✅ All API endpoints return expected schema structure
- ✅ Non-empty data validation for valid requests
- ✅ Proper error handling for invalid inputs
- ✅ Comprehensive parameter coverage
- ✅ Rate limiting compliance
- ✅ Performance benchmarks met

### For Overall Project:
- ✅ 100% endpoint coverage
- ✅ All tests pass with live API
- ✅ Comprehensive error scenario coverage
- ✅ Documentation and examples
- ✅ CI/CD integration ready

## Notes

### Important Considerations:
1. **Rate Limiting**: Tests must respect API rate limits
2. **API Key Management**: Secure handling of credentials
3. **Data Freshness**: Some endpoints may have delayed data
4. **Market Hours**: Some tests may behave differently outside market hours
5. **Maintenance Windows**: API may be unavailable during maintenance

### Testing Best Practices:
1. **Isolation**: Each test should be independent
2. **Deterministic**: Tests should produce consistent results
3. **Fast Feedback**: Critical tests should run quickly
4. **Clear Assertions**: Explicit validation of expected behavior
5. **Comprehensive Coverage**: Edge cases and error conditions

## Validation Summary

### Complete Function Coverage Verification ✅
- **Total Public API Functions**: 217
- **Functions Documented in Test Plan**: 217 (100% coverage)
- **Modules Covered**: 28 test files for 28 source modules
- **Missing Functions**: 0
- **Utility Functions**: 2 (iterate_over_pages, parse_response) - tested implicitly
- **Duplicate Functions**: 2 remaining duplicates
  - `available_sectors()` in both directory.py and indexes.py
  - `news_forex()` two versions (latest and historical)

### Schema Validation Requirements ✅
- All functions mapped to appropriate schemas in model_registry.py
- Pydantic models defined for all return types
- Custom validation for edge cases and error conditions

### Test Parameter Coverage ✅
- Symbol format validation for all asset types
- Edge case scenarios for all endpoints
- Error handling and negative testing
- Performance and rate limiting considerations

---
*Last Updated: July 5, 2025*
*Status: Implementation Phase - 6/28 Modules Completed (21.4%)*
*Total Functions Documented: 217 (100% Coverage)*
*Tests Implemented: 198 tests across 6 modules*
*Modules Completed:*
- ✅ test_quote.py (49 tests) - All 16 quote endpoints with comprehensive coverage
- ✅ test_search.py (40 tests) - Search, screener, and discovery endpoints
- ✅ test_company.py (33 tests) - Company profiles, data, and executive information
- ✅ test_analyst.py (27 tests) - Analyst estimates, ratings, price targets, and stock grades
- ✅ test_chart.py (23 tests) - Historical price data and intraday charts with all timeframes
- ✅ test_technical_indicators.py (26 tests) - All 9 technical indicators with API limitation handling
