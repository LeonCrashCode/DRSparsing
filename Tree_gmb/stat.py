import sys
import re


drs_l = 0
var = {}
def stat(line):
	line = line.split()
	drs = 0
	for tok in line:
		#if tok[-1] == "(":
		#	tok = tok[:-1]
		if tok == "DRS(":
			drs += 1
		if re.match("^[XESTPK][0-9]+\($",tok):
			if tok[0] not in var:
				var[tok[0]] = int(tok[1:-1])
			else:
				var[tok[0]] = max(var[tok[0]], int(tok[1:-1]))
		if re.match("^[XESTPK][0-9]+$",tok):
			if tok[0] not in var:
				var[tok[0]] = int(tok[1:])
			else:
				var[tok[0]] = max(var[tok[0]], int(tok[1:]))
	global drs_l
	drs_l = max(drs, drs_l)

rel_max = 0
rel_g_max = 0
d_rel_max = 0
d_rel_g_max = 0
def stat_rel(line):
	line = line.split()
	rel_g = 0
	d_rel_g = 0
	global rel_max
	global d_rel_max 
	stack = []
	for tok in line:
		#if tok[-1] == "(":
		#	tok = tok[:-1]
		if tok[-1] == "(":
			stack.append([tok, 0])
		elif tok == ")":
			if stack[-1][0] == "DRS(":
				if stack[-1][1] == 110:
					print line
				rel_max = max(stack[-1][1], rel_max)
				rel_g += stack[-1][1]
			elif stack[-1][0] == "SDRS(":
				d_rel_max = max(stack[-1][1], d_rel_max)
				d_rel_g += stack[-1][1]
			b = stack.pop()
			if b[0] in  ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "DUP(", "OR("]:
				pass
			elif re.match("^[XESTPK][0-9]+\($",b[0]):
				pass
			else:
				stack[-1][1] += 1
	global rel_g_max
	global d_rel_g_max

	rel_g_max = max(rel_g, rel_g_max)
	d_rel_g_max = max(d_rel_g, d_rel_g_max)

rel = {}
def stat_equ(line):
	# see which relations have two same arguments
	line = line.split()
	for i in range(len(line)):
		if i + 2 < len(line):
			if re.match("^[XESTPK][0-9]+$",line[i+1]) and re.match("^[XESTPK][0-9]+$",line[i+2]) and line[i+1] == line[i+2]:
				if line[i] not in rel:
					rel[line[i]] = 1
				else:
					rel[line[i]] += 1

def stat_pk_bracket(line):
	# see if there are two same p brackets or k brackets, e.g. p1( / k1( will appear twice or more or 
	pk = []
	line = line.split()
	for tok in line:
		if re.match("^[PK][0-9]+\($", tok):
			assert tok not in pk
			pk.append(tok)

def add(key, d):
	if key in d:
		d[key] += 1
	else:
		d[key] = 1

	
if __name__ == "__main__":

	for line in open(sys.argv[1]):
		line = line.strip()
		#stat(line)
		#stat_rel(line)
		#stat_equ(line)
		stat_pk_bracket(line)
	#for key in var.keys():
	#	print key, var[key]
	#print "drs-l", drs_l

	#print "rel-l", rel_max
	#print "rel-g-l", rel_g_max

	#print "d-rel-l", d_rel_max
	#print "d-rel-g-l", d_rel_g_max

	#for key in rel.keys():
	#	print key, rel[key] 
	