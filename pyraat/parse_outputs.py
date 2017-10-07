import re


def parse_point_script_output(script_output):
    """
    Parse the output from Praat into a dictionary of acoustic measurements.
    See docstring of analyze_script for formatting requirements.
    Prints the Praat script output if it doesn't fit the specified format (usually because the Praat script crashed),
    and returns None in that case

    Parameters
    ----------
    script_output : str
        output from Praat. (This is what appears in the Info window when using the Praat GUI)

    Returns
    ----------
    dict
        dictionary of measurement : value, based on the columns output by the Praat script
    """
    headers = []
    output = {}
    unexpected_input = False
    for line in script_output.split('\n'):
        if line.strip() is not "" and line.strip() is not "." and "Warning" not in line and "warning" not in line:
            values = line.strip().split()
            if not headers:
                headers = values
            else:
                for (measurement, value) in zip(headers, values):
                    if value.replace('.', '').strip('-').isnumeric():
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    elif value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    else:
                        unexpected_input = True
                        value = None
                    output[measurement] = value
    if unexpected_input:
        print('Praat output: ' + script_output)
    return output


def parse_track_script_output(text):
    if not text:
        return None
    lines = text.splitlines()
    head = None
    while head is None:
        try:
            l = lines.pop(0)
        except IndexError:
            print(text)
            raise
        if l.startswith('time'):
            head = re.sub('[(]\w+[)]', '', l)
            head = head.split("\t")[1:]
    output = {}
    for l in lines:
        if '\t' in l:
            line = l.split("\t")
            time = line.pop(0)
            values = {}
            for j in range(len(line)):
                v = line[j]
                if v != '--undefined--':
                    try:
                        v = float(v)
                    except ValueError:
                        print(text)
                        print(head)
                else:
                    v = None
                values[head[j]] = v
            if values:
                output[float(time)] = values
    return output
