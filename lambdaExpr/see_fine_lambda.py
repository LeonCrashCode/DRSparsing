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

D = {}
L = []	
for line in open(sys.argv[1]):
	line = line.strip()
	if line == "":
		tc = L[2] + "<-" + L[4]
		if tc in D:
			D[tc] += 1
		else:
			D[tc] = 1		
		L = []
	else:
		L.append(line)

for key in D.keys():
	L.append([key, D[key]])

L = sorted(L, key=lambda x:x[1], reverse=True)

for item in L:
	print item[0], item[1]
