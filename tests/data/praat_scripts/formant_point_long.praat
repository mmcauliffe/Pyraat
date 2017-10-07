
form Variables
    sentence filename
    real begin
    real end
    integer channel
    real measurement_point
    integer nformants
    real ceiling
endform

timestep = 0.01
windowlen = 0.025

Open long sound file... 'filename$'

seg_duration = end - begin
seg_begin = begin


seg_end = end

Extract part... seg_begin seg_end 1
channel = channel + 1
Extract one channel... channel

Rename... segment_of_interest

duration = Get total duration

To Formant (burg)... 'timestep' 'nformants' 'ceiling' 'windowlen' 50

output$ = ""
for i from 1 to nformants
    formNum$ = string$(i)
    output$ = output$ +tab$+ "F"+formNum$ + tab$ + "B" + formNum$
endfor
output$ = output$ + newline$

t  = measurement_point * duration + seg_begin

for i from 1 to nformants
    formant = Get value at time... 'i' 't' Hertz Linear
    formant$ = fixed$(formant, 2)
    bw = Get bandwidth at time... 'i' 't' Hertz Linear
    bw$ = fixed$(bw, 2)
    output$ = output$ + tab$ + formant$ + tab$ + bw$
endfor


echo 'output$'
