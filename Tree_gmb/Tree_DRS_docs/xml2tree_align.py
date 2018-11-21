import os
import sys
import xml.etree.ElementTree as ET
import re


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
def logic_cond(parent):
	assert parent.tag == "cond"

	child = parent[0]
	if child.tag in ["named", "pred"]:
		logic.append(child.attrib["symbol"]+"( "+child.attrib["arg"].upper()+" )")
	elif child.tag == "card":
		#logic.append("CARD( "+child.attrib["arg"].upper() + " " + child.attrib["value"]+" )")
		logic.append("Card( "+child.attrib["arg"].upper() + " " + "CARD_NUMBER"+" )")
	elif child.tag == "timex":
		#logic.append("TIMEX( "+child.attrib["arg"].upper() + " " + child[1].text+" )")
		logic.append("Timex( "+child.attrib["arg"].upper() + " " + "TIME_NUMBER"+ " )")
	
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

prev_index = 0
def logic_drs(parent):
	assert parent.tag == "drs"
	indexs = []
	def aligns(parent):
		if parent.tag == "index":
			indexs.append(parent.text)
		for child in parent:
			aligns(child)

	aligns(parent)

	#print indexs
	for i in range(len(indexs)-1):
		if indexs[i][0:-3] != indexs[i+1][0:-3]:
			print indexs
		assert indexs[i][0:-3] == indexs[i+1][0:-3]

	global prev_index

	if len(indexs) == 0:
		logic.append("DRS-S(")
	else:
		if prev_index+1 == int(indexs[0][1:-3]):
			logic.append("DRS-N(")
		elif prev_index == int(indexs[0][1:-3]):
			logic.append("DRS-S(")
		else:
			assert False, "indexs are not continued"
		prev_index = int(indexs[0][1:-3])
		#logic.append("DRS-"+indexs[0][0:-3]+"(")

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

def out_sents(parent):
	sents = []
	tokens = []
	lemmas = []
	prev_id = 1
	for child in parent:
		current_id = int(child.attrib["{http://www.w3.org/XML/1998/namespace}id"][1])
		if len(child.attrib["{http://www.w3.org/XML/1998/namespace}id"]) == 6:
			current_id = int(child.attrib["{http://www.w3.org/XML/1998/namespace}id"][1:3])
		if current_id != prev_id:
			assert current_id == prev_id + 1
			sents.append((tokens,lemmas))
			tokens = []
			lemmas = []
			prev_id = current_id
		tmp = {}
		for cc in child[0]:
			if cc.attrib["type"] == "tok":
				tmp["tok"] = cc.text
			elif cc.attrib["type"] == "lemma":
				tmp["lemma"] = cc.text
		tokens.append(tmp["tok"])
		lemmas.append(tmp["lemma"])
	if len(tokens) != 0 and len(lemmas) != 0:
		sents.append((tokens, lemmas))
	return sents

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
	root = tree.getroot()[0]
	
	assert len(root) == 2
	assert root[0].tag == "taggedtokens"
	assert (root[1].tag == "sdrs" or root[1].tag == "drs")

	sents = out_sents(root[0])
	for sent in sents:
		print " ".join(sent[0]).encode("UTF-8")
		print " ".join(sent[1]).encode("UTF-8")

	print "TREE"
	global logic
	logic = []
	if root[1].tag == "sdrs":
		logic_sdrs(root[1])
	else:
		logic_drs(root[1])

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
#			newpath = "data/"+path.split("/")[-2]+"/"+path.split("/")[-1]
#			if not os.path.exists(newpath):
#				os.makedirs(newpath)
#			out = open(newpath+"/en.logic", "w")
#			xmlReader(path+"/en.drs.xml.notime.index_normalized",out)
#			out.close()
