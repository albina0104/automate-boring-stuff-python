import re
import unittest

# Regular expression that can detect dates in the DD/MM/YYYY format
date_regex = re.compile(r'^([0-3]\d)/([0-1]\d)/([1-2]\d{3})$')

def is_leap_year(year):
    if year % 4 != 0:
        return False
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        return False
    return True


def is_valid_date(date):
    """
    Checks if the date in the DD/MM/YYYY format is valid.

    :param date: The date to be checked.
    :type date: str
    :return: True if the date is valid, False otherwise.
    :rtype: bool
    """

    match_obj = date_regex.search(date)

    if not match_obj:
        return False

    day = int(match_obj.group(1))
    month = int(match_obj.group(2))
    year = int(match_obj.group(3))

    if month < 1 or month > 12:
        return False

    if month in (4, 6, 9, 11):
        if day < 1 or day > 30:
            return False
    elif month == 2:
        if is_leap_year(year):
            if day < 1 or day > 29:
                return False
        else:
            if day < 1 or day > 28:
                return False
    else:
        if day < 1 or day > 31:
            return False

    return True


class TestDates(unittest.TestCase):

    def test_valid_dates(self):
        valid_dates = [
            '01/02/2024',
            '31/08/1997',
            '29/02/2024'
        ]
        for date in valid_dates:
            self.assertTrue(is_valid_date(date), f'Failed on valid date: {date}')

    def test_invalid_dates(self):
        invalid_dates = [
            '31/02/2025',
            '234/38/32',
            '10/31/2004'
        ]
        for date in invalid_dates:
            self.assertFalse(is_valid_date(date), f'Failed on invalid date: {date}')


if __name__ == '__main__':
    unittest.main()
