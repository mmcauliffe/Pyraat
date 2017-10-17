import pytest
import os

from pyraat.praat_script import inspect_praat_script
from pyraat.exceptions import PraatScriptNoOutputError, PraatScriptMultipleOutputError, PraatScriptInvalidArgumentError


def test_check_praat_script_short(praat_script_test_dir):
    uses_long, point_measure, num_args = inspect_praat_script(os.path.join(praat_script_test_dir, 'COG.praat'))
    assert not uses_long
    assert point_measure
    assert num_args == 0

    uses_long, point_measure, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'formant_track.praat'))
    assert not uses_long
    assert not point_measure
    assert num_args == 4

    uses_long, point_measure, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'formant_point.praat'))
    assert not uses_long
    assert point_measure
    assert num_args == 3


def test_check_praat_script_long(praat_script_test_dir):
    uses_long, point_measure, num_args = inspect_praat_script(
        os.path.join(praat_script_test_dir, 'multiple_formants_bandwidth_segment.praat'))
    assert uses_long
    assert point_measure
    assert num_args == 5

    uses_long, point_measure, num_args = inspect_praat_script(os.path.join(praat_script_test_dir, 'COG_long.praat'))
    assert uses_long
    assert point_measure
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
