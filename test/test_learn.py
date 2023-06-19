import pytest

"""
Unit tests for mathematical operations and login functionality.

The following test functions are included in this module:

    - testMultiplication(): Test case for multiplication. This test verifies that multiplying 11 by 11 
                            results in 121.

    - testAddition(): Test case for addition. This test verifies that adding 2 and 10 results in 12.

    - test_add(): Test case for addition. This test verifies that adding 15 and 15 does not result in 31.

    - test_login(): Test the login functionality. This test prints a message indicating successful login.

    - testCalculation(): Test a calculation. This test asserts that the result of multiplying 2 and 3 is 
                         6.

    - testLogoff(): Test the logoff functionality. This test prints a message indicating successful logoff.

These tests cover different scenarios and functionalities. They are marked with specific markers using the `pytest.mark`
decorator. The markers provide additional metadata for categorizing and organizing the tests, allowing selective test
execution based on markers.

Markers:
    - `@pytest.mark.mul`: These tests are marked with the "mul" marker.

    - `@pytest.mark.test`: This test is marked with the "test" marker.

    - `@pytest.mark.regression`: This test is marked with the "regression" marker.

Note: The markers can be used with pytest's command-line options to run specific subsets of tests.

"""

@pytest.mark.mul
def testMultiplication():
    """
    Test case for multiplication.

    This test verifies the multiplication operation by checking if multiplying 11 by 11 equals 121.

    Marker:
        - `@pytest.mark.mul`: This test is marked with the "mul" marker.

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

@pytest.mark.test
def test_login():
    """
    Test case for login functionality.

    This test verifies the login functionality by printing a message indicating successful login.

    Marker:
        - `@pytest.mark.test`: This test is marked with the "test" marker.
    
    """
    print("Login Successful !!!")

@pytest.mark.mul
def testCalculation():
    """
    Test case for multiplication calculation.

    This test verifies the multiplication calculation by asserting that multiplying 2 by 3 equals 6.

    Marker:
        - `@pytest.mark.mul`: This test is marked with the "mul" marker.

    """
    assert 2*3 == 6

@pytest.mark.regression
def testLogoff():
    """
    Test case for logoff functionality.

    This test verifies the logoff functionality by printing a success message indicating successful logoff.

    Marker:
        - `@pytest.mark.regression`: This test is marked with the "regression" marker.

    """
    print("Logging out successfully!!!")


