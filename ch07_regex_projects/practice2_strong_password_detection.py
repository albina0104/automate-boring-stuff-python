import re, unittest

password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')    # To use more than one lookahead in regex, we need to put `.*` into the lookahead.

def is_strong_password(password):
    """
    Checks if the given password is strong.

    A strong password is defined as one that is at least eight characters long,
    contains both uppercase and lowercase characters, and has at least one digit.

    :param password: The password string to be checked.
    :type password: str
    :return: True if the password is strong, False otherwise.
    :rtype: bool
    """
    return True if password_regex.fullmatch(password) else False


class TestIsStrongPassword(unittest.TestCase):

    def test_valid_passwords(self):
        valid_passwords = [
            'Abc12345',
            '23dfAk8f',
            'd8k8KK8d',
            '#84383Jdfj$',
            '123456zA'
        ]
        for password in valid_passwords:
            self.assertTrue(is_strong_password(password), f'Failed on valid password: {password}')

    def test_invalid_passwords(self):
        invalid_passwords = [
            'abcd1234',
            'ABCD1234',
            '12345678',
            'abDCadKJ',
            'Abc238'
        ]
        for password in invalid_passwords:
            self.assertFalse(is_strong_password(password), f'Failed on invalid password: {password}')


if __name__ == '__main__':
    unittest.main()

