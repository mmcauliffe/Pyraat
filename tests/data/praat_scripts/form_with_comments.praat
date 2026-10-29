form Variables
    # Comment lines inside the form are not arguments
    sentence filename
    comment Neither is a comment field
    choice method 1
        option plain
        option weighted
    ! nor this
    real power 2
endform

Read from file... 'filename$'
To Spectrum... yes
if method$ = "weighted"
    cog = Get centre of gravity... power
else
    cog = Get centre of gravity... 2
endif
output$ = "cog" + newline$ + string$(cog)
echo 'output$'
