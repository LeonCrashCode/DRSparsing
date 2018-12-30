import sys
import re
import argparse
import types

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
#parser.add_argument("--novar", action='store_true')
#parser.add_argument("--norel", action='store_true')
#parser.add_argument("--partial", action='store_true')
args = parser.parse_args()

special = ["NOT(", "POS(", "NEC(", "OR(","IMP(", "DUP("]

drs = re.compile("^DRS-[0-9]+\($")

def get_b(stack, b):
	if b != "B0":
		return b.lower()
	for item in stack[::-1]:
		if type(item) == types.ListType:
			return item[0]

def get_sent(stack):
	for item in stack[::-1]:
                if type(item) == types.ListType and item[1] != None:
                        return item[1]
	return None

def import_sent(s_idx, w_idx):
	if re.match("^\$[0-9]+$", w_idx):
		assert s_idx != None
		w_idx = w_idx[1:]
		assert len(w_idx) <= 3
		assert len(s_idx) <= 2
		return "$"+"0" * (2-len(s_idx)) + s_idx +"," + "0" * (3 - len(w_idx)) + w_idx
	else:
		return w_idx
def process(tokens):

	p = 1
	k = 1
	for i in range(len(tokens)):
		if tokens[i] == "@P(":
			tokens[i] = "P"+str(p)+"("
			p += 1
		elif tokens[i] == "@K(":
			tokens[i] = "K"+str(k)+"("
			k += 1
	
	i = 0
	b = 1001
	b_n = []
	while i < len(tokens):
		if tokens[i] == "SDRS(":
			b_n.append(["b"+str(b), None])
			b += 1
		elif drs.match(tokens[i]):
			b_n.append(["b"+str(b), str(int(tokens[i][4:-1])+1)])
			b += 1
		else:
			b_n.append(None)
		i += 1

	i = 0
	k2b = {}
	while i < len(tokens):
		if re.match("^K[0-9]+\($", tokens[i]):
			assert tokens[i+1] == "SDRS(" or drs.match(tokens[i+1])
			k2b[tokens[i][:-1].lower()] = b_n[i+1][0]
		i += 1

	i = 0
	stack = []
	tuples = []
#	if args.norel:
#		tuples.append(["w0", "ROOT", "b0"])
	while i < len(tokens):
		tok = tokens[i]
		if tok ==  "SDRS(" or drs.match(tok):
			assert b_n[i] != None
			stack.append(b_n[i])
			i += 1
		elif tok in special:
			stack.append(tok)
			if tok in special[:3]:
				assert tokens[i+2] == "SDRS(" or drs.match(tokens[i+2])
				assert re.match("^B[0-9]+$", tokens[i+1])
				assert b_n[i+2] != None
				tuples.append([get_b(stack, tokens[i+1]), tok[:-1], b_n[i+2][0]])
			else:
				j = i + 1
				tmp = []
				while j < len(tokens):
					if tokens[j][-1] == "(":
						tmp.append(tokens[j])
					elif tokens[j] == ")":
						tmp.pop()
					if len(tmp) == 0:
						break
					j += 1
				assert tokens[i+2] == "SDRS(" or drs.match(tokens[i+2])
				assert b_n[i+2] != None
				assert tokens[j+1] == "SDRS(" or drs.match(tokens[j+1])
				assert b_n[j+1] != None
				tuples.append([get_b(stack, tokens[i+1]), tok[:-1], b_n[i+2][0], b_n[j+1][0]])
			i += 1
		elif re.match("^K[0-9]+\($", tok):
			stack.append(tok)
			assert tokens[i+1] == "SDRS(" or drs.match(tokens[i+1])
			assert b_n[i+1] != None
			tuples.append([get_b(stack, "B0"), "DRS", b_n[i+1][0]])
			i += 1
		elif re.match("^P[0-9]+\($", tok):
			stack.append(tok)
			assert tokens[i+2] == "SDRS(" or drs.match(tokens[i+2])
			assert b_n[i+2] != None
			assert re.match("^B[0-9]+$", tokens[i+1])
			tuples.append([get_b(stack, tokens[i+1]), "Prop", tok[:-1].lower(), b_n[i+2][0]])
			i += 1
		elif tok == ")":
			stack.pop()
			i += 1
		elif re.match("^B[0-9]+$", tokens[i]):
			i += 1
			pass
		else:
			idx = tokens[i:].index(")")
			atom = tokens[i:i+idx]
			i += idx + 1
			
			if atom[0] == "Equ(":
				atom[0] = "EQU("
			assert atom[0][-1] == "("
			atom[0] = atom[0][:-1]

			rel = atom[0]
			p = get_b(stack, atom[1])
			sent = get_sent(stack)
			if re.match("^K[0-9]+$", atom[1]):
				p = get_b(stack, "B0")
				atom = atom[1:]
			elif re.match("^B[0-9]+$", atom[1]):
				atom = atom[2:]
			else:
				print atom
				assert False, "ill formed"
				
			rel = import_sent(sent,rel)
			if re.match("^[XESTPK][0-9]+$", atom[0]) and all([re.match("^\$[0-9]+$", a) for a in atom[1:]]):
				#rel p var constants. e.g. Named B0 X1 $1+
				for j in range(len(atom))[1:]:
					atom[j] = import_sent(sent, atom[j])
				tuples.append([p, rel, atom[0].lower(), '"'+"~".join(atom[1:])+'"'])
			elif len(atom) == 2 and re.match("^[XESTPK][0-9]+$", atom[0]) and re.match("^[avnr]\.[0-9][0-9]$", atom[1]):
				#rel p var sense
				tuples.append([p, rel, '"'+atom[1]+'"', atom[0].lower()])
			elif len(atom) == 2 and all([re.match("^[XESTPK][0-9]+$", a) for a in atom]):
				#rel p var var
				if atom[0].lower() in k2b:
					atom[0] = k2b[atom[0].lower()]
				if atom[1].lower() in k2b:
					atom[1] = k2b[atom[1].lower()]
				tuples.append([p, rel, atom[0].lower(), atom[1].lower()])
			elif len(atom) == 1 and re.match("^[XESTPK][0-9]+$", atom[0]):
				#rel p var
				tuples.append([p, rel, atom[0].lower()])
			else:
				assert False, "unrecognized form"
	assert len(tuples)!=0

	"""
	if args.partial and args.novar == False and args.norel == False:
		c = 0
		for item in tuples:
			if item[1] in ["NOT", "POS", "NEC", "OR", "IMP", "DUP", "DRS"]:
				print " ".join(item)
			else:
				print item[0], item[1], "c"+str(c)
				print "c"+str(c), "ARG1", item[2]
				if len(item) == 4:
					print "c"+str(c), "ARG2", item[3]
				else:
					assert len(item) == 3
				c += 1
		print 
	else:
		for item in tuples:
			print " ".join(item)
		print
	"""

	b_list = []
	for i in range(len(tuples)):
		for j in range(len(tuples[i])):
			if re.match("^b[0-9]+$", tuples[i][j]):
				if tuples[i][j] not in b_list:
					b_list.append(tuples[i][j])
					tuples[i][j] = "b"+str(len(b_list))
				else:
					idx = b_list.index(tuples[i][j])
					tuples[i][j] = "b"+str(idx+1)
	for item in tuples:
		print " ".join(item)
	print
for line in open(args.input):
	line = line.strip()
	#assert line[:5] == "SDRS(" or line[:4] == "DRS("
	process(line.split())
