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

def normal_variables_for_tuples(tuples):
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
	for i in range(len(tuples)):
		tmp = tuples[i].split()
		for j in range(len(tmp)):
			idx = match(tmp[j])
			if idx != -1:
				if tmp[j] in vl[idx]:
					tmp[j] = starts[idx] + str(vl[idx].index(tmp[j]) + 1)
				else:
					vl[idx].append(tmp[j])
					tmp[j] = starts[idx] + str(len(vl[idx]))
		tuples[i] = " ".join(tmp)

def normal_variables_for_tuples2(tuples):
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
	for i in range(len(tuples)):
		tmp = tuples[i].split()
		for j in range(len(tmp)):
			idx = match(tmp[j])
			if idx != -1:
				if tmp[j] in vl[idx]:
					if idx == 0:
						tmp[j] = starts[idx] + str(vl[idx].index(tmp[j]))
					else:
						tmp[j] = starts[idx] + str(vl[idx].index(tmp[j])+1)
				else:
					vl[idx].append(tmp[j])
					if idx == 0:
						tmp[j] = starts[idx] + str(len(vl[idx]) - 1)
					else:
						tmp[j] = starts[idx] + str(len(vl[idx]))
					
		tuples[i] = " ".join(tmp)

def normal_variables_for_trees(trees):
	ps = []
	starts = ["X", "E", "S"]
	for start in starts:
		ps.append(re.compile("^"+start+"[0-9]+?$"))

	pp = re.compile("^P[0-9]+?$")
	pk = re.compile("^K[0-9]+?$")
	pv = []
	kv = []
	
	pp_c = re.compile("^P[0-9]+\($")
	pk_c = re.compile("^K[0-9]+\($")
	pcv = []
	kcv = []
	for i in range(len(trees)):
		if pp_c.match(trees[i]) and (trees[i] not in pcv):
			pcv.append(trees[i])
			pv.append(trees[i][:-1])
		if pk_c.match(trees[i]) and (trees[i] not in kcv):
			kcv.append(trees[i])
			kv.append(trees[i][:-1])

	vl = [[] for i in range(3)]
	def match(a):
		for i in range(3):
			if ps[i].match(a):
				return i
		return -1
	for i in range(len(trees)):
		idx = match(trees[i])
		if idx != -1:
			if trees[i] in vl[idx]:
				trees[i] = starts[idx] + str(vl[idx].index(trees[i]) + 1)
			else:
				vl[idx].append(trees[i])
				trees[i] = starts[idx] + str(len(vl[idx]))
		elif pp_c.match(trees[i]):
			trees[i] = "P"+str(pcv.index(trees[i])+1)+"("
		elif pk_c.match(trees[i]):
			trees[i] = "K"+str(kcv.index(trees[i])+1)+"("
		elif pp.match(trees[i]):
			trees[i] = "P"+str(pv.index(trees[i])+1)
		elif pk.match(trees[i]):
			trees[i] = "K"+str(kv.index(trees[i])+1)

def redundent_ref(L):
	variable = []
	for tuples in L:
		tuples = tuples.split()
		if tuples[1] == "REF":
			continue
		for tup in tuples[2:]:
			if tup not in variable:
				variable.append(tup)

	new_L = []
	for tuples in L:
		tuples = tuples.split()
		if tuples[1] == "REF" and tuples[-1] not in variable:
			continue
		else:
			new_L.append(" ".join(tuples))
	return new_L


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







