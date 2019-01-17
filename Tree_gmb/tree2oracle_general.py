import os
import sys
import re

from patterns import *



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

def tree2oracle(tree, out_action, domain):

	v = ["X","E","S","T","B","P","K"]
	vl = [ [] for i in range(7)]

	def add(item):
		idx = v.index(item[0])
		if item not in vl[idx]:
			vl[idx].append(item)
	def exist(item):
		idx = v.index(item[0])
		return item in vl[idx]
	def getn(item):
		if item == "B0":
			return -1
		idx = v.index(item[0])
		if item in vl[idx]:
			return vl[idx].index(item)
		else:
			return -10000
	#B maps travel for p and other scoped symbol. i.e. NEC, NOT, POS, OR, DUP, IMP

	tmpl  = []
	for i, tok in enumerate(tree):
		if tok[-1] == "(":
			if drs_n.match(tok):
				assert vb.match(tree[i+1])
				if tree[i+1] not in tmpl:
					tmpl.append(tree[i+1])

	box_stack = []
	for i, tok in enumerate(tree):
		if tok[-1] == "(":
			if drs_n.match(tok):
				assert vb.match(tree[i+1])
				box_stack.append(tree[i+1])
				add(tree[i+1])
			else:
				if bp.match(tok) or tok in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
					if tree[i+1] == box_stack[-1]:
						pass
					elif tree[i+1] in vl[4]:
						pass
					elif tree[i+1] not in vl[4] and tree[i+1] not in tmpl:
						print tok
						pass
					else:
						assert False, "lookahead"
					#if tree[i+1] == box_stack[-1]:
					#	tree[i+1] = "B0"
					#else:
					#	add(tree[i+1])
				box_stack.append(-1)
		elif tok == ")":
			box_stack.pop()
	assert len(box_stack) == 0

	return 
	for tok in tree:
		if bp.match(tok):
			add(tok[:-1])
		elif bk.match(tok):
			add(tok[:-1])

	def is_struct(tok):
		if tok in ["SDRS(", "NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			return True
		if drs_n.match(tok):
			return True
		if bp.match(tok) or bk.match(tok):
			return True
		return False


	n_tree = []
	def travel(root):
		parent = root[0]
		n_tree.append(parent)
		child = root[1:]
		if parent == "SDRS(":
			for c in child:
				if not is_struct(c[0]):
					n_tree.append(c[0])
					for cc in c[1:]:
						n_tree.append("(K,"+cc+")")
						assert vk.match(cc)
						add(cc)
					n_tree.append(")")
			for c in child:
				if is_struct(c[0]):
					travel(c)
		elif drs_n.match(parent):
			box_stack.append(child[0])
			child = child[1:]
			for c in child:
				if not is_struct(c[0]):
					n_tree.append(c[0])
					assert vb.match(c[1])
					if c[1] == box_stack[-1]:
						n_tree.append("B0")
					else:
						n_tree.append(c[1])
						#add(c[1])
					i = 2
					while i < len(c):
						if vall.match(c[i]):
							if exist(c[i]) or vp.match(c[i]):
								c[i] = "("+c[i][0]+","+c[i]+")"
							else:
								add(c[i])
								if c[i+1] == c[1]:
									c[i] = "("+c[i][0]+","+c[i]+","+"B0"+")"
								else:
									#add(c[i+1])
									c[i] = "("+c[i][0]+","+c[i]+","+c[i+1]+")"
							n_tree.append(c[i])
							i += 2
						else:
							n_tree.append(c[i])
							i += 1
					n_tree.append(")")
			for c in child:
				if is_struct(c[0]):
					travel(c)
			box_stack.pop()
		elif bp.match(parent) or parent in ["NOT(", "POS(", "NEC(", "IMP(", "OR(", "DUP("]:
			n_tree.append(child[0])
			for c in child[1:]:
				travel(c)
		elif bk.match(parent):
			for c in child:
				travel(c)
		else:
			assert False, "only travel for non-terminal nodes"
		n_tree.append(")")
	root = bracket2list(tree)
	travel(root)
	tree = n_tree
	print vl[4]
	#print tree
	# normalize variable
	for i,_ in enumerate(tree):
		tok = tree[i]
		if vb.match(tok):
			idx = getn(tok)
			tree[i] = "B"+str(idx+1)
		if tok[0] == "(" and tok[-1] == ")":
			tok = tok[1:-1].split(",")
			idx = getn(tok[1])
			tok[1] = tok[0]+str(idx+1)
			if len(tok) == 3:
				idx = getn(tok[2])
				tok[2] = "B"+str(idx+1)
			tree[i] = "("+",".join(tok)+")"

	print tree
	# normalize scoped K and P
	p_n = 0
	k_n = 0
	for i in range(len(tree)):
		tok = tree[i]
		if bp.match(tok):
			assert int(tok[1:-1]) == p_n + 1
			tree[i] = "@P("
			p_n += 1
		if bk.match(tok):
			assert int(tok[1:-1]) == k_n + 1
			tree[i] = "@K("
			k_n += 1
	
	# keep index and remove [***]
	n_tree = []
	for i in range(len(tree)):
		if tree[i][0] == "[" and tree[i][-1] == "]":
			pass
		elif re.match("^\$[0-9]+\[.+\]\($", tree[i]):
			idx = tree[i].index("[")
			n_tree.append(tree[i][:idx]+"(")
		elif re.match("^\$[0-9]+\[.+\]$", tree[i]): 	
			idx = tree[i].index("[")
			n_tree.append(tree[i][:idx])
		else:
			n_tree.append(tree[i])
	out_action.write(" ".join(n_tree)+"\n")
	

if __name__ == "__main__":
	
	
	lines = []
	filename = ""
	out_input = open(sys.argv[1]+".oracle.in", "w")
	out_action = open(sys.argv[1]+".oracle.out", "w")
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":

			idx = lines.index("VARIABLE")
			words = " ||| ".join(lines[:idx])

			idx = lines.index("TREE")
			domain = {}
			for item in lines[idx-1].split():
				item = item.split(":")
				domain[item[0]] = item[1]
			tree = lines[idx+1].split()

			out_input.write(words + "\n\n")
			tree2oracle(tree, out_action, domain)
			out_input.flush()
			out_action.flush()
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-1]
				print filename
				continue
			lines.append(line)
	out_input.close()
	out_action.close()

			
