import os
import sys
import xml.etree.ElementTree as ET
import re

x_p = re.compile("^x[0-9]+$")
e_p = re.compile("^e[0-9]+$")
s_p = re.compile("^s[0-9]+$")
t_p = re.compile("^t[0-9]+$")
c_p = re.compile("^c[0-9]+$")
p_p = re.compile("^p[0-9]+$")
b_p = re.compile("^b[0-9]+$")

sc_p = re.compile("\"[a-z]\.[0-9]+\"")
r_p = re.compile("r[0-9]+?")
k_p = re.compile("k[0-9]+?")

def is_var(item):
	if x_p.match(item):
		return True
	elif e_p.match(item):
		return True
	elif s_p.match(item):
		return True
	elif t_p.match(item):
		return True
	elif p_p.match(item):
		return True
	elif b_p.match(item):
		return True
	elif c_p.match(item):
		return True
	elif item in ["\"speaker\"", "\"hearer\"", "\"now\""]:
		return True
	else:
		return False
def is_box(item):
	if b_p.match(item):
		return True
	elif c_p.match(item):
		return True
	else:
		return False
def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"" and item not in  ["\"speaker\"", "\"hearer\"", "\"now\""]:
		return True
	else:
		return False
def is_subclass(item):
	if sc_p.match(item):
		return True
	else:
		return False

def normal_lines(lines):

	xb = []
	xb_cc = []
	xp = []
	def is_new_xb(item):
		if not is_box(item):
			assert x_p.match(item)
			if item not in xb:
				return -1
			return xb.index(item)
		return -2
	def is_new_xp(item):
		if not p_p.match(item):
			assert x_p.match(item) or s_p.match(item)
			if item not in xp:
				return True
		return False

	for line in lines:
		line = line.strip()
		if line[0] == "%":
			continue
		line = "%".join(line.split("%")[:1]).strip()
		toks = line.split()
		idx = is_new_xb(toks[0])
		if idx == -1:
			xb.append(toks[0])
			if toks[1] == "DRS":
				xb_cc.append(1)
			else:
				xb_cc.append(0)
		elif idx == -2:
			pass
		else:
			xb_cc[idx] += 1

		if len(toks) == 3:
			#b DRS b
			if toks[1] in ["DRS", "NOT", "POS", "NEC"]:
				idx = is_new_xb(toks[2])
				if idx == -1:
					xb.append(toks[2])
					xb_cc.append(0)

		if len(toks) == 4:
			#b PRP p b
			if toks[1] == "PRP":
				if is_new_xp(toks[2]):
					xp.append(toks[2])
				idx = is_new_xb(toks[3])
				if idx == -1:
					xb.append(toks[3])
					xb_cc.append(0)
	newlines = []
	for line in lines:
		line = line.strip()
		if line[0] == "%":
			continue
		toks = line.split()
		new_toks = []
		for tok in toks:
			if tok in xb:
				if xb_cc[xb.index(tok)] >= 2:
					new_toks.append("c"+str(10000+xb.index(tok)))
				else:
					new_toks.append("b"+str(10000+xb.index(tok)))
			elif tok in xp:
				new_toks.append("p"+str(10000+xp.index(tok)))
			else:
				new_toks.append(tok)
		newlines.append(" ".join(new_toks))
	if len(xb) != 0:
		print xb
		print xb_cc
		for line in lines:
			print line
		print "========"
		for line in newlines:
			print line
	if len(xp) != 0:
		print xp
		for line in lines:
			print line
		print "========"
		for line in newlines:
			print line
	return newlines
def tuple_lines(lines):
	r_id = 0
	c_id = 0
	k_id = 0
	d_id = 0
	newlines = []
	for line in lines:
		line = line.strip()
		if line[0] == "%":
			continue
		line = "%".join(line.split("%")[:1]).strip()
		toks = line.split()
		assert b_p.match(toks[0])

		if toks[1] == "REF":
			assert len(toks) == 3 and is_var(toks[2])
			newlines.append(line)
		elif toks[1] in ["NOT", "POS", "NEC", "DRS"]:
			assert len(toks) == 3 and b_p.match(toks[2])
			newlines.append(line)
		elif toks[1] in ["IMP", "DIS"]:
			assert len(toks) == 4 and b_p.match(toks[2]) and b_p.match(toks[3])
			newlines.append(" ".join([toks[0], toks[1], "k"+str(k_id)]))
			newlines.append(" ".join(["k"+str(k_id), "ARG0", toks[2]]))
			newlines.append(" ".join(["k"+str(k_id), "ARG1", toks[3]]))
			k_id += 1
		elif toks[1] == "PRP":
			assert len(toks) == 4 and p_p.match(toks[2]) and b_p.match(toks[3])
			newlines.append(" ".join([toks[0], toks[1], "c"+str(c_id)]))
			newlines.append(" ".join(["c"+str(c_id), "ARG0", toks[2]]))
			newlines.append(" ".join(["c"+str(c_id), "ARG1", toks[3]]))
			c_id += 1
		elif toks[1] in ["EQU", "NEQ", "APX", "LES", "LEQ", "TPR", "TAB"]:
			assert len(toks) ==4 and is_var(toks[2]) and is_var(toks[3])
			newlines.append(" ".join([toks[0], toks[1], "r"+str(r_id)]))
			newlines.append(" ".join(["r"+str(r_id), "ARG0", toks[2]]))
			newlines.append(" ".join(["r"+str(r_id), "ARG1", toks[3]]))
			r_id += 1
		# B REL B' B''
		elif len(toks) == 4 and b_p.match(toks[2]) and b_p.match(toks[3]):
			newlines.append(" ".join([toks[0], toks[1], "d"+str(r_id)]))
			newlines.append(" ".join(["d"+str(r_id), "ARG0", toks[2]]))
			newlines.append(" ".join(["d"+str(r_id), "ARG1", toks[3]]))
			d_id += 1
		# B SYM SNS X  e.g. b0 company n.01 x1
		elif len(toks) == 4 and is_subclass(toks[2]):
			assert is_var(toks[3])
			if sense:
				newline.append(" ".join([toks[0], toks[1]+"."+toks[2], toks[3]]))
			else:
				newline.append(" ".join([toks[0], toks[1], toks[3]]))
		# B ROL X Y 
		elif len(toks) == 4:
			assert toks[1] in ["Name"]
			if is_realword(toks[2]) and (not is_realword(toks[3])):
				newline.append(" ".join([toks[0], toks[1]+"_"+toks[2][1:-1], toks[3]]))
			elif is_realword(toks[3]) and (not is_realword(toks[2])):
				newline.append(" ".join([toks[0], toks[1]+"_"+toks[3][1:-1], toks[2]]))
			elif is_var(toks[])
			else:
				assert False

	return newlines

any_p = [x_p, e_p, s_p, t_p, c_p, p_p, b_p, r_p, k_p]
cls_v = ["x", "e", "s", "t", "c", "p", "b", "r", "k"]

stat_v = [ 0 for i in range(9)]
def normal_variables(lines):
	def variable_index(item):
		for i in range(len(any_p)):
			if any_p[i].match(item):
				if i == 4: # change every c to b
					i = 6
				return i
		assert False, "unrecoginzed variables"

	v = [ [] for i in range(9)]
	for line in lines:
		line = line.strip().split()
		assert len(line) == 3
		
		if line[0] not in ["\"speaker\"", "\"hearer\"", "\"now\""]:
			idx = variable_index(line[0])
			if line[0] not in v[idx]:
				v[idx].append(line[0])
		if line[-1] not in ["\"speaker\"", "\"hearer\"", "\"now\""]:
			idx = variable_index(line[-1])
			if line[-1] not in v[idx]:
				v[idx].append(line[-1])

	for i in range(len(stat_v)):
		stat_v[i] = max(stat_v[i], len(v[i]))

	newlines = []
	for line in lines:
		line = line.strip().split()
		assert len(line) == 3

		l = line[0]
		if line[0] not in ["\"speaker\"", "\"hearer\"", "\"now\""]:
			idx = variable_index(line[0])
			assert line[0] in v[idx]
			l = cls_v[idx] + str(v[idx].index(line[0]))

		r = line[-1]
		if line[-1] not in ["\"speaker\"", "\"hearer\"", "\"now\""]:
			idx = variable_index(line[-1])
			assert line[-1] in v[idx]
			r = cls_v[idx] + str(v[idx].index(line[-1]))

		newlines.append(" ".join([l, line[1], r]))
	return newlines



def CLFReader(filename, out):

	lines = []
	for line in open(filename):
		line = line.strip()
		lines.append(line)

	#lines = normal_lines(lines)
	lines = tuple_lines(lines)
	#lines = normal_variables(lines)

	for line in lines:
		out.write(line+"\n")
	out.flush()

def normal_mwe(item):
	return item.replace("~", "_")

def XMLReader(filename, out):
	tree = ET.parse(filename)
	root = tree.getroot()

	raws = []
	lems = []
	for child in root[0][0]:
		f = -1
		t = -1
		for cc in child[0]:
			if cc.attrib["type"] == "tok":
				cc.text = normal_mwe(cc.text)
				raws.append(cc.text)
			elif cc.attrib["type"] == "lemma":
				cc.text = normal_mwe(cc.text)
				lems.append(cc.text)
			elif cc.attrib["type"] == "from":
				f = int(cc.text)
			elif cc.attrib["type"] == "to":
				t = int(cc.text)
		if f < 0 or t < 0:
			raws.pop()
			lems.pop()
	out.write(" ".join(raws).encode("UTF-8")+"\n")
	out.write(" ".join(lems).encode("UTF-8")+"\n")

cnt = 0
if __name__ == "__main__":
	if path in ["data/silver/p06/d3327","data/silver/p41/d2218", "data/silver/p03/d2739"]: # informal format in xml
		continue
	if not os.path.exists(sys.argv[1]+"/en.drs.clf"):
		continue
	out = open(path+"/en.drg", "w")
	out.write("%%% "+" ".join(sys.arg)+"\n")
	XMLReader(path+"/en.drs.xml", out)
	CLFReader(path+"/en.drs.clf",out)
	out.write("\n")
	out.close()
