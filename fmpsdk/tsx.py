import typing

from pydantic import RootModel

from .general import __quotes
from .models import FMPSymbolAndNameList


def tsx_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/tsx/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "tsx"
    return __quotes(apikey=apikey, value=path)
