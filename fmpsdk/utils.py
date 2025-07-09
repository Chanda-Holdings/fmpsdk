import typing
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def iterate_over_pages(
    func, args, page_limit=100
) -> typing.Union[typing.List, typing.Dict]:
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

    if len(data_list) == 0 and len(data_dict) > 0:
        return data_dict
    else:
        return data_list


def parse_response(func: Callable[..., Any]) -> Callable[..., Any]:
    from functools import wraps

    from .model_registry import ENDPOINT_MODEL_MAP

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        raw = func(*args, **kwargs)

        # Check for HTTP Response objects (e.g., 402 for premium endpoints)
        if hasattr(raw, "status_code"):
            return raw  # Return response object as-is for premium endpoint detection

        # Check for API error responses and return them as-is
        if isinstance(raw, dict) and "Error Message" in raw:
            return raw

        model = ENDPOINT_MODEL_MAP.get(func.__name__)
        if model:
            # Defensive: If API returns None, convert to empty list for list models
            if raw is None:
                raw = []

            try:
                # Try BaseModel.model_validate first
                if hasattr(model, "model_validate"):
                    result = model.model_validate(raw)
                else:
                    # Fallback to constructor for RootModel
                    result = model(raw)
            except (AttributeError, TypeError):
                # Final fallback to constructor
                result = model(raw)
            # Do NOT unwrap __root__ or root; always return the model instance
            return result
        return raw

    return wrapper
