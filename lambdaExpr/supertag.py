import sys
import os
import xml.etree.ElementTree as ET
filename = ""
der = 0
import json
from defination import *
import types

def general(token, expre):
	if type(expre) == types.StringType or type(expre) == types.UnicodeType:
		if expre == token:
			return "LEMMA"
		return expre

	elif type(expre) == types.DictType:
		for key in expre.keys():
			if key == "indexs":
				expre[key] = None
			else:
				expre[key] = general(token,expre[key])
		return expre
	elif type(expre) == types.ListType:
		for i in range(len(expre)):
			expre[i] = general(token, expre[i])
		return expre
	else:
		assert False, "unrecognized type"

def process_cat(parent):
	if parent.tag == "atomic":
		if "feature" in parent.attrib:
			return parent.text+"["+parent.attrib["feature"]+"]"
		else:
			return parent.text
	elif parent.tag == "forward":
		assert len(parent) == 2
		return process_cat(parent[0]) + "/" + process_cat(parent[1])
	elif parent.tag == "backward":
		assert len(parent) == 2
		return process_cat(parent[0]) + "\\" + process_cat(parent[1])
	else:
		print parent.tag
		assert False, "cat error"

def process_rule(parent):
	for child in parent:
		if child.tag == "binaryrule":
			process_rule(child)
		elif child.tag == "unaryrule":
			process_rule(child)
		elif child.tag == "lex":
			d = {}
			for cc in child:
				if cc.tag == "token":
					d["token"] = cc.text
				if cc.tag == "tag":
					d[cc.attrib["type"]] = cc.text
				if cc.tag == "cat":
					d["cat"] = process_cat(cc[0])
				if cc.tag == "sem":
					find = True
					supertag = lam(cc[0])
					d["sem"] = supertag.serialization()
			d["sem"] = general(d["lemma"], d["sem"])
			print "\t".join([d["token"].encode("utf-8"), d["lemma"].encode("utf-8"), d["pos"], d["cat"], json.dumps(d["sem"]).encode("utf-8")])

	

def process_lex(parent):
	d = {}
	find = False
	for child in parent:
		if child.tag == "token":
			d["token"] = child.text
		if child.tag == "tag":
			d[child.attrib["type"]] = child.text
		if child.tag == "cat":
			d["cat"] = process_cat(child[0])
		if child.tag == "sem":
			find = True
			supertag = lam(child[0])
			d["sem"] = supertag.serialization()
		d["sem"] = general(d["lemma"], d["sem"])
	print "\t".join([d["token"].encode("utf-8"), d["lemma"].encode("utf-8"), d["pos"], d["cat"], json.dumps(d["sem"]).encode("utf-8")])
	assert find

def process_der(parent):
	assert parent.tag == "der"
	assert len(parent) == 1

	if parent[0].tag == "binaryrule":
		process_rule(parent[0])
	elif parent[0].tag == "unaryrule":
		process_rule(parent[0])
	elif parent[0].tag == "lex":
		process_lex(parent[0])
	else:
		print parent[0].tag
		assert False, "unrecognized tag in der"

for root, dirs, files in os.walk("data/p14/d0559"):
	if len(root.split("/")) != 3:
		continue
	tree = ET.parse(root+"/en.der.xml")
	filename = root
	root = tree.getroot()
	der = 1
	for child in root:
		print "===", filename, der
		process_der(child)
		der += 1
