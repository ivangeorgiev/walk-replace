import os
import pytest

@pytest.fixture(scope="session")
def testsdir():
    return os.path.abspath(os.path.dirname(__file__))

@pytest.fixture(scope="session")
def fixdir(testsdir):
    return os.path.abspath(f"{testsdir}/fixture")

