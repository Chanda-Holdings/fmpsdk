
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

        if page >= page_limit:
            print(f"ERROR: Reached FMP page limit: {page}")
            break

        page += 1

    if len(data_list) == 0:
        return data_dict
    else:
        return data_list

