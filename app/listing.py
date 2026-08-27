from app.pagination import page_slice, total_pages
from app.slug import slugify


def list_page(titles: list[str], page: int, per_page: int) -> dict[str, object]:
    window = page_slice(titles, page, per_page)
    return {
        "page": page,
        "total_pages": total_pages(len(titles), per_page),
        "items": [{"title": t, "slug": slugify(t)} for t in window],
    }
