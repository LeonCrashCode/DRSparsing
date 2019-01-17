import sys
import re

predefined = ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "DUP(", "OR(", ")"]

node_rel = {}
node_pred = {}
node_special = {}
node_dis_rel = {}
node_constant = {}
node_sense = {}


def stat(line):
	line = line.split()
	drs = 0
	predicate = False
	i = 0
	for tok in line:
		if tok in predefined or re.match("^DRS-[0-9]+\($", tok):
			pass
		elif re.match("^\$[0-9]+\[.+\]\($",tok):
			pass
		elif re.match("^\$[0-9]+$",tok):
			pass
		elif re.match("^[XESTPKB][0-9]+$",tok):
			pass
		elif re.match("^[PK][0-9]+\($", tok):
			pass
		elif tok[0] == "[" and tok[-1] == "]":
			pass
		elif re.match("^\"[anvr]\.[0-9][0-9]\"$", tok):
			add(tok, node_sense)
		elif re.match("^\".+\"$", tok):
			if predicate:
				add(tok, node_pred)
			else:
				add(tok, node_constant)
		elif tok.isupper():
			add(tok, node_dis_rel)
		elif tok in [":(", "-(", "(("]:
			if line[i+1][0] == "K":
				add(tok, node_dis_rel)
			else:
				add(tok, node_rel)
		elif tok[0].isupper() or tok.startswith("comp_"):
			add(tok, node_rel)
			if tok == "Pred(":
				predicate = True
			else:
				predicate = False
		else:
			print tok
			assert False, "unrecognized token"
		i += 1
		
def add(key, d):
	if key in d:
		d[key] += 1
	else:
		d[key] = 1

def show(node, label):
	print label
	keys = node.keys()
	keys.sort()
	for key in keys:
		print key #node[key]
	print "###"
	
if __name__ == "__main__":
	print "### BOX"
	print "\n".join(predefined[:-1]) #no )
	print "###"
	lines = []
	flag = False
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "TREE":
			flag = True
			continue
		if flag:
			stat(line)
			flag = False

	show(node_dis_rel, "### DISCOURSE")
	show(node_rel, "### RELATION")
	show(node_pred, "### PREDICATE")
	show(node_sense, "### SENSE")
	show(node_constant, "### CONSTANT")
	#for key in var.keys():
	#	print "#", key, var[key]
	#print "# drs-l", drs_l  
# B 46
# E 52
# K 32
# P 23
# S 53
# T 41
# X 165
# drs-l 60


# B 16
# E 15
# K 14
# P 8
# S 13
# T 15
# X 40
# drs-l 20	
