
def iterate_over_pages(func, args, page_limit=100):
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

        page += 1
        if page >= page_limit:
            break

    return data_list, data_dict
