import sys
import os
import xml.etree.ElementTree as ET
import re

br = re.compile("^b[0-9]+?$")


def handle_sense(predicate):
	if len(predicate.split(".")) < 3:
		if len(predicate) >= 3 and predicate[0] == "\"" and predicate[-1] == "\"":
			return predicate[1:-1]
		else:
			return predicate
	pred = ".".join(predicate.split(".")[:-2])
	typ = predicate.split(".")[-2]
	idx = predicate.split(".")[-1]

	if len(pred) > 2 and pred[0] == "\"" and pred[-1] == "\"":
		pred = pred[1:-1]
	return pred + " " + "\""+typ+"."+idx+"\""

def handle_rel(rel, context):
	if rel not in context:
		return rel.capitalize()
	return rel
def pack(lines, context):
	argset = {}

	for line in lines:
		toks = line.split()
		if br.match(toks[0]):
			continue
		if toks[0] in argset:
			argset[toks[0]].append(toks[2])
		else:
			argset[toks[0]] = [toks[2]]

	newline = []
	for line in lines:
		toks = line.split()
		if not br.match(toks[0]):
			continue
		if toks[1] in ["REF", "POS", "NEC", "NOT", "DRS"]:
			newline.append(line)
			continue
		if toks[1] in ["PRP", "DUPLEX", "IMP", "OR"]:
			if toks[1] == "DUPLEX":
				toks[1] = "DUP"
			newline.append(" ".join([toks[0]]+argset[toks[2]]))
			continue
		if toks[1] == "Pred":
			newline.append(" ".join([toks[0], handle_sense(argset[toks[2]][1]), argset[toks[2]][0]]))
			continue
		assert toks[2] in argset
		assert len(argset[toks[2]]) == 2
		newline.append(" ".join([toks[0], handle_rel(toks[1], context)] + argset[toks[2]]))
	return newline
#for root, dirs, files in os.walk("data"):
#	if len(root.split("/")) != 3:
#		continue
if __name__ == "__main__":
	if not os.path.exists(sys.argv[1]):
		pass
	else:
		print "###", " ".join(sys.argv)
		lines = []
		for line in open(sys.argv[1]):
			line = line.strip()
			if line == "" or line[0] == "#":
				continue
			lines.append(line)
		if len(lines) != 0:
			idx = lines.index("Graph")
			context = " ".join(lines[:idx])
			context = context.split()
			print "\n".join(lines[:idx])
			print "Graph"
			lines = pack(lines[idx+1:], context)
			print "\n".join(lines)
			print

