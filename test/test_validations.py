from ..model.validations import *

def test_isbn13_valid():
    isbn13 = "9780486272740"
    assert is_valid_isbn13(isbn13) is True

def test_isbn13_with_bad_check_digit():
    isbn13 = "9780199540021"
    assert is_valid_isbn13(isbn13) is False

def test_isbn13_too_short():
    isbn13 = "97855426"
    assert is_valid_isbn13(isbn13) is False

def test_isbn13_too_long():
    isbn13 = "978556698741354252"
    assert is_valid_isbn13(isbn13) is False

def test_isbn13_non_numeric():
    isbn13 = "978048q272740"
    assert is_valid_isbn13(isbn13) is False

def test_isbn13_empty():
    isbn13 = ""
    assert is_valid_isbn13(isbn13) is False