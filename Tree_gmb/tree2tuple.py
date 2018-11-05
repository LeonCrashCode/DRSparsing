import sys
import re

special = ["NOT(", "POS(", "NEC(", "OR(", "IMP(", "DUP("]


def get_b(stack):
	for item in stack[::-1]:
		if item[0] == "b":
			return item

def process(tokens, partially):
	
	i = 0
	b = 0
	card_num = 0
	time_num = 0
	b_n = []
	while i < len(tokens):
		if tokens[i] in ["DRS(", "SDRS("]:
			b_n.append(str(b))
			b += 1
		else:
			b_n.append(None)
			if tokens[i] == "CARD_NUMBER":
				tokens[i] = tokens[i] + "-" + str(card_num)
				card_num += 1
			if tokens[i] == "TIME_NUMBER":
				tokens[i] = tokens[i] + "-" + str(time_num)
				time_num += 1
		i += 1

	i = 0
	k2b = {}
	while i < len(tokens):
		if re.match("^K[0-9]\($", tokens[i]):
			assert tokens[i+1] in ["DRS(", "SDRS("]
			k2b[tokens[i][:-1]] = "b"+b_n[i+1]
		i += 1

	i = 0
	stack = []
	tuples = []
	while i < len(tokens):
		tok = tokens[i]
		if tok in ["DRS(", "SDRS("]:
			idx = b_n[i]
			assert idx != None
			stack.append("b"+idx)
			i += 1
		elif tok in special:
			stack.append(tok)
			if tok in special[:3]:
				assert tokens[i+1] in ["DRS(", "SDRS("]
				tuples.append([get_b(stack), tok[:-1], "b"+b_n[i+1]])
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
				assert tokens[i+1] in ["DRS(", "SDRS("]
				assert b_n[i+1] != None
				assert tokens[j+1] in ["DRS(", "SDRS("]
				assert b_n[j+1] != None
				tuples.append([get_b(stack), tok[:-1], "b"+b_n[i+1], "b"+b_n[j+1]])
			i += 1
		elif re.match("^K[0-9]+\($", tok):
			stack.append(tok)
			assert tokens[i+1]in ["DRS(", "SDRS("]
			assert b_n[i+1] != None
			tuples.append([get_b(stack), "DRS", "b"+b_n[i+1]])
			i += 1
		elif re.match("^P[0-9]+\($", tok):
			stack.append(tok)
			assert tokens[i+1] in ["DRS(", "SDRS("]
			assert b_n[i+1] != None
			tuples.append([get_b(stack), "Prop", tok, "b"+b_n[i+1]])
			i += 1
		elif tok == ")":
			stack.pop()
			i += 1
		else:
			if tok == "Equ(":
				tok = "EQU("
			tuples.append([get_b(stack), tok[:-1]])
			#v1
			i += 1
			assert tokens[i] != ")"
			if re.match("^K[0-9]+$", tokens[i]):
				tuples[-1].append(k2b[tokens[i]].lower())
			else:
				tuples[-1].append(tokens[i].lower())

			#v2
			i += 1
			if tokens[i] == ")":
				i += 1
			else:
				if tokens[i].startswith("CARD_NUMBER") or tokens[i].startswith("TIME_NUMBER"):
					tuples[-1].append('"'+tokens[i]+'"')
				else:
					if re.match("^K[0-9]+$", tokens[i]):
						tuples[-1].append(k2b[tokens[i]].lower())
					else:
						tuples[-1].append(tokens[i].lower())

					#v at most 2
				i += 1
				assert tokens[i] == ")"

				i += 1
	assert len(tuples)!=0

	if partially:
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
	else:
		for item in tuples:
			print " ".join(item)
		print
for line in open(sys.argv[1]):
	line = line.strip()
	assert line[:5] == "SDRS(" or line[:4] == "DRS("
	if len(sys.argv) >= 3 and sys.argv[2] == "partially":
		process(line.split(), True)
	else:
		process(line.split(), False)
