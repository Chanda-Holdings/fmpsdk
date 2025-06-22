"""
Integration tests for economic_indicators endpoints.
Requires FMP API key set as the environment variable FMP_API_KEY.
"""

import os

import pytest

from fmpsdk.economic_indicators import economic_indicators, treasury_rates

API_KEY = os.getenv("FMP_API_KEY")


@pytest.mark.parametrize(
    "func,kwargs",
    [
        (treasury_rates, {}),
        (treasury_rates, {"from_date": "2024-01-01", "to_date": "2024-01-31"}),
        (economic_indicators, {"name": "GDP"}),
        (economic_indicators, {"name": "unemployment_rate"}),
        (economic_indicators, {"name": "inflation"}),
    ],
)
def test_economic_indicators_endpoints(func, kwargs):
    """Test economic indicators endpoints with various parameter combinations."""
    kwargs["apikey"] = API_KEY
    result = func(**kwargs)

    # Should return a RootModel with list data or be iterable
    assert result is not None, f"{func.__name__} should return a non-None result"

    # Check if it's a RootModel with root attribute
    if hasattr(result, "root"):
        data = result.root
        if data is not None:
            assert isinstance(
                data, list
            ), f"{func.__name__} should return RootModel with list data"
            # If there are results, check that each item is a Pydantic model
            if data:
                assert hasattr(
                    data[0], "__dict__"
                ), f"{func.__name__} should return list of Pydantic models"
    elif hasattr(result, "__iter__") and not isinstance(result, (str, bytes)):
        # Handle legacy list responses
        result_list = list(result)
        if result_list:
            assert hasattr(
                result_list[0], "__dict__"
            ), f"{func.__name__} should return list of Pydantic models"


def test_treasury_rates_structure():
    """Test treasury rates endpoint structure."""
    result = treasury_rates(apikey=API_KEY)
    assert result is not None

    # Check if it's a RootModel with root attribute
    if hasattr(result, "root"):
        data = result.root
        if data is not None and isinstance(data, list) and data:
            rate = data[0]
            expected_fields = ["date"]
            for field in expected_fields:
                if hasattr(rate, field):
                    assert getattr(rate, field) is not None
                    # Date should be a string
                    if field == "date":
                        assert isinstance(getattr(rate, field), str)


def test_treasury_rates_with_date_range():
    """Test treasury rates with specific date range."""
    result = treasury_rates(
        apikey=API_KEY, from_date="2024-01-01", to_date="2024-01-31"
    )
    assert result is not None

    # Check if it's a RootModel with root attribute
    if hasattr(result, "root"):
        data = result.root
        if data is not None and isinstance(data, list) and data:
            rate = data[0]
            if hasattr(rate, "date"):
                assert isinstance(rate.date, str)
            # Date should be in expected format
            assert len(rate.date.split("-")) >= 2


def test_economic_indicators_gdp():
    """Test economic indicator endpoint for GDP."""
    result = economic_indicators(apikey=API_KEY, name="GDP")
    assert result is not None

    # Check if it's a RootModel with root attribute
    if hasattr(result, "root"):
        data = result.root
        if data is not None and isinstance(data, list) and data:
            indicator = data[0]
            expected_fields = ["date", "value"]
            for field in expected_fields:
                if hasattr(indicator, field):
                    assert getattr(indicator, field) is not None


def test_economic_indicators_unemployment():
    """Test economic indicator endpoint for unemployment rate."""
    result = economic_indicators(apikey=API_KEY, name="unemployment_rate")
    assert result is not None

    # Check if it's a RootModel with root attribute - may be None for unemployment_rate
    if hasattr(result, "root"):
        data = result.root
        if data is not None and isinstance(data, list) and data:
            indicator = data[0]
            # Value should be numeric if present
            if hasattr(indicator, "value") and indicator.value is not None:
                assert isinstance(indicator.value, (int, float))


def test_economic_indicators_with_date_range():
    """Test economic indicator with date range."""
    result = economic_indicators(
        apikey=API_KEY, name="GDP", from_date="2023-01-01", to_date="2023-12-31"
    )
    assert result is not None

    # Check if it's a RootModel with root attribute
    if hasattr(result, "root"):
        data = result.root
        if data is not None and isinstance(data, list) and data:
            indicator = data[0]
            if hasattr(indicator, "date"):
                assert isinstance(indicator.date, str)


def test_treasury_rates_empty_params():
    """Test treasury rates with no additional parameters."""
    result = treasury_rates(apikey=API_KEY)
    assert result is not None

    # Should not raise an exception even with no additional params


def test_economic_indicators_different_names():
    """Test economic indicator with different indicator names."""
    indicators = ["GDP", "unemployment_rate", "inflation", "CPI"]

    for indicator_name in indicators:
        result = economic_indicators(apikey=API_KEY, name=indicator_name)
        assert result is not None, f"Failed for indicator: {indicator_name}"

        # Check if it's a RootModel with root attribute
        if hasattr(result, "root"):
            data = result.root
            if data is not None and isinstance(data, list) and data:
                item = data[0]
                assert hasattr(
                    item, "__dict__"
                ), f"Failed for indicator: {indicator_name}"
