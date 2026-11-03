import datetime
import typing

from pydantic import RootModel

from .models import (
    FMPEconomicCalendarEvent,
    FMPEconomicIndicator,
    FMPMarketRiskPremium,
    FMPTreasuryRates,
)
from .url_methods import __return_json
from .utils import parse_response

# Calendar days requested per call. FMP silently drops rows more than 90 days
# before ``to``; staying a day under that means a tighter cap can't lose rows.
_INDICATOR_WINDOW_DAYS = 90


def _parse_date(param: str, value: typing.Any) -> datetime.date:
    """Parse a date parameter. FMP ignores bad dates rather than rejecting them."""
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise ValueError(f"{param} must be YYYY-MM-DD, got {value!r}") from e


def _date_windows(
    start: datetime.date, end: datetime.date
) -> typing.List[typing.Tuple[datetime.date, datetime.date]]:
    """Split the inclusive range into adjacent request windows, newest first."""
    windows = []
    window_end = end
    while window_end >= start:
        window_start = max(
            start, window_end - datetime.timedelta(days=_INDICATOR_WINDOW_DAYS - 1)
        )
        windows.append((window_start, window_end))
        window_end = window_start - datetime.timedelta(days=1)
    return windows


@parse_response
def treasury_rates(
    apikey: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPTreasuryRates]]:
    """
    Get US Treasury rates.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    list
        List of US Treasury rates.
    """
    path = "treasury-rates"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def economic_indicators(
    apikey: str, name: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPEconomicIndicator]]:
    """
    Get economic indicators, newest first.

    FMP returns at most 90 days per request, so a longer range is fetched in
    several requests (about 4 per year), each counting against your rate limit.

    Without ``from_date`` only a single 90-day window is returned. With no dates
    at all that is the last 90 days, which is usually empty for quarterly series
    such as GDP, because a quarter is dated by its first day and published months
    later. Pass ``from_date`` to reach those.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    name : str
        Name of the economic indicator (e.g., GDP, RETAIL SALES, CPI).
    from_date : str, optional
        Start date (YYYY-MM-DD). Without ``to_date``, the range runs through today.
    to_date : str, optional
        End date (YYYY-MM-DD). Without ``from_date``, returns the 90 days ending here.

    Returns
    -------
    list
        List of economic indicators. If a request fails partway through a range,
        the error is returned or raised instead of the rows fetched so far.

    Raises
    ------
    ValueError
        If a date is malformed, or ``from_date`` is after ``to_date``.
    """
    path = "economic-indicators"
    query_vars = {"apikey": apikey, "name": name}
    end = _parse_date("to_date", to_date) if to_date else None

    if not from_date:
        if end:
            query_vars["to"] = end.isoformat()
        return __return_json(path, query_vars)  # type: ignore[no-any-return]

    start = _parse_date("from_date", from_date)
    if end and start > end:
        raise ValueError(f"from_date {from_date} is after to_date {to_date}")

    rows: typing.List[typing.Any] = []
    for window_start, window_end in _date_windows(start, end or datetime.date.today()):
        page = __return_json(
            path,
            {
                **query_vars,
                "from": window_start.isoformat(),
                "to": window_end.isoformat(),
            },
        )
        if page is None:
            continue
        if not isinstance(page, list):
            # An error payload. Returning it keeps a failed range from looking
            # like a complete one, since parse_response passes errors through.
            return page  # type: ignore[no-any-return]
        rows.extend(page)
    return rows  # type: ignore[return-value]


@parse_response
def economic_calendar(
    apikey: str, from_date: str = None, to_date: str = None
) -> RootModel[typing.List[FMPEconomicCalendarEvent]]:
    """
    Get economic calendar events.

    Parameters
    ----------
    apikey : str
        Your FMP API key.
    from_date : str, optional
        Start date (YYYY-MM-DD).
    to_date : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    list
        List of economic calendar events.
    """
    path = "economic-calendar"
    query_vars = {"apikey": apikey}
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json(path, query_vars)  # type: ignore[no-any-return]


@parse_response
def market_risk_premium(apikey: str) -> RootModel[typing.List[FMPMarketRiskPremium]]:
    """
    Get market risk premium.

    Parameters
    ----------
    apikey : str
        Your FMP API key.

    Returns
    -------
    list
        List of market risk premium.
    """
    path = "market-risk-premium"
    query_vars = {"apikey": apikey}
    return __return_json(path, query_vars)  # type: ignore[no-any-return]
