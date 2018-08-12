
def get_index(node):
	index = []
	for subnode in node:
		if subnode.tag == "indexlist":
			for cc in subnode:
				index.append(cc.text[1:])
	if len(index) == 0:
		return None
	return index

def normal(r):
	new_r = ""
	for i in range(len(r)):
		if r[i] == "(":
			new_r += "-LRB-"
		elif r[i] == ")":
			new_r += "-RRB-"
		elif r[i] == "[":
			new_r += "-LCB-"
		elif r[i] == "]":
			new_r += "-RCB-"
		else:
			new_r += r[i]
	return new_r
	