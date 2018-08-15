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
	if len(expre["indexs"]) != 0:
		re.append("["+" ".join(expre["indexs"])+"]")
	if expre["text"] != "":
		re.append(expre["text"])
	if len(expre["attrib"]) != 0:
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
			#print tostring(json.loads(L[3], object_hook=ascii_encode_dict))
			print "\n".join(L[4:6])
			#print tostring(json.loads(L[5], object_hook=ascii_encode_dict))
			print
		L = []
	else:
		L.append(line)




