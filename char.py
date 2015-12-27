f=open('text.txt','w')

f.write('  ')

for a in range(16):
    f.write("%X "%a)

f.write('\n')

for a in range(2,16):
    f.write("%X "%a)
    for b in range(16):

        n = a*16+b

        if n in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,26,28,29,30]:
            f.write('\ ')
        else:
            c=chr(n)
            f.write(c+' ')


    f.write('\n')


f.close()
