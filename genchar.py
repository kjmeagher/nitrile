f = open('char.tex','w')
f.write(r"\documentclass{article}\begin{document}\begin{verbatim}")
for x in range(9,256):
    if x not in [11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,127]:
        f.write("0x{:X} {}\n".format(x,chr(x)))
    
f.write(r"\end{verbatim}\end{document}"+'\n\n')

