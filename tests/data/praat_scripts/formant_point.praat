
form Variables
    sentence filename
    real measurement_point
    integer nformants
    real ceiling
endform

timestep = 0.01
windowlen = 0.025

Read from file... 'filename$'

duration = Get total duration

To Formant (burg)... 'timestep' 'nformants' 'ceiling' 'windowlen' 50
frames = Get number of frames

output$ = ""
for i from 1 to nformants
    formNum$ = string$(i)
    output$ = output$ +tab$+ "F"+formNum$ + tab$ + "B" + formNum$
endfor
output$ = output$ + newline$

t  = measurement_point * duration

for i from 1 to nformants
    formant = Get value at time... 'i' 't' Hertz Linear
    formant$ = fixed$(formant, 2)
    bw = Get bandwidth at time... 'i' 't' Hertz Linear
    bw$ = fixed$(bw, 2)
    output$ = output$ + tab$ + formant$ + tab$ + bw$
endfor


echo 'output$'
