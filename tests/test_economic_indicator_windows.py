"""Offline tests for economic_indicators date-range splitting (no API key required).

FMP returns at most 90 days per request and silently drops the rest, so the SDK
has to split longer ranges itself.
"""

import datetime
from unittest.mock import Mock, patch

import pytest

from fmpsdk.economics import economic_indicators
from fmpsdk.exceptions import RateLimitExceededException
from fmpsdk.models import FMPEconomicIndicator

RETURN_JSON = "fmpsdk.economics.__return_json"
API_CAP_DAYS = 90


def _row(day):
    return {"name": "CPI", "date": day, "value": 1.0}


def _query_vars(mock_return_json):
    return [call.args[1] for call in mock_return_json.call_args_list]


def _as_date(value):
    return datetime.date.fromisoformat(value)


def _fetch(**dates):
    return economic_indicators(apikey="key", name="CPI", **dates)


class _FrozenDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2025, 6, 30)


class TestLongRangesAreSplit:
    @pytest.mark.parametrize(
        "from_date, to_date",
        [
            ("2020-01-01", "2024-12-31"),
            ("2024-01-01", "2024-12-31"),  # leap year
            ("2025-04-01", "2025-06-30"),  # one day over a single window
        ],
    )
    def test_every_day_covered_once_within_the_api_cap(self, from_date, to_date):
        with patch(RETURN_JSON, return_value=[]) as mock_return_json:
            _fetch(from_date=from_date, to_date=to_date)

        sent = _query_vars(mock_return_json)
        assert len(sent) > 1
        assert sent[0]["to"] == to_date
        assert sent[-1]["from"] == from_date
        for query in sent:
            assert (
                _as_date(query["to"]) - _as_date(query["from"])
            ).days <= API_CAP_DAYS
        for newer, older in zip(sent, sent[1:]):
            gap = _as_date(newer["from"]) - _as_date(older["to"])
            assert gap == datetime.timedelta(days=1)

    def test_rows_merge_newest_first_as_validated_models(self):
        pages = [
            [_row("2025-06-01"), _row("2025-05-01")],
            [_row("2025-04-01"), _row("2025-03-01"), _row("2025-02-01")],
        ]
        with patch(RETURN_JSON, side_effect=pages):
            result = _fetch(from_date="2025-01-02", to_date="2025-06-30")

        assert [row.date for row in result.root] == [
            "2025-06-01",
            "2025-05-01",
            "2025-04-01",
            "2025-03-01",
            "2025-02-01",
        ]
        assert all(isinstance(row, FMPEconomicIndicator) for row in result.root)

    @pytest.mark.parametrize("empty_page", [[], None])
    def test_empty_window_does_not_stop_fetching(self, empty_page):
        # Quarterly series such as GDP have windows with no observation in them.
        pages = [[_row("2024-10-01")], empty_page, [_row("2024-04-01")]]
        with patch(RETURN_JSON, side_effect=pages) as mock_return_json:
            result = _fetch(from_date="2024-04-01", to_date="2024-10-31")

        assert mock_return_json.call_count == 3
        assert [row.date for row in result.root] == ["2024-10-01", "2024-04-01"]

    def test_apikey_and_name_sent_on_every_request(self):
        with patch(RETURN_JSON, return_value=[]) as mock_return_json:
            _fetch(from_date="2024-01-01", to_date="2024-12-31")

        for query in _query_vars(mock_return_json):
            assert query["apikey"] == "key"
            assert query["name"] == "CPI"


class TestSingleRequestCases:
    @pytest.mark.parametrize(
        "dates, expected_dates",
        [
            (
                {"from_date": "2025-03-15", "to_date": "2025-04-15"},
                {"from": "2025-03-15", "to": "2025-04-15"},
            ),
            (
                {"from_date": "2025-04-02", "to_date": "2025-06-30"},
                {"from": "2025-04-02", "to": "2025-06-30"},
            ),
            (
                {"from_date": "2025-04-01", "to_date": "2025-04-01"},
                {"from": "2025-04-01", "to": "2025-04-01"},
            ),
            ({"to_date": "2025-06-30"}, {"to": "2025-06-30"}),
            ({}, {}),
        ],
    )
    def test_sends_one_request(self, dates, expected_dates):
        with patch(RETURN_JSON, return_value=[]) as mock_return_json:
            _fetch(**dates)

        assert _query_vars(mock_return_json) == [
            {"apikey": "key", "name": "CPI", **expected_dates}
        ]


class TestFromDateOnly:
    def test_runs_through_today(self):
        with patch("datetime.date", _FrozenDate):
            with patch(RETURN_JSON, return_value=[]) as mock_return_json:
                _fetch(from_date="2024-01-01")

        sent = _query_vars(mock_return_json)
        assert sent[0]["to"] == "2025-06-30"
        assert sent[-1]["from"] == "2024-01-01"

    def test_future_start_makes_no_request(self):
        with patch("datetime.date", _FrozenDate):
            with patch(RETURN_JSON) as mock_return_json:
                result = _fetch(from_date="2030-01-01")

        mock_return_json.assert_not_called()
        assert result.root == []


class TestFailureInsideARange:
    """A failed window must never come back looking like a complete result."""

    def test_error_message_is_returned_instead_of_partial_rows(self):
        error = {"Error Message": "Limit Reach"}
        with patch(
            RETURN_JSON, side_effect=[[_row("2024-10-01")], error]
        ) as mock_return_json:
            result = _fetch(from_date="2024-01-01", to_date="2024-12-31")

        assert result == error
        assert mock_return_json.call_count == 2

    def test_http_response_is_returned_instead_of_partial_rows(self):
        premium = Mock(status_code=402)
        with patch(RETURN_JSON, side_effect=[[_row("2024-10-01")], premium]):
            result = _fetch(from_date="2024-01-01", to_date="2024-12-31")

        assert result is premium

    def test_exception_propagates(self):
        pages = [[_row("2024-10-01")], RateLimitExceededException("slow down")]
        with patch(RETURN_JSON, side_effect=pages):
            with pytest.raises(RateLimitExceededException):
                _fetch(from_date="2024-01-01", to_date="2024-12-31")


class TestInvalidDates:
    """FMP ignores bad dates and answers with some other window, so reject them."""

    @pytest.mark.parametrize(
        "dates",
        [
            {"from_date": "not-a-date", "to_date": "2025-06-30"},
            {"from_date": "2025-01-01", "to_date": "06/30/2025"},
            {"from_date": "not-a-date"},
            {"to_date": "not-a-date"},
            {"from_date": "2025-02-30", "to_date": "2025-06-30"},
        ],
    )
    def test_malformed_date_raises_before_any_request(self, dates):
        with patch(RETURN_JSON) as mock_return_json:
            with pytest.raises(ValueError, match="YYYY-MM-DD"):
                _fetch(**dates)

        mock_return_json.assert_not_called()

    def test_reversed_range_raises_before_any_request(self):
        with patch(RETURN_JSON) as mock_return_json:
            with pytest.raises(ValueError, match="after to_date"):
                _fetch(from_date="2025-06-30", to_date="2025-01-01")

        mock_return_json.assert_not_called()
