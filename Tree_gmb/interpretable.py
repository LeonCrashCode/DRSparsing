def illegal_struct(struct):
	if struct[0] not in ["DRS(" ,"SDRS("]:
		return True, "root error"
	for item in struct:
		if item in ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP(", ")"]:
			continue
		if re.match("^[PK][0-9]+\($", item):
			continue
		return True, "label error"
	cnt = 0
	for item in struct:
		if item == ")":
			cnt -= 1
		else:
			cnt += 1
	if cnt != 0:
		return True, "bracket error"

	for i in range(len(struct)):
		if re.match("^[PK][0-9]+\($", struct[i]):
			if i + 1 < len(struct) and (struct[i+1] in ["DRS(", "SDRS("]):
				continue
			else:
				return True, "PK should have box"
	
	stack = []
	for item in struct:
		if item[-1] == "(":
			stack.append([item[-1],0])
		else:
			b = stack[-1]
			stack.pop()
			if re.match("^P[0-9]+\($", b[0]):
				if stack[-1][0] == "DRS(":
					pass
				else:
					return True, "P should be in DRS"
			if re.match("^K[0-9]+\($", b[0]):
				if stack[-1][0] == "SDRS(":
                                        pass
                                else:
                                        return True, "K should be in SDRS"
				stack[-1][1] += 1
			if b[0] == "SDRS(":
				if b[1] >= 2:
					pass
				else:
					return True, "SDRS should have at least two segments"
	return False, "no message"

def illegal_rel(actn_v, rel):
	for item in rel:
		a = ""
		if item >= actn_v.size():
			a = "dummy("
		else:
			a = actn_v.totok(item)
		if a[-1] != "(" and a != ")":
			return True, "should be relation"
	if rel[-1] < actn_v.size() and actn_v.totok(rel[-1]) == ")":
		pass
	else:
		return True, "relation loop"
	return False, "no message"

def illegal_var(actn_v, rel, var):
	for item in var:
		a = actn_v.totok(item)
		if a == ")":
			pass
		elif a in ["CARD_NUMBER", "TIME_NUMBER"]:
			pass
		elif re.match("^[XESTPK][0-9]+$",a):
			pass
		else:
			return True, "should be variable"
	if len(var) != 2 and len(var) != 3:
		return True, "should have one or two variable"
	if var[-1] < actn_v.size() and actn_v.totok(var[-1]) == ")":
		pass
	else:
		return True, "variable loop"
	
	cansame = False
	
	if rel < actn_v.size() and actn_v.totok(rel) == "Equ(":
		cansame = True
	if cansame == False and len(var) == 3 and var[0] == var[1]:
		return True, "relation semantic loop"
	return False, "no message"


#structure
def bracket_legal(tree):
	# should be a tree
	cnt = 0
	for item in tree:
		if item[-1] == "(":
			cnt += 1
		elif item == ")":
			cnt -= 1
	return cnt == 0
def root_legal(tree):
	# root should be DRS or SDRS
	return tree[0] in ["DRS(", "SDRS("]

def pk(tree):
	# P( and K( should have only one box to represent its meaning
	stack = []
	for n in tree:
		if n[-1] == "(":
			stack.append([n,0])
		elif n == ")":
			b = stack[-1]
			stack.pop()
			if re.match("^[PK][0-9]+\($",stack[-1][0]):
				if b[0] not in ["SDRS(", "DRS("]:
					return False
				stack[-1][0] += 1
			elif re.match("^[PK][0-9]+\(", b[0]):
				if b[1] != 1:
					return False
	return True

def SDRSsegments(tree):
	# SDRS should only have segments, and at least two segments.
	stack = []
	for n in tree:
		if n[-1] == "(":
			stack.append([n,0])
		elif n == ")":
			b = stack[-1]
			stack.pop()
			if stack[-1][0] == "SDRS(":
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

def is_relation(tok):
	if tok[-1] != "(":
		return False
	if tol in ["DRS(", "SDRS(", "NOT(", "NEC(", "POS(", "IMP(", "OR(", "DUP("]:
		return False
	if re.match("^[PK][0-9]+\($",tok):
		return False
	return True
def is_variable(tok):
	if re.match("^[XESTPK][0-9]+$", tok):
		return True
	if tok in ["CARD_NUMBER", "TIME_NUMBER"]:
		return True
	return False
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
			if cnt == 40:
				return True
	return False

def NoSemanticLoop(tree):
	# should not assign two same variables a relation except Equ()
	for i in range(len(tree)):
		if is_relation(tree[i]) == False:
			continue
		if tree[i] == "Equ(":
			continue
		if i + 3 < len(tree) and is_variable(tree[i+1]) and is_variable(tree[i+2]) and tree[i+3] == ")":
			if tree[i+1] == tree[i+2]:
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
				stack.append([n, sdrs_idx, []])
				sdrs_idx += 1
			else:
				stack.append([n, -1, []])
		elif n == ")":
			b = stack[-1]
			stack.pop()
			if stack[-1][0] == "SDRS(":
				if re.match("^K[0-9]+\($",b[0]):
					stack[-1][-1].append(b[0][:-1])
			elif b[0] == "SDRS(":
				k_scoped[b[1]] = b[2]

	for n in tree:
		if n[-1] == "(":
				stack.append([n, []])
		elif n == ")":
			b = stack[-1]
			stack.pop()
			if is_relation(stack[-1][0]):
				if re.match("^K[0-9]+\($",b[0]):
					stack[-1][-1].append(b[0][:-1])
			elif b[0] == "SDRS(":
				k_scoped[b[1]] = b[2]
	return True


if __name__ == "__main__":
	#structure
