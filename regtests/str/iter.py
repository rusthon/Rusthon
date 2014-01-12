"""The string iterator"""

a = list("abc")
Error(a[0] == 'a')
Error(a[1] == 'b')
Error(a[2] == 'c')

# Does not work with javascript
a = []
for i in "abc":
    a.append(i)
Warning(a[0] == 'a')
Warning(a[1] == 'b')
Warning(a[2] == 'c')
