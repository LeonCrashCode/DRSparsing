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
	"""	
	B = 1
	for i in range(len(tree)):
		if tree[i] in ["@P(", "POS(", "NEC(", "NOT(", "IMP(", "OR(", "DUP("]:
			if tree[i+1] == "B"+str(B):
				tree[i+1] = "@B"
				B += 1
	X = E = S = T = 1
	for i in range(len(tree)):
		if re.match("^X[0-9]+$", tree[i]):
			assert int(tree[i][1:]) <= X
			if tree[i] == "X"+str(X):
				tree[i] = "@X"
				X += 1
		elif re.match("^E[0-9]+$", tree[i]):
			assert int(tree[i][1:]) <= E
			if tree[i] == "E"+str(E):
				tree[i] = "@E"
				E += 1
		elif re.match("^S[0-9]+$", tree[i]):
                        assert int(tree[i][1:]) <= S
                        if tree[i] == "S"+str(S):
                                tree[i] = "@S"
                                S += 1
		elif re.match("^T[0-9]+$", tree[i]):
                        assert int(tree[i][1:]) <= T
                        if tree[i] == "T"+str(T):
                                tree[i] = "@T"
                                T += 1
		elif re.match("^B[0-9]+$", tree[i]):
                        assert int(tree[i][1:]) <= B
                        if tree[i] == "B"+str(B):
                                tree[i] = "@B"
                                B += 1
	"""
	out_action.write(" ".join(tree)+"\n")	
		

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
	"""
	for line in open("illform"):
		line = line.strip()
		if line == "":
			continue
		illform.append(line.split()[-2])
	"""
	if os.path.exists("manual_correct2"):
		for line in open("manual_correct2"):
			line = line.strip()
			if line == "" or line[0] == "#":
				continue
			illform.append(line.split()[0])
	
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
			if filter(illform, tree):
				lines = []
				continue

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

			
