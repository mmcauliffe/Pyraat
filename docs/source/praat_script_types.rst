.. _praat_script_types:

Praat script types
==================

There are two main types of scripts that can be run.  The first loads and analyzes an entire wav file (best for short files),
and the second analyzes segments of a wav file without loading all of the file.

1. :ref:`full_file`
2. :ref:`file_segment`

1. :ref:`point_measures`
2. :ref:`track_measures`


.. _full_file:

Load and analyze full wav file
------------------------------

The first supported style of script uses an entire file to generate an output. Examples of such scripts would be calculating the
long-term average spectra of the file, or if words/phones have
been extracted previously into short wav files.

Header
``````

For shorter wav files, the following header is used to specify arguments.  The only required argument is for ``filename``
as that will point to which file to analyze.

.. code-block:: praat

   form Variables
       sentence filename
       real measurement_point
       integer nformants
       real ceiling
   endform


Required lines in the script
````````````````````````````

To load the wav file, use the following style:

.. code-block:: praat

   Read from file... 'filename$'


This will load the file into memory (so therefore it's best to use this style with short files).  Following this, the
rest of your script and processing can be done.

.. _file_segment:

Load and analyze just a segment of a wav file
---------------------------------------------

The second supported style of script uses just one part of the file from a longer file, ranging anywhere from several minutes
to several hours.  Loading those longer sound files into memory is prohibitive in many cases, so this style takes advantage
of the ``Open long sound file`` feature of Praat.

Header
``````

For analyzing one segment of a file, the following header is used to specify arguments.  The first four arguments are
required, specifying the name of the sound file, the begin time of the segment of interest, its end time, and which channel
to extract (for mono files, this will always be 0 in Python).

.. code-block:: praat

   form Variables
       sentence filename
       real begin
       real end
       integer channel
       real measurement_point
       integer nformants
       real ceiling
   endform

Required lines in the script
````````````````````````````

To load the wav file in the script, use the following style (assuming the header above):

.. code-block:: praat

   Open long sound file... 'filename$'


   Extract part... begin end 1
   channel = channel + 1
   Extract one channel... channel

   Rename... segment_of_interest

These lines first load the sound file as a "long" sound file, which does not immediately load the file into memory (necessary for longer sound files).

The next several lines extract one part of the file based on the ``begin``, ``end``, and ``channel`` arguments from the form above.

.. note::

   The above script assumes that channels are specified from 0 (left = 0, right = 1) in the Python code,
   whereas Praat begins from 1 (left = 1, right = 2).

Once the segment has been extracted, the final line renames the segment to something more referrable for later in the script
(since the default name in Praat for the segment will be a combination of the filename, begin, end, and channel).

Output types
------------

For all supported Praat scripts, Pyraat inspects the script for a line containing ``echo`` followed by some variable name
that stores the output of the script, i.e.:

.. code-block:: praat

   echo 'output$'

From this, Pyraat can see how this variable was built up and where there is a ``time`` column associated with output, which
determines whether the output is a track of values over time or just a single measurement for the whole file (i.e., a point
measure or an averaged measure).

.. _point_measures:

Output point measures
`````````````````````

If there is no time column in the output variable, then the output type is a point measure.
The expected output of a point measure Praat script should look something like the following:

::

   Point_measure_name1  Point_measure_name2
   30  40.54

The output consists of names of the point measures on the first line, separated by white space (any number of spaces or tabs),
and the corresponding values on the second line (likewise, separated by white space).

To generate such an output, the Praat script should have something like:

.. code-block:: praat

   cog$ = fixed$(cog, 4)
   peak$ = fixed$(peak, 4)
   slope$ = fixed$(slope, 4)
   spread$ = fixed$(spread, 4)
   output$ = "peak slope cog spread" + newline$ + peak$ + " " + slope$ + " "+ cog$+ " " + spread$
   echo 'output$'


.. _track_measures:

Output track measures
`````````````````````

For outputs involving time points, the output should be a track measure, like the following:

::

   time measure_name1 measure_name2
   0.01 10 20
   0.02 11 19
   0.03 12 18

As above, the columns are separated by white space (any number of tabs or spaces), but there must be one column named ``time``.

To generate such an output, the Praat script (i.e., for time series of formants) should look something like:

.. code-block:: praat


   output$ = "time"
   for i from 1 to nformants
       formNum$ = string$(i)
       output$ = output$ +tab$+ "F"+formNum$ + tab$ + "B" + formNum$
   endfor

   for f from 1 to frames
       t = Get time from frame number... 'f'
       t$ = fixed$(t, 3)
       output$ = output$ + t$
       for i from 1 to nformants
           formant = Get value at time... 'i' 't' Hertz Linear
           formant$ = fixed$(formant, 2)
           bw = Get bandwidth at time... 'i' 't' Hertz Linear
           bw$ = fixed$(bw, 2)
           output$ = output$ + tab$ + formant$ + tab$ + bw$
       endfor
       output$ = output$ + newline$
   endfor

The above part of the script generates an output variable (``output$``) that has the first line as the column headers
(containing ``time`` and a column for each formant and their respective bandwidth up to a number of formants).
It then loops through the frames in a Formant object and gets each frame's time point and formant and bandwidth values.
These are then added to the output line separated by tabs and each successive frame is separated by a newline.