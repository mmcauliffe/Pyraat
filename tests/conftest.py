import pytest
import os
import sys


@pytest.fixture(scope='session')
def test_dir():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'data')


@pytest.fixture(scope='session')
def praat_script_test_dir(test_dir):
    return os.path.join(test_dir, 'praat_scripts')


@pytest.fixture(scope='session')
def sound_file_dir(test_dir):
    return os.path.join(test_dir, 'sound_files')


@pytest.fixture(scope='session')
def vowel_sound_file(sound_file_dir):
    return os.path.join(sound_file_dir, 'vowel_a_16k.wav')


@pytest.fixture(scope='session')
def long_sound_file(sound_file_dir):
    return os.path.join(sound_file_dir, 'acoustic_corpus.wav')


@pytest.fixture(scope='session')
def sh_times():
    return 24.362, 24.456


@pytest.fixture(scope='session')
def s_times():
    return 25.146, 25.252


@pytest.fixture(scope='session')
def iy_times():
    return 13.551, 13.898


@pytest.fixture(scope='session')
def ih_times():
    return 12.941, 13.033


@pytest.fixture(scope='session')
def praat_path():
    if sys.platform == 'win32':
        return 'praat.exe'
    elif sys.platform == 'darwin':
        return '/Applications/Praat.app/Contents/MacOS/Praat'
    else:
        return os.environ.get('praat', 'praat')
