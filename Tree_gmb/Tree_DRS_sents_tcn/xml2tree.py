import os
import sys
import xml.etree.ElementTree as ET
import re

"""
Remain time informations, Timex(x1, TIME_NUMBER) --> Timex(x1, Junary 1 2019)
Remain number information, Card(x1, CARD_NUMBER) --> Card(x1, 510 millions)
Distinguish name and predicate, john(x1) --> Named(x1, john)
Consider predicate sense, eat(e1) --> eat(e1, v.01)
"""
def logic_relations(parent):
	assert parent.tag == "relations", "function relations errors"

	for child in parent:
		logic.append(child.attrib["sym"].upper()+"( "+child.attrib["arg1"].upper()+" "+child.attrib["arg2"].upper()+" )")

def logic_constituent(parent):
	assert parent.tag == "constituent"

	logic.append(parent.attrib["label"].upper()+"(")
	
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

def logic_prev(parent, tag):
	if tag == "prop":
		logic.append(parent.attrib["argument"].upper()+"(")
	elif tag == "not" or tag == "nec" or tag == "pos" or tag == "imp" or tag == "or":
		logic.append(tag.upper()+"(")
	elif tag == "duplex":
		logic.append("DUP"+"(")
	else:
		assert False, "prev errors"

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

lemmas = []
def getValue(parent):
	global lemmas
	child = parent[0]
	
	l = []
	for cc in child:
		pos = int(cc.attrib["pos"])
		l.append(lemmas[pos-1])
	assert len(l) > 0
	return " ".join(l)
def logic_cond(parent):
	assert parent.tag == "cond"

	child = parent[0]
	if child.tag == "named":
		logic.append("Named( "+child.attrib["arg"].upper() + " " + child.attrib["symbol"]+" )")
	elif child.tag == "pred":
		sense = child.attrib["sense"]
		if len(sense) == 1:
			sense = "0"+sense
		assert len(sense) == 2
		logic.append(child.attrib["symbol"]+"( "+child.attrib["arg"].upper()+ " " + child.attrib["type"]+"."+sense+" )")
	elif child.tag == "card":
		value = getValue(child)
		logic.append("Card( "+child.attrib["arg"].upper() + " " + value +" )")
	elif child.tag == "timex":
		value = getValue(child)
		logic.append("Timex( "+child.attrib["arg"].upper() + " " + value +" )")
	
	elif child.tag == "eq":
		logic.append("Equ( "+child.attrib["arg1"].upper() + " "+child.attrib["arg2"].upper()+" )")
	elif child.tag == "rel":
		rel = child.attrib["symbol"]
		logic.append(rel[0].upper()+rel[1:]+"( "+child.attrib["arg1"].upper() + " "+ child.attrib["arg2"].upper()+" )")

	elif child.tag == "prop":
		logic_prev(child, "prop")
	elif child.tag == "not":
		logic_prev(child, "not")
	elif child.tag == "pos":
		logic_prev(child, "pos")
	elif child.tag == "nec":
		logic_prev(child, "nec")
	elif child.tag == "duplex":
		logic_prev(child, "duplex")
	elif child.tag == "or":
		logic_prev(child, "or")
	elif child.tag == "imp":
		logic_prev(child, "imp")

	else:
		assert False, "cond confused"

def logic_conds(parent):
	assert parent.tag == "conds"

	for child in parent:
		if child.tag == "cond":
			logic_cond(child)
		else:
			assert False, "conds confused"

def logic_drs(parent):
	assert parent.tag == "drs"

	logic.append("DRS(")

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

def out_tokens(parent):
	tokens = []
	for child in parent:
		if child.tag == "taggedtokens":
			for cc in child:
					tmp = {}
					for ccc in cc:
						if ccc.attrib["type"] == "tok":
							tmp["tok"] = ccc.text
						elif ccc.attrib["type"] == "lemma":
							tmp["lemma"] = ccc.text
					tokens.append(tmp["tok"]+" "+tmp["lemma"])
			break
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
	v = ["X", "S", "E", "P", "K", "T"]
	c = [ [] for i in range(6)]


	for i in range(len(tree)):
		if re.match("^[XESTPK][0-9]+$",tree[i]):
			idx = v.index(tree[i][0])
			if tree[i] not in c[idx]:
				c[idx].append(tree[i])
		if re.match("^[PK][0-9]+\($", tree[i]):
			idx = v.index(tree[i][0])
			if tree[i][:-1] not in c[idx]:
				c[idx].append(tree[i][:-1])

	for i in range(len(tree)):
		if re.match("^[XESTPK][0-9]+$",tree[i]):
			idx = v.index(tree[i][0])
			assert tree[i] in c[idx]
			iidx = c[idx].index(tree[i])
			tree[i] = v[idx] + str(iidx+1)
		if re.match("^[XESTPK][0-9]+\($",tree[i]):
			idx = v.index(tree[i][0])
			assert tree[i][:-1] in c[idx]
			iidx = c[idx].index(tree[i][:-1])
			tree[i] = v[idx] + str(iidx+1) + "("

def xmlReader(filename):
	tree = ET.parse(filename)
	root = tree.getroot()


	for child in root:
		#print "sentid",sentid
		global logic
		global lemmas
		logic = []
		tokens = out_tokens(child)
		print " ".join([tok.split()[0] for tok in tokens]).encode("UTF-8")
		print " ".join([tok.split()[1] for tok in tokens]).encode("UTF-8")
		lemmas = [tok.split()[1] for tok in tokens]
		#print ("|||".join(tokens)).encode("UTF-8")
		print "TREE"
		logic_drs(child) # sentence
		tree = " ".join(logic).encode("UTF-8")
		tree = tree.split()
		normalized_p(tree)
		normalized_index(tree)
		print " ".join(tree)
		print 




if __name__ == "__main__":
	print "###", " ".join(sys.argv)
	xmlReader(sys.argv[1])
#if __name__ == "__main__":
#	for (path, dirs, files) in os.walk(sys.argv[1]):
#		if len(files) != 0:
#			print path
#			tokens = []
#			out = open(path+"/sentence.logic", "w")
#			xmlReader(path+"/sentence.drs.xml.notime.index_normalized",out)
#			out.close()
