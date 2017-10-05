import os
from subprocess import Popen, PIPE
import re

from .exceptions import PraatError


def run_script(praat_path, script_path, *args):
    com = [praat_path]
    if praat_path.endswith('con.exe'):
        com += ['-a']
    com += ['--run']
    com += [script_path] + list(map(str, args))
    err = ''
    text = ''
    with Popen(com, stdout=PIPE, stderr=PIPE, stdin=PIPE) as p:
        try:
            text = str(p.stdout.read().decode('latin'))
            err = str(p.stderr.read().decode('latin'))
        except UnicodeDecodeError:
            print(p.stdout.read())
            print(p.stderr.read())
    if (err and not err.strip().startswith('Warning')) or not text:
        print(com)
        print(args)
        raise (PraatError(err))
    return text

