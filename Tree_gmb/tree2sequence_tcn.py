import os
import sys
import re

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--timex", default='exp', help="exp, span, span_index, constant")
parser.add_argument("--card", default='exp', help="exp, span, span_index, constant")
parser.add_argument("--name", default='exp', help="exp, span, span_index")
parser.add_argument("--pred", default='exp', help="exp, span, span_index")

parser.add_argument("--card-span-connect", default='~', help="it connects two spans, default is ~")
parser.add_argument("--timex-span-connect", default='~', help="it connects two spans, default is ~")
parser.add_argument("--name-span-connect", default='~', help="it connects two spans, default is ~")
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
			n_tree.append(t)
			i += 1
		elif t in ["DRS(", "SDRS("]:
			n_tree.append(t)
			stack.append(-1)
			i += 1
		elif d_p.match(t):
			n_tree.append(t)
			stack.append(int(t[4:-1])) #DRS-10(
			i += 1
		elif pb.match(t) or kb.match(t): 
			n_tree.append(t)
			stack.append(-1)
			i += 1
		elif t == ")":
			n_tree.append(t)
			stack.pop()
			i += 1
		elif t in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			n_tree.append(t)
			stack.append(-1)
			i += 1
		elif t[0:5]== "Named" and t[-1] == "(": #Named( B0 X1 $1 [John] )
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

			if args.card == "exp":
				n_tree.append(exp)
			elif args.card == "span_index":
                                n_tree.append(args.name_span_connect.join(indexs))
                        elif args.card == "span":
                                cons = []
                                for index in indexs:
                                        cons.append(words[stack[-1]][int(index[1:])])
                                n_tree.append(args.name_span_connect.join(cons))
			else:
				assert False, "unrecognized option for --name"
			n_tree.append(")")
			i = i + idx + 1
		elif t == "Card(":
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

			if args.card == "exp":
				n_tree.append(exp)
			elif args.card == "span_index":
				n_tree.append(args.card_span_connect.join(indexs))
			elif args.card == "span":
				cons = []
				for index in indexs:
					cons.append(words[stack[-1]][int(index[1:])])
				n_tree.append(args.card_span_connect.join(cons))
			elif args.card == "constant":
				n_tree.append("CARD_NUMBER")
			else:
				assert False, "unrecognized option for --card"
			n_tree.append(")")
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

			if args.timex == "exp":
				n_tree.append(exp)
			elif args.timex == "span_index":
				n_tree.append(args.timex_span_connect.join(indexs))
			elif args.timex == "span":
				cons = []
				for index in indexs:
					cons.append(words[stack[-1]][int(index[1:])])
				n_tree.append(args.timex_span_connect.join(cons))
			elif args.timex == "constant":
				n_tree.append("TIME_NUMBER")
			else:
				assert False, "unrecognized option for --timex"
			n_tree.append(")")
			i = i + idx + 1
		elif t[-1] == "(":
			idx = tree[i:].index(")")
			#Rel( B0 X1 X2 )
			if idx == 4 and all([v_p.match(x) for x in tree[i+1:i+idx]]):
				assert stack[-1] != -1
				if re.match("^\$[0-9]+\[.+\]\($", t):
					j = t.index("[")
					n_tree.append(t[j+1:-2]+"(")
				else:
					n_tree.append(t)
				n_tree += tree[i+1:i+idx]
			#Rel( B0 X1 n.00 )
			elif idx == 4 and all([v_p.match(x) for x in tree[i+1:i+idx-1]]) and re.match("^[anvr]\.[0-9][0-9]$", tree[i+idx-1]):
				assert stack[-1] != -1
				if re.match("^\$[0-9]+\[.+\]\($", t):
					j = t.index("[")
					if args.pred == "exp":
						n_tree.append(t[j+1:-2]+"(")
					elif args.pred == "span":
						n_tree.append(words[stack[-1]][int(t[1:j])]+"(")
					elif args.pred == "span_index":
						n_tree.append(t[:j]+"(")
					else:
						assert False, "unrecognized option for --pred"
				n_tree += tree[i+1:i+idx]
			#CONTINUATION( K1 K2 )
			elif idx == 3 and all([v_p.match(x) for x in tree[i+1:i+idx]]):
				assert t.isupper()
				n_tree += tree[i:i+idx]
			else:
				assert False, "unrecognized format"

			n_tree.append(")")

			i = i + idx + 1
		else:
			assert False, "unrecognized format"
	print " ".join(n_tree)

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

			print " ||| ".join([" ".join(w) for w in words])
			#tree2ground(tree)
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-1]
				continue
			lines.append(line)


			
