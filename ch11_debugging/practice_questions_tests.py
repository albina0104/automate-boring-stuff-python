import pytest

from practice_questions import *

def test_assert_int_is_not_less_10():
    # Test case: spam is an integer >= 10
    assert_int_is_not_less_10(10)
    assert_int_is_not_less_10(20)

    # Test case: spam is an integer < 10
    with pytest.raises(AssertionError, match='spam should be an integer and at least 10'):
        assert_int_is_not_less_10(5)

    # Test case: spam is not an integer
    with pytest.raises(AssertionError, match='spam should be an integer and at least 10'):
        assert_int_is_not_less_10('not an integer')


def test_assert_strings_not_same():
    # Test case: strings are not same
    assert_strings_not_same('eggs', 'bacon')

    # Test case: strings are same
    with pytest.raises(AssertionError, match='strings should not be the same'):
        assert_strings_not_same('eggs', 'eggs')

    # Test case: strings are same, but case is different
    with pytest.raises(AssertionError, match='strings should not be the same'):
        assert_strings_not_same('eggs', 'EGgs')

    # Test case: provided variables are not strings
    with pytest.raises(AssertionError, match='strings should not be the same'):
        assert_strings_not_same(4, 7)


def test_trigger_assertion_error():
    # Test case: always raises AssertionError
    with pytest.raises(AssertionError):
        trigger_assertion_error()


if __name__ == '__main__':
    pytest.main()
