import os
import sys
import re


def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"":
		return True
	else:
		return False

def drg2oracle(lines):
	v = []
	idx = 0
	while idx < len(lines):
		l, c, r = lines[idx].split()
		if l not in v:
			print "ADD_NODE_"+l[0],
			v.append(l)
			for t in lines[idx:]:
				el, ec, er = t.split()
				if el == l and er in v:
					print "ADD_EDGE_OUT_"+ec+"_"+er,
				if er == l and el in v:
					print "ADD_EDGE_IN_"+ec+"_"+el,
			print
		if r not in v:
			if is_realword(r):
				print "ADD_NODE_"+r,
			else:
				print "ADD_NODE_"+r[0],
			v.append(r)
			for t in lines[idx:]:
				el, ec, er = t.split()
				if el == r and er in v:
					print "ADD_EDGE_OUT_"+ec+"_"+er,
				if er == r and el in v:
					print "ADD_EDGE_IN_"+ec+"_"+el,
			print
		idx += 1
			
if __name__ == "__main__":
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			idx = lines.index("Graph")
			print "\n".join(lines[:idx+1])
			drg2oracle(lines[idx+1:])
			print
			lines = []
		else:
			if line[0] == "#":
				continue
			lines.append(line)
			
