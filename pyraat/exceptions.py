class PyraatError(Exception):
    pass


class PraatError(PyraatError):
    def __init__(self, command, error_output):
        msg = "The command `{}` gave the following error output:\n\n{}".format(command, error_output)
        super(PraatError, self).__init__(msg)


class PraatParseError(PyraatError):
    pass


class PraatScriptMultipleOutputError(PraatParseError):
    def __init__(self, script_path):
        msg = 'The script {} contained multiple lines with echo, ' \
              'please ensure that all output is concatenated into a single output line.'.format(script_path)
        super(PraatScriptMultipleOutputError, self).__init__(msg)


class PraatScriptNoOutputError(PraatParseError):
    def __init__(self, script_path):
        msg = 'The script {} contained no lines with echo, ' \
              'please ensure that there is a line at the end to echo the output.'.format(script_path)
        super(PraatScriptNoOutputError, self).__init__(msg)


class PraatScriptInvalidArgumentError(PraatParseError):
    def __init__(self, script_path, arguments, uses_long):
        if uses_long:
            msg = 'The script {} has invalid arguments. ' \
                  'The first five arguments must specify: ' \
                  'the file name (sentence), ' \
                  'the beginning of the segment (real), ' \
                  'the end of the segment (real), ' \
                  'the channel of the segment (integer), ' \
                  'and padding surrounding the segment. ' \
                  'The current first four arguments are: {}'.format(script_path, ', '.join(
                '{} ({})'.format(*x) for x in arguments[:4]))
        else:
            msg = 'The script {} has invalid arguments. ' \
                  'The first argument must specify ' \
                  'the file name (sentence). ' \
                  'The current first argument is: {} ({})'.format(script_path, *arguments[0])
        super(PraatScriptInvalidArgumentError, self).__init__(msg)
