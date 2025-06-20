# FMP SDK
The idea behind this project is to provide a 'one-stop-shop' to the API endpoints provided by 
[Financial Model Prep](http://financialmodelingprep.com) website.

**Note: fmpsdk should be synced with FMP's API changelog as of 20250515.  Changes thereafter are not yet included.**

## How to Use
1. Install the package: `pip install fmpsdk`
1. Create a .env file and put your apikey in it.  Inside .env: `apikey='blah'`
1. Use `fmpsdk.<some function>(apikey=apikey, <possibly more variables>)` to query the API for that "some function".
1. The return from that function call is almost always a List of Dictionaries.  It is up to you to parse it.

## Example code
Here is a "quick start" script example.  A larger, more detailed example is in the file `fmpsdk-example.py`.
```python
#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import fmpsdk
from fmpsdk.models import FmpStockSymbolSearchResponse

# Actual API key is stored in a .env file. Not good to store API key directly in script.
load_dotenv()
apikey = os.environ.get("apikey")

# Query an endpoint (response is auto-parsed to a Pydantic model)
result = fmpsdk.search_symbol(apikey=apikey, query="AAPL")
print(result)  # result is a FmpStockSymbolSearchResponse instance

# Access parsed data
for item in result.__root__:
    print(item.symbol, item.name)
```

## Response Models
All endpoint responses are automatically parsed into Pydantic models for type safety and autocompletion. Models are available in `fmpsdk.models` and mapped in `fmpsdk.model_registry.ENDPOINT_MODEL_MAP`.

- Each endpoint function returns a model instance (or list of models) matching the FMP API schema.
- You can import and use these models directly for type checking and IDE support.

## Endpoint Coverage
fmpsdk covers all documented FMP endpoints. The following endpoint functions are available:

- actives
- analyst_estimates
- analyst_recommendations
- commodities_quote
- commodities_quote_short
- batch_commodity_quotes
- available_cryptocurrencies
- available_etfs
- available_euronext
- available_forex
- available_indexes
- available_industries
- available_mutual_funds
- available_sectors
- available_traded_list
- batch_pre_post_market_trade
- batch_quote
- biggest_gainers
- biggest_losers
- cash_flow_statement
- company_news
- company_news_latest
- company_press_releases
- company_press_releases_latest
- company_profile
- commitment_of_traders_report
- commitment_of_traders_report_analysis
- commitment_of_traders_report_list
- crypto_news
- cryptocurrencies_list
- cusip
- cik
- cik_list
- cik_search
- delisted_companies
- dowjones_constituent
- earning_calendar
- earning_calendar_confirmed
- earnings_surprises
- etf_country_weightings
- etf_holders
- etf_info
- etf_sector_weightings
- exchange_realtime
- financial_growth
- financial_ratios
- financial_ratios_ttm
- financial_statement
- financial_statement_full_as_reported
- financial_statement_symbol_lists
- form_13f
- full_real_time_price
- gainers
- general_news
- historical_chart
- historical_daily_discounted_cash_flow
- historical_discounted_cash_flow
- historical_employee_count
- historical_market_capitalization
- historical_nasdaq_constituent
- historical_price_full
- historical_rating
- historical_sectors_performance
- historical_sp500_constituent
- historical_stock_dividend
- historical_stock_split
- income_statement
- income_statement_as_reported
- income_statement_growth
- indexes
- insider_trade_statistics
- insider_trading
- insider_trading_rss_feed
- institutional_holders
- key_executives
- key_metrics
- key_metrics_ttm
- last_crypto_price
- live_full_price
- losers
- market_capitalization
- market_hours
- market_open
- mergers_acquisitions_rss_feed
- most_actives
- mutual_fund_holders
- mutual_fund_list
- nasdaq_constituent
- news_sentiment_rss
- press_releases
- price_target
- price_target_consensus
- quote
- quote_short
- rating
- search
- search_ticker
- sec_filings
- sec_rss_feeds
- sectors_performance
- senate_disclosure_rss
- senate_disclosure_symbol
- senate_trading_rss
- senate_trading_symbol
- shares_float
- social_sentiments
- sp500_constituent
- stock_news
- stock_screener
- symbols_list
- technical_indicators
- trending_sentiment
- upgrades_downgrades
- upgrades_downgrades_consensus
- upgrades_downgrades_consensus_bulk
- bulk_historical_eod
- bulk_profiles
- economic_indicator
- treasury_rates
- scores_bulk


## Advanced Usage
- All endpoints are accessible from the package root: `fmpsdk.<endpoint_function>()`
- All responses are parsed using the `@parse_response` decorator.
- Models are mapped in `fmpsdk.model_registry.ENDPOINT_MODEL_MAP`.

## Contributing
See `plan.md` for the current roadmap and coverage checklist.

## Attribution
Special thanks to the following people who have pitched in on this project!  Open source works thanks to people who 
jump in and help!  These are this project's stars.  Thank you.
  - [Ken Caruso](https://github.com/ipl31)
  - [iforgotmypass](https://github.com/iforgotmypass)
  - [Ivelin Ivanov](https://github.com/ivelin)
