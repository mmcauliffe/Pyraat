form Variables
    sentence filename
    real
endform
Read from file... 'filename$'
To Spectrum... yes
cog = Get centre of gravity... 2
output$ = "cog" + newline$ + string$(cog)
echo 'output$'
