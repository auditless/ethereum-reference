"""Create the reference."""

from yattag import Doc, indent
import sh

from .html import code


@code
def version_s():
    """
    >>> str(sh.solc("--version"))[50:65]
    'Version: 0.5.12'
    """
    return """$ solc --version
Version: 0.5.12"""


@code
def version_v():
    """
    >>> str(sh.vyper("--version"))[:8]
    '0.1.0b13'
    """
    return """$ vyper --version
0.1.0b13 (0.1.0 Beta 13)"""


def render() -> str:
    """Render the final page."""
    doc, tag, text, line = Doc().ttl()
    trip = [doc, tag, text]

    # Final reference doc
    with tag("html"):
        with tag("body"):
            with tag("h1"):
                text("Solidity & Vyper Cheat Sheet")
            with tag("p"):
                text(
                    "A feature by feature reference guide to the two most popular programming languages on Ethereum."
                )
            with tag("h2"):
                text("Setup and basic syntax")
            with tag("table"):
                with tag("tr"):
                    line("th", "Feature")
                    line("th", "Solidity")
                    line("th", "Vyper")
                with tag("tr"):
                    line("th", "Version")
                    version_s(*trip)
                    version_v(*trip)

    # Prettify the HTML
    unindented = doc.getvalue()
    return indent(unindented)


if __name__ == "__main__":
    print(render())
