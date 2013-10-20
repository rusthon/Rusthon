def generator():
    for i in range(5):
        yield i * 10

for i in generator():
    print i
