"""negative list indices"""
a = [1,2,3,4]
idx = -2
Error( a[-1]==4 )  ## this works in javascript mode because the translator knows index is negative
Error( a[idx]==3 ) ## this fails in javascript mode.
