import pytest

from app.pagination import page_slice, total_pages


def test_exact_multiple() -> None:
    assert total_pages(20, 10) == 2


def test_partial_page() -> None:
    assert total_pages(25, 10) == 3


def test_single_leftover_item() -> None:
    assert total_pages(11, 10) == 2


def test_no_items() -> None:
    assert total_pages(0, 10) == 0


def test_rejects_zero_per_page() -> None:
    with pytest.raises(ValueError):
        total_pages(10, 0)


def test_slice_first_page() -> None:
    assert page_slice(list("abcdef"), 1, 2) == ["a", "b"]


def test_slice_last_page() -> None:
    assert page_slice(list("abcde"), 3, 2) == ["e"]
