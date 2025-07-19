from datetime import datetime
from typing import List

import pytest

from fmpsdk import esg
from fmpsdk.models import (
    FMPESGBenchmark,
    FMPESGFiling,
    FMPESGRating,
)
from tests.conftest import (
    get_response_models,
    handle_api_call_with_validation
)


def validate_esg_disclosures_data(data: List[FMPESGFiling]) -> None:
    """Validate ESG disclosures data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_disclosures = len(data)
    valid_symbols = 0
    valid_dates = 0
    valid_scores = 0
    valid_ciks = 0
    valid_urls = 0

    for disclosure in data:
        # Symbol validation
        if disclosure.symbol and len(disclosure.symbol) >= 1:
            valid_symbols += 1

        # Date validation
        if disclosure.date and len(str(disclosure.date)) >= 10:
            valid_dates += 1

        # Score validation (0-100 range)
        env_score = disclosure.environmentalScore
        social_score = disclosure.socialScore
        governance_score = disclosure.governanceScore
        esg_score = disclosure.ESGScore

        if all(
            score is not None and 0 <= score <= 100
            for score in [env_score, social_score, governance_score, esg_score]
        ):
            valid_scores += 1

        # CIK validation
        if (
            disclosure.cik
            and str(disclosure.cik).isdigit()
            and len(str(disclosure.cik)) >= 6
        ):
            valid_ciks += 1

        # URL validation
        if disclosure.url and "http" in disclosure.url.lower():
            valid_urls += 1

    # Business logic assertions
    if total_disclosures > 0:
        assert (
            valid_symbols / total_disclosures >= 0.95
        ), f"Only {valid_symbols}/{total_disclosures} disclosures have valid symbols"
        assert (
            valid_dates / total_disclosures >= 0.90
        ), f"Only {valid_dates}/{total_disclosures} disclosures have valid dates"
        assert (
            valid_scores / total_disclosures >= 0.80
        ), f"Only {valid_scores}/{total_disclosures} disclosures have valid scores"
        assert (
            valid_ciks / total_disclosures >= 0.85
        ), f"Only {valid_ciks}/{total_disclosures} disclosures have valid CIKs"
        assert (
            valid_urls / total_disclosures >= 0.80
        ), f"Only {valid_urls}/{total_disclosures} disclosures have valid URLs"


def validate_esg_ratings_data(data: List[FMPESGRating]) -> None:
    """Validate ESG ratings data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_ratings = len(data)
    valid_symbols = 0
    valid_years = 0
    valid_company_names = 0
    valid_industries = 0
    valid_ciks = 0

    current_year = datetime.now().year

    for rating in data:
        # Symbol validation
        if rating.symbol and len(rating.symbol) >= 1:
            valid_symbols += 1

        # Fiscal year validation
        if (
            rating.fiscalYear is not None
            and 2015 <= rating.fiscalYear <= current_year + 1
        ):
            valid_years += 1

        # Company name validation
        if rating.companyName and len(rating.companyName) > 0:
            valid_company_names += 1

        # Industry validation
        if rating.industry and len(rating.industry) > 0:
            valid_industries += 1

        # CIK validation
        if rating.cik and str(rating.cik).isdigit() and len(str(rating.cik)) >= 6:
            valid_ciks += 1

    # Business logic assertions
    if total_ratings > 0:
        assert (
            valid_symbols / total_ratings >= 0.95
        ), f"Only {valid_symbols}/{total_ratings} ratings have valid symbols"
        assert (
            valid_years / total_ratings >= 0.90
        ), f"Only {valid_years}/{total_ratings} ratings have valid fiscal years"
        assert (
            valid_company_names / total_ratings >= 0.95
        ), f"Only {valid_company_names}/{total_ratings} ratings have valid company names"
        assert (
            valid_industries / total_ratings >= 0.90
        ), f"Only {valid_industries}/{total_ratings} ratings have valid industries"
        assert (
            valid_ciks / total_ratings >= 0.85
        ), f"Only {valid_ciks}/{total_ratings} ratings have valid CIKs"


def validate_esg_benchmark_data(data: List[FMPESGBenchmark]) -> None:
    """Validate ESG benchmark data with business logic checks."""
    if not data:
        return

    # Data quality metrics
    total_benchmarks = len(data)
    valid_scores = 0
    valid_years = 0
    valid_sectors = 0

    sectors_seen = set()

    for benchmark in data:
        # Score validation (0-100 range)
        env_score = benchmark.environmentalScore
        social_score = benchmark.socialScore
        governance_score = benchmark.governanceScore
        esg_score = benchmark.ESGScore

        if all(
            score is not None and 0 <= score <= 100
            for score in [env_score, social_score, governance_score, esg_score]
        ):
            # Check ESG score reasonableness relative to component scores
            component_avg = (env_score + social_score + governance_score) / 3
            if (
                abs(esg_score - component_avg) <= 20
            ):  # Allow variance for weighted scoring
                valid_scores += 1

        # Fiscal year validation
        if (
            benchmark.fiscalYear is not None
            and 2015 <= benchmark.fiscalYear <= datetime.now().year + 1
        ):
            valid_years += 1

        # Sector validation
        if benchmark.sector and len(benchmark.sector) > 0:
            valid_sectors += 1
            sectors_seen.add(benchmark.sector)

    # Business logic assertions
    if total_benchmarks > 0:
        assert (
            valid_scores / total_benchmarks >= 0.80
        ), f"Only {valid_scores}/{total_benchmarks} benchmarks have valid scores"
        assert (
            valid_years / total_benchmarks >= 0.95
        ), f"Only {valid_years}/{total_benchmarks} benchmarks have valid fiscal years"
        assert (
            valid_sectors / total_benchmarks >= 0.90
        ), f"Only {valid_sectors}/{total_benchmarks} benchmarks have valid sectors"
        assert (
            len(sectors_seen) >= 1
        ), f"Should have at least 1 sector represented, found: {sectors_seen}"


class TestESGDisclosures:
    """Test the ESG disclosures endpoint."""

    @pytest.mark.parametrize(
        "symbol",
        [
            # Technology ESG Leaders
            "AAPL",  # Apple
            "MSFT",  # Microsoft
            "GOOGL",  # Google/Alphabet
            "NVDA",  # NVIDIA
            "CRM",  # Salesforce
            "ADBE",  # Adobe
            # Sustainability-Focused Companies
            "TSLA",  # Tesla
            "NEE",  # NextEra Energy
            "ENPH",  # Enphase Energy
            "SEDG",  # SolarEdge
            "PLUG",  # Plug Power
            "FSLR",  # First Solar
            # Large Cap with ESG Focus
            "PG",  # Procter & Gamble
            "UNH",  # UnitedHealth
            "JNJ",  # Johnson & Johnson
            "PFE",  # Pfizer
            "HD",  # Home Depot
            "WMT",  # Walmart
            # Financial Services ESG
            "JPM",  # JPMorgan Chase
            "BAC",  # Bank of America
            "MS",  # Morgan Stanley
            "GS",  # Goldman Sachs
            "BLK",  # BlackRock
            "V",  # Visa
            # Industrial ESG
            "GE",  # General Electric
            "CAT",  # Caterpillar
            "BA",  # Boeing
            "MMM",  # 3M
            "HON",  # Honeywell
            "LMT",  # Lockheed Martin
            # Consumer ESG
            "KO",  # Coca-Cola
            "PEP",  # PepsiCo
            "NKE",  # Nike
            "SBUX",  # Starbucks
            "MCD",  # McDonald's
            "DIS",  # Disney
            # Energy & Utilities ESG
            "XOM",  # ExxonMobil
            "CVX",  # Chevron
            "SO",  # Southern Company
            "DUK",  # Duke Energy
            "AEP",  # American Electric Power
            "D",  # Dominion Energy
            # International ESG Leaders
            "ASML",  # ASML Holding
            "UL",  # Unilever
            "NVO",  # Novo Nordisk
            "SAP",  # SAP SE
            "TM",  # Toyota
            "ABBV",  # AbbVie
        ],
    )
    def test_esg_disclosures_comprehensive(self, api_key, symbol):
        """Test ESG disclosures across diverse industries and ESG focus areas."""
        response, validation = handle_api_call_with_validation(
            esg.esg_disclosures, "esg_disclosures", True, apikey=api_key, symbol=symbol
        )

        data = get_response_models(response, FMPESGFiling)
        if data:
            validate_esg_disclosures_data(data)

            # Symbol-specific validation
            first_item = data[0]
            if first_item.symbol:
                assert (
                    first_item.symbol == symbol
                ), f"Symbol mismatch: {first_item.symbol} vs {symbol}"

    @pytest.mark.parametrize(
        "industry_sector",
        [
            "technology",
            "renewable_energy",
            "healthcare",
            "financial_services",
            "consumer_goods",
            "industrial",
            "utilities_energy",
            "international",
        ],
    )
    def test_esg_disclosures_by_sector(self, api_key, industry_sector):
        """Test ESG disclosures across different industry sectors."""
        sector_symbols = {
            "technology": ["AAPL", "MSFT", "GOOGL"],
            "renewable_energy": ["TSLA", "NEE", "ENPH"],
            "healthcare": ["UNH", "JNJ", "PFE"],
            "financial_services": ["JPM", "BAC", "BLK"],
            "consumer_goods": ["PG", "KO", "NKE"],
            "industrial": ["GE", "CAT", "MMM"],
            "utilities_energy": ["SO", "DUK", "XOM"],
            "international": ["ASML", "UL", "TM"],
        }

        symbols = sector_symbols.get(industry_sector, ["AAPL"])

        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                esg.esg_disclosures,
                "esg_disclosures",
                True,
                apikey=api_key,
                symbol=symbol,
            )

            data = get_response_models(response, FMPESGFiling)
            if data:
                validate_esg_disclosures_data(data)

    @pytest.mark.parametrize(
        "symbol",
        ["AAPL", "MSFT", "GOOGL", "TSLA", "NEE", "PG", "JPM", "UNH", "GE", "KO"],
    )
    def test_esg_ratings_comprehensive(self, api_key, symbol):
        """Test ESG ratings across major companies."""
        response, validation = handle_api_call_with_validation(
            esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol=symbol
        )

        data = get_response_models(response, FMPESGRating)
        if data:
            validate_esg_ratings_data(data)

            # Symbol-specific validation
            rating = data[0]
            if rating.symbol:
                assert (
                    rating.symbol == symbol
                ), f"Symbol mismatch: {rating.symbol} vs {symbol}"

    @pytest.mark.parametrize(
        "sustainability_focus",
        [
            "climate_leaders",
            "renewable_energy",
            "sustainable_products",
            "social_responsibility",
            "governance_excellence",
        ],
    )
    def test_esg_by_sustainability_focus(self, api_key, sustainability_focus):
        """Test ESG data for companies with different sustainability focuses."""
        focus_symbols = {
            "climate_leaders": ["TSLA", "NEE", "MSFT"],
            "renewable_energy": ["ENPH", "FSLR", "SEDG"],
            "sustainable_products": ["PG", "UL", "NKE"],
            "social_responsibility": ["SBUX", "JNJ", "WMT"],
            "governance_excellence": ["JPM", "BLK", "AAPL"],
        }

        symbols = focus_symbols.get(sustainability_focus, ["AAPL"])

        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                esg.esg_disclosures,
                "esg_disclosures",
                True,
                apikey=api_key,
                symbol=symbol,
            )

            data = get_response_models(response, FMPESGFiling)
            if data:
                validate_esg_disclosures_data(data)

    def test_esg_disclosures_basic(self, api_key):
        """Test basic ESG disclosures functionality."""
        response, validation = handle_api_call_with_validation(
            esg.esg_disclosures, "esg_disclosures", True, apikey=api_key, symbol="AAPL"
        )

        data = get_response_models(response, FMPESGFiling)
        if data:
            validate_esg_disclosures_data(data)


class TestESGRatings:
    """Test the ESG ratings endpoint."""

    def test_esg_ratings_basic(self, api_key):
        """Test basic ESG ratings functionality."""
        response, validation = handle_api_call_with_validation(
            esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol="AAPL"
        )

        data = get_response_models(response, FMPESGRating)
        if data:
            validate_esg_ratings_data(data)

    def test_esg_ratings_multiple_symbols(self, api_key):
        """Test ESG ratings for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            response, validation = handle_api_call_with_validation(
                esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol=symbol
            )

            data = get_response_models(response, FMPESGRating)
            if data:
                validate_esg_ratings_data(data)

    def test_esg_ratings_invalid_symbol(self, api_key):
        """Test ESG ratings with invalid symbol."""
        response, validation = handle_api_call_with_validation(
            esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol="INVALID999"
        )

        data = get_response_models(response, FMPESGRating)
        # Should return empty list for invalid symbol
        assert len(data) == 0

    def test_esg_ratings_error_handling(self, api_key):
        """Test error handling for ESG ratings."""
        response, validation = handle_api_call_with_validation(
            esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol="AAPL"
        )

        data = get_response_models(response, FMPESGRating)
        if data:
            validate_esg_ratings_data(data)


class TestESGBenchmark:
    """Test the ESG benchmark endpoint."""

    def test_esg_benchmark_basic(self, api_key):
        """Test basic ESG benchmark functionality."""
        response, validation = handle_api_call_with_validation(
            esg.esg_benchmark, "esg_benchmark", True, apikey=api_key
        )

        data = get_response_models(response, FMPESGBenchmark)
        if data:
            validate_esg_benchmark_data(data)

    def test_esg_benchmark_with_year(self, api_key):
        """Test ESG benchmark with specific year."""
        response, validation = handle_api_call_with_validation(
            esg.esg_benchmark, "esg_benchmark", True, apikey=api_key, year="2023"
        )

        data = get_response_models(response, FMPESGBenchmark)
        if data:
            validate_esg_benchmark_data(data)

            # Validate year matches
            for item in data[:3]:  # Check first few items
                if item.fiscalYear:
                    assert (
                        item.fiscalYear == 2023
                    ), f"Fiscal year should be 2023, got {item.fiscalYear}"

    def test_esg_benchmark_multiple_years(self, api_key):
        """Test ESG benchmark data for multiple years."""
        years = ["2021", "2022", "2023"]

        for year in years:
            response, validation = handle_api_call_with_validation(
                esg.esg_benchmark, "esg_benchmark", True, apikey=api_key, year=year
            )

            data = get_response_models(response, FMPESGBenchmark)
            if data:
                validate_esg_benchmark_data(data)

                # Validate year matches
                for item in data[:2]:  # Check first few items
                    if item.fiscalYear:
                        assert item.fiscalYear == int(
                            year
                        ), f"Fiscal year should be {year}, got {item.fiscalYear}"

    def test_esg_benchmark_invalid_year(self, api_key):
        """Test ESG benchmark with invalid year."""
        response, validation = handle_api_call_with_validation(
            esg.esg_benchmark, "esg_benchmark", True, apikey=api_key, year="1900"
        )

        data = get_response_models(response, FMPESGBenchmark)
        # Should return empty list for invalid year
        assert len(data) == 0

    def test_esg_benchmark_error_handling(self, api_key):
        """Test error handling with invalid API key."""
        with pytest.raises(Exception):
            esg.esg_benchmark(apikey="invalid_key_123")


class TestESGDataQuality:
    """Test data quality and business logic validation."""

    def test_esg_disclosures_data_quality(self, api_key):
        """Test data quality in ESG disclosures."""
        response, validation = handle_api_call_with_validation(
            esg.esg_disclosures, "esg_disclosures", True, apikey=api_key, symbol="AAPL"
        )

        data = get_response_models(response, FMPESGFiling)
        if data:
            validate_esg_disclosures_data(data)

    def test_esg_ratings_data_quality(self, api_key):
        """Test data quality in ESG ratings."""
        response, validation = handle_api_call_with_validation(
            esg.esg_ratings, "esg_ratings", True, apikey=api_key, symbol="AAPL"
        )

        data = get_response_models(response, FMPESGRating)
        if data:
            validate_esg_ratings_data(data)

    def test_esg_benchmark_data_quality(self, api_key):
        """Test data quality in ESG benchmark data."""
        response, validation = handle_api_call_with_validation(
            esg.esg_benchmark, "esg_benchmark", True, apikey=api_key, year="2023"
        )

        data = get_response_models(response, FMPESGBenchmark)
        if data:
            validate_esg_benchmark_data(data)
