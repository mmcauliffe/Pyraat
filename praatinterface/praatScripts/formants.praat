form Variables
    sentence filename
    real nformants
    real ceiling
endform

Read from file... 'filename$'

To Formant (burg)... 0.001 'nformants' 'ceiling' 0.025 50
frames = Get number of frames

output$ = "time"+tab$+"F1"+tab$+"B1"+tab$+"F2"+tab$+"B2"+newline$

for f from 1 to frames
    t = Get time from frame number... 'f'
    t$ = fixed$(t, 3)
    f1 = Get value at time... 1 't' Hertz Linear
    f1$ = fixed$(f1, 2)
    f2 = Get value at time... 2 't' Hertz Linear
    f2$ = fixed$(f2, 2)
    b1 = Get bandwidth at time... 1 't' Hertz Linear
    b1$ = fixed$(b1, 2)
    b2 = Get bandwidth at time... 2 't' Hertz Linear
    b2$ = fixed$(b2, 2)
    output$ = output$+t$+tab$+f1$+tab$+b1$+tab$+f2$+tab$+b2$+newline$
endfor

echo 'output$'
