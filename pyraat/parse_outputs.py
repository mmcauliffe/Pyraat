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
    for line in script_output.split('\n'):
        if line.strip() is not "" and line.strip() is not "." and "Warning" not in line and "warning" not in line:
            values = line.strip().split()
            if not headers:
                headers = values
            else:
                for (measurement, value) in zip(headers, values):
                    if value == '--undefined--':
                        value = None
                    elif value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = None
                    output[measurement] = value
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

def parse_multiple_tracks_script_output(text):
    if not text:
        return None
    lines = text.splitlines()
    final_output = {}
    while lines:
        header = tuple(lines.pop(0).strip().split('\t'))
        tracks = lines.pop(0).strip().split('\t')
        output = {t:[] for t in tracks}
        l = lines.pop(0).strip()
        while l and lines:
            values = l.split('\t')
            for t, v in zip(tracks, values):
                if v == '--undefined--' or v == "'undefined'":
                    v = None
                else:
                    v = float(v)
                output[t].append(v)
            l = lines.pop(0).strip()
        final_output[header] = output
    return final_output
