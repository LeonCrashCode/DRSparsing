import os
import sys
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
	if item[0] == "\"" and item[-1] == "\"" and (not is_other_var(item)) and (not is_subclass(item)):
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


D = {}
def RelationReader(filename):
	for line in open(filename):
		line = line.strip()
		if line[0] == "%":
			continue
		toks = line.split()

		if len(toks) >= 3 and is_B(toks[0]) and toks[1] == "REF" and is_X(toks[2]):
			pass
		#B NOT/POS/NEC/DRS B'
		elif len(toks) >= 3 and is_B(toks[0]) and toks[1] in ["NOT", "POS", "NEC", "DRS"] and is_B(toks[2]):
			pass
		#B IMP/DIS B' B''
		elif len(toks) >= 4 and is_B(toks[0]) and toks[1] in ["IMP", "DIS", "DUP"] and is_B(toks[2]) and is_B(toks[3]):
			pass
		#B PRP X B'
		elif len(toks) >=4 and is_B(toks[0]) and toks[1] == "PRP" and is_X(toks[2]) and is_B(toks[3]):
			pass
		#B EQU/NEQ/APX/LES/LEQ/TPR/TAB X Y
		elif len(toks) >= 4 and is_B(toks[0]) and toks[1] in ["EQU", "NEQ", "APX", "LES", "LEQ", "TPR", "TAB"] and is_X(toks[2]) and is_X(toks[3]):
			pass
		# B SYM SNS X  e.g. b0 company n.01 x1
		elif len(toks) >= 4 and is_B(toks[0]) and is_subclass(toks[2]) and is_X(toks[3]):
			pass
		elif len(toks) >= 4 and is_B(toks[0]) and is_X(toks[2]) and is_X(toks[3]):
			D[toks[1]] = 1
		elif len(toks) >= 4 and is_B(toks[0]) and is_B(toks[2]) and is_B(toks[3]):
			pass
		else:
			pass

if __name__ == "__main__":
	print "#", " ".join(sys.argv)
	for root, dirs, files in os.walk(sys.argv[1]):
		if len(root.split("/")) != 4:
			continue
		path = root

		sys.stderr.write(path+"\n")
		if path in ["data/silver/p06/d3327","data/silver/p41/d2218", "data/silver/p03/d2739"]: # informal format in xml
			pass 
		elif not os.path.exists(path+"/en.drs.clf"):
			pass
		else: 
			RelationReader(path+"/en.drs.clf")

	keys = D.keys()
	keys.sort()
	print "\n".join(keys)
