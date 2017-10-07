import os
import pytest
from pyraat import PraatAnalysisFunction

from pyraat.parse_outputs import parse_track_script_output, parse_point_script_output
from pyraat.exceptions import PraatError


def test_long_track(praat_path, praat_script_test_dir, long_sound_file, iy_times, ih_times):
    script_path = os.path.join(praat_script_test_dir, 'formant_track_long.praat')
    func = PraatAnalysisFunction(script_path, praat_path, arguments=[0.01, 0.025, 5, 5500])

    assert not func.point_measure
    assert func.uses_long
    assert func._output_parse_function == parse_track_script_output

    output = func(long_sound_file, *iy_times, 0)
    print(output)

    header = ['F1', 'B1', 'F2', 'B2', 'F3', 'B3', 'F4', 'B4', 'F5', 'B5']

    assert all(isinstance(x, float) for x in output.keys())
    for k, v in output.items():
        assert isinstance(k, float)
        assert sorted(v.keys()) == sorted(header)
        for k2, v2 in v.items():
            assert isinstance(k2, str)
            assert isinstance(v2, (float, type(None)))

    output = func(long_sound_file, *ih_times, 0)
    print(output)

    assert all(isinstance(x, float) for x in output.keys())
    for k, v in output.items():
        assert isinstance(k, float)
        assert sorted(v.keys()) == sorted(header)
        for k2, v2 in v.items():
            assert isinstance(k2, str)
            assert isinstance(v2, (float, type(None)))


def test_long_formant_point(praat_path, praat_script_test_dir, long_sound_file, iy_times, ih_times):
    script_path = os.path.join(praat_script_test_dir, 'formant_point_long.praat')
    func = PraatAnalysisFunction(script_path, praat_path, arguments=[0.33, 5, 5500])

    assert func.point_measure
    assert func.uses_long
    assert func._output_parse_function == parse_point_script_output

    header = ['F1', 'B1', 'F2', 'B2', 'F3', 'B3', 'F4', 'B4', 'F5', 'B5']

    output = func(long_sound_file, *iy_times, 0, 0.33, 5, 5000)
    with pytest.raises(PraatError):
        func(long_sound_file, 0, 0.33, 5, 5000)
    print(output)
    assert sorted(output.keys()) == sorted(header)
    for k, v in output.items():
        assert isinstance(k, str)
        assert isinstance(v, (float, type(None)))
    iy_F1 = output['F1']
    iy_F2 = output['F2']

    output = func(long_sound_file, *ih_times, 0)
    print(output)
    assert sorted(output.keys()) == sorted(header)
    for k, v in output.items():
        assert isinstance(k, str)
        assert isinstance(v, (float, type(None)))
    ih_F1 = output['F1']

    ih_F2 = output['F2']
    assert ih_F1 < iy_F1
    assert ih_F2 < iy_F2


def test_long_multiple_output(praat_path, praat_script_test_dir, long_sound_file, s_times, sh_times):
    script_path = os.path.join(praat_script_test_dir, 'sibilant_jane.praat')
    func = PraatAnalysisFunction(script_path, praat_path)

    assert func.point_measure
    assert func.uses_long
    output = func(long_sound_file, *s_times, 0)
    assert sorted(output.keys()) == sorted(['peak', 'slope', 'cog', 'spread'])
    assert all(isinstance(x, float) for x in output.values())

    s_cog = output['cog']

    output = func(long_sound_file, *sh_times, 0)
    assert sorted(output.keys()) == sorted(['peak', 'slope', 'cog', 'spread'])
    assert all(isinstance(x, float) for x in output.values())

    sh_cog = output['cog']

    assert sh_cog < s_cog
