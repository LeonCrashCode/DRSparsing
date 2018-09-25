import os
import sys
import xml.etree.ElementTree as ET
import re

sense = False
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


def is_common_var(item):
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
	else:
		return False
def is_other_var(item):
	if item in ["\"speaker\"", "\"hearer\"", "\"now\""]:
		return True
	else:
		return False

def is_drs(item):
	if b_p.match(item):
		return True
	else:
		return False

def is_sdrs(item):
	if c_p.match(item):
		return True
	else:
		return False

def is_box(item):
	if is_drs(item) or is_sdrs(item):
		return True
	return False

def is_var(item):
	if is_common_var(item) or is_other_var(item):
		return True
	return False

def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"" and (not is_other_var(item)):
		return True
	else:
		return False
def is_subclass(item):
	if sc_p.match(item):
		return True
	else:
		return False

def is_X(item):
	if is_var(item) or is_realword(item):
		return True
	else:
		return False
def is_B(item):
	return is_drs(item)

def is_C(item):
	return is_sdrs(item)

def is_SNS(item):
	return is_subclass(item)


GlobalRelation = []
for line in open("GlobalRelation"):
	if line[0] == "#":
		continue
	GlobalRelation.append(line.strip())
RhetoricRelation = []
for line in open("RhetoricRelation"):
	if line[0] == "#":
		continue
	RhetoricRelation.append(line.strip())


def normal_lines(lines):

	xp = {}
	for line in lines:
		line = line.strip()
		if line[0] == "%":
			continue
		toks = line.split()

		#B PRP X B'
		if len(toks) >= 4 and is_box(toks[0]) and toks[1] == "PRP" and (not p_p.match(toks[2])) and is_box(toks[3]):
			xp[toks[2]] = "p"+str(100+len(xp))

	newlines = []
	for line in lines:
		line = line.strip()
		if line[0] == "%":
			newlines.append(line)
			continue
		toks = line.split()

		for i in range(len(toks)):
			if is_common_var(toks[i]) and (toks[i] in xp):
				toks[i] = xp[toks[i]]
		newlines.append(" ".join(toks))
	return newlines


def tuple_lines(lines):
	v_id = 0
	o_id = 0
	r_id = 0
	d_id = 0
	newlines = []
	for line in lines:
		line = line.strip()
		if line[0] == "%":
			continue
		toks = line.split()
		

		#B REF X
		if len(toks) >= 3 and is_B(toks[0]) and toks[1] == "REF" and is_X(toks[2]):
			assert is_common_var(toks[2]), "errors on 'B REF X'"
			newlines.append(line)
		#B NOT/POS/NEC/DRS B'
		elif len(toks) >= 3 and is_B(toks[0]) and toks[1] in ["NOT", "POS", "NEC", "DRS"] and is_B(toks[2]):
			newlines.append(line)
		#B IMP/DIS B' B''
		elif len(toks) >= 4 and is_B(toks[0]) and toks[1] in ["IMP", "DIS", "DUP"] and is_B(toks[2]) and is_B(toks[3]):
			newlines.append(" ".join([toks[0], toks[1], "v"+str(v_id)]))
			newlines.append(" ".join(["v"+str(v_id), "ARG0", (toks[2])]))
			newlines.append(" ".join(["v"+str(v_id), "ARG1", (toks[3])]))
			v_id += 1
		#B PRP X B'
		elif len(toks) >=4 and is_B(toks[0]) and toks[1] == "PRP" and is_X(toks[2]) and is_B(toks[3]):
			assert p_p.match(toks[2]), "errors on 'B PRP X B'"
			newlines.append(" ".join([toks[0], toks[1], "o"+str(o_id)]))
			newlines.append(" ".join(["o"+str(o_id), "ARG0", (toks[2])]))
			newlines.append(" ".join(["o"+str(o_id), "ARG1", (toks[3])]))
			o_id += 1
		#B EQU/NEQ/APX/LES/LEQ/TPR/TAB X Y
		elif len(toks) >= 4 and is_B(toks[0]) and toks[1] in ["EQU", "NEQ", "APX", "LES", "LEQ", "TPR", "TAB"] and is_X(toks[2]) and is_X(toks[3]):
			#assert is_common_var(toks[2]) or is_common_var(toks[3]), "errors on 'B EQU/NEQ/APX/LES/LEQ/TPR/TAB X Y'"
			newlines.append(" ".join([toks[0], toks[1], "r"+str(r_id)]))
			newlines.append(" ".join(["r"+str(r_id), "ARG0", (toks[2])]))
			newlines.append(" ".join(["r"+str(r_id), "ARG1", (toks[3])]))
			r_id += 1
		# B SYM SNS X  e.g. b0 company n.01 x1
		elif len(toks) >= 4 and is_B(toks[0]) and is_subclass(toks[2]) and is_X(toks[3]):
			#assert is_common_var(toks[3]), "errors on 'B SYM SNS X'"
			if sense:
				newlines.append(" ".join([toks[0], "Pred", "r"+str(r_id)]))
				newlines.append(" ".join(["r"+str(r_id), "ARG0", toks[3]]))
				newlines.append(" ".join(["r"+str(r_id), "ARG1", "\""+correct(normal_mwe(toks[1]))+"\"."+toks[2]]))
				r_id += 1
				#newlines.append(" ".join([toks[0], toks[1]+"."+toks[2], toks[3]]))
			else:
				newlines.append(" ".join([toks[0], "Pred", "r"+str(r_id)]))
				newlines.append(" ".join(["r"+str(r_id), "ARG0", toks[3]]))
				newlines.append(" ".join(["r"+str(r_id), "ARG1", "\""+correct(normal_mwe(toks[1]))+"\""]))
				r_id += 1
				#newlines.append(" ".join([toks[0], toks[1], toks[3]]))

		# B ROL X Y 
		elif len(toks) >= 4 and is_B(toks[0]) and is_X(toks[2]) and is_X(toks[3]):
			if toks[1] not in GlobalRelation:
				print "####G:", line
			assert toks[1] in GlobalRelation, "errors on 'B ROL X Y'"
			newlines.append(" ".join([toks[0], toks[1], "r"+str(r_id)]))
			newlines.append(" ".join(["r"+str(r_id), "ARG0", correct(normal_mwe(toks[2]))]))
			newlines.append(" ".join(["r"+str(r_id), "ARG1", correct(normal_mwe(toks[3]))]))
			r_id += 1

			"""
			if is_realword(toks[2]) and is_common_var(toks[3]):
				newlines.append(" ".join([toks[0], toks[1]+"_"+normal_mwe(toks[2][1:-1]), toks[3]]))
			elif is_realword(toks[3]) and is_common_var(toks[2]):
				newlines.append(" ".join([toks[0], toks[1]+"_"+normal_mwe(toks[3][1:-1]), toks[2]]))
			elif (is_common_var(toks[2]) and is_common_var(toks[3])) or (is_common_var(toks[2]) and is_other_var(toks[3])) or (is_common_var(toks[3]) and is_other_var(toks[2])):
				newlines.append(" ".join([toks[0], toks[1], "r"+str(r_id)]))
				newlines.append(" ".join(["r"+str(r_id), "ARG0", toks[2]]))
				newlines.append(" ".join(["r"+str(r_id), "ARG1", toks[3]]))
				r_id += 1
			else:
				print line
				assert False
			"""
		# B REL B' B''
		elif len(toks) >= 4 and is_B(toks[0]) and is_B(toks[2]) and is_B(toks[3]):
			if toks[1] not in RhetoricRelation:
				print "####R:", line
			assert toks[1] in RhetoricRelation, "errors on 'B REL B B'"
			newlines.append(" ".join([toks[0], toks[1], "d"+str(r_id)]))
			newlines.append(" ".join(["d"+str(r_id), "ARG0", (toks[2])]))
			newlines.append(" ".join(["d"+str(r_id), "ARG1", (toks[3])]))
			d_id += 1
		else:
			assert False
	return newlines


def normal_variables(lines):

	start_v = ["b", "x", "e", "s", "t", "p", "v", "o", "r", "d"]
	any_p = []
	stack_v = [ [] for i in range(10)]
	for v in start_v:
		any_p.append(re.compile("^"+v+"[0-9]+?$"))

	def index(v):
		for i in range(len(any_p)):
			if any_p[i].match(v):
				return i
		return -1

	def norm(v):
		if not (is_common_var(v) or is_drs(v) or is_sdrs(v)):
			return v
		idx = index(v)
		if idx == -1:
			print v
		assert idx != -1
		if v in stack_v[idx]:
			return start_v[idx]+str(stack_v[idx].index(v))
		else:
			stack_v[idx].append(v)
			return start_v[idx]+str(len(stack_v[idx]) - 1)
	
	newlines = []
	for line in lines:
		toks = line.strip().split()
		assert len(toks) >= 3
		toks[0] = norm(toks[0])
		toks[2] = norm(toks[2])
		newlines.append(" ".join(toks[:3]))

	return newlines


def CLFReader(filename):

	lines = []
	for line in open(filename):
		line = line.strip()
		lines.append(line)
	lines = normal_lines(lines)
	lines = tuple_lines(lines)
	lines = normal_variables(lines)

	print "\n".join(lines)

def correct(item):
	if item == "\"1~5~0\"":
		return "\"1.5.0\""
	if item == "\"stl~3456\"":
		return "\"stl#3456\""
	if item == "\"3~000\"":
		return "\"3,000\""
	if item == "\"13~7\"":
		return "\"13.7\""
	if item == "\"1~700-pound\"":
		return "\"1,700-pound\""
	if item == "\"1~000-megawatt\"":
		return "\"1,000-megawatt\""
	if item == "\"8~586-meter\"":
		return "\"8,586-meter\""
	if item == "\"4~387\"":
		return "\"4.387\""
	if item == "\"32~000\"":
		return "\"32,000\""
	if item == "\"5~\"":
		return "\"5%\""
	if item == "\"145~099\"":
		return "\"145,099\""
	if item == "\"hans@karlolo~net\"":
		return "\"hans@karlolo.net\""
	if item == "\"hirosey@genet~co~jp\"":
		return "\"hirosey@genet.co.jp\""
	if item == "\"7~000\"":
		return "\"7,000\""
	if item == "\"20~000\"":
		return "\"20,000\""
	if item == "\"14~000\"":
		return "\"14,000\""
	if item == "\"150~000\"":
		return "\"150,000\""
	if item == "\"deane~~adams~and~deane\"":
		return "\"deane,~adams~and~deane\""
	if item == "\"c~\"":
		return "\"c#\""
	if item == "\"~~~\"":
		return "\"...\""
	return item
def normal_mwe(item):
	return item.replace("_", "~")

def XMLReader(filename):
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
	print " ".join(raws).encode("UTF-8")
	print " ".join(lems).encode("UTF-8")

cnt = 0
if __name__ == "__main__":
	path = "/".join(sys.argv[1].split("/")[:4])
	if path in ["data/silver/p06/d3327","data/silver/p41/d2218", "data/silver/p03/d2739", "data/silver/p22/d1417", "data/silver/p74/d0943"]: # informal format in xml
		pass 
	elif not os.path.exists(sys.argv[2]):
		pass
	else: 
		print "###", " ".join(sys.argv)
		XMLReader(sys.argv[1])
		print "Graph"
		CLFReader(sys.argv[2])
		print
