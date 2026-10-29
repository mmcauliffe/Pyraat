# Comment lines above the form are not arguments either.
# A script reading the whole recording would call
# Open long sound file, but this line is only a comment.

form Variables
    sentence filename
    real begin
    real end
    integer channel
    real padding
endform

Open long sound file... 'filename$'
Extract part... begin end 1
channel = channel + 1
Extract one channel... channel
To Spectrum... yes
cog = Get centre of gravity... 2
output$ = "cog" + newline$ + string$(cog)
echo 'output$'
