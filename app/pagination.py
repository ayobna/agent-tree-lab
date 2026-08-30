def total_pages(total_items: int, per_page: int) -> int:
    """How many pages are needed to show every item."""
    if per_page <= 0:
        raise ValueError("per_page must be positive")
    return (total_items + per_page - 1) // per_page


def page_slice(items: list[str], page: int, per_page: int) -> list[str]:
    start = (page - 1) * per_page
    return items[start : start + per_page]
