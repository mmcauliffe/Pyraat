import sys
import os
import re

from .run_scripts import run_script
from .parse_outputs import parse_point_script_output, parse_track_script_output, parse_multiple_tracks_script_output
from .exceptions import PraatScriptInvalidArgumentError, PraatScriptMultipleOutputError, PraatScriptNoOutputError, \
    PraatParseError, PyraatError


COMMENT_PREFIXES = ('#', '!', ';')
NON_ARGUMENT_FIELDS = ('comment', 'option', 'button')


def inspect_praat_script(script_path):
    arguments = []
    parsing_form = False
    form_seen = False
    uses_long = False
    script_body = []
    output_name = None
    with open(script_path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(COMMENT_PREFIXES):
                continue
            first_word = line.split()[0]
            if parsing_form:
                if first_word == 'endform':
                    parsing_form = False
                    continue
                if first_word not in NON_ARGUMENT_FIELDS:
                    t = line.split()
                    if len(t) < 2:
                        raise PraatParseError('The Praat script {} has a field without a name: '
                                              '"{}"'.format(script_path, line))
                    arguments.append((t[1], first_word))
            elif not form_seen and first_word == 'form':
                parsing_form = True
                form_seen = True
                continue
            elif 'echo' in line:
                m = re.match(r"echo\s'(\w+)[$]'", line)
                if m is not None:
                    if output_name is None:
                        output_name = m.groups()[0]
                    else:
                        raise PraatScriptMultipleOutputError(script_path)
            else:
                script_body.append(line)
            if 'Open long sound file' in line:
                uses_long = True
    if output_name is None:
        raise PraatScriptNoOutputError(script_path)
    valid_args = True
    if uses_long:
        if len(arguments) < 5:
            valid_args = False
        for i, a in enumerate(arguments):
            if i == 0 and a[1] != 'sentence':
                valid_args = False
            elif i in [1, 2, 4] and a[1] != 'real':
                valid_args = False
            elif i == 3 and a[1] != 'integer':
                valid_args = False
        additional_args = len(arguments) - 5
    else:
        if len(arguments) < 1 or arguments[0][1] != 'sentence':
            valid_args = False
        additional_args = len(arguments) - 1
    if not valid_args:
        raise PraatScriptInvalidArgumentError(script_path, arguments, uses_long)
    output_type = "point" 
    for line in script_body:
        if output_name in line:
            if "time" in line:
                output_type = "track"
        if "MULTIPLE_TRACKS" in line:
            output_type = "multiple_track"
            break
    return uses_long, output_type, additional_args


class PraatAnalysisFunction(object):
    def __init__(self, praat_script_path, praat_path=None, arguments=None):
        if praat_path is None:
            praat_path = 'praat'
        if arguments is None:
            arguments = []
        self.arguments = arguments
        self.praat_path = praat_path
        if not os.path.exists(praat_script_path):
            raise PraatParseError('The Praat script {} does not exist.'.format(praat_script_path))
        self.praat_script_path = praat_script_path
        self.uses_long, self.output_type, self.num_args = inspect_praat_script(self.praat_script_path)
        if self.uses_long:
            self.num_file_args = 5
        else:
            self.num_file_args = 1
        if self.arguments and len(self.arguments) != self.num_args:
            raise PraatParseError('The number of non-file specific arguments in the script '
                                  'do not match the number of arguments specified.')
        self._function = run_script
        self.point_measure = self.output_type == "point"
        if self.output_type == "track":
            self._output_parse_function = parse_track_script_output
        elif self.output_type == "point":
            self._output_parse_function = parse_point_script_output
        elif self.output_type == "multiple_track":
            self._output_parse_function = parse_multiple_tracks_script_output

    def __call__(self, *args, **kwargs):
        if len(args) == self.num_file_args:
            return self._output_parse_function(self._function(self.praat_path, self.praat_script_path, *args, *self.arguments))
        elif len(args) == self.num_file_args + self.num_args:
            return self._output_parse_function(self._function(self.praat_path, self.praat_script_path, *args))
        else:
            raise PyraatError('The arguments {} should be either just the file-specific ones ({}) '
                             'or all of the arguments in the script ({}).'.format(', '.join(map(str, args)),
                             self.num_file_args, self.num_file_args+self.num_args))
