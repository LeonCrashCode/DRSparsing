import types

def get_index(node):
	index = []
	for subnode in node:
		if subnode.tag == "indexlist":
			for cc in subnode:
				index.append(int(cc.text[1:]))
	if len(index) == 0:
		return []
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

import re

def normal_variables(expre, start="v"):
	p = re.compile("^v[0-9]+?$")
	vl = []
	print expre
	def normalization(expre):
		if type(expre) == types.StringType or type(expre) == types.UnicodeType:
			if p.match(expre):
				if expre in vl:
					return start + str(vl.index(expre) + 1)
				else:
					vl.append(expre)
					return start + str(len(vl))
			else:
				return expre
		elif type(expre) == types.ListType:
			for i in range(len(expre)):
				expre[i] = normalization(expre[i])
			return expre
		elif type(expre) == types.DictType:
			for key in expre.keys():
				expre[key] = normalization(expre[key])
			return expre
		else:
			print type(expre)
			assert False, "unrecognized type"
	return normalization(expre)