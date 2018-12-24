import sys
import re

predefined = ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "DUP(", "OR(", ")"]

node_rel = {}
node_pred = {}
node_special = {}
node_dis_rel = {}
node_constant = {}
node_sense = {}
drs_l = 0
var = {}
def stat(line):
	line = line.split()
	drs = 0
	for tok in line:
		if tok == ")":
			continue
		#if tok[-1] == "(":
		#	tok = tok[:-1]
		if tok[-1] == "(":
			if (tok in predefined) or re.match("^DRS-[0-9]+\($", tok):
				if tok == "DRS(" or re.match("^DRS-[0-9]+\($", tok):
					drs += 1
				pass
			elif re.match("^\$[0-9]+\($",tok):
				pass
			elif tok in ["@P(", "@K("]:
				pass
			elif tok.isupper():
				add(tok, node_dis_rel)
			elif tok[0].isupper():
				add(tok, node_rel)
			else:
				add(tok, node_pred)
		else:
			if re.match("^[XESTPK][0-9]+$",tok):
				if tok[0] not in var:
					var[tok[0]] = int(tok[1:])
				else:
					var[tok[0]] = max(var[tok[0]], int(tok[1:]))
				pass
			elif re.match("^[anvr]\.[0-9][0-9]$", tok):
				add(tok, node_sense)
			elif re.match("^\$[0-9]+$",tok):
				pass
			else:
				add(tok, node_constant)
	global drs_l
	drs_l = max(drs, drs_l)
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
		#print key, node[key]
		#if key not in ["CARD_NUMBER", "TIME_NUMBER", ")"]:
		#	print key+"("
		#else:
		#	print key
		print key
	print "###"
	
if __name__ == "__main__":
	print "### BOX"
	print "\n".join(predefined[:-1]) #no )
	print "###"
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		stat(line)

	show(node_dis_rel, "### DISCOURSE")
	show(node_rel, "### RELATION")
	show(node_pred, "### PREDICATE")
	show(node_sense, "### SENSE")
	show(node_constant, "### CONSTANT")
	for key in var.keys():
		print "#", key, var[key]
	print "# drs-l", drs_l  
	
