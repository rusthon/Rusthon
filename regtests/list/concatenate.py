"""concatenate lists"""
a = [1,2]
b = [3,4]
c = a + b

Error( len(c)==4 )
Error( c[0]==1 )
Error( c[1]==2 )
Error( c[2]==3 )
Error( c[3]==4 )
