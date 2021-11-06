import pytest


def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f" phrase '{phrase}' is lower than 15 characters'"
