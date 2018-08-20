import sys
import os
import xml.etree.ElementTree as ET
filename = ""
der = 0
import json
from defination import DRSnode

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

def process_binaryrule(parent):
	List = []
	List.append("binary")
	List.append(parent.attrib["type"]+" "+parent.attrib["description"])
	i = 0
	while i < len(parent):
		if parent[i].tag == "cat":
			List.append(process_cat(parent[i][0]))
			break
		i += 1

	while i < len(parent):
		if parent[i].tag == "sem":
			supertag = DRSnode()
			supertag.init_from_xml(parent[i][0])
			List.append(json.dumps(supertag.serialization()))
			break
		i += 1

	print filename, der
	print List[0], List[1]
	print List[2]
	print List[3].encode("UTF-8")
	print 

def process_unaryrule(parent):
	List = []
	List.append("unary")
	List.append(parent.attrib["type"]+" "+parent.attrib["description"])
	i = 0
	while i < len(parent):
		if parent[i].tag == "cat":
			List.append(process_cat(parent[i][0]))
			break
		i += 1

	while i < len(parent):
		if parent[i].tag == "sem":
			supertag = DRSnode()
			supertag.init_from_xml(parent[i][0])
			List.append(json.dumps(supertag.serialization()))
			break
		i += 1
	print filename, der
	print List[0], List[1]
	print List[2]
	print List[3].encode("UTF-8")
	print 

def process_lex(parent):
	print filename, der
	print "lex lex"
	for child in parent:
		if child.tag == "cat":
			print process_cat(child[0])
		if child.tag == "sem":
			find = True
			supertag = DRSnode()
			supertag.init_from_xml(child[0])
			print json.dumps(supertag.serialization())	
			break
	assert find

def process_der(parent):
	assert parent.tag == "der"
	assert len(parent) == 1

	if parent[0].tag == "binaryrule":
		process_binaryrule(parent[0])
	elif parent[0].tag == "unaryrule":
		process_unaryrule(parent[0])
	elif parent[0].tag == "lex":
		process_lex(parent[0])
	else:
		print parent[0].tag
		assert False, "unrecognized tag in der"

for root, dirs, files in os.walk("data"):
	if len(root.split("/")) != 3:
		continue
	tree = ET.parse(root+"/en.der.xml")
	filename = root
	root = tree.getroot()
	der = 1
	for child in root:
		process_der(child)
		der += 1

