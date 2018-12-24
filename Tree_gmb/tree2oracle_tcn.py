import os
import sys
import re

v_p = re.compile("^[XESTPK][0-9]+$")
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

def tree2oracle(tree, out_action):
	for i in range(len(tree)):
		if pb.match(tree[i]):
			tree[i] = "@P("
		elif kb.match(tree[i]):
			tree[i] = "@K("
	correct(tree)
	out_action.write(" ".join(tree)+"\n")

if __name__ == "__main__":
	
	illform = []
	"""
	for line in open("illform"):
		line = line.strip()
		if line == "":
			continue
		illform.append(line.split()[-2])
	"""
	
	lines = []
	filename = ""
	out_input = open(sys.argv[1]+".oracle.in", "w")
	out_action = open(sys.argv[1]+".oracle.out", "w")
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":

			idx = lines.index("TREE")
			
			words = " ||| ".join(lines[:idx])

			tree = lines[idx+1].split()
			out_input.write(words + "\n\n")
			tree2oracle(tree, out_action)
			out_input.flush()
			out_action.flush()
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-1]
				continue
			lines.append(line)
	out_input.close()
	out_action.close()

			
