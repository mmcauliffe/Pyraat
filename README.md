python-praat-scripts
====================

Interface for running Praat scripts through Python

Installation
============

You can install python-praat-scripts through pip via:

```
pip install python-praat-scripts
```

Or through downloading this repository and running:

```
python setup.py install
```

Once installed, the `praatinterface` package will be importable.

Use
===

This package allows users to specify Praat scripts in Python code (as strings),
which can be called through a PraatLoader object, which can parse the output
to something more useable than plain text.  There are several predefined
scripts included in the loader.

For basic usage, instantiate a PraatLoader object as below:

```
from praatinterface import PraatLoader

pl = PraatLoader(praatpath = '/path/to/praat')

text = pl.run_script('formants.praat', '/path/to/wav/file', 5, 5500)

formants = pl.read_praat_out(text)
```

The result of running the formants script gives the first two formants estimated by
Praat in the wav file specified, as a list of dictionaries with keys for
Time, F1, B1, F2, and B2.

The full list of scripts prewritten in this module are in `praatinterface.scripts.py`.

User-specified scripts can be given via keyword arguments to the PraatLoader class.

```
from praatinterface import PraatLoader

basic_script = 'echo hello'

pl = PraatLoader(praatpath = '/path/to/praat', basic = basic_script)

text = pl.run_script('basic')
```

For the above code, text should equal 'hello'.


Scripts that need to return some value should use the Praat function `echo`
which will be sent to the Python process.
