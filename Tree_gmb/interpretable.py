import sys
import re
#tool function
def is_p_scope(tok):
	return re.match("^P[0-9]+\($",tok)
def is_k_scope(tok):
	return re.match("^K[0-9]+\($",tok)
def is_relation(tok):
	if tok[-1] != "(":
		return False
	if tok in ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP("]:
		return False
	if is_p_scope(tok):
		return False
	if is_k_scope(tok):
		return False
	return True
def is_variable(tok):
	if re.match("^[XESTPK][0-9]+$", tok):
		return True
	if tok in ["CARD_NUMBER", "TIME_NUMBER"]:
		return True
	return False

#structure
def bracket(tree):
	# should be a tree
	cnt = 0
	for item in tree:
		if item[-1] == "(":
			cnt += 1
		elif item == ")":
			cnt -= 1
	return cnt == 0
def root(tree):
	# root should be DRS or SDRS
	return tree[0] in ["DRS(", "SDRS("]
def recursive(tree):
	# structure should be recursively constructed
	stack = []
	for n in tree:
		#print n
		if n[-1] == "(":
			stack.append(n)
		elif n == ")":
			if len(stack) == 0:
				return True
			b = stack.pop()
			if len(stack) == 0:
				continue
			if b == "DRS(" or b == "SDRS(":
				if stack[-1] in ["NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP("]:
					pass
				elif is_p_scope(stack[-1]) or is_k_scope(stack[-1]):
					pass
				else:
					return False
			else:
				if stack[-1] != "DRS(" and stack[-1] != "SDRS(":
					return False
	return True

def sixscope(tree):
	stack = []
	for n in tree:
		if n[-1] == "(":
			stack.append([n,0])
		elif n == ")":
			if len(stack) == 0:
				return True
			b,i = stack.pop()
			if len(stack) == 0:
				continue
			if b == "DRS(" or b == "SDRS(":
				if stack[-1][0] in ["NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP("]:
					stack[-1][1] += 1
			if b in ["NOT(", "NEC(", "POS("]:
				if i != 1:
					return False
			if b in ["IMP(", "OR(", "DUP("]:
				if i != 2:
					return False
	return True	 

def pk(tree):
	# P( and K( should have only one box to represent its meaning
	stack = []
	for n in tree:
		if n[-1] == "(":
			stack.append([n,0])
		elif n == ")":
			if len(stack) == 0:
				return True
			b = stack.pop()
			if len(stack) == 0:
				continue
			if is_p_scope(stack[-1][0]) or is_k_scope(stack[-1][0]):
				if b[0] not in ["SDRS(", "DRS("]:
					return False
				stack[-1][1] += 1
			elif is_p_scope(b[0]) or is_k_scope(b[0]):
				if b[1] != 1:
					return False
	return True
def pk_only(tree):
	# P( and K( scope's names should be identified.
	scopes = {}
	for n in tree:
		if is_p_scope(n) or is_k_scope(n):
			if n in scopes:
				return False
			scopes[n] = 1
	return True
def SDRSsegment(tree):
	# SDRS should only have segments, and at least two segments.
	stack = []
	for n in tree:
		if n[-1] == "(":
			stack.append([n,0])
		elif n == ")":
			if len(stack) == 0:
				return True
			b = stack.pop()
			if len(stack) != 0 and stack[-1][0] == "SDRS(":
				if re.match("^K[0-9]+\($",b[0]):
					stack[-1][1] += 1
					pass
				elif is_relation(b[0]):
					pass
				else:
					return False
			elif b[0] == "SDRS(":
				if b[1] < 2:
					return False
	return True
def NoEmpty(tree):
	# there should no empty box, and relations which have no variables
	for i in range(len(tree)-1):
		if tree[i][-1] == "(" and tree[i+1] == ")":
			return False
	return True
def VariableCount(tree):
	# relation should only have one or two variables
	for i in range(len(tree)):
		if is_relation(tree[i]) == False:
			continue
		if i + 2 < len(tree) and is_variable(tree[i+1]) and tree[i+2] == ")":
			pass
		elif i + 3 < len(tree) and is_variable(tree[i+1]) and is_variable(tree[i+2]) and tree[i+3] == ")":
			pass
		else:
			return False
	return True
#Semantics
def NoRelationLoop(tree):
	# should not produce relation unlimitedly 
	for n in tree:
		if n[-1] == "(" and (n not in ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP("] ):
			cnt = 0
			for nn in tree:
				if n == nn:
					cnt += 1
			if cnt > 30:
				return False
	return True
def get_set(tok, set):
	for i in range(len(set)):
		if tok in set[i]:
			return i
	return None
def issameset(tok1, tok2, set):
	if tok1 in ["CARD_NUMBER", "TIME_NUMBER"]:
		return False
	if tok2 in ["CARD_NUMBER", "TIME_NUMBER"]:
		return False
	for s in set:
		if (tok1 in s) and (tok2 in s):
			return True
	return False
def NoSemanticLoop(tree):
	# should not assign two same variables a relation except Equ()
	equ = []
	for i in range(len(tree)):
		if is_relation(tree[i]) == False:
			continue
		if tree[i] == "Equ(" and i + 3 < len(tree) and is_variable(tree[i+1]) and is_variable(tree[i+2]) and tree[i+3] == ")":
			set1_idx = get_set(tree[i+1], equ)
			set2_idx = get_set(tree[i+2], equ)
			if set1_idx == None and set2_idx == None:
				equ.append([tree[i+1], tree[i+2]])
			elif set1_idx == None:
				equ[set2_idx].append(tree[i+1])
			elif set2_idx == None:
				equ[set1_idx].append(tree[i+2])
			else:
				equ[set1_idx] += equ[set2_idx]
				equ.remove(equ[set2_idx])

	for i in range(len(tree)):
		if is_relation(tree[i]) == False:
			continue
		if tree[i] == "Equ(":
			continue
		if i + 3 < len(tree) and is_variable(tree[i+1]) and is_variable(tree[i+2]) and tree[i+3] == ")":
			if (tree[i+1] == tree[i+2]) or issameset(tree[i+1], tree[i+2], equ):
				return False
	return True
def scopedSegments(tree):
	# an SDRS only assign relations onto segments, which are scoped in current SDRS
	stack = []
	k_scoped = {}
	sdrs_idx = 0
	for n in tree:
		if n[-1] == "(":
			if n == "SDRS(":
				stack.append([sdrs_idx, []])
				sdrs_idx += 1
			elif is_k_scope(n):
				stack.append([1000+int(n[1:-1]), []])
			else:
				stack.append([-1, []])
		elif n == ")":
			if len(stack) == 0:
				return True
			b = stack.pop()
			if b[0] != -1 and b[0] < 1000:
				k_scoped[b[0]] = b[1]
			if len(stack) > 0:
				stack[-1][1] = stack[-1][1] + b[1]
			if len(stack) > 0 and b[0] >= 1000:
				stack[-1][1].append("K"+str(b[0]%1000))

	sdrs_idx = 0
	for n in tree:
		if n[-1] == "(":
			if n == "SDRS(":
				stack.append([sdrs_idx, []])
				sdrs_idx += 1
			else:
				stack.append([-1, []])
		elif n == ")":
			if len(stack) == 0:
				return True
			b = stack.pop()
			if len(stack) > 0 and stack[-1][0] != -1:
				stack[-1][1] = stack[-1][1] + b[1]
			if b[0] != -1:
				for k in b[1]:
					if k not in k_scoped[b[0]]:
						return False
		else:
			stack[-1][1].append(n)
	return True

if __name__ == "__main__":
	n = 0

	fun1 = [bracket, root, recursive, pk, pk_only, SDRSsegment, NoEmpty, VariableCount, sixscope]
	#fun2 = [NoRelationLoop, NoSemanticLoop, scopedSegments]
	fun2 = [NoRelationLoop, scopedSegments]
	count1 = [0 for i in range(len(fun1))]
	count2 = [0 for i in range(len(fun2))]
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			continue
		line = line.split()
		#print n
		n += 1

		for i, fun in enumerate(fun1):
			if fun(line) == False:
				count1[i] += 1
		for i, fun in enumerate(fun2):
			if fun(line) == False:
				if fun.__name__ == "NoSemanticLoop":
					print " ".join(line)
					exit(1)
				count2[i] += 1

	for i, err in enumerate(count1):
		print fun1[i].__name__, ":", err

	for i, err in enumerate(count2):
		print fun2[i].__name__, ":", err

