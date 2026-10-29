import os
import pytest

from pyraat.run_scripts import run_script, decode_praat_output
from pyraat.parse_outputs import parse_point_script_output
from pyraat.exceptions import PraatError


def test_decode_praat_output():
    assert decode_praat_output('dur\u00e9e \u201cquoted\u201d'.encode('utf-8')) == 'dur\u00e9e \u201cquoted\u201d'
    # Bytes that aren't valid UTF-8 are read as Latin-1 instead of raising (except on
    # Windows, where Praat's output is decoded with the ANSI code page)
    if os.name != 'nt':
        assert decode_praat_output('dur\u00e9e'.encode('latin-1')) == 'dur\u00e9e'


def test_nonascii_output(praat_path, praat_script_test_dir, vowel_sound_file):
    script_path = os.path.join(praat_script_test_dir, 'nonascii_output.praat')
    output = parse_point_script_output(run_script(praat_path, script_path, vowel_sound_file))
    assert output == {'dur\u00e9e': 1.5}


def test_error_message_encoding(praat_path, praat_script_test_dir, vowel_sound_file):
    # Praat's error messages quote file names with curly quotes
    script_path = os.path.join(praat_script_test_dir, 'error_message.praat')
    with pytest.raises(PraatError) as excinfo:
        run_script(praat_path, script_path, vowel_sound_file)
    message = str(excinfo.value)
    assert '\u201c/nonexistent/sound.wav\u201d' in message
    assert '\u00e2\u0080' not in message
