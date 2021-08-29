print("pattern a):-")
for x in range(1,6):
    for y in range(x):
        print("*",end='\t')
    print()

print("pattern b):-")

for x in range(1,8):
    if x<=4:
        for y in range(x):
            print("*",end='\t')
    print()
    if x>=4:
        for z in range(8,x,-1):
            print("*",end='\t')


