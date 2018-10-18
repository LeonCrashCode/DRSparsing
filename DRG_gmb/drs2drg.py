import sys
import os
import xml.etree.ElementTree as ET
import re

pr = re.compile("^p[0-9]+?$")
br = re.compile("^b[0-9]+?$")
### add projection to sdrs
sdrs_p = 1000
def add_pointer(parent):
	global sdrs_p
	if parent.tag == "sdrs":
		parent.set("label", "b"+str(sdrs_p))
		sdrs_p += 1
	for child in parent:
		add_pointer(child)
### get mapping from k to b
k2b = {}
def get_k2b(parent):
	if parent.tag == "constituent":
		assert len(parent) == 1
		k = parent.attrib["label"]
		assert k not in k2b
		k2b[k] = parent[0].attrib["label"]
	for child in parent:
		get_k2b(child)

projection = {}
def get_projectoin(parent):
	if parent.tag == "dr":
		name = parent.attrib["name"]
		label = parent.attrib["label"]
		if name in projection:
			assert projection[name] == label
		else:
			projection[name] = label
	for child in parent:
		get_projectoin(child)
DRS = {}
def get_DRS(parent, prev_label):
	if parent.tag in ["sdrs", "drs"]:
		prev_label = parent.attrib["label"]

	if parent.tag == "drel":
		arg1 = parent.attrib["arg1"]
		arg2 = parent.attrib["arg2"]

		DRS[prev_label+"_"+k2b[arg1]] = 1
		DRS[prev_label+"_"+k2b[arg2]] = 1
	for child in parent:
		get_DRS(child,prev_label)
### normalize common variables to p
def normal_p(parent):

	p_list = []
	def travel(p):
		if p.tag == "prop":
			a1 = p.attrib["argument"]
			if (a1 not in p_list) and (not pr.match(a1)):
				p_list.append(a1)
		for c in p:
			travel(c)

	travel(parent)

	p_id = [1000]
	def travel2(p):
		if p.tag == "dr" and (p.attrib["name"] in p_list):
			p.attrib["name"] = "p" + str(p_id[0] + p_list.index(p.attrib["name"]))
		if ("arg" in p.attrib) and (p.attrib["arg"] in p_list):
			p.attrib["arg"] = "p" + str(p_id[0] + p_list.index(p.attrib["arg"]))
		if ("arg1" in p.attrib) and (p.attrib["arg1"] in p_list):
			p.attrib["arg1"] = "p" + str(p_id[0] + p_list.index(p.attrib["arg1"]))
		if ("arg2" in p.attrib) and (p.attrib["arg2"] in p_list):
			p.attrib["arg2"] = "p" + str(p_id[0] + p_list.index(p.attrib["arg2"]))
		if ("argument" in p.attrib) and (p.attrib["argument"] in p_list):
			p.attrib["argument"] = "p" + str(p_id[0] + p_list.index(p.attrib["argument"]))
		for c in p:
			travel2(c)
	travel2(parent)



sense = int(sys.argv[2])
tuples = []
d_id = 0
v_id = 0
r_id = 0
o_id = 0
assign = {}

def sdrs(parent, prev_label):
	global DRS
	if prev_label != "":
		key = prev_label+"_"+parent.attrib["label"]
		if (key in DRS) and DRS[key] == 1:
			tuples.append([prev_label, "DRS", parent.attrib["label"]])
			DRS[key] = 0
	for child in parent:
		if child.tag == "constituents":
			constituents(child, parent.attrib["label"])
		elif child.tag == "relations":
			relations(child, parent.attrib["label"])
		else:
			assert False, "unrecognized child in sdrs"
def constituents(parent, prev_label):
	for child in parent:
		if child.tag == "constituent":
			constituent(child, prev_label)
		elif child.tag == "sub":
			sub(child, prev_label)
		else:
			assert False, "unrecognized child in constituents"
def relations(parent, prev_label):
	for child in parent:
		if child.tag == "drel":
			drel(child, prev_label)
		else:
			assert False, "unrecognized child in relations"
def drel(parent, prev_label):
	global d_id
	arg1 = parent.attrib["arg1"]
	arg2 = parent.attrib["arg2"]
	symbol = parent.attrib["sym"]
	tuples.append([prev_label, symbol.upper(), "d"+str(d_id)])
	tuples.append(["d"+str(d_id), "ARG0", k2b[arg1]])
	tuples.append(["d"+str(d_id), "ARG1", k2b[arg2]])
	d_id += 1
def constituent(parent, prev_label):
	assert len(parent) == 1, "unrecognized child in constituent"
	for child in parent:
		if child.tag == "drs":
			drs(child, prev_label)
		elif child.tag == "sdrs":
			sdrs(child, prev_label)
		else:
			assert False, "unrecognized child in constituent"
def sub(parent, prev_label):
	for child in parent:
		#if child.tag == "sdrs":
		#	sdrs(child, prev_label)
		#elif child.tag == "drs":
		#	drs(child, prev_label)
		if child.tag == "constituent":
			constituent(child, prev_label)
		else:
			assert False, "unrecognized child in sub"
def drs(parent, prev_label):
	if prev_label != "":
		assert br.match(parent.attrib["label"])
		key = prev_label+"_"+parent.attrib["label"]
		if (key in DRS) and DRS[key] == 1:
			tuples.append([prev_label, "DRS", parent.attrib["label"]])
			DRS[key] = 0
	for child in parent:
		if child.tag == "tokens":
			pass
		elif child.tag == "domain":
			pass
		elif child.tag == "conds":
			conds(child, parent.attrib["label"])
		else:
			assert False, "unrecognized child in drs"
def conds(parent, prev_label):
	for child in parent:
		if child.tag == "cond":
			cond(child, prev_label)
		else:
			assert False, "unrecognized child in conds"
def cond(parent, prev_label):
	for child in parent:
		if child.tag == "named":
			named(child, prev_label, parent.attrib["label"])
		elif child.tag == "pred":
			pred(child, prev_label, parent.attrib["label"])
		elif child.tag == "rel":
			rel(child, prev_label, parent.attrib["label"])
		elif child.tag == "prop":
			prop(child, prev_label, parent.attrib["label"])
		elif child.tag in ["not", "pos", "nec"]:
			single(child, prev_label, parent.attrib["label"])
		elif child.tag in ["imp", "or", "duplex"]:
			couple(child, prev_label, parent.attrib["label"])
def named(parent, prev_label, cond_label):
	global r_id
	arg = parent.attrib["arg"]
	symbol = parent.attrib["symbol"]
	if arg not in assign:
		tuples.append([projection[arg], "REF", arg])
		assign[arg] = 1
	tuples.append([cond_label, "Named", "r"+str(r_id)])
	tuples.append(["r"+str(r_id), "ARG0", arg])
	tuples.append(["r"+str(r_id), "ARG1", "\""+symbol+"\""])
	r_id += 1

def pred(parent, prev_label, cond_label):
	global r_id
	arg = parent.attrib["arg"]
	symbol = parent.attrib["symbol"]
	typ = parent.attrib["type"]
	sen = parent.attrib["sense"]
	if len(sen) == 1:
		sen = "0" + sen
	if arg not in assign:
		tuples.append([projection[arg], "REF", arg])
		assign[arg] = 1
	tuples.append([cond_label, "Pred", "r"+str(r_id)])
	tuples.append(["r"+str(r_id), "ARG0", arg])
	if sense:
		tuples.append(["r"+str(r_id), "ARG1", "\""+symbol+"\"."+typ+"."+sen])
	else:
		tuples.append(["r"+str(r_id), "ARG1", "\""+symbol+"\""])
	r_id += 1
def rel(parent, prev_label, cond_label):
	global r_id
	arg1 = parent.attrib["arg1"]
	arg2 = parent.attrib["arg2"]
	symbol = parent.attrib["symbol"]
	if arg1 not in assign:
		tuples.append([projection[arg1], "REF", arg1])
		assign[arg1] = 1
	if arg2 not in assign:
		tuples.append([projection[arg2], "REF", arg2])
		assign[arg2] = 1
	tuples.append([cond_label, symbol, "r"+str(r_id)])
	tuples.append(["r"+str(r_id), "ARG0", arg1])
	tuples.append(["r"+str(r_id), "ARG1", arg2])
	r_id += 1
def prop(parent, prev_label, cond_label):
	global o_id
	arg1 = parent.attrib["argument"]
	if arg1 not in assign:
		tuples.append([projection[arg1], "REF", arg1])
		assign[arg1] = 1
	assert len(parent) == 2, "unrecognized child in prop"
	arg2 = parent[1].attrib["label"]
	tuples.append([cond_label, "PRP", "o"+str(o_id)])
	tuples.append(["o"+str(o_id), "ARG0", arg1])
	tuples.append(["o"+str(o_id), "ARG1", arg2])
	o_id += 1
	for child in parent:
		if child.tag == "indexlist":
			pass
		elif child.tag == "drs":
			drs(child, prev_label)
		elif child.tag == "sdrs":
			sdrs(child, prev_label)
		else:
			assert False, "unrecognized child in prop"
def single(parent, prev_label, cond_label):
	assert len(parent) == 2, "unrecognized child in single"
	tuples.append([cond_label, parent.tag.upper(), parent[1].attrib["label"]])
	for child in parent:
		if child.tag == "indexlist":
			pass
		elif child.tag == "drs":
			drs(child, prev_label)
		elif child.tag == "sdrs":
			sdrs(child, prev_label)
		else:
			assert False, "unrecognized child in single"
def couple(parent, prev_label, cond_label):
	global v_id
	assert len(parent) == 3, "unrecognized child in couple"
	arg1 = parent[1].attrib["label"]
	arg2 = parent[2].attrib["label"]
	tuples.append([cond_label, parent.tag.upper(), "v"+str(v_id)])
	tuples.append(["v"+str(v_id), "ARG0", arg1])
	tuples.append(["v"+str(v_id), "ARG1", arg2])
	v_id += 1
	for child in parent:
		if child.tag == "indexlist":
			pass
		elif child.tag == "drs":
			drs(child, prev_label)
		elif child.tag == "sdrs":
			sdrs(child, prev_label)
		else:
			assert False, "unrecognized child in couple"

def normal_variables(lines):

	start_v = ["b", "x", "e", "s", "t", "p", "v", "o", "r", "d"]
	any_p = []
	stack_v = [ [] for i in range(10)]
	for v in start_v:
		any_p.append(re.compile("^"+v+"[0-9]+?$"))

	def is_common_var(v):
		for p in any_p:
			if p.match(v):
				return True
		return False

	def index(v):
		for i in range(len(any_p)):
			if any_p[i].match(v):
				return i
		return -1

	def norm(v):
		if not is_common_var(v):
			return v
		idx = index(v)
		if idx == -1:
			print v
		assert idx != -1
		if v in stack_v[idx]:
			return start_v[idx]+str(stack_v[idx].index(v))
		else:
			stack_v[idx].append(v)
			return start_v[idx]+str(len(stack_v[idx]) - 1)
	
	for i in range(len(lines)):
		assert len(lines[i]) >= 3
		lines[i][0] = norm(lines[i][0])
		lines[i][2] = norm(lines[i][2])


def drg(parent):
	normal_p(parent)
	add_pointer(parent)
	get_k2b(parent)
	get_projectoin(parent)
	get_DRS(parent, "")

	if parent.tag == "sdrs":
		sdrs(parent, prev_label = "")
	elif parent.tag == "drs":
		drs(parent,prev_label = "")
	else:
		assert False, "unrecognized child in drg"

	normal_variables(tuples)
	print "Graph"
	for t in tuples:
		print " ".join(t).encode("utf8")
	print

	global DRS
	for key in DRS.keys():
		assert DRS[key] == 0
def taggedtokens(parent):
	def get_value(parent, t):
		for child in parent:
			if child.attrib["type"] == t:
				return child.text
	doc = []
	lem = []
	prev_idx = -1
	for child in parent:
		idx = int(child.attrib["{http://www.w3.org/XML/1998/namespace}id"][1:-3])-1
		if idx != prev_idx:
			doc.append([])
			lem.append([])
			prev_idx = idx
		doc[-1].append(get_value(child[0], "tok"))
		lem[-1].append(get_value(child[0], "lemma"))

	assert len(doc) == len(lem)
	for d, l in zip(doc, lem):
		print " ".join(d).encode("utf8")
		print " ".join(l).encode("utf8")

#for root, dirs, files in os.walk("data"):
#	if len(root.split("/")) != 3:
#		continue
if __name__ == "__main__":
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	print "###", " ".join(sys.argv)
	taggedtokens(root[0][0])
	drg(root[0][1])

