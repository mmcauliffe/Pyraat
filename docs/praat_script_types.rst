.. _praat_script_types:

Praat script types
==================

There are two main types of scripts that can be run.  The first loads and analyzes an entire wav file (best for short files),
and the second analyzes segments of a wav file without loading all of the file.

1. `full_file`_
2. `file_segment`_

1. `point_measures`_
2. `track_measures`_


.. _full_file:

Load and analyze full wav file
------------------------------

Header
``````

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



.. _file_segment:

Load and analyze just a segment of a wav file
---------------------------------------------

Header
``````

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



.. _point_measures:

Output point measures
---------------------

.. _track_measures:

Output track measures
---------------------

