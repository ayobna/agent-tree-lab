from app.slug import slugify


def test_simple_title() -> None:
    assert slugify("Hello World") == "hello-world"


def test_trims_trailing_punctuation() -> None:
    assert slugify(" Hello, World! ") == "hello-world"


def test_collapses_separator_runs() -> None:
    assert slugify("C++ / Rust") == "c-rust"


def test_strips_edge_dashes() -> None:
    assert slugify("--Draft--") == "draft"
