

praatscripts = {
'formants.praat':"""form Variables
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

                    echo 'output$'""",
'extract.praat':"""form Variables
                        sentence filename
                        real begin
                        real end
                        sentence outname
                    endform

                    Read from file... 'filename$'

                    Extract part... 'begin' 'end' rectangular 1.0 0

                    Save as WAV file... 'outname$'""",
'pitch.praat': """form Variables
                      sentence filename
                    endform

                    Read from file... 'filename$'

                    To Pitch (ac)... 0.001 75.0 15 yes 0.03 0.45 0.01 0.35 0.14 600.0
                    frames = Get number of frames

                    output$ = "Time"+tab$+"Pitch"+newline$

                    for f from 1 to frames
                        t = Get time from frame number... 'f'
                        t$ = fixed$(t, 3)
                        v = Get value in frame... 'f' Hertz
                        v$ = fixed$(v, 2)
                        output$ = output$+t$+tab$+v$+newline$
                    endfor

                    echo 'output$'""",
'intensity.praat': """form Variables
                      sentence filename
                    endform

                    Read from file... 'filename$'
                    To Intensity... 100 0.001 yes

                    frames = Get number of frames

                    output$ = "time(s)"+tab$+"Intensity(dB)"+newline$

                    for f from 1 to frames
                        t = Get time from frame number... 'f'
                        t$ = fixed$(t, 3)
                        v = Get value in frame... 'f'
                        v$ = fixed$(v, 2)
                        output$ = output$+t$+tab$+v$+newline$
                    endfor

                    echo 'output$'""",
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
                    Save as EPS file... 'outname$'"""
                }
