#!- encoding: utf-8 -
import os
import sys
import xml.etree.ElementTree as ET
import re
import types

def argument(arg, child):
	if re.match("^[xestpk][0-9]+$",arg):
		return arg.upper()
	elif arg in ["speaker", "hearer", "now"]:
		return "\""+arg+"\""
	else:

		f = int(child.attrib["from"])
		t = int(child.attrib["to"])
		if f >= t:
			return "\""+arg+"\""
		for token in tokens:
			for tok in token:
				if int(tok["from"]) == f and int(tok["to"]) == t: #and arg == tok["sym"]:
					return tok["wid"]+" ["+arg+"]"
		assert False, "not legal aligns"


def logic_relations(parent):
	assert parent.tag == "relations", "function relations errors"

	for child in parent:
		logic.append(child.attrib["sym"].upper()+"( "+"K"+child.attrib["arg1"].upper()[1:]+" "+"K"+child.attrib["arg2"].upper()[1:]+" )")

def logic_constituent(parent):
	assert parent.tag == "constituent"

	logic.append("K"+parent.attrib["label"].upper()[1:]+"(")
	
	for child in parent:
		if child.tag == "sdrs":
			logic_sdrs(child)
		elif child.tag == "drs":
			logic_drs(child)
		else:
			assert False, "constituent confused"

	logic.append(")")

def logic_sub(parent):
	assert parent.tag == "sub"

	for child in parent:
		if child.tag == "constituent":
			logic_constituent(child)
		else:
			assert False, "sub confused"

def logic_constituents(parent):
	assert parent.tag == "constituents"

	for child in parent:
		if child.tag == "sub":
			logic_sub(child)
		elif child.tag == "constituent":
			logic_constituent(child)
		else:
			assert False, "constituents confused"

def logic_sdrs(parent):
	assert parent.tag == "sdrs"
	assert len(parent) == 2

	logic.append("SDRS(")
	logic_constituents(parent[0])
	logic_relations(parent[1])
	logic.append(")")

def logic_prev(parent, tag, p):
	if tag == "prop":
		logic.append(parent.attrib["argument"].upper()+"(")
	elif tag == "not" or tag == "nec" or tag == "pos" or tag == "imp" or tag == "or":
		logic.append(tag.upper()+"(")
	elif tag == "duplex":
		logic.append("DUP"+"(")
	else:
		assert False, "prev errors"

	logic.append(p[:-1])
	for child in parent:
		if child.tag == "sdrs":
			logic_sdrs(child)
		elif child.tag == "drs":
			logic_drs(child)
		elif child.tag == "indexlist":
			pass
		else:
			assert False, "prev confused"

	logic.append(")")

def getName(parent):
	f = int(parent.attrib["from"])
	t = int(parent.attrib["to"])
	assert f < t

	for token in tokens:
		for tok in token:
			if int(tok["from"]) == f and int(tok["to"]) == t and parent.attrib["symbol"] == tok["sym"]:
				return tok["wid"]
	assert False, "not found named aligns"

def getPred(parent):
	f = int(parent.attrib["from"])
	t = int(parent.attrib["to"])
	if f >= t:
		return ""

	#print tokens

	#tok["sym"] is break~up
	#parent.attrib["symbol"] is break_up

	#No ~ or - 
	for token in tokens:
		for tok in token:
			if "~" in tok["tok"] or "-" in tok["tok"]:
				continue
			if int(tok["from"]) == f and int(tok["to"]) == t and parent.attrib["symbol"] == tok["sym"]:
					assert len(tok["wid"].split()) == 1
					return [[tok["wid"],parent.attrib["symbol"]]]

	#only ~
	for token in tokens:
		for tok in token:
			if "~" not in tok["tok"]:
				continue
			if "-" in tok["tok"]:
				continue
			
			if int(tok["from"]) == f and int(tok["to"]) == t and tok["sym"] in [parent.attrib["symbol"].replace("_","~"), parent.attrib["symbol"].replace("-","~"), parent.attrib["symbol"]]:
				if len(tok["tok"].split("~")) == len(parent.attrib["symbol"].split("_")):
					return zip(tok["wid"].split(), parent.attrib["symbol"].split("_"))
				#special case: some synnet connected with "~" not "_"
				if len(tok["tok"].split("~")) == len(parent.attrib["symbol"].split("~")):
					return zip(tok["wid"].split(), parent.attrib["symbol"].split("~"))
				#special case: some synnect connected with "-" not "_"
				if len(tok["tok"].split("~")) == len(parent.attrib["symbol"].split("-")):
					return zip(tok["wid"].split(), parent.attrib["symbol"].split("-"))
	#only -
	for token in tokens:
		for tok in token:
			if "~" in tok["tok"]:
				continue
			if "-" not in tok["tok"]:
				continue
			if int(tok["from"]) == f and int(tok["to"]) == t and tok["sym"] in [parent.attrib["symbol"].replace("_","~"), parent.attrib["symbol"].replace("-","~"), parent.attrib["symbol"]]:
				if len(tok["tok"].split("-")) == len(parent.attrib["symbol"].split("_")):
					assert len(tok["wid"].split()) == 1
					return [[tok["wid"], parent.attrib["symbol"]]]
				if len(tok["tok"].split("-")) == len(parent.attrib["symbol"].split("-")):
					assert len(tok["wid"].split()) == 1
					return [[tok["wid"], parent.attrib["symbol"]]]
	#both - and ~
	for token in tokens:
		for tok in token:
			if "~" not in tok["tok"] and "-" not in tok["tok"]:
				pass
			if int(tok["from"]) == f and int(tok["to"]) == t and parent.attrib["symbol"] == tok["sym"].replace("~","_"):

				if len(re.split("~|-", tok["tok"])) == len(parent.attrib["symbol"].split("_")):
					assert len(tok["tok"].split("~")) == len(tok["wid"].split())
					res = []
					wid = tok["wid"].split()
					i = 0
					sym = parent.attrib["symbol"].split("_")
					j = 1
					pj = 0
					for t in tok["tok"]:
						if t == "~":
							res.append([wid[i], "_".join(sym[pj:j])])
							i += 1
							pj = j
						if t == "-":
							j += 1
					res.append([wid[i], "_".join(sym[pj:])])
					return res
				#special case: some synnect connected with "-" not "_"
				if len(re.split("~", tok["tok"])) == len(re.split("_", parent.attrib["symbol"])):
					assert len(tok["tok"].split("~")) == len(tok["wid"].split())
					return zip(tok["wid"].split("~"), parent.attrib["symbol"].split("_"))


	#skip
	#No ~ or - 
	i = 0
	j = 0
	while i < len(tokens):
		j = 0
		while j < len(tokens[i]):
			tok = tokens[i][j]
			if "~" in tok["tok"] or "-" in tok["tok"]:
				j += 1
				continue
			if int(tok["from"]) == f and int(tok["to"]) == t and tok["sym"] in [parent.attrib["symbol"].replace("_","~")]:
				sym = tok["sym"]
				break
			j += 1
		if j != len(tokens[i]):
			break
		i += 1

	if i != len(tokens):
		sym = sym.split("~")
		res = [[tokens[i][j]["wid"], sym[0]]]
		k = 1
		j += 1
		while j < len(tokens[i]) and k < len(sym):
			tok = tokens[i][j]
			if tok["sym"] == sym[k]:
				res.append([tok["wid"], sym[k]])
				k += 1
			j += 1
		if k == len(sym):
			return res

	return ""
	"""
	i = 0
	j = 0
	sym = ""
	while i < len(tokens):
		j = 0
		while j < len(tokens[i]):
			tok = tokens[i][j]
			if int(tok["from"]) == f and int(tok["to"]) == t and tok["sym"].replace("~","_") == parent.attrib["symbol"]:
				sym = tok["sym"]
				break
			j += 1
		if j != len(tokens[i]):
			break
		i += 1

	if i == len(tokens):
		return ""

	sym = sym.split("~")
	#print sym
	#print tokens[i]
	re = [[tokens[i][j]["wid"], sym[0]]]
	k = 1
	while j < len(tokens[i]) and k < len(sym):
		tok = tokens[i][j]
		if tok["sym"] == sym[k]:
			re.append([tok["wid"], sym[k]])
			k += 1
		j += 1
	assert k == len(sym)
	return re
	"""


def getRel(parent):
	f = int(parent.attrib["from"])
	t = int(parent.attrib["to"])

	for token in tokens:
		for tok in token:
			if int(tok["from"]) == f and int(tok["to"]) == t and parent.attrib["symbol"] == tok["sym"]:
				return tok["wid"]
	return ""

def getPointer(pointer):
	#print box_stack
	if pointer != box_stack[-1]:
		return pointer.upper()+" "
	else:
		return "B0 "

def logic_cond(parent):
	assert parent.tag == "cond"

	child = parent[0]
	p = getPointer(parent.attrib["label"])
	if child.tag == "named":
		index = getName(child)
		assert index != -1
		tag = "Named("
		logic.append(tag+" "+p+" "+argument(child.attrib["arg"], child)+" "+index+" ["+child.attrib["symbol"]+"]"+" )")

	elif child.tag == "pred":
		sense = ".".join(child.attrib["synset"].split(".")[-2:])
		symbol = ".".join(child.attrib["synset"].split(".")[:-2])
		assert symbol == child.attrib["symbol"]

		index = getPred(child)
		if type(index) == types.ListType:
			for idx in index:
				logic.append(idx[0]+"["+idx[1]+"]"+"( "+p+argument(child.attrib["arg"], child)+" "+sense+" )")
		elif index == "":
			logic.append(child.attrib["symbol"]+"( "+p+argument(child.attrib["arg"], child)+" "+sense+" )")
		else:
			assert False, "unrecoginzed"

	elif child.tag == "comp":
		logic.append("comp_"+child.attrib["symbol"]+"( "+p+argument(child.attrib["arg1"], child)+" "+argument(child.attrib["arg2"], child)+" )")
	
	elif child.tag == "rel":
		rel = child.attrib["symbol"]
		index = getRel(child)
		if index == "":
			logic.append(rel+"( "+p+argument(child.attrib["arg1"], child)+ " "+ argument(child.attrib["arg2"], child)+" )")
		else:
			logic.append(index+"["+rel+"]"+"( "+p+argument(child.attrib["arg1"], child)+ " "+ argument(child.attrib["arg2"], child)+" )")
	elif child.tag == "prop":
		logic_prev(child, "prop", p)
	elif child.tag == "not":
		logic_prev(child, "not", p)
	elif child.tag == "pos":
		logic_prev(child, "pos", p)
	elif child.tag == "nec":
		logic_prev(child, "nec", p)
	elif child.tag == "duplex":
		logic_prev(child, "duplex", p)
	elif child.tag == "or":
		logic_prev(child, "or", p)
	elif child.tag == "imp":
		logic_prev(child, "imp", p)
	else:
		assert False, "cond confused"

def logic_conds(parent):
	assert parent.tag == "conds"

	for child in parent:
		if child.tag == "cond":
			logic_cond(child)
		else:
			assert False, "conds confused"

def get_sentidx(f, t):
	i = 1
	while i < len(boundary):
		if t <= boundary[i] and f >= boundary[i-1]:
			return i
		i += 1
	assert False, "cross sentences"

box_stack = []
def logic_drs(parent):
	assert parent.tag == "drs"


	indexs = []
	def aligns(parent):
		if "from" in parent.attrib and "to" in parent.attrib:
			if int(parent.attrib["from"]) < int(parent.attrib["to"]):
				indexs.append(get_sentidx(int(parent.attrib["from"]), int(parent.attrib["to"])))
		for child in parent:
			aligns(child)
	aligns(parent)

	global cur_index, prev_index
	for i in range(len(indexs)-1):
		if indexs[i] != indexs[i+1]:
			print indexs
		assert indexs[i] == indexs[i+1]
		i += 1	

	if len(indexs) == 0:
		logic.append("DRS-"+str(prev_index-1)+"(")
		cur_index = prev_index - 1
	else:
		if prev_index+1 == indexs[0]:
			logic.append("DRS-"+str(prev_index)+"(")
			cur_index = prev_index
		elif prev_index == indexs[0]:
			logic.append("DRS-"+str(prev_index-1)+"(")
			cur_index = prev_index - 1
		else:
			assert False, "indexs are not continued"
		prev_index = indexs[0]
		#logic.append("DRS-"+indexs[0][0:-3]+"(")

	box_stack.append(parent.attrib["label"])
	for child in parent:
		if child.tag == "domain":
			pass
		elif child.tag == "conds":
			logic_conds(child)
		elif child.tag == "tokens":
			pass
		elif child.tag == "taggedtokens":
			pass
		else:
			assert False, "drs confused"

	logic.append(")")
	box_stack.pop()

def out_tokens(parent):

	tokens = []
	sent_idx = int(parent[0].attrib['{http://www.w3.org/XML/1998/namespace}id'][1:-3])-1
	tok_idx = 1
	for child in parent:
		if int(child.attrib['{http://www.w3.org/XML/1998/namespace}id'][1:-3]) == sent_idx:
			pass
		elif int(child.attrib['{http://www.w3.org/XML/1998/namespace}id'][1:-3]) > sent_idx:
			sent_idx = int(child.attrib['{http://www.w3.org/XML/1998/namespace}id'][1:-3])
			tok_idx = 1
			tokens.append([])
		else:
			assert False, "No continuouse sentences"

		for cc in child:
			tmp = {}
			for ccc in cc:
				tmp[ccc.attrib["type"]] = ccc.text

			if tmp["tok"].encode("utf-8") == "ø":
				pass
			else:
				tok = tmp["tok"].split("~")
				tmp["sid"] = sent_idx
				tmp["wid"] = " ".join(["$"+str(tok_idx+i-1) for i in range(len(tok))])
				tok_idx += len(tok)
				tokens[-1].append(tmp)
	return tokens

def normalized_p(tree):
	p = 1000
	v = []
	for i in range(len(tree)):
		if re.match("^[XEST][0-9]+\($", tree[i]):
			if tree[i][:-1] not in v:
				v.append(tree[i][:-1])

	for i in range(len(tree)):
		if re.match("^[XEST][0-9]+\($", tree[i]) and tree[i][:-1] in v:
			idx = v.index(tree[i][:-1])
			tree[i] = "P"+str(p+idx)+"("
		elif re.match("^[XEST][0-9]+$", tree[i]) and tree[i] in v:
			idx = v.index(tree[i])
			tree[i] = "P"+str(p+idx)

def normalized_index(tree):
	v = ["X", "S", "E", "P", "K", "T", "B"]
	c = [ [] for i in range(7)]

	#preprocess pointer for scope, because it will be predicted in the first stage.
	for i in range(len(tree)):
		if re.match("^P[0-9]+\($", tree[i]) or (tree[i] in ["NOT(", "NEC(", "POS(", "DUP(", "IMP(", "OR("]):
			if (tree[i+1] not in c[6]) and (tree[i+1] != "B0"):
				c[6].append(tree[i+1])
	for i in range(len(tree)):
		if tree[i] == "B0":
			continue
		if re.match("^[XESTPKB][0-9]+$",tree[i]):
			idx = v.index(tree[i][0])
			if tree[i] not in c[idx]:
				c[idx].append(tree[i])
		if re.match("^[PK][0-9]+\($", tree[i]):
			idx = v.index(tree[i][0])
			if tree[i][:-1] not in c[idx]:
				c[idx].append(tree[i][:-1])

	for i in range(len(tree)):
		if tree[i] == "B0":
			continue
		if re.match("^[XESTPKB][0-9]+$",tree[i]):
			idx = v.index(tree[i][0])
			assert tree[i] in c[idx]
			iidx = c[idx].index(tree[i])
			tree[i] = v[idx] + str(iidx+1)
		if re.match("^[XESTPKB][0-9]+\($",tree[i]):
			idx = v.index(tree[i][0])
			assert tree[i][:-1] in c[idx]
			iidx = c[idx].index(tree[i][:-1])
			tree[i] = v[idx] + str(iidx+1) + "("

def xmlReader(filename, head):
	tree = ET.parse(filename)
	root = tree.getroot()[0]

	taggedtokens = root[0]
	drs = root[1]

	

	global tokens
	tokens = out_tokens(taggedtokens)
	#print tokens
	global boundary
	boundary = [-1]
	for token in tokens:
		boundary.append(-1)
		for tok in token:
			if int(tok["from"]) < int(tok["to"]):
				boundary[-1] = max(int(tok["to"]), boundary[-1])
		if len(boundary) >= 2:
			assert boundary[-1] > boundary[-2], "illegal sentence boudary"
	global cur_index, prev_index
	cur_index = -1
	prev_index = 1

	global logic
	logic = []
	if drs.tag == "drs":
		logic_drs(drs)
	else:
		logic_sdrs(drs)
	

	print head
	for token in tokens:
		print " ".join([" ".join(tok["tok"].split("~")) for tok in token]).encode("UTF-8")
	print "TREE"
	tree = " ".join(logic).encode("UTF-8")
	tree = tree.split()
	normalized_p(tree)
	normalized_index(tree)
	print " ".join(tree)
	print 
	
	




if __name__ == "__main__":
	head = "### "+" ".join(sys.argv)
	xmlReader(sys.argv[1], head)
#if __name__ == "__main__":
#	for (path, dirs, files) in os.walk(sys.argv[1]):
#		if len(files) != 0:
#			print path
#			tokens = []
#			out = open(path+"/sentence.logic", "w")
#			xmlReader(path+"/sentence.drs.xml.notime.index_normalized",out)
#			out.close()
