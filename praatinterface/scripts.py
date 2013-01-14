

praatscripts = {
                'formants-all.praat':"""form Variables
                    sentence filename
                    real begin
                    real end
                    real nformants
                    real ceiling
                    endform

                    Read from file... 'filename$'

                    Extract part... 'begin' 'end' rectangular 1.0 0
                    name$ = "slice"
                    Rename... 'name$'

                    To Formant (burg)... 0.0 'nformants' 'ceiling' 0.025 50

                    list$ =  List... 0 1 4 0 1 0 1 0

                    echo 'list$' """,
                'extract.praat':"""form Variables
    sentence filename
    real begin
    real end
    sentence outname
endform

Read from file... 'filename$'

Extract part... 'begin' 'end' rectangular 1.0 0

Save as WAV file... 'outname$'""",
                'spectroPic.praat':"""form Variables
    sentence filename
    boolean formants
    real nformants
    real ceiling
    real numBounds
    text boundaries
endform



Erase all

Read from file... 'filename$'
outname$ = filename$ -".wav"+"-spectro.eps"

name$ = selected$("Sound")

dur = Get total duration

step = dur / 512
Colour... black
To Spectrogram... 0.005 'ceiling' 'step' 20 Gaussian

Paint... 0.0 0.0 0.0 0.0 100 1 50.0 6.0 0.0 1
bound$ = boundaries$
for i from 1 to numBounds
    if index(bound$,",") = 0
        b$ = bound$
    else
    b$ = left$(bound$,index(bound$,",")-1)
    bound$ = right$(bound$,length(bound$)-index(bound$,","))
    endif
    Colour... blue
    Draw line... 'b$' 0 'b$' 'ceiling'
endfor

if formants = 1
    select Sound 'name$'
    To Formant (burg)... 0.0 'nformants' 'ceiling' 0.025 50
    Colour... red
    Speckle... 0.0 0.0 'ceiling' 30 1
    Draw tracks... 0.0 0.0 'ceiling' 1
endif

Save as EPS file... 'outname$'""",
                'waveformPic.praat':"""form Variables
    sentence filename
    real numBounds
    text boundaries
endform

outname$ = filename$-".wav"+"-waveform.eps"

printline 'numBounds'
Erase all

Read from file... 'filename$'

min = Get minimum... 0.0 0.0 None

max = Get maximum... 0.0 0.0 None

Draw... 0.0 0.0 0.0 0.0 1 Curve
bound$ = boundaries$
for i from 1 to numBounds
    if index(bound$,",") = 0
        b$ = bound$
    else
    b$ = left$(bound$,index(bound$,",")-1)
    bound$ = right$(bound$,length(bound$)-index(bound$,","))
    endif
    Colour... blue
    Draw line... 'b$' 'min' 'b$' 'max'
endfor
Save as EPS file... 'outname$'
"""
                }
