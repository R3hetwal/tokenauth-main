import pytest

@pytest.mark.mul
def testMultiplication():
    """
    Test case for multiplication.

    This test verifies that multiplying 11 by 11 results in 121.
    """
    assert 11 * 11 == 121

def testAddition():
    """
    Test case for addition.

    This test verifies that adding 2 and 10 results in 12.
    """
    assert 2 + 10 == 12

def test_add():
    """
    Test case for addition.

    This test verifies that adding 15 and 15 does not result in 31.
    """
    assert 15 + 15 != 31
