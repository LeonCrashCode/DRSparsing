import types

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

def equals(expre1, expre2):
	if type(expre1) != type(expre2):
		return False
	t = type(expre1)
	if t == types.NoneType:
		if expre1 != expre2:
			return False
	elif t == types.StringType or t == types.UnicodeType:
		if expre1 != expre2:
			return False
	elif t == types.DictType:
		if len(expre1) != len(expre2):
			return False
		for key in expre1.keys():
			if key not in expre2:
				return False
			if not equals(expre1[key], expre2[key]):
				return False
	elif t == types.ListType:
		if len(expre1) != len(expre2):
			return False
		for i in range(len(expre1)):
			if not equals(expre1[i], expre2[i]):
				return False
	else:
		print t
		assert False, "unrecognized type" 
	return True	

