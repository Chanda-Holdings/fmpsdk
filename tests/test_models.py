"""Offline tests for model field coercion (no API key required)."""

import pytest
from pydantic import ValidationError

from fmpsdk.models import FMPBaseModel, FMPIncomeStatement, LenientInt


def _income_row(**overrides):
    """A GE quarterly income statement row with whole-number values."""
    row = {
        "date": "2020-12-31",
        "symbol": "GE",
        "reportedCurrency": "USD",
        "cik": "0000040545",
        "filingDate": "2021-02-12",
        "acceptedDate": "2021-02-12 16:01:46",
        "fiscalYear": "2020",
        "period": "Q4",
        "revenue": 21933000000,
        "costOfRevenue": 16727000000,
        "grossProfit": 5206000000,
        "researchAndDevelopmentExpenses": 0,
        "generalAndAdministrativeExpenses": 0,
        "sellingAndMarketingExpenses": 0,
        "sellingGeneralAndAdministrativeExpenses": 3164000000,
        "otherExpenses": 0,
        "operatingExpenses": 3164000000,
        "costAndExpenses": 19891000000,
        "netInterestIncome": -560000000,
        "interestIncome": 0,
        "interestExpense": 560000000,
        "depreciationAndAmortization": 1218000000,
        "ebitda": 3870000000,
        "ebit": 2652000000,
        "nonOperatingIncomeExcludingInterest": 0,
        "operatingIncome": 2042000000,
        "totalOtherIncomeExpensesNet": 50000000,
        "incomeBeforeTax": 2092000000,
        "incomeTaxExpense": -323000000,
        "netIncomeFromContinuingOperations": 2415000000,
        "netIncomeFromDiscontinuedOperations": 0,
        "otherAdjustmentsToNetIncome": 0,
        "netIncome": 2415000000,
        "netIncomeDeductions": 0,
        "bottomLineNetIncome": 2415000000,
        "eps": 0.18,
        "epsDiluted": 0.18,
        "weightedAverageShsOut": 1756172378,
        "weightedAverageShsOutDil": 1757777471,
    }
    row.update(overrides)
    return row


class _Holder(FMPBaseModel):
    value: LenientInt


class TestLenientInt:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            (5, 5),
            ("7", 7),
            (3.0, 3),
            (1756172378.625, 1756172379),
            (1773627764.9999995, 1773627765),
            (-2.75, -3),
            (2.5, 3),
            (-2.5, -3),
        ],
    )
    def test_rounds_to_nearest_int(self, raw, expected):
        result = _Holder(value=raw).value
        assert result == expected
        assert type(result) is int

    @pytest.mark.parametrize("raw", ["abc", "1.5", float("nan"), float("inf")])
    def test_still_rejects_non_numeric(self, raw):
        with pytest.raises(ValidationError):
            _Holder(value=raw)


class TestIncomeStatementFractionalValues:
    """FMP split-adjusts historical share counts, producing fractional values.

    Values taken from GE quarterly rows (Q1 2019 - Q3 2021) that previously
    failed validation.
    """

    @pytest.mark.parametrize(
        "shs_out, shs_out_dil, expected_out, expected_dil",
        [
            (1773627765, 1773627764.9999995, 1773627765, 1773627765),
            (1756172378.625, 1757777471.625, 1756172379, 1757777472),
            (1756774288.5, 1756774288.5, 1756774289, 1756774289),
            (1755570468.75, 1755570468.75, 1755570469, 1755570469),
            (1753965375.75, 1755369832.125, 1753965376, 1755369832),
            (1751557736.25, 1751557736.25, 1751557736, 1751557736),
            (1747745640.375, 1750755189.75, 1747745640, 1750755190),
        ],
    )
    def test_fractional_share_counts_validate(
        self, shs_out, shs_out_dil, expected_out, expected_dil
    ):
        stmt = FMPIncomeStatement.model_validate(
            _income_row(
                weightedAverageShsOut=shs_out,
                weightedAverageShsOutDil=shs_out_dil,
            )
        )
        assert stmt.weightedAverageShsOut == expected_out
        assert stmt.weightedAverageShsOutDil == expected_dil
        assert type(stmt.weightedAverageShsOut) is int
        assert type(stmt.weightedAverageShsOutDil) is int

    def test_fractional_currency_fields_validate(self):
        stmt = FMPIncomeStatement.model_validate(
            _income_row(revenue=21933000000.5, ebitda=3869999999.75)
        )
        assert stmt.revenue == 21933000001
        assert stmt.ebitda == 3870000000

    def test_whole_number_rows_unchanged(self):
        row = _income_row()
        stmt = FMPIncomeStatement.model_validate(row)
        dumped = stmt.model_dump()
        for key, value in row.items():
            assert dumped[key] == value
