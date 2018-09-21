import sys
import os
import xml.etree.ElementTree as ET
import re

br = re.compile("^b[0-9]+?$")


def pack(lines):
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
		assert toks[2] in argset
		assert len(argset[toks[2]]) == 2
		newline.append(" ".join([toks[0], toks[1]] + argset[toks[2]]))
	return newline
#for root, dirs, files in os.walk("data"):
#	if len(root.split("/")) != 3:
#		continue
if __name__ == "__main__":
	print "###", " ".join(sys.argv)
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "" or line[0] == "#":
			continue
		lines.append(line)
	idx = lines.index("Graph")
	print "\n".join(lines[:idx])
	print "Graph"
	lines = pack(lines[idx+1:])
	print "\n".join(lines)
	print

