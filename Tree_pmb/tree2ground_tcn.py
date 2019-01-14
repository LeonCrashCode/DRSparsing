import os
import sys
import re

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-t", "--type", default="exp", help="exp | span | span_index")
parser.add_argument("-c", "--connect", default='~', help="it connects two spans, default is ~")
args = parser.parse_args()

v_p = re.compile("^[XESTPKB][0-9]+$")
d_p = re.compile("^DRS-[0-9]+\($")
pb = re.compile("^P[0-9]+\($")
kb = re.compile("^K[0-9]+\($")

def is_variable(v):
	if v_p.match(v):
		return True
	if v in ["\"speaker\"", "\"hearer\"", "\"now\"", "\"?\""]:
		return True
	return False

def lookahead(t, b, v, s):
	if len(t) < 4:
		return False

	if re.match("^\$[0-9]+\[.+\]\($",t[0]) and t[1] == b and t[2] == v and t[3] == s:
		return True
	return False
			
def tree2ground(tree):

	#print tree
	n_tree = []
	stack = []
	i = 0
	while i < len(tree):
		t = tree[i]
		if re.match("^B[0-9]+$", t):
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
		elif t[0:5]== "Named" and t[-1] == "(":
			#Named( B0 X1 $1 [John] )
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

			if args.type == "exp":
				n_tree.append('\"'+exp+'\"')
			elif args.type == "span_index":
				n_tree.append('\"'+args.connect.join(indexs)+'\"')
			elif args.type == "span":
				cons = []
				for index in indexs:
					cons.append('\"'+words[stack[-1]][int(index[1:])]+'\"')
				n_tree.append(args.connect.join(cons))
			else:
				assert False, "unrecognized option for --type"
			n_tree.append(")")
			i = i + idx + 1
		elif t[-1] == "(" and re.match("[anvr]\.[0-9]{2}", tree[i+3]):
			idx = tree[i:].index(")")
			if re.match("^\$[0-9]+\[.+\]\($",t):
				# $0[rel0]( B0 X1 sense )
				j = t.index("[")
				indexs = [t[0:j]]
				exps = [t[j+1:-2]]
				while lookahead(tree[i+idx+1:], tree[i+1], tree[i+2], tree[i+3]):
					t = tree[idx+1]
					j = t.index("[")
					indexs.append(t[0:j])
					exps.append(t[j+1:-2])
					idx += tree[i+idx+1:].index(")")
				if args.type == "exp":
					n_tree.append(args.connect.join(exps)+"(")
				elif args.type == "span_index":
					n_tree.append(args.connect.join(indexs)+"(")
				elif args.type == "span":
					cons = []
					for index in indexs:
						cons.append(words[stack[-1]][int(index[1:])])
					n_tree.append(args.name_span_connect.join(cons)+"(")
				else:
					assert False, "unrecognized option for --type"
				n_tree.append(tree[i+1])
				n_tree.append(tree[i+2])
				n_tree.append(tree[i+3])
				n_tree.append(")")
			else:
				# pred( B0 X1 sense )
				n_tree.append(tree[i])
				n_tree.append(tree[i+1])
				n_tree.append(tree[i+2])
				n_tree.append(tree[i+3])
				n_tree.append(")")
			i = i + idx + 1

		elif t[-1] == "(":
			idx = tree[i:].index(")")
			#print tree[i:i+idx+1]
			#Rel( B0 X1 X2 )
			if idx == 4 and all([is_variable(x) for x in tree[i+1:i+idx]]):
				assert stack[-1] != -1
				if re.match("^\$[0-9]+\[.+\]\($", t):
					j = t.index("[")
					n_tree.append(t[j+1:-2]+"(")
				else:
					n_tree.append(t)
				n_tree += tree[i+1:i+idx]
			#Rel( B0 X1 ... )
			elif idx == 4 and all([is_variable(x) for x in tree[i+1:i+3]]):
				assert stack[-1] != -1
				if re.match("^\$[0-9]+\[.+\]\($", t):
					j = t.index("[")
					n_tree.append(t[j+1:-2]+"(")
				else:
					n_tree.append(t)
				n_tree += tree[i+1:i+3]
				
				indexs = []
				exps = []
				for item in tree[i+3:]:
					if re.match("^\$[0-9]+$", item):
						indexs.append(item)
					elif item[0] == "[" and item[-1] == "]":
						exps.append(item)
					else:
						assert False, "unrecognized format"

				if args.type == "exp":
					n_tree.append(args.connect.join(exps))
				elif args.type == "span_index":
					n_tree.append(args.connect.join(indexs))
				elif args.type == "span":
					cons = []
					for index in indexs:
						cons.append(words[stack[-1]][int(index[1:])])
					n_tree.append(args.name_span_connect.join(cons))
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


if __name__ == "__main__":
	

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
			tree2ground(tree)
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-1]
				continue
			lines.append(line)


			
