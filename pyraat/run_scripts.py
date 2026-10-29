import os
import sys
from subprocess import Popen, PIPE
import re

from .exceptions import PraatError


def decode_praat_output(data):
    """Decode what Praat writes to its standard output or error.

    Praat writes UTF-8 when its output is redirected, except on Windows, where
    ``run_script`` passes ``-a`` and Praat writes in the ANSI code page instead
    (Python's ``mbcs`` codec). Output that isn't valid UTF-8 falls back to Latin-1
    rather than failing.
    """
    if sys.platform == 'win32':
        return data.decode('mbcs', errors='replace')
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('latin-1')


def run_script(praat_path, script_path, *args):
    com = [praat_path]
    if sys.platform == 'win32':
        com += ['-a']
    com += ['--run']
    com += [script_path] + list(map(str, args))
    err = ''
    text = ''
    with Popen(com, stdout=PIPE, stderr=PIPE, stdin=PIPE) as p:
        text = decode_praat_output(p.stdout.read())
        err = decode_praat_output(p.stderr.read())
    if (err and not err.strip().startswith('Warning')) or not text:
        raise (PraatError(com, err))
    return text

