"""if empty list then false"""
d = []
if d:
	err1 = 1
else:
	err1 = 0

if []:
	err2 = 1
else:
	err2 = 0

d.append('xxx')
if d:
	err3 = 0
else:
	err3 = 1

Error( err1 == 0 )
Error( err2 == 0 )
Error( err3 == 0 )
