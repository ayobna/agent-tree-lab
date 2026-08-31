# Filter the listing by a search term

app.listing.list_page() returns a page of titles.

Add an optional search term:
- When provided, list only titles containing it, case-insensitively.
- The page count must reflect the filtered set, not the full set.
- No search term must preserve today's behavior.
- Reject per_page of zero or less with a clear error.
- Cover the new behavior with tests.
