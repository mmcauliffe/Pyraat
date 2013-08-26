form Variables
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

                    Save as EPS file... 'outname$'