def get_logs_sessions_filters(url_params):
    filters = {}
    date_from = url_params.get("date_from")
    date_to = url_params.get("date_to")

    if date_from:
        filters["start_date__gte"] = date_from

    if date_to:
        filters["start_date__lte"] = date_to

    return filters
