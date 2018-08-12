import sys
import os
import xml.etree.ElementTree as ET

filename = ""
der = 0
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

D = {}
class sem:
	def __init__(self):
		self.init()
	def init(self):
		self.sem = ""
	def proc_sem(self, parent):
		self.init()
		assert len(parent) == 1 and parent[0].tag == "lam"
		self.division(parent[0])
	def division(self, parent):
		if parent.tag not in D:
			D[parent.tag] = []
		for child in parent:
			if child.tag not in D[parent.tag]:
				D[parent.tag].append(child.tag)
		if parent.tag == "lam":
			self.proc_lam(parent)
		elif parent.tag == "var":
			self.proc_var(parent)
		elif parent.tag == "merge":
			self.proc_merge(parent)
		elif parent.tag == "drs":
			self.proc_drs(parent)
		elif parent.tag == "app":
			self.proc_app(parent)
		elif parent.tag == "domain":
			self.proc_domain(parent)
		elif parent.tag == "conds":
			self.proc_conds(parent)
		elif parent.tag == "not":
			self.proc_cond_not(parent)
		elif parent.tag == "nec":
			self.proc_cond_nec(parent)
		elif parent.tag == "pos":
			self.proc_cond_pos(parent)
		elif parent.tag == "imp":
			self.proc_cond_imp(parent)
		elif parent.tag == "or":
			self.proc_cond_or(parent)
		elif parent.tag == "duplex":
			self.proc_cond_duplex(parent)
		elif parent.tag == "prop":
			self.proc_cond_prop(parent)
		elif parent.tag == "sdrs":
			self.proc_sdrs(parent)
		elif parent.tag == "constituents":
			self.proc_constituents(parent)
		elif parent.tag == "constituent":
			self.proc_constituent(parent)
		elif parent.tag == "sub":
			self.proc_sub(parent)
		elif parent.tag == "relations":
			self.proc_relations(parent)
		elif parent.tag == "alfa":
			self.proc_alfa(parent)
		elif parent.tag == "pred":
			self.proc_cond_pred(parent)
		elif parent.tag == "named":
			self.proc_cond_named(parent)
		elif parent.tag == "card":
			self.proc_cond_card(parent)
		elif parent.tag == "timex":
			self.proc_cond_timex(parent)
		elif parent.tag == "rel":
			self.proc_cond_rel(parent)
		elif parent.tag == "eq":
			self.proc_cond_eq(parent)
		else:
			print parent.tag
			assert False, "unrecognized"
	def proc_alfa(self, parent):
		self.sem += "alfa("+parent.attrib["type"]+","
		for child in parent:
			self.division(child)
			self.sem += ","
		self.sem = self.sem.strip(",")
		self.sem += ")"
	def proc_constituent(self, parent):
		assert len(parent) == 1
		self.sem += "lab("
		self.sem += "$"+parent.attrib["label"]+"$,"
		self.division(parent[0])
		self.sem += ")"
	def proc_sub(self, parent):
		self.sem += "sub("
		for child in parent:
			self.division(child)
			self.sem += ","
		if self.sem[-1] == ",":
			self.sem = self.sem[:-1]
		self.sem += ")"
	def proc_relations(self, parent):
		self.sem += "["
		for child in parent:
			indexs = self.get_index(child)
			self.sem += "[" + indexs + "]:"
			self.sem += "rel("
			self.sem += "$"+child.attrib["arg1"]+"$,$"+child.attrib["arg2"]+"$,"+normal(child.attrib["sym"])
			self.sem += "),"
		if self.sem[-1] == ",":
			self.sem = self.sem[:-1]
		self.sem += "]"
	def proc_constituents(self, parent):
		self.sem += "["
		for child in parent:
			if child.tag == "constituent":
				self.division(child)
				self.sem += ","
			elif child.tag == "sub":
				self.division(child)
				self.sem += ","
			elif child.tag == "relations":
				pass
			else:
				assert False, "unrecognized tag in constituents"
		if self.sem[-1] == ",":
			self.sem = self.sem[:-1]
		self.sem += "]"

	def proc_sdrs(self, parent):
		assert len(parent) == 2
		assert parent[0].tag == "constituents"
		assert parent[1].tag == "relations"
		self.sem += "sdrs("
		self.division(parent[0])
		self.sem += ","
		self.division(parent[1])
		self.sem += ")"
	def proc_cond_not(self, parent):
		assert len(parent) == 2
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "not("
		self.division(parent[1])
		self.sem += ")"
	def proc_cond_nec(self, parent):
		assert len(parent) == 2
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "nec("
		self.division(parent[1])
		self.sem += ")"
	def proc_cond_pos(self, parent):
		assert len(parent) == 2
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "pos("
		self.division(parent[1])
		self.sem += ")"
	def proc_cond_imp(self, parent):
		assert len(parent) == 3
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "imp("
		self.division(parent[1])
		self.sem += ","
		self.division(parent[2])
		self.sem += ")"
	def proc_cond_or(self, parent):
		assert len(parent) == 3
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "or("
		self.division(parent[1])
		self.sem += ","
		self.division(parent[2])
		self.sem += ")"
	def proc_cond_duplex(self, parent):
		assert len(parent) == 3
		indexs = self.get_index(parent)
                self.sem += "[" + indexs + "]:"
		self.sem += "duplex("
		self.sem += parent.attrib["type"]+","
		self.division(parent[1])
		self.sem += ","
		self.sem += "$"+parent.attrib["var"]+"$,"
		self.division(parent[2])
		self.sem += ")"
	def proc_cond_prop(self, parent):
		assert len(parent) == 2
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "prop($" + parent.attrib["argument"] + "$,"
		for child in parent:
			if child.tag == "indexlist":
				continue
			else:
				self.division(child)
		self.sem += ")"
	def proc_cond_eq(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "eq("
		self.sem += "$"+parent.attrib["arg1"]+"$,$"+parent.attrib["arg2"]+"$"
		self.sem += ")"
	def proc_cond_pred(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "pred("
		self.sem += "$"+parent.attrib["arg"]+"$,"+normal(parent.attrib["symbol"])+","+parent.attrib["type"]+","+parent.attrib["sense"]
		self.sem += ")"
	def proc_cond_named(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "named("
		self.sem += "$"+parent.attrib["arg"]+"$,"+normal(parent.attrib["symbol"])+","+parent.attrib["class"]+","+parent.attrib["type"]
		self.sem += ")"
	def proc_cond_card(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "card("
		self.sem += "$"+parent.attrib["arg"]+"$,"+parent.attrib["value"]
		self.sem += ")"
	def proc_cond_timex(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "timex("
		self.sem += "$"+parent.attrib["arg"]+"$,"+parent[1].text
		self.sem += ")"
	def proc_cond_rel(self, parent):
		indexs = self.get_index(parent)
		self.sem += "[" + indexs + "]:"
		self.sem += "rel("
		self.sem += "$"+parent.attrib["arg1"]+"$,$"+parent.attrib["arg2"]+"$,"+normal(parent.attrib["symbol"])+","+parent.attrib["sense"]
		self.sem += ")"
	def get_index(self, parent):
		for child in parent:
			if child.tag == "indexlist":
				indexs = []
				for cc in child:
					indexs.append(cc.text[1:])
				return ",".join(indexs)
		assert False, "no indexlist"
	def proc_domain(self, parent):
		self.sem += "["
		for child in parent:
			indexs = self.get_index(child)
			self.sem += "$"+child.attrib["label"]+"$:"
			self.sem += "["+indexs+"]:"
			self.sem += "$"+child.attrib["name"]+"$,"
		if self.sem[-1] == ",":
			self.sem = self.sem[:-1]
		self.sem += "]"
	def proc_conds(self, parent):
		self.sem += "["
		for child in parent:
			self.sem += "$"+child.attrib["label"]+"$:"
			if child.tag in D:
				if child[0].tag not in D[child.tag]:
					D[child.tag].append(child[0].tag)
			else:
				D[child.tag] = []
			self.division(child[0])
			self.sem += ","
		if self.sem[-1] == ",":
			self.sem = self.sem[:-1]
		self.sem += "]"
	def proc_drs(self, parent):
		assert len(parent) == 2
		assert parent[0].tag == "domain"
		assert parent[1].tag == "conds"
		#self.sem += "drs("
		self.sem += "$"+parent.attrib["label"]+"$:"+"drs("
		self.division(parent[0])
		self.sem += ","
		self.division(parent[1])
		self.sem += ")"
	def proc_app(self, parent):
		assert len(parent) == 2
		self.sem += "app("
		for child in parent:
			self.division(child)
			self.sem += ","
		self.sem = self.sem[:-1] + ")"
	def proc_merge(self, parent):
		assert len(parent) == 2
		self.sem += "merge("
		self.division(parent[0])
		self.sem += ","
		self.division(parent[1])
		self.sem += ")"
	def proc_var(self, parent):
		assert len(parent) == 0
		self.sem += "$"+parent.text+"$"
	def proc_lam(self, parent):
		assert len(parent) == 2
		self.sem += "lam("
		for child in parent:
			self.division(child)
			self.sem += ","
		self.sem = self.sem[:-1]+")"

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
	supertag = sem()
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
			supertag.proc_sem(parent[i])
			List.append(supertag.sem)
			break
		i += 1

	i = 0
	cnt = 0
	while i < len(parent):
		if parent[i].tag in ["binaryrule", "unaryrule", "lex"]:
			find = False
			for child in parent[i]:
				if child.tag == "cat":
					List.append(process_cat(child[0]))
				if child.tag == "sem":
					find = True
					supertag.proc_sem(child)
					List.append(supertag.sem)
					break
			assert find
			cnt += 1
		i += 1

	while i < len(parent):
		if parent[i].tag in ["binaryrule", "unaryrule", "lex"]:
			find = False
			for child in parent[i]:
				if child.tag == "cat":
                                        List.append(process_cat(child[0]))
				if child.tag == "sem":
					find = True
					supertag.proc_sem(child)
					List.append(supertag.sem)
					break
			assert find
			cnt += 1
		i += 1
	assert cnt == 2

	#print filename, der
	#print List[0], List[1]
	#print List[2]
	#print List[3].encode("UTF-8")
	#print List[4]
	#print List[5].encode("UTF-8")
	#print List[6]
	#print List[7].encode("UTF-8")
	#print 
	for child in parent:
		if child.tag == "binaryrule":
			process_binaryrule(child)
		elif child.tag == "unaryrule":
			process_unaryrule(child)

def process_unaryrule(parent):
	List = []
	supertag = sem()
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
			supertag.proc_sem(parent[i])
			List.append(supertag.sem)
			break
		i += 1

	i = 0
	cnt = 0
	while i < len(parent):
		if parent[i].tag in ["binaryrule", "unaryrule", "lex"]:
			find = False
			for child in parent[i]:
				if child.tag == "cat":
                                        List.append(process_cat(child[0]))
				if child.tag == "sem":
					find = True
					supertag.proc_sem(child)
					List.append(supertag.sem)
					break
			assert find
			cnt += 1
		i += 1
	assert cnt == 1
	#print filename, der
	#print List[0], List[1]
	#print List[2]
	#print List[3].encode("UTF-8")
	#print List[4]
	#print List[5].encode("UTF-8")
	#print 
	for child in parent:
		if child.tag == "binaryrule":
			process_binaryrule(child)
		elif child.tag == "unaryrule":
			process_unaryrule(child)

def process_lex(parent):
	#print filename, der
	#print "lex lex"
	supertag = sem()
	for child in parent:
		if child.tag == "cat":
			#print process_cat(child[0])
			pass
		if child.tag == "sem":
			find = True
			supertag.proc_sem(child)
			#print supertag.sem
			#print
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

for root, dirs, files in os.walk("data/p00"):
	if len(root.split("/")) != 3:
		continue
	tree = ET.parse(root+"/en.der.xml")
	filename = root
	root = tree.getroot()
	der = 1
	for child in root:
		process_der(child)
		der += 1
for key in D.keys():
	print key, D[key]

