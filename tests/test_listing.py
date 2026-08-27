from app.listing import list_page


def test_page_one_of_two() -> None:
    page = list_page(["Alpha One", "Beta Two", "Gamma Three"], page=1, per_page=2)
    assert page["items"] == [
        {"title": "Alpha One", "slug": "alpha-one"},
        {"title": "Beta Two", "slug": "beta-two"},
    ]
