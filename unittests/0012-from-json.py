d = json_to_pythonjs("""{"a":1,"b":2}""")
print d["a"], d["b"]
print json_to_pythonjs("""{"a":1.2}""")["a"]
l = json_to_pythonjs("""["spam","egg"]""")
print l[0], l[1]
n = json_to_pythonjs("""{"a_list":["spam","egg"]}""")
print n["a_list"][0], n["a_list"][1]
n2 = json_to_pythonjs("""{"a":{"a":1,"b":2},"b":2}""")
print n2["a"]["a"]
