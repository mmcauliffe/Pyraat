import pytest
import os

from pyraat.praat_script import inspect_praat_script, read_praat_script
from pyraat.exceptions import PraatScriptNoOutputError, PraatScriptMultipleOutputError, PraatScriptInvalidArgumentError, \
    PraatParseError


def test_check_praat_script_short(praat_script_test_dir):
    uses_long, output_type, num_args = inspect_praat_script(os.path.join(praat_script_test_dir, 'COG.praat'))
    assert not uses_long
    assert output_type == "point"
    assert num_args == 0

    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'formant_track.praat'))
    assert not uses_long
    assert not output_type == "point"
    assert num_args == 4

    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'formant_point.praat'))
    assert not uses_long
    assert output_type == "point"
    assert num_args == 3


def test_check_praat_script_long(praat_script_test_dir):
    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'multiple_formants_bandwidth_segment.praat'))
    assert uses_long
    assert output_type == "point"
    assert num_args == 5

    uses_long, output_type, num_args = inspect_praat_script(os.path.join(praat_script_test_dir, 'COG_long.praat'))
    assert uses_long
    assert output_type == "point"
    assert num_args == 0


def test_exceptions(praat_script_test_dir):
    with pytest.raises(PraatScriptNoOutputError):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'no_output_script.praat'))

    with pytest.raises(PraatScriptMultipleOutputError):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'multiple_output_script.praat'))

    with pytest.raises(PraatScriptInvalidArgumentError):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'invalid_reg_script.praat'))

    with pytest.raises(PraatScriptInvalidArgumentError):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'invalid_long_script.praat'))


def test_form_comments_and_display_fields(praat_script_test_dir):
    # Only real form fields count as arguments: not comment lines, comment fields,
    # or the options of a choice field
    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'form_with_comments.praat'))
    assert not uses_long
    assert output_type == "point"
    assert num_args == 2


def test_comments_outside_form(praat_script_test_dir):
    # Comment lines above the form are not arguments
    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'comments_above_form_long.praat'))
    assert uses_long
    assert output_type == "point"
    assert num_args == 0

    # A commented-out Open long sound file line doesn't make a script Format 2
    uses_long, output_type, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'commented_long.praat'))
    assert not uses_long
    assert num_args == 0


def test_no_form(praat_script_test_dir):
    with pytest.raises(PraatScriptInvalidArgumentError):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'no_form.praat'))


def test_nameless_field(praat_script_test_dir):
    # A form field with no name is malformed, and reported as such
    with pytest.raises(PraatParseError, match='field without a name'):
        inspect_praat_script(os.path.join(praat_script_test_dir, 'nameless_field.praat'))


ENCODING_TEST_SCRIPT = """# Centre de gravit\u00e9 du spectre
form Variables
    sentence filename
    real power
endform
Read from file... 'filename$'
To Spectrum... yes
cog = Get centre of gravity... power
output$ = "cog" + newline$ + string$(cog)
echo 'output$'
"""


@pytest.mark.parametrize('encoding', ['utf-8', 'utf-8-sig', 'utf-16', 'latin-1'])
def test_script_encodings(tmp_path, encoding):
    # Scripts saved as UTF-16 (Praat's default for non-ASCII text), as UTF-8 with a
    # byte-order mark, or as Latin-1 are read like Praat reads them. The byte-order
    # mark case starts with the form, where a leftover mark would hide it
    text = ENCODING_TEST_SCRIPT
    if encoding == 'utf-8-sig':
        text = text.split('\n', 1)[1]
    script_path = str(tmp_path / 'script.praat')
    with open(script_path, 'w', encoding=encoding) as f:
        f.write(text)
    uses_long, output_type, num_args = inspect_praat_script(script_path)
    assert not uses_long
    assert output_type == "point"
    assert num_args == 1
    assert read_praat_script(script_path) == text


@pytest.mark.parametrize('newline', ['\n', '\r\n', '\r'])
def test_script_line_endings(tmp_path, newline):
    # Unix, Windows and classic Mac line endings are all split into lines, as open() does
    script_path = str(tmp_path / 'script.praat')
    with open(script_path, 'w', encoding='utf-8', newline='') as f:
        f.write(ENCODING_TEST_SCRIPT.replace('\n', newline))
    assert inspect_praat_script(script_path) == (False, "point", 1)
