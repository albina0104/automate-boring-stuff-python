import re, unittest

def strip_regex(string, chars=None):
    """
    A function that takes a string and does the same thing as the strip() string method.
    If no other arguments are passed other than the string to strip, then whitespace
    characters will be removed from the beginning and end of the string.
    Otherwise, the characters specified in the second argument to the function will be
    removed from the string.

    :param string: The string to remove characters from.
    :type string: str
    :param chars: The characters to remove from the string (optional).
    :type chars: str
    :return: The stripped string.
    :rtype: str
    """
    if chars is None:
        whitespace_regex = re.compile(r'^\s+|\s+$')
        return whitespace_regex.sub('', string)

    chars_regex = re.compile(f'^[{chars}]+|[{chars}]+$')
    return chars_regex.sub('', string)


class TestStripRegex(unittest.TestCase):

    def test_strip_regex_remove_whitespace(self):
        strings = [
            ' asdfk3234 ',
            'sdkfasd  ',
            '  sdfa3   ',
            '   kjdfks'
        ]
        for string in strings:
            self.assertEqual(strip_regex(string), string.strip(),
                             f'Failed on string: {string}, whitespaces not removed')

    def test_strip_regex_remove_characters(self):
        strings_chars = [
            ('abcdefgh123', 'a3'),
            (',,..adfffdsffffi8L8*', ',f*8'),
            (' 33v  dsfe2 84e4', 'e4')
        ]
        for string, chars in strings_chars:
            self.assertEqual(strip_regex(string, chars), string.strip(chars),
                             f'Failed on string: {string}, chars not removed: {chars}')


if __name__ == '__main__':
    unittest.main()
