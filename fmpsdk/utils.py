import typing
from pydantic import BaseModel

def iterate_over_pages(func, args, page_limit=100) -> typing.Union[typing.List, typing.Dict]:
    page = 0
    data_list = []
    data_dict = {}
    while True:
        args["page"] = page
        response = func(**args)
        if len(response) == 0:
            break

        if isinstance(response, list):
            data_list.extend(response)
        elif isinstance(response, dict):
            data_dict.update(response)
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")

        if page >= page_limit:
            print(f"ERROR: Reached FMP page limit: {page}")
            break

        page += 1

    if len(data_list) == 0:
        return data_dict
    else:
        return data_list


def parse_response(func) -> typing.Callable:
    from functools import wraps

    from .model_registry import ENDPOINT_MODEL_MAP

    @wraps(func)
    def wrapper(*args, **kwargs) -> typing.Any:
        raw = func(*args, **kwargs)
        
        # Check for API error responses and return them as-is
        if isinstance(raw, dict) and "Error Message" in raw:
            return raw
            
        model = ENDPOINT_MODEL_MAP.get(func.__name__)
        if model:
            # Defensive: If API returns None, convert to empty list for list models
            if raw is None:    
                raw = []

            result = model.model_validate(raw)
            # Do NOT unwrap __root__ or root; always return the model instance
            return result
        return raw

    return wrapper
