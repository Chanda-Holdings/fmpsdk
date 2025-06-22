import typing

from pydantic import RootModel

from .general import __quotes
from .models import *


def euronext_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/euronext/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = "euronext"
    return __quotes(apikey=apikey, value=path)
