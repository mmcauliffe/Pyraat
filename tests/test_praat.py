
import pytest

from praatinterface import PraatLoader

def test_formants(praatpath, sound_file):
    pl = PraatLoader(praatpath = praatpath, debug = True)
    text = pl.run_script('formants.praat',sound_file, 5, 5500)

    formants = pl.read_praat_out(text)

def test_basic(praatpath):
    basic_script = 'echo hello'

    pl = PraatLoader(praatpath = praatpath, basic = basic_script, debug = True)

    text = pl.run_script('basic')
    assert(text == 'hello')

def test_another_praatloader(praatpath):
    basic_script = 'echo hello'

    pl = PraatLoader(praatpath = praatpath, basic = basic_script, debug = True)
    pl.reinit_scripts()

    pl2 = PraatLoader(praatpath = praatpath, basic2 = basic_script, debug = True)
    pl2.reinit_scripts()
