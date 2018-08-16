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
		print type(expre1)
		print type(expre2)
		return False
	t = type(expre1)
	if t == types.NoneType:
		if expre1 != expre2:
			print expre1
			print expre2
			return False
	elif t == types.StringType or t == types.UnicodeType or t == types.IntType:
		if expre1 != expre2:
			print expre1
			print expre2
			return False
	elif t == types.DictType:
		if len(expre1) != len(expre2):
			print expre1
			print expre2
			return False
		for key in expre1.keys():
			if key not in expre2:
				print expre1
				print expre2
				return False
			if not equals(expre1[key], expre2[key]):
				return False
	elif t == types.ListType:
		if len(expre1) != len(expre2):
			print expre1
			print expre2
			return False
		for i in range(len(expre1)):
			if not equals(expre1[i], expre2[i]):
				return False
	else:
		print t
		assert False, "unrecognized type" 
	return True	

import re

def normal_variables(node, start="v"):
	p = re.compile("^v[0-9]+?$")
	vl = []
	def normal(a):
		assert type(a) == types.StringType or type(a) == types.UnicodeType
		if p.match(a):
			if a in vl:
				return start + str(vl.index(a) + 1)
			else:
				vl.append(a)
				return start + str(len(vl)) 
		return a
	def normalization(node):
		node.text = normal(node.text)
		for k in node.attrib.keys():
			node.attrib[k] = normal(node.attrib[k])
		for i in range(len(node.expression)):
			node.expression[i] = normalization(node.expression[i])
		return node
	return normalization(node)