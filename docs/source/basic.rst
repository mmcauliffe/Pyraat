
.. _basic:

Basic usage
===========

To use Pyraat's Praat functions, the PraatAnalysisFunction is first imported and then constructed as follows:


.. code-block:: python

   from pyraat import PraatAnalysisFunction

   script_path = '/path/to/script.praat'
   praat_path = '/path/to/praat'
   wav_file = '/path/to/file.wav'

   func = PraatAnalysisFunction(script_path, praat_path)

   output = func(wav_file)


The ``praat_path`` argument can be omitted if ``praat`` is available on the system path.

.. note::

   The above snippet assumes a script that analyzes a whole file.  See :ref:`praat_script_types` for more information on the types of Praat scripts.

Arguments to the Praat script that are constant over multiple evaluations on wav files:

.. code-block:: python

   from pyraat import PraatAnalysisFunction

   script_path = '/path/to/script.praat'
   praat_path = '/path/to/praat'
   wav_file = '/path/to/file.wav'
   wav_file2 = '/path/to/file2.wav'

   func = PraatAnalysisFunction(script_path, praat_path, arguments=[1, 2, 3])

   output = func(wav_file)
   output2 = func(wav_file2)

If the arguments depend on the file, they can be specified on each evaluation:

.. code-block:: python

   from pyraat import PraatAnalysisFunction

   script_path = '/path/to/script.praat'
   praat_path = '/path/to/praat'
   wav_file = '/path/to/file.wav'
   wav_file2 = '/path/to/file2.wav'

   func = PraatAnalysisFunction(script_path, praat_path)

   output = func(wav_file, 1, 2, 3)
   output2 = func(wav_file2, 4, 5, 6)
