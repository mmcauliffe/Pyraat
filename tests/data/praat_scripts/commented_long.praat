form Variables
    sentence filename
endform
# A commented-out line must not change how the script is classified:
# Open long sound file... 'filename$'

Read from file... 'filename$'
To Spectrum... yes
cog = Get centre of gravity... 2
output$ = "cog" + newline$ + string$(cog)
echo 'output$'
