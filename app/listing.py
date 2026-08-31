from app.pagination import page_slice, total_pages
from app.slug import slugify


def list_page(
    titles: list[str], page: int, per_page: int, search: str | None = None
) -> dict[str, object]:
    filtered = (
        [t for t in titles if search.lower() in t.lower()] if search else titles
    )
    window = page_slice(filtered, page, per_page)
    return {
        "page": page,
        "total_pages": total_pages(len(filtered), per_page),
        "items": [{"title": t, "slug": slugify(t)} for t in window],
    }
