import os
import sys
import re


def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"":
		return True
	else:
		return False

def add(k,d):
	if k in d:
		d[k] += 1
	else:
		d[k] = 1
gc = {}
def global_count(lemmas, lines):
	lem = lemmas.split()
	idx = 0
	v = []
	while idx < len(lines):
		l, c, r = lines[idx].split()
		if is_realword(r) and (r not in v) and r[1:-1] not in lem:
			add(r,gc)
			v.append(r)
		idx += 1

def rare(lemmas, k):
	if is_realword(k) and (k[1:-1] not in lemmas) and gc[k] <= 0:
		return "\"RARE\""
	return k


def drg2oracle(lemmas, lines):
	lem = lemmas.split()
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
					print "ADD_EDGE_OUT_"+rare(lem, ec)+"_"+rare(lem, er),
				if er == l and el in v:
					print "ADD_EDGE_IN_"+rare(lem, ec)+"_"+rare(lem, el),
			print
		if r not in v:
			if is_realword(r):
				print "ADD_NODE_"+rare(lem, r),
			else:
				print "ADD_NODE_"+r[0],
			v.append(r)
			for t in lines[idx:]:
				el, ec, er = t.split()
				if el == r and er in v:
					print "ADD_EDGE_OUT_"+rare(lem, ec)+"_"+rare(lem, er),
				if er == r and el in v:
					print "ADD_EDGE_IN_"+rare(lem, ec)+"_"+rare(lem, el),
			print
		idx += 1
			
if __name__ == "__main__":
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			idx = lines.index("Graph")
			global_count(lines[idx-1], lines[idx+1:])
			lines = []
		else:
			if line[0] == "#":
				continue
			lines.append(line)

	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			idx = lines.index("Graph")
			print "\n".join(lines[:idx+1])
			drg2oracle(lines[idx-1], lines[idx+1:])
			print
			lines = []
		else:
			if line[0] == "#":
				continue
			lines.append(line)
			
