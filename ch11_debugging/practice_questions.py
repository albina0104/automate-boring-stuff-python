# 1. Write an assert statement that triggers an AssertionError
# if the variable spam is an integer less than 10.
def assert_int_is_not_less_10(spam):
    assert isinstance(spam, int) and spam >= 10, 'spam should be an integer and at least 10'


# 2. Write an assert statement that triggers an AssertionError
# if the variables `eggs` and `bacon` contain strings that are
# the same as each other, even if their cases are different
# (that is, 'hello' and 'hello' are considered the same,
# and 'goodbye' and 'GOODbye' are also considered the same).
def assert_strings_not_same(eggs, bacon):
    assert isinstance(eggs, str) and isinstance(bacon, str) and \
        eggs.lower() != bacon.lower(), 'strings should not be the same'


# 3. Write an assert statement that always triggers an AssertionError.
def trigger_assertion_error():
    assert True == False
