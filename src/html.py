"""Tools for building the reference page."""

from functools import wraps


def code(get_code):
    """Add a code cell to a table, used as a decorator."""

    @wraps(get_code)
    def render(doc, tag, text):
        with tag("td"):
            with tag("pre"):
                text(get_code())

    return render
