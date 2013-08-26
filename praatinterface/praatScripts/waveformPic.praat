form Variables
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