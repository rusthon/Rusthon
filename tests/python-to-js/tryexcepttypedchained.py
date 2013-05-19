var(Exception1, Exception2)

Exception1 = JSObject()
Exception2 = JSObject()

try:
    raise Exception2
except Exception1:
    print False
except Exception2:
    print True
