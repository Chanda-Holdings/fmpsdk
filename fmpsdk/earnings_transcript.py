import typing

from pydantic import RootModel

from .models import (
    FMPEarningsTranscript,
    FMPEarningsTranscriptBySymbol,
    FMPEarningsTranscriptList,
)
from .url_methods import __return_json
from .utils import parse_response


@parse_response
def earnings_transcript_latest(
    apikey: str,
    limit: str = None,
    page: int = None,
) -> RootModel[typing.List[FMPEarningsTranscript]]:
    path = "earning-call-transcript-latest"
    query_vars = {"apikey": apikey}
    if limit:
        query_vars["limit"] = limit
    if page is not None:
        query_vars["page"] = str(page)
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def earnings_transcript(
    apikey: str,
    symbol: str,
    year: int,
    quarter: int,
    limit: str = None,
) -> RootModel[typing.List[FMPEarningsTranscript]]:
    path = "earning-call-transcript"
    query_vars = {"apikey": apikey, "symbol": symbol, "year": year, "quarter": quarter}
    if limit:
        query_vars["limit"] = limit
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def earnings_transcript_by_symbol(
    apikey: str, symbol: str
) -> RootModel[typing.List[FMPEarningsTranscriptBySymbol]]:
    path = "earning-call-transcript-dates"
    query_vars = {"apikey": apikey, "symbol": symbol}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]


@parse_response
def earnings_transcript_list(
    apikey: str,
) -> RootModel[typing.List[FMPEarningsTranscriptList]]:
    path = "earnings-transcript-list"
    query_vars = {"apikey": apikey}
    return __return_json(path=path, query_vars=query_vars)  # type: ignore[no-any-return]
