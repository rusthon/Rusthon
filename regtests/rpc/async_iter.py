"""iteration"""
## note mycollection is hard coded in run.py as `range(10)`

def main():
	a = []
	with rpc('http://localhost:8080') as server:
		for ob in server.mycollection:
			a.append( ob )

	print(a)
	TestError( len(a)==10 )
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( a[2]==2 )

	