
import pytest
import os

@pytest.fixture(scope = 'module')
def test_dir():
    return os.path.abspath('tests/data')

@pytest.fixture(scope = 'module')
def sound_file(test_dir):
    return os.path.join(test_dir, 'vowel_a_16k.wav')

@pytest.fixture(scope='module')
def praatpath():
    if os.environ.get('TRAVIS'):
        return os.path.join(os.environ.get('HOME'),'tools','praat')
    return r'C:\Users\michael\Documents\Praat\praatcon.exe'

