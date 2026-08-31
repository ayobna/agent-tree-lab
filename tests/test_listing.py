import pytest

from app.listing import list_page


def test_page_one_of_two() -> None:
    page = list_page(["Alpha One", "Beta Two", "Gamma Three"], page=1, per_page=2)
    assert page["items"] == [
        {"title": "Alpha One", "slug": "alpha-one"},
        {"title": "Beta Two", "slug": "beta-two"},
    ]


def test_search_filters_to_matching_titles() -> None:
    page = list_page(
        ["Alpha One", "Beta Two", "Gamma Three"], page=1, per_page=2, search="two"
    )
    assert page["items"] == [{"title": "Beta Two", "slug": "beta-two"}]


def test_search_total_pages_reflects_filtered_count() -> None:
    page = list_page(
        ["Alpha One", "Beta Two", "Gamma Three"], page=1, per_page=1, search="two"
    )
    assert page["total_pages"] == 1


def test_search_is_case_insensitive() -> None:
    page = list_page(["Alpha One", "Beta Two"], page=1, per_page=10, search="ALPHA")
    assert page["items"] == [{"title": "Alpha One", "slug": "alpha-one"}]


def test_no_search_term_preserves_existing_behavior() -> None:
    page = list_page(["Alpha One", "Beta Two", "Gamma Three"], page=1, per_page=2)
    assert page["total_pages"] == 2
    assert page["items"] == [
        {"title": "Alpha One", "slug": "alpha-one"},
        {"title": "Beta Two", "slug": "beta-two"},
    ]


def test_non_positive_per_page_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="per_page must be positive"):
        list_page(["Alpha One"], page=1, per_page=0, search="a")
