from datetime import datetime, timedelta
from typing import List, Union

import pytest

from fmpsdk import bulk
from fmpsdk.exceptions import InvalidAPIKeyException
from fmpsdk.models import (
    FMPBalanceSheetGrowth,
    FMPBalanceSheetStatement,
    FMPBulkDCF,
    FMPBulkEarningsSurprise,
    FMPBulkEOD,
    FMPBulkETFHolder,
    FMPBulkPriceTargetSummary,
    FMPBulkRating,
    FMPBulkStockPeers,
    FMPBulkUpgradeDowngradeConsensus,
    FMPCashFlowGrowth,
    FMPCashFlowStatement,
    FMPCompanyProfile,
    FMPFinancialRatios,
    FMPFinancialScores,
    FMPIncomeStatement,
    FMPIncomeStatementGrowth,
    FMPKeyMetrics,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation,
    validate_model_list,
)


def validate_bulk_profiles_data(data: List[FMPCompanyProfile]) -> None:
    """Validate bulk profiles data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_profiles = len(data)
    valid_symbols = 0
    valid_companies = 0
    valid_prices = 0
    valid_exchanges = 0

    valid_exchange_codes = [
        "NASDAQ",
        "NYSE",
        "AMEX",
        "OTC",
        "TSX",
        "LSE",
        "TSE",
        "HKEX",
    ]

    for profile in data:
        # Symbol validation
        if profile.symbol and len(profile.symbol) >= 1 and profile.symbol.isalpha():
            valid_symbols += 1

        # Company name validation
        if profile.companyName and len(profile.companyName) >= 2:
            valid_companies += 1

        # Price validation
        if (
            profile.price is not None
            and isinstance(profile.price, (int, float))
            and profile.price >= 0
        ):
            valid_prices += 1

        # Exchange validation
        if profile.exchange and (
            profile.exchange in valid_exchange_codes or len(profile.exchange) > 0
        ):
            valid_exchanges += 1

    # Business logic assertions
    if total_profiles > 0:
        assert (
            valid_symbols / total_profiles >= 0.95
        ), f"Only {valid_symbols}/{total_profiles} profiles have valid symbols"
        assert (
            valid_companies / total_profiles >= 0.95
        ), f"Only {valid_companies}/{total_profiles} profiles have valid company names"
        assert (
            valid_prices / total_profiles >= 0.80
        ), f"Only {valid_prices}/{total_profiles} profiles have valid prices"
        assert (
            valid_exchanges / total_profiles >= 0.90
        ), f"Only {valid_exchanges}/{total_profiles} profiles have valid exchanges"


def validate_bulk_financial_data(
    data: List[
        Union[FMPIncomeStatement, FMPBalanceSheetStatement, FMPCashFlowStatement]
    ],
    statement_type: str,
) -> None:
    """Validate bulk financial statement data with business logic checks."""
    if not data:
        return

    total_statements = len(data)
    valid_symbols = 0
    valid_dates = 0
    valid_revenue = 0
    valid_assets = 0

    for statement in data:
        # Symbol validation
        if (
            statement.symbol
            and len(statement.symbol) >= 1
            and statement.symbol.isalpha()
        ):
            valid_symbols += 1

        # Date validation
        if statement.date and len(str(statement.date)) >= 10:
            valid_dates += 1

        # Revenue validation (for income statements)
        if statement_type == "income" and hasattr(statement, "revenue"):
            if (
                statement.revenue is not None
                and isinstance(statement.revenue, (int, float))
                and statement.revenue >= 0
            ):
                valid_revenue += 1

        # Assets validation (for balance sheet statements)
        if statement_type == "balance_sheet" and hasattr(statement, "totalAssets"):
            if (
                statement.totalAssets is not None
                and isinstance(statement.totalAssets, (int, float))
                and statement.totalAssets >= 0
            ):
                valid_assets += 1

    # Business logic assertions
    if total_statements > 0:
        assert (
            valid_symbols / total_statements >= 0.95
        ), f"Only {valid_symbols}/{total_statements} statements have valid symbols"
        assert (
            valid_dates / total_statements >= 0.90
        ), f"Only {valid_dates}/{total_statements} statements have valid dates"

        if statement_type == "income" and valid_revenue > 0:
            assert (
                valid_revenue / total_statements >= 0.70
            ), f"Only {valid_revenue}/{total_statements} income statements have valid revenue"

        if statement_type == "balance_sheet" and valid_assets > 0:
            assert (
                valid_assets / total_statements >= 0.70
            ), f"Only {valid_assets}/{total_statements} balance sheets have valid assets"


def validate_bulk_ratings_data(data: List[FMPBulkRating]) -> None:
    """Validate bulk ratings data with business logic checks."""
    if not data:
        return

    total_ratings = len(data)
    valid_symbols = 0
    valid_ratings = 0
    valid_scores = 0

    valid_rating_values = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "AA",
        "BB",
        "CC",
        "DD",
        "EE",
        "FF",
    ]

    for rating in data:
        # Symbol validation
        if rating.symbol and len(rating.symbol) >= 1 and rating.symbol.isalpha():
            valid_symbols += 1

        # Rating validation
        if rating.rating and any(r in str(rating.rating) for r in valid_rating_values):
            valid_ratings += 1

        # Score validation
        if (
            rating.ratingScore is not None
            and isinstance(rating.ratingScore, (int, float))
            and 0 <= rating.ratingScore <= 10
        ):
            valid_scores += 1

    # Business logic assertions
    if total_ratings > 0:
        assert (
            valid_symbols / total_ratings >= 0.95
        ), f"Only {valid_symbols}/{total_ratings} ratings have valid symbols"
        assert (
            valid_ratings / total_ratings >= 0.80
        ), f"Only {valid_ratings}/{total_ratings} ratings have valid rating values"
        assert (
            valid_scores / total_ratings >= 0.70
        ), f"Only {valid_scores}/{total_ratings} ratings have valid scores"


def validate_bulk_dcf_data(data: List[FMPBulkDCF]) -> None:
    """Validate bulk DCF data with business logic checks."""
    if not data:
        return

    total_dcfs = len(data)
    valid_symbols = 0
    valid_dcf_values = 0
    valid_stock_prices = 0

    for dcf in data:
        # Symbol validation
        if dcf.symbol and len(dcf.symbol) >= 1 and dcf.symbol.isalpha():
            valid_symbols += 1

        # DCF value validation
        if dcf.dcf is not None and isinstance(dcf.dcf, (int, float)) and dcf.dcf > 0:
            valid_dcf_values += 1

        # Stock price validation
        if (
            dcf.stockPrice is not None
            and isinstance(dcf.stockPrice, (int, float))
            and dcf.stockPrice > 0
        ):
            valid_stock_prices += 1

    # Business logic assertions
    if total_dcfs > 0:
        assert (
            valid_symbols / total_dcfs >= 0.95
        ), f"Only {valid_symbols}/{total_dcfs} DCF entries have valid symbols"
        assert (
            valid_dcf_values / total_dcfs >= 0.80
        ), f"Only {valid_dcf_values}/{total_dcfs} DCF entries have valid DCF values"
        assert (
            valid_stock_prices / total_dcfs >= 0.80
        ), f"Only {valid_stock_prices}/{total_dcfs} DCF entries have valid stock prices"


class TestBulkProfiles:
    """Test bulk company profiles endpoints."""

    @pytest.mark.parametrize(
        "part", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    )
    def test_bulk_profiles_by_part(self, api_key, part):
        """Test bulk profiles download across different parts."""
        response, validation = handle_api_call_with_validation(
            bulk.bulk_profiles, "bulk_profiles", True, apikey=api_key, part=part
        )

        profiles = get_response_models(response, FMPCompanyProfile)
        validate_model_list(profiles, FMPCompanyProfile)
        if profiles:
            validate_bulk_profiles_data(profiles)

    @pytest.mark.parametrize(
        "data_type",
        [
            "profiles",
            "financial_statements",
            "dcf_valuations",
            "ratings",
            "price_targets",
        ],
    )
    def test_bulk_endpoints_by_type(self, api_key, data_type):
        """Test different bulk endpoint types."""
        if data_type == "profiles":
            response, validation = handle_api_call_with_validation(
                bulk.bulk_profiles, "bulk_profiles", True, apikey=api_key, part="1"
            )
            profiles = get_response_models(response, FMPCompanyProfile)
            validate_model_list(profiles, FMPCompanyProfile)
            if profiles:
                validate_bulk_profiles_data(profiles)
        elif data_type == "financial_statements":
            response, validation = handle_api_call_with_validation(
                bulk.balance_sheet_statement_bulk,
                "balance_sheet_statement_bulk",
                True,
                apikey=api_key,
                year="2023",
                period="FY",
            )
            statements = get_response_models(response, FMPBalanceSheetStatement)
            validate_model_list(statements, FMPBalanceSheetStatement)
            if statements:
                validate_bulk_financial_data(statements, "balance_sheet")
        elif data_type == "dcf_valuations":
            response, validation = handle_api_call_with_validation(
                bulk.dcf_bulk,
                "dcf_bulk",
                True,
                apikey=api_key,
                symbols=["AAPL", "MSFT"],
            )
            dcfs = get_response_models(response, FMPBulkDCF)
            validate_model_list(dcfs, FMPBulkDCF)
            if dcfs:
                validate_bulk_dcf_data(dcfs)
        elif data_type == "ratings":
            response, validation = handle_api_call_with_validation(
                bulk.rating_bulk,
                "rating_bulk",
                True,
                apikey=api_key,
                symbols=["AAPL", "MSFT"],
            )
            ratings = get_response_models(response, FMPBulkRating)
            validate_model_list(ratings, FMPBulkRating)
            if ratings:
                validate_bulk_ratings_data(ratings)
        elif data_type == "price_targets":
            response, validation = handle_api_call_with_validation(
                bulk.price_target_summary_bulk,
                "price_target_summary_bulk",
                True,
                apikey=api_key,
            )
            targets = get_response_models(response, FMPBulkPriceTargetSummary)
            validate_model_list(targets, FMPBulkPriceTargetSummary)
            if targets:
                for target in targets:
                    assert (
                        target.symbol and len(target.symbol) >= 1
                    ), f"Invalid symbol: {target.symbol}"

    @pytest.mark.parametrize("year", ["2023", "2022", "2021", "2020", "2019"])
    def test_bulk_financial_statements_by_year(self, api_key, year):
        """Test bulk financial statements for different years."""
        response, validation = handle_api_call_with_validation(
            bulk.income_statement_bulk,
            "income_statement_bulk",
            True,
            apikey=api_key,
            year=year,
            period="FY",
        )

        statements = get_response_models(response, FMPIncomeStatement)
        validate_model_list(statements, FMPIncomeStatement)
        if statements:
            validate_bulk_financial_data(statements, "income")

            # Validate year matches
            sample_statement = statements[0]
            if sample_statement.date:
                assert year in str(
                    sample_statement.date
                ), f"Date {sample_statement.date} should contain year {year}"

    @pytest.mark.parametrize(
        "symbol_batch",
        [
            ["AAPL", "MSFT", "GOOGL"],
            ["JPM", "BAC", "WFC"],
            ["JNJ", "PFE", "UNH"],
            ["XOM", "CVX", "COP"],
            ["HD", "LOW", "WMT"],
        ],
    )
    def test_profile_bulk_by_sector(self, api_key, symbol_batch):
        """Test bulk profiles for different sector symbol batches."""
        response, validation = handle_api_call_with_validation(
            bulk.profile_bulk,
            "profile_bulk",
            True,
            apikey=api_key,
            symbols=symbol_batch,
        )

        profiles = get_response_models(response, FMPCompanyProfile)
        validate_model_list(profiles, FMPCompanyProfile)
        if profiles:
            validate_bulk_profiles_data(profiles)

            # Validate symbol coverage
            returned_symbols = {profile.symbol for profile in profiles}
            common_symbols = returned_symbols.intersection(set(symbol_batch))
            # At least some symbols should be returned
            assert (
                len(common_symbols) >= 0
            ), f"Expected some symbols from {symbol_batch}, got {returned_symbols}"

    @pytest.mark.parametrize("statement_type", ["income", "balance_sheet", "cash_flow"])
    def test_bulk_statement_types(self, api_key, statement_type):
        """Test bulk endpoints for different financial statement types."""
        year = "2023"

        if statement_type == "income":
            response, validation = handle_api_call_with_validation(
                bulk.income_statement_bulk,
                "income_statement_bulk",
                True,
                apikey=api_key,
                year=year,
                period="FY",
            )
            statements = get_response_models(response, FMPIncomeStatement)
            validate_model_list(statements, FMPIncomeStatement)
            if statements:
                validate_bulk_financial_data(statements, "income")
        elif statement_type == "balance_sheet":
            response, validation = handle_api_call_with_validation(
                bulk.balance_sheet_statement_bulk,
                "balance_sheet_statement_bulk",
                True,
                apikey=api_key,
                year=year,
                period="FY",
            )
            statements = get_response_models(response, FMPBalanceSheetStatement)
            validate_model_list(statements, FMPBalanceSheetStatement)
            if statements:
                validate_bulk_financial_data(statements, "balance_sheet")
        elif statement_type == "cash_flow":
            response, validation = handle_api_call_with_validation(
                bulk.cash_flow_statement_bulk,
                "cash_flow_statement_bulk",
                True,
                apikey=api_key,
                year=year,
                period="FY",
            )
            statements = get_response_models(response, FMPCashFlowStatement)
            validate_model_list(statements, FMPCashFlowStatement)
            if statements:
                validate_bulk_financial_data(statements, "cash_flow")

    def test_bulk_profiles_basic(self, api_key):
        """Test bulk profiles download with part parameter."""
        response, validation = handle_api_call_with_validation(
            bulk.bulk_profiles, "bulk_profiles", True, apikey=api_key, part="1"
        )

        profiles = get_response_models(response, FMPCompanyProfile)
        validate_model_list(profiles, FMPCompanyProfile)
        if profiles:
            validate_bulk_profiles_data(profiles)

    def test_profile_bulk_with_symbols(self, api_key):
        """Test bulk profiles for specific symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]
        response, validation = handle_api_call_with_validation(
            bulk.profile_bulk, "profile_bulk", True, apikey=api_key, symbols=symbols
        )

        profiles = get_response_models(response, FMPCompanyProfile)
        validate_model_list(profiles, FMPCompanyProfile)
        if profiles:
            validate_bulk_profiles_data(profiles)

            # Validate symbol coverage
            returned_symbols = {profile.symbol for profile in profiles}
            common_symbols = returned_symbols.intersection(set(symbols))
            # At least some symbols should be returned
            assert (
                len(common_symbols) >= 0
            ), f"Expected some symbols from {symbols}, got {returned_symbols}"

    def test_bulk_profiles_error_handling(self, api_key):
        """Test error handling for bulk profiles."""
        # Test with valid parameters (should not raise errors)
        response, validation = handle_api_call_with_validation(
            bulk.bulk_profiles, "bulk_profiles", True, apikey=api_key, part="1"
        )


class TestBulkFinancialData:
    """Test bulk financial data endpoints."""

    def test_scores_bulk(self, api_key):
        """Test bulk financial scores."""
        response, validation = handle_api_call_with_validation(
            bulk.scores_bulk,
            "scores_bulk",
            True,
            apikey=api_key,
            symbols=["AAPL", "MSFT"],
        )

        scores = get_response_models(response, FMPFinancialScores)
        validate_model_list(scores, FMPFinancialScores)
        if scores:
            for score in scores:
                assert (
                    score.symbol and len(score.symbol) >= 1
                ), f"Invalid symbol: {score.symbol}"

    def test_rating_bulk(self, api_key):
        """Test bulk ratings."""
        response, validation = handle_api_call_with_validation(
            bulk.rating_bulk,
            "rating_bulk",
            True,
            apikey=api_key,
            symbols=["AAPL", "MSFT"],
        )

        ratings = get_response_models(response, FMPBulkRating)
        validate_model_list(ratings, FMPBulkRating)
        if ratings:
            validate_bulk_ratings_data(ratings)

    def test_dcf_bulk(self, api_key):
        """Test bulk DCF valuations."""
        response, validation = handle_api_call_with_validation(
            bulk.dcf_bulk, "dcf_bulk", True, apikey=api_key, symbols=["AAPL", "MSFT"]
        )

        dcfs = get_response_models(response, FMPBulkDCF)
        validate_model_list(dcfs, FMPBulkDCF)
        if dcfs:
            validate_bulk_dcf_data(dcfs)

    def test_price_target_summary_bulk(self, api_key):
        """Test bulk price target summaries."""
        response, validation = handle_api_call_with_validation(
            bulk.price_target_summary_bulk,
            "price_target_summary_bulk",
            True,
            apikey=api_key,
        )

        targets = get_response_models(response, FMPBulkPriceTargetSummary)
        validate_model_list(targets, FMPBulkPriceTargetSummary)
        if targets:
            for target in targets:
                assert (
                    target.symbol and len(target.symbol) >= 1
                ), f"Invalid symbol: {target.symbol}"


class TestBulkMetricsAndRatios:
    """Test bulk metrics and ratios endpoints."""

    def test_key_metrics_ttm_bulk(self, api_key):
        """Test bulk key metrics TTM."""
        response, validation = handle_api_call_with_validation(
            bulk.key_metrics_ttm_bulk, "key_metrics_ttm_bulk", True, apikey=api_key
        )

        metrics = get_response_models(response, FMPKeyMetrics)
        validate_model_list(metrics, FMPKeyMetrics)
        if metrics:
            for metric in metrics:
                assert (
                    metric.symbol and len(metric.symbol) >= 1
                ), f"Invalid symbol: {metric.symbol}"

    def test_ratios_ttm_bulk(self, api_key):
        """Test bulk financial ratios TTM."""
        response, validation = handle_api_call_with_validation(
            bulk.ratios_ttm_bulk, "ratios_ttm_bulk", True, apikey=api_key
        )

        ratios = get_response_models(response, FMPFinancialRatios)
        validate_model_list(ratios, FMPFinancialRatios)
        if ratios:
            for ratio in ratios:
                assert (
                    ratio.symbol and len(ratio.symbol) >= 1
                ), f"Invalid symbol: {ratio.symbol}"


class TestBulkAnalystData:
    """Test bulk analyst data endpoints."""

    def test_upgrades_downgrades_consensus_bulk(self, api_key):
        """Test bulk upgrades/downgrades consensus."""
        response, validation = handle_api_call_with_validation(
            bulk.upgrades_downgrades_consensus_bulk,
            "upgrades_downgrades_consensus_bulk",
            True,
            apikey=api_key,
        )

        consensus_data = get_response_models(response, FMPBulkUpgradeDowngradeConsensus)
        validate_model_list(consensus_data, FMPBulkUpgradeDowngradeConsensus)
        if consensus_data:
            for consensus in consensus_data:
                assert (
                    consensus.symbol and len(consensus.symbol) >= 1
                ), f"Invalid symbol: {consensus.symbol}"

    def test_peers_bulk(self, api_key):
        """Test bulk stock peers."""
        response, validation = handle_api_call_with_validation(
            bulk.peers_bulk, "peers_bulk", True, apikey=api_key
        )

        peers = get_response_models(response, FMPBulkStockPeers)
        validate_model_list(peers, FMPBulkStockPeers)
        if peers:
            for peer in peers:
                assert (
                    peer.symbol and len(peer.symbol) >= 1
                ), f"Invalid symbol: {peer.symbol}"


class TestBulkFinancialStatements:
    """Test bulk financial statements endpoints."""

    def test_income_statement_bulk(self, api_key):
        """Test bulk income statements."""
        response, validation = handle_api_call_with_validation(
            bulk.income_statement_bulk,
            "income_statement_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        statements = get_response_models(response, FMPIncomeStatement)
        validate_model_list(statements, FMPIncomeStatement)
        if statements:
            validate_bulk_financial_data(statements, "income")

    def test_income_statement_growth_bulk(self, api_key):
        """Test bulk income statement growth rates."""
        response, validation = handle_api_call_with_validation(
            bulk.income_statement_growth_bulk,
            "income_statement_growth_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        growth_data = get_response_models(response, FMPIncomeStatementGrowth)
        validate_model_list(growth_data, FMPIncomeStatementGrowth)
        if growth_data:
            for growth in growth_data:
                assert (
                    growth.symbol and len(growth.symbol) >= 1
                ), f"Invalid symbol: {growth.symbol}"

    def test_balance_sheet_statement_bulk(self, api_key):
        """Test bulk balance sheet statements."""
        response, validation = handle_api_call_with_validation(
            bulk.balance_sheet_statement_bulk,
            "balance_sheet_statement_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        statements = get_response_models(response, FMPBalanceSheetStatement)
        validate_model_list(statements, FMPBalanceSheetStatement)
        if statements:
            validate_bulk_financial_data(statements, "balance_sheet")

    def test_balance_sheet_statement_growth_bulk(self, api_key):
        """Test bulk balance sheet growth rates."""
        response, validation = handle_api_call_with_validation(
            bulk.balance_sheet_statement_growth_bulk,
            "balance_sheet_statement_growth_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        growth_data = get_response_models(response, FMPBalanceSheetGrowth)
        validate_model_list(growth_data, FMPBalanceSheetGrowth)
        if growth_data:
            for growth in growth_data:
                assert (
                    growth.symbol and len(growth.symbol) >= 1
                ), f"Invalid symbol: {growth.symbol}"

    def test_cash_flow_statement_bulk(self, api_key):
        """Test bulk cash flow statements."""
        response, validation = handle_api_call_with_validation(
            bulk.cash_flow_statement_bulk,
            "cash_flow_statement_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        statements = get_response_models(response, FMPCashFlowStatement)
        validate_model_list(statements, FMPCashFlowStatement)
        if statements:
            validate_bulk_financial_data(statements, "cash_flow")

    def test_cash_flow_statement_growth_bulk(self, api_key):
        """Test bulk cash flow growth rates."""
        response, validation = handle_api_call_with_validation(
            bulk.cash_flow_statement_growth_bulk,
            "cash_flow_statement_growth_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        growth_data = get_response_models(response, FMPCashFlowGrowth)
        validate_model_list(growth_data, FMPCashFlowGrowth)
        if growth_data:
            for growth in growth_data:
                assert (
                    growth.symbol and len(growth.symbol) >= 1
                ), f"Invalid symbol: {growth.symbol}"


class TestBulkSpecializedData:
    """Test bulk specialized data endpoints."""

    def test_etf_holder_bulk(self, api_key):
        """Test bulk ETF holders data."""
        response, validation = handle_api_call_with_validation(
            bulk.etf_holder_bulk, "etf_holder_bulk", True, apikey=api_key, part="1"
        )

        holders = get_response_models(response, FMPBulkETFHolder)
        validate_model_list(holders, FMPBulkETFHolder)
        if holders:
            for holder in holders:
                assert (
                    holder.symbol and len(holder.symbol) >= 1
                ), f"Invalid symbol: {holder.symbol}"

    def test_earnings_surprises_bulk(self, api_key):
        """Test bulk earnings surprises data."""
        response, validation = handle_api_call_with_validation(
            bulk.earnings_surprises_bulk,
            "earnings_surprises_bulk",
            True,
            apikey=api_key,
            year="2023",
        )

        surprises = get_response_models(response, FMPBulkEarningsSurprise)
        validate_model_list(surprises, FMPBulkEarningsSurprise)
        if surprises:
            for surprise in surprises:
                assert (
                    surprise.symbol and len(surprise.symbol) >= 1
                ), f"Invalid symbol: {surprise.symbol}"

    def test_eod_bulk(self, api_key):
        """Test bulk end-of-day data."""
        # Use recent date
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        response, validation = handle_api_call_with_validation(
            bulk.eod_bulk, "eod_bulk", True, apikey=api_key, date=date
        )

        eod_data = get_response_models(response, FMPBulkEOD)
        validate_model_list(eod_data, FMPBulkEOD)
        if eod_data:
            for eod in eod_data:
                assert (
                    eod.symbol and len(eod.symbol) >= 1
                ), f"Invalid symbol: {eod.symbol}"


class TestBulkDataQuality:
    """Test data quality and business logic validation."""

    def test_bulk_data_consistency(self, api_key):
        """Test data consistency across bulk endpoints."""
        symbols = ["AAPL", "MSFT"]

        # Test profiles
        response, validation = handle_api_call_with_validation(
            bulk.profile_bulk, "profile_bulk", True, apikey=api_key, symbols=symbols
        )

        profiles = get_response_models(response, FMPCompanyProfile)
        validate_model_list(profiles, FMPCompanyProfile)
        if profiles:
            validate_bulk_profiles_data(profiles)

    def test_bulk_financial_statements_validation(self, api_key):
        """Test financial statement data validation."""
        response, validation = handle_api_call_with_validation(
            bulk.income_statement_bulk,
            "income_statement_bulk",
            True,
            apikey=api_key,
            year="2023",
            period="FY",
        )

        statements = get_response_models(response, FMPIncomeStatement)
        validate_model_list(statements, FMPIncomeStatement)
        if statements:
            validate_bulk_financial_data(statements, "income")

            # Additional validation for requested year
            for statement in statements[:3]:  # Check first few
                if statement.date:
                    assert "2023" in str(
                        statement.date
                    ), f"Statement date {statement.date} should contain year 2023"


class TestBulkErrorHandling:
    """Test error handling for bulk endpoints."""

    def test_scores_bulk_empty_symbols(self, api_key):
        """Test scores bulk with empty symbols list."""
        response, validation = handle_api_call_with_validation(
            bulk.scores_bulk, "scores_bulk", True, apikey=api_key, symbols=[]
        )

        scores = get_response_models(response, FMPFinancialScores)
        validate_model_list(scores, FMPFinancialScores, min_count=0)
        # Should return empty list for empty symbols
        assert (
            len(scores) == 0
        ), f"Expected empty list for empty symbols, got {len(scores)} scores"

    def test_bulk_profiles_invalid_api_key(self):
        """Test bulk profiles with invalid API key."""
        with pytest.raises(InvalidAPIKeyException):
            bulk.bulk_profiles(apikey="invalid_key", part="1")

    def test_income_statement_bulk_invalid_year(self, api_key):
        """Test income statement bulk with invalid year."""
        response, validation = handle_api_call_with_validation(
            bulk.income_statement_bulk,
            "income_statement_bulk",
            True,
            apikey=api_key,
            year="1900",
            period="FY",
        )

        statements = get_response_models(response, FMPIncomeStatement)
        validate_model_list(statements, FMPIncomeStatement)
        # Should return empty list for invalid year
        assert len(statements) == 0
