import sys
import types
import json

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tostring(expre):
	assert type(expre) == types.DictType
	re = []
	re.append(expre["type"]+"(")
	keys = ["pointer", "indexs", "label"]
	if "pointer" in expre:
		re.append(expre["pointer"])
	if "indexs" in expre:
		if expre["indexs"] == None:
			re.append("[]")
		else:
			re.append("["+" ".join(expre["indexs"])+"]")
	if "label" in expre:
		re.append(expre["label"]) 
	if "expression" in expre:
		for subexpre in expre["expression"]:
			re.append(tostring(subexpre))
	if "attrib" in expre:
		for key in expre["attrib"].keys():
			re.append(expre["attrib"][key])
	re.append(")")
	return " ".join(re)

L = []	
for line in open(sys.argv[1]):
	line = line.strip()
	if line == "":
		if L[1].split()[1] == sys.argv[2]:
			print "\n".join(L[0:4])
			print tostring(json.loads(L[3], object_hook=ascii_encode_dict))
			print "\n".join(L[4:6])
			print tostring(json.loads(L[5], object_hook=ascii_encode_dict))
			print
		L = []
	else:
		L.append(line)




