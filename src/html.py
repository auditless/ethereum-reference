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


def comment(get_comment):
    """Add a comment cell to a table, used as a decorator."""

    @wraps(get_comment)
    def render(doc, tag, text):
        with tag("td"):
            with tag("p"):
                text(get_comment())

    return render


def empty(doc, tag, text):
    """Empty cell."""
    with tag("td"):
        with tag("p"):
            pass


def table_section(name):
    """New table header row."""

    def render(doc, tag, text, line):
        with tag("tr"):
            with tag("th", colspan="3"):
                text(name)
        with tag("tr"):
            line("th", "Feature")
            line("th", "Solidity")
            line("th", "Vyper")


    return render