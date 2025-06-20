from .general import __quotes
from .models import *
import typing


def euronext_list(apikey: str) -> RootModel[typing.List[FMPSymbolAndNameList]]:
    """
    Query FMP /quotes/euronext/ API

    :param apikey: Your API key.
    :return: A list of dictionaries.
    """
    path = f"euronext"
    return __quotes(apikey=apikey, value=path)
