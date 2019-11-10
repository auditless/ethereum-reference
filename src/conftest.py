"""Shared fixtures for doctests."""
import pytest


@pytest.fixture(autouse=True)
def number_to(doctest_namespace):
    doctest_namespace["x"] = 2
