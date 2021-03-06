import os
import sys
import xml.etree.ElementTree as ET
import re
import types

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

lemmas = []
multiple_lemmas = []
def getCard(parent):
	child = parent[0]
	l = []
	for cc in child:
		pos1 = int(cc.text[1:-3])
		pos2 = int(cc.text[-3:])
		l.append(pos2-1)
	assert len(l) > 0
	return  " ".join(["$"+str(index) for index in l])

def getTime(parent):
	child = parent[0]

	l = []
	pos1 = 999
	for cc in child:
		pos1 = int(cc.text[1:-3]) - 1
		pos2 = int(cc.text[-3:])
		l.append(pos2-1)
	assert len(l) > 0
	
	
	date = parent[1].text
	
	assert len(date) == 9
	Year = date[1:5]
	Month = date[5:7]
	Day = date[7:9]
	
	Year_ex = Month_ex = Day_ex = 1
	
	if Year == "XXXX":
		Year_ex = 0
	if Month == "XX":
		Month_ex = 0
	if Day == "XX":
		Day_ex = 0
	
	ex = Year_ex + Month_ex + Day_ex 
	assert ex !=0

	s = "T"
	if Year_ex == 1:
		s += "y"
	else:
		s += "x"

	if Month_ex == 1:
		s += "m"
	else:
		s += "x"
	
	if Day_ex == 1:
		s += "d"
	else:
		s += "x"
	return s+"(", " ".join(["$"+str(index) for index in l])
	"""
	if Year_ex == 1:
		for pos2 in l:
			if isYear(words[pos1][pos2]):
				timex.append([pos2, Year, pos2])
				break
		assert len(timex) == 0
	else:
		timex.append([])
	if Month_ex == 1:
		for pos2 in l:
			if isMonth(words[pos1][pos2]):
				timex.append([pos2, Year, pos2])
				break
		assert len(timex) == 1
	else:
		timex.append([])

	if day_ex == 1:
		for pos2 in l:
			if isMonth(words[pos1][pos2]):
				timex.append([pos2, Year, pos2])
				break
		assert len(timex) == 2
	else:
		timex.append([])

		
	return  " ".join(["$"+str(index) for index in l])
	"""
def getName(parent):
	child = parent[0]
	l = []
	for cc in child:
		pos1 = int(cc.text[1:-3])
		pos2 = int(cc.text[-3:])
		l.append((lemmas[pos2-1],pos2-1))
	if len(l) == 1:
		assert parent.attrib["symbol"] == l[0][0]
		return l[0][1]
	elif len(l) == 0:
		assert parent.attrib["symbol"] in lemmas
		come = multiple_lemmas[parent.attrib["symbol"]]
		index = -1
		for i, v in enumerate(lemmas):
			if parent.attrib["symbol"] == v:
				index = i
				if come == 0:
					break
				come -= 1
		assert index != -1
		multiple_lemmas[parent.attrib["symbol"]] += 1
		return index
	else:
		return [x[1] for x in l]
		assert False, "more than two indexs" 
		print "out of", sys.argv[1]

def getPred(parent):
	child = parent[0]
	l = []
	for cc in child:
		pos1 = int(cc.text[1:-3])
		pos2 = int(cc.text[-3:])
		l.append((lemmas[pos2-1],pos2-1))

	if len(l) == 1:
		if parent.attrib["symbol"] == l[0][0]:
			return l[0][1]
		else:
			return -1
	elif len(l) == 0:
		if parent.attrib["symbol"] not in lemmas:
			return -1
		come = multiple_lemmas[parent.attrib["symbol"]]
		index = -1
		for i, v in enumerate(lemmas):
			if parent.attrib["symbol"] == v:
				index = i
				if come == 0:
					break
				come -= 1
		multiple_lemmas[parent.attrib["symbol"]] += 1
		return index
	else:
		assert False, "more than two indexs" 
		print "out of", sys.argv[1]
def getRel(parent):
	child = parent[0]
	l = []
	for cc in child:
		pos1 = int(cc.text[1:-3])
		pos2 = int(cc.text[-3:])
		l.append((lemmas[pos2-1], pos2-1))
	if len(l) == 1:
		if parent.attrib["symbol"] == l[0][0]:
			return l[0][1]
		else:
			return -1
	elif len(l) == 0:
		return -1
	else:
		assert False, "more than two indexs" 
		print "out of", sys.argv[1]

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
		tag = "Named_"+child.attrib["class"].upper()+"_"+child.attrib["type"].upper()+"("
		if type(index) == types.ListType:
			index = ["$"+str(idx) for idx in index]
			logic.append(tag+" "+p+" "+child.attrib["arg"].upper()+" "+" ".join(index)+" ["+child.attrib["symbol"]+"]"+" )")
		else:
			logic.append(tag+" "+p+" "+child.attrib["arg"].upper()+" "+"$"+str(index)+" ["+child.attrib["symbol"]+"]"+" )")
	elif child.tag == "pred":
		sense = child.attrib["sense"]
		if len(sense) == 1:
			sense = "0"+sense
		assert len(sense) == 2
		index = getPred(child)
		if index == -1:
			logic.append(child.attrib["symbol"]+"( "+p+child.attrib["arg"].upper()+" "+child.attrib["type"]+"."+sense+" )")
		else:
			logic.append("$"+str(index)+"["+child.attrib["symbol"]+"]"+"( "+p+child.attrib["arg"].upper()+" "+child.attrib["type"]+"."+sense+" )")
	elif child.tag == "card":
		#logic.append("CARD( "+child.attrib["arg"].upper() + " " + child.attrib["value"]+" )")
		value = getCard(child)
		logic.append("Card( "+p+child.attrib["arg"].upper() + " " + value+" ["+child.attrib["value"]+"]"+" )")
	elif child.tag == "timex":
		#logic.append("TIMEX( "+child.attrib["arg"].upper() + " " + child[1].text+" )")
		tag, value = getTime(child)
		logic.append(tag+" "+p+child.attrib["arg"].upper() + " " + value+" ["+child[1].text+"]"+ " )")

	elif child.tag == "eq":
		logic.append("Equ( "+p+child.attrib["arg1"].upper() + " "+child.attrib["arg2"].upper()+" )")
	elif child.tag == "rel":
		rel = child.attrib["symbol"]
		index = getRel(child)
		if index == -1:
			logic.append(rel[0].upper()+rel[1:]+"( "+p+child.attrib["arg1"].upper() + " "+ child.attrib["arg2"].upper()+" )")
		else:
			logic.append("$"+str(index)+"["+rel+"]"+"( "+p+child.attrib["arg1"].upper() + " "+ child.attrib["arg2"].upper()+" )")
	elif child.tag == "prop":
		#print child.attrib["argument"]
		#assert p[:-1] == "B0"
		logic_prev(child, "prop", p)
	elif child.tag == "not":
		#assert p[:-1] == "B0"
		logic_prev(child, "not", p)
	elif child.tag == "pos":
		#assert p[:-1] == "B0"
		logic_prev(child, "pos", p)
	elif child.tag == "nec":
		#assert p[:-1] == "B0"
		logic_prev(child, "nec", p)
	elif child.tag == "duplex":
		#assert p[:-1] == "B0"
		logic_prev(child, "duplex", p)
	elif child.tag == "or":
		#assert p[:-1] == "B0"
		logic_prev(child, "or", p)
	elif child.tag == "imp":
		#assert p[:-1] == "B0"
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

box_stack = []
#prev_index = 1
#cur_index = 0
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

	"""
	global prev_index
	
	if len(indexs) == 0:
		logic.append("DRS-"+str(prev_index-1)+"(")
		cur_index = prev_index - 1
	else:
		if prev_index+1 == int(indexs[0][1:-3]):
			logic.append("DRS-"+str(prev_index)+"(")
			cur_index = prev_index
		elif prev_index == int(indexs[0][1:-3]):
			logic.append("DRS-"+str(prev_index-1)+"(")
			cur_index = prev_index - 1
		else:
			assert False, "indexs are not continued"
		prev_index = int(indexs[0][1:-3])
		#logic.append("DRS-"+indexs[0][0:-3]+"(")
	"""
	logic.append("DRS-0(")
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

def out_sents(parent):
	
	sents = []
	tokens = []
	lemmas = []
	for child in parent:
		if child.tag == "taggedtokens":
			for c in child:
				tmp = {}
				for cc in c:
					if cc.attrib["type"] == "tok":
						tmp["tok"] = cc.text
					elif cc.attrib["type"] == "lemma":
						tmp["lemma"] = cc.text
				tokens.append(tmp["tok"])
				lemmas.append(tmp["lemma"])
	if len(tokens) != 0 and len(lemmas) != 0:
		#sents.append((tokens, lemmas))
		sents.append(tokens)
		sents.append(lemmas)
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

def xmlReader(filename):
	tree = ET.parse(filename)
	tree = tree.getroot()
	global words
	global logic

	global lemmas
	global multiple_lemmas
	for root in tree:
		assert (root.tag == "sdrs" or root.tag == "drs")

		words, lemmas= out_sents(root)
		print " ".join(words).encode("UTF-8")
		multiple_lemmas = {}
		for lem in lemmas:
			if lem not in multiple_lemmas:
				multiple_lemmas[lem] = 1
			else:
				multiple_lemmas[lem] += 1

		logic = []
		if root.tag == "sdrs":
			logic_sdrs(root)
		else:
			logic_drs(root)

		print "TREE"
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
