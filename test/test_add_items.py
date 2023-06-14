import pytest

@pytest.mark.mul
def testMultiplication():
    assert 11 * 11 == 121
 
def testAddition():
    assert 2 + 10 == 12
    
def test_add():
    assert 15 + 15 != 31