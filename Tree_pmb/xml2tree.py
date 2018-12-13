#!- encoding: utf-8 -
import os
import sys
import xml.etree.ElementTree as ET
import re

logic = []
def argument(arg):
	if re.match("^[xestpk][0-9]+$",arg):
		return arg.upper()
	else:
		return arg


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
def logic_cond(parent):
	assert parent.tag == "cond"

	child = parent[0]
	if child.tag in ["named", "pred"]:
		logic.append(child.attrib["symbol"]+"( "+argument(child.attrib["arg"])+" )")
	
	elif child.tag == "comp":
		logic.append(child.attrib["symbol"].lower()+"( "+argument(child.attrib["arg1"]) + " "+argument(child.attrib["arg2"])+" )")
	elif child.tag == "rel":
		rel = child.attrib["symbol"]
		logic.append(rel[0].upper()+rel[1:]+"( "+argument(child.attrib["arg1"])+ " "+ argument(child.attrib["arg2"])+" )")

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

	logic.append("DRS-0(")

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
		for cc in child:
			tmp = {}
			for ccc in cc:
				if ccc.attrib["type"] == "tok":
					tmp["tok"] = ccc.text
				elif ccc.attrib["type"] == "lemma":
					tmp["lemma"] = ccc.text
			tok = tmp["tok"].split("~")
			lem = tmp["lemma"].split("~")
			if len(tok) > len(lem):
				for t in tok:
					if t.encode("utf-8") == "ø":
						pass
					else:
						tokens.append(t+" "+t.lower())
			elif len(tok) < len(lem):
				for i in range(len(tok)):
					t = tok[i]
					if t.encode("utf-8") == "ø":
						pass
					else:
						tokens.append(t+" "+lem[i].lower())
			else:
				for t, l in zip(tok,lem):
					if t.encode("utf-8") == "ø":
						pass
					else:
						tokens.append(t+" "+l)
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

def xmlReader(filename, head):
	tree = ET.parse(filename)
	root = tree.getroot()[0]

	taggedtokens = root[0]
	drs = root[1]

	global logic 
	tokens = out_tokens(taggedtokens)
	
	

	if drs.tag == "drs":
		logic_drs(drs)
	else:
		logic_sdrs(drs)
		
	print head
	print " ".join([tok.split()[0] for tok in tokens]).encode("UTF-8")
	print " ".join([tok.split()[1] for tok in tokens]).encode("UTF-8")
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
