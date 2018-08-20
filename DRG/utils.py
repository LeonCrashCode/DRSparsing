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
	elif t == types.StringType or t == types.UnicodeType or t == types.IntType:
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

def normal_variables(node):
	ps = []
	starts = ["b", "x", "e", "s", "t", "p", "k", "v"]
	for start in starts:
		ps.append(re.compile("^"+start+"[0-9]+?$"))

	vl = [[] for i in range(8)]

	def match(a):
		for i in range(8):
			if ps[i].match(a):
				return i
		return -1
	def normal(a):
		assert type(a) == types.StringType or type(a) == types.UnicodeType
		idx = match(a)
		if idx == -1:
			return a
		if a in vl[idx]:
			return starts[idx] + str(vl[idx].index(a) + 1)
		else:
			vl[idx].append(a)
			return starts[idx] + str(len(vl[idx])) 
		return a
	def normalization(node):
		node.text = normal(node.text)
		for k in node.attrib.keys():
			node.attrib[k] = normal(node.attrib[k])
		for i in range(len(node.expression)):
			normalization(node.expression[i])
	normalization(node)
def add_variable(node, v):

	first_node = []
	def travel(node):
		if node.type == "drs" and len(first_node) == 0:
			first_node.append(node)
			return
		if len(first_node) == 1:
			return
		for subnode in node.expression:
			travel(subnode)
	travel(node)
	first_node[0].expression[0].expression.insert(0, v)

def modify_attrib(node, fr, to):

	last_node = []
	last_node_expr_idx = []
	def have_fr(node):
		for key in node.attrib:
			if node.attrib[key] == fr:
				return True
		for subnode in node.expression:
			if have_fr(subnode):
				return True
		return False
	def travel(node):
		for key in node.attrib:
			if node.attrib[key] == fr:
				node.attrib[key] = to

		for idx in range(len(node.expression))[::-1]:
			if node.type in ["lam", "constituent"] and node.expression[idx].type == "drs" and len(last_node) == 0:
				if have_fr(node.expression[idx]):
					last_node.append(node)
					last_node_expr_idx.append(idx)
			travel(node.expression[idx])

	travel(node)
	assert len(last_node) == 1, "last drs node is not found"
	return last_node[0], last_node_expr_idx[0]







