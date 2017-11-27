import os
import pytest
from pyraat import PraatAnalysisFunction

from pyraat.parse_outputs import parse_track_script_output, parse_point_script_output
from pyraat.exceptions import PyraatError


def test_short_formant_track(praat_path, praat_script_test_dir, vowel_sound_file):
    script_path = os.path.join(praat_script_test_dir, 'formant_track.praat')
    func = PraatAnalysisFunction(script_path, praat_path, arguments=[0.01, 0.025, 5, 5500])

    assert not func.point_measure
    assert not func.uses_long
    assert func._output_parse_function == parse_track_script_output

    output = func(vowel_sound_file)
    header = ['F1', 'B1', 'F2', 'B2', 'F3', 'B3', 'F4', 'B4', 'F5', 'B5']

    assert all(isinstance(x, float) for x in output.keys())
    for k, v in output.items():
        assert isinstance(k, float)
        assert sorted(v.keys()) == sorted(header)
        for k2, v2 in v.items():
            assert isinstance(k2, str)
            assert isinstance(v2, (float, type(None)))


def test_short_formant_point(praat_path, praat_script_test_dir, vowel_sound_file):
    script_path = os.path.join(praat_script_test_dir, 'formant_point.praat')
    func = PraatAnalysisFunction(script_path, praat_path, arguments=[0.33, 5, 5500])

    assert func.point_measure
    assert not func.uses_long
    assert func._output_parse_function == parse_point_script_output

    header = ['F1', 'B1', 'F2', 'B2', 'F3', 'B3', 'F4', 'B4', 'F5', 'B5']
    output = func(vowel_sound_file, 0.33, 5, 5000)
    with pytest.raises(PyraatError):
        func(vowel_sound_file, 0, 0.33, 5, 5000)
    assert sorted(output.keys()) == sorted(header)
    for k, v in output.items():
        assert isinstance(k, str)
        assert isinstance(v, (float, type(None)))


def test_short_cog(praat_path, praat_script_test_dir, vowel_sound_file):
    script_path = os.path.join(praat_script_test_dir, 'COG.praat')
    func = PraatAnalysisFunction(script_path, praat_path)

    assert func.point_measure
    assert not func.uses_long
    assert func._output_parse_function == parse_point_script_output

    output = func(vowel_sound_file)
    assert sorted(output.keys()) == ['cog']
    assert all(isinstance(x, float) for x in output.values())

