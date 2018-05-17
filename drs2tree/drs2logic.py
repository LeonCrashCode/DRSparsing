import os
import sys
import xml.etree.ElementTree as ET
import re


def logic_relations(parent):
	assert parent.tag == "relations", "function relations errors"

	for child in parent:
		logic.append(child.attrib["sym"]+"( "+child.attrib["arg1"].upper()+" "+child.attrib["arg2"].upper()+" )")

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
	elif tag == "not" or tag == "nec" or tag == "pos" or tag == "imp" or tag == "or" or tag == "duplex":
		logic.append(tag.upper()+"(")
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

	elif child.tag == "comp":
		logic.append(child.attrib["symbol"]+"( "+child.attrib["arg1"].upper() + " "+child.attrib["arg2"].upper()+" )")
	elif child.tag == "rel":
		logic.append(child.attrib["symbol"]+"( "+child.attrib["arg1"].upper() + " "+ child.attrib["arg2"].upper()+" )")

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
def xmlReader(filename, out):
	tree = ET.parse(filename)
	root = tree.getroot()[0]
	
	assert len(root) == 2
	assert root[0].tag == "taggedtokens"
	assert (root[1].tag == "sdrs" or root[1].tag == "drs")

	sents = out_sents(root[0])
	for sent in sents:
		out.write((" ".join(sent[0])+"\n").encode("UTF-8"))
		out.write((" ".join(sent[1])+"\n").encode("UTF-8"))


	global logic
	logic = []
	if root[1].tag == "sdrs":
		logic_sdrs(root[1])
	else:
		logic_drs(root[1])
	out.write((" ".join(logic)+"\n").encode("UTF-8"))

if __name__ == "__main__":
	for (path, dirs, files) in os.walk(sys.argv[1]):
		if len(files) != 0:
			print path
			tokens = []
			newpath = "data/"+path.split("/")[-2]+"/"+path.split("/")[-1]
			if not os.path.exists(newpath):
				os.makedirs(newpath)
			if os.path.exists(newpath+"en.drs.xml"):
				out = open(newpath+"/en.logic", "w")
				xmlReader(path+"/en.drs.xml",out)
				out.close()
			
