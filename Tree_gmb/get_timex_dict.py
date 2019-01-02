import os
import sys
import re

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()

v_p = re.compile("^[XESTPKB][0-9]+$")
d_p = re.compile("^DRS-[0-9]+\($")
pb = re.compile("^P[0-9]+\($")
kb = re.compile("^K[0-9]+\($")

def correct(tree):
	# Here we correct some weired things

	#e.g. :( K1 K2 )
	for i in range(len(tree)):
		if tree[i] == ":(" and tree[i+1][0] == "K":
			tree[i] = "THAT("
		if tree[i] == "-(" and tree[i+1][0] == "K":
			tree[i] = "THAT("
		if tree[i] == "((" and tree[i+1][0] == "K":
			tree[i] = "THAT("

def bracket2list(bracket):
	stack = []
	for tok in bracket:
		if tok[-1] == "(":
			stack.append([tok])
		elif tok == ")":
			if len(stack) != 1:
				back = stack.pop()
				stack[-1].append(back)
		else:
			stack[-1].append(tok)
	assert len(stack) == 1
	return stack[0]

def tree2ground(tree):
	v = ["X","E","S","T","B","P","K"]
	vl = [ [] for i in range(7)]

	for i in range(len(tree)):
		tok = tree[i]
		if pb.match(tok):
			assert tok[:-1] not in vl[-2]
			vl[-2].append(tok[:-1])
			assert v_p.match(tree[i+1]) and tree[i+1][0] == "B"
			if tree[i+1] != "B0" and tree[i+1] not in vl[-3]:
				vl[-3].append(tree[i+1])
		if kb.match(tok):
			assert tok[:-1] not in vl[-1]
			vl[-1].append(tok[:-1])
		if tok in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			assert v_p.match(tree[i+1]) and tree[i+1][0] == "B"
			if tree[i+1] != "B0" and tree[i+1] not in vl[-3]:
				vl[-3].append(tree[i+1])
	#print vl
	#exit(1)
	root = bracket2list(tree)

	def is_struct(tok):
		if tok in ["DRS(", "SDRS(", "NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			return True
		if d_p.match(tok):
			return True
		if re.match("^[PK][0-9]+\($", tok):
			return True
		return False

	def travel(root):
		#global v
		#global vl
		parent = root[0]
		child = root[1:]
		if parent == "SDRS(":
			for c in child:
				if not is_struct(c[0]):
					for cc in c[1:]:
						if v_p.match(cc):
							idx = v.index(cc[0])
							if cc not in vl[idx]:
								vl[idx].append(cc)
			for c in child:
				if is_struct(c[0]):
					travel(c)
		elif parent == "DRS(" or d_p.match(parent):
			for c in child:
				if not is_struct(c[0]):
					assert c[1][0] == "B"
					assert v_p.match(c[1]) and c[1][0] == "B"
					idx = v.index(c[1][0])
					if c[1] not in vl[idx] and c[1] != "B0":
						vl[idx].append(c[1])
					for cc in c[2:]:
						if v_p.match(cc):
							idx = v.index(cc[0])
							if cc not in vl[idx]:
								vl[idx].append(cc)
			for c in child:
				if is_struct(c[0]):
					travel(c)
		elif pb.match(parent) or parent in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			for c in child[1:]:
				travel(c)
		elif kb.match(parent):
			for c in child:
				travel(c)
		
	travel(root)
	correct(tree)

	# normalize variables
	i = 0
	cur = 0
	while i < len(tree):
		tok = tree[i]
		if pb.match(tok):
			idx = vl[-2].index(tok[:-1])
			tree[i] = "P"+str(idx+1)+"("
		elif kb.match(tok):
			idx = vl[-1].index(tok[:-1])
			tree[i] = "K"+str(idx+1)+"("
		elif v_p.match(tok) and tok != "B0":
			vl_idx = v.index(tok[0])
			idx = vl[vl_idx].index(tok)
			tree[i] = v[vl_idx] + str(idx+1)
		i += 1

	# normalize scoped K and P
	p_n = 0
	k_n = 0
	for i in range(len(tree)):
		tok = tree[i]
		if pb.match(tok):
			assert int(tok[1:-1]) == p_n + 1
			#tree[i] = "@P("
			p_n += 1
		if kb.match(tok):
			assert int(tok[1:-1]) == k_n + 1
			#tree[i] = "@K("
			k_n += 1

	#print tree
	n_tree = []
	stack = []
	i = 0
	while i < len(tree):
		t = tree[i]
		if v_p.match(t):
			#n_tree.append(t)
			i += 1
		elif t in ["DRS(", "SDRS("]:
			#n_tree.append(t)
			stack.append(-1)
			i += 1
		elif d_p.match(t):
			#n_tree.append(t)
			stack.append(int(t[4:-1])) #DRS-10(
			i += 1
		elif pb.match(t) or kb.match(t): 
			#n_tree.append(t)
			stack.append(-1)
			i += 1
		elif t == ")":
			#n_tree.append(t)
			stack.pop()
			i += 1
		elif t in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			#n_tree.append(t)
			stack.append(-1)
			i += 1
		elif t == "Named(": #Named( B0 X1 $1[John] )
			assert stack[-1] != -1
			idx = tree[i:].index(")")
			i = i + idx + 1
		elif t == "Card(":
			assert stack[-1] != -1
			idx = tree[i:].index(")")
			i = i + idx + 1
		elif re.match("^T[yx][mx][dx]\($", t):
			assert stack[-1] != -1
			idx = tree[i:].index(")")
			n_tree.append(t)
			n_tree.append(tree[i+1])
			n_tree.append(tree[i+2])

			indexs = []
			exp = ""
			for item in tree[i+3:i+idx-1]:
				assert re.match("^\$[0-9]+$", item)
				indexs.append(item)
			assert tree[i+idx-1][0] == "[" and tree[i+idx-1][-1] == "]"
			exp = tree[i+idx-1][1:-1]

			cons = []
			for index in indexs:
				cons.append(words[stack[-1]][int(index[1:])])
			cons = "~".join(cons) + " ||| " + t[:-1]

			if cons not in timex_dict:
				timex_dict[cons] = exp
			else:
				assert timex_dict[cons] == exp
			i = i + idx + 1
		elif t[-1] == "(":
			idx = tree[i:].index(")")
			i = i + idx + 1
		else:
			assert False, "unrecognized format"


def filter(illform, tree):
	#filter two long sentences, actually only one
	"""
	cnt = 0
	for item in tree:
		if item == "DRS(":
			cnt += 1
	if cnt >= 21:
		return True
	"""
	for item in illform:
		if item in tree:
			return True
	return False

if __name__ == "__main__":
	
	illform = []
	if os.path.exists("manual_correct2"):
		for line in open("manual_correct2"):
			line = line.strip()
			if line == "" or line[0] == "#":
				continue
			illform.append(line.split()[0])

	global words
	global timex_dict
	timex_dict = {}
	lines = []
	filename = ""
	for line in open(args.input):
		line = line.strip()
		if line == "":
			idx = lines.index("TREE")
			words = lines[:idx]
			for i in range(len(words)):
				words[i] = words[i].split()
			tree = lines[idx+1].split()
			if filter(illform, tree):
				lines = []
				continue
			tree2ground(tree)
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-1]
				continue
			lines.append(line)
	keys = timex_dict.keys()
	keys.sort()
	for key in keys:
		print key, timex_dict[key]

			
