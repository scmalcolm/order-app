import re

ISBN13_REGEX = re.compile("^\d{13}$")

def is_valid_isbn13(isbn13):
    if ISBN13_REGEX.match(isbn13) is None:
        return False
    total = sum([int(num)*weight for num, weight in zip(isbn13, (1,3)*6)])
    ck = (10-(total%10))%10
    return ck == int(isbn13[-1])
    