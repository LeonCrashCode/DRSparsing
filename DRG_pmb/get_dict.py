import sys
import re
x_p = re.compile("^x[0-9]+$")
e_p = re.compile("^e[0-9]+$")
s_p = re.compile("^s[0-9]+$")
t_p = re.compile("^t[0-9]+$")
p_p = re.compile("^p[0-9]+$")
b_p = re.compile("^b[0-9]+$")

cpy1_p = re.compile("^\"\$[0-9|,]+\"")
cpy2_p = re.compile("^\$[0-9|,]+")

predefined = ["DRS", "REF", "PRP", "NOT", "NEC", "POS", "IMP", "DUP", "OR", "EQU", "NEQ", "APX", "LES", "LEQ", "TPR", "TAB"]
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
	else:
		return False

def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"":
		return True
	else:
		return False

node_rel = {}
node_pred = {}
node_sense = {}
node_special = {}
node_dis_rel = {}
node_extra_constant = {}
def stat(line):
	line = line.split("|||")
	for l in line:
		toks = l.split()
		assert len(toks) in [3,4]
		for tok in toks:
			if tok in ["X", "E", "S", "T", "P", "B"]:
				pass
			elif tok in predefined:
				pass
			elif is_var(tok):
				pass
			elif cpy1_p.match(tok) or cpy2_p.match(tok):
				pass
			else:
				if re.match("^\"[avnr]\.\d+\"$", tok):
					node_sense.setdefault(tok)
				elif tok in ["\"speaker\"", "\"hearer\"", "\"now\""]:
					node_special.setdefault(tok)
				elif len(tok) > 2 and tok[0] == "\"" and tok[-1] == "\"":
					node_extra_constant.setdefault(tok)
				elif tok.isupper():
					node_dis_rel.setdefault(tok)
				elif tok[0].isupper():
					node_rel.setdefault(tok)
				else:
					node_pred.setdefault(tok)
					
					

def show(node, label):
	print label
	keys = node.keys()
	keys.sort()
	for key in keys:
		print key
	print "###"
	
if __name__ == "__main__":
	print "### BOX"
	print "\n".join(predefined)
	print "###"
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		stat(line)

	show(node_special, "### SPECIAL")
	show(node_sense, "### SENSE")
	show(node_dis_rel, "### DISCOURSE")
	show(node_rel, "### RELATION")
	show(node_pred, "### PREDICATE")
	show(node_extra_constant, "### CONSTANT")
	