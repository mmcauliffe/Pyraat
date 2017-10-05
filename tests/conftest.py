import pytest
import os


@pytest.fixture(scope='session')
def test_dir():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'data')


@pytest.fixture(scope='session')
def praat_script_test_dir(test_dir):
    return os.path.join(test_dir, 'praat_scripts')


@pytest.fixture(scope='module')
def sound_file(test_dir):
    return os.path.join(test_dir, 'vowel_a_16k.wav')


@pytest.fixture(scope='module')
def praat_path():
    if os.environ.get('TRAVIS'):
        return os.path.join(os.environ.get('HOME'), 'tools', 'praat')
    return 'praat'
