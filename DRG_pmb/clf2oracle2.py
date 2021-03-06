import os
import sys
import re

x_p = re.compile("^x[0-9]+$")
e_p = re.compile("^e[0-9]+$")
s_p = re.compile("^s[0-9]+$")
t_p = re.compile("^t[0-9]+$")
p_p = re.compile("^p[0-9]+$")
b_p = re.compile("^b[0-9]+$")

def is_var(item):
	if x_p.match(item):
		return 0
	elif e_p.match(item):
		return 1
	elif s_p.match(item):
		return 2
	elif t_p.match(item):
		return 3
	elif p_p.match(item):
		return 4
	elif b_p.match(item):
		return 5
	else:
		return -1

def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"":
		return True
	else:
		return False

def index(lem, tok):
	l = []
	for i, v in enumerate(lem):
		if v == tok:
			l.append(str(i))
	return l

def rule_out_percent(toks):
	ts = []
	for tok in toks:
		if tok == "%":
			break
		ts.append(tok)
	return ts
def drg2oracle(lemmas, lines, out_action):
	lem = lemmas.split()
	v = [ [] for i in range(6)]
	idx = 0
	newline = []
	while idx < len(lines):
		toks = lines[idx].split()
		toks = rule_out_percent(toks)
		if len(toks) == 0:
			idx += 1
			continue
		for tok in toks:
			typ = is_var(tok)
			if typ != -1:
				if tok not in v[typ]:
					newline.append(tok[0].upper())
					v[typ].append(tok)
				else:
					newline.append(tok[0]+str(len(v[typ])-int(tok[1:])-1))
			elif re.match("^\"[avnr]\.\d+\"$", tok):
				newline.append(tok)
			elif is_realword(tok):
				if tok[1:-1] in lem:
					#newline.append("\"$"+",".join(index(lem, tok[1:-1]))+"\"")
					#newline.append("$"+",".join(index(lem, tok[1:-1])))
					newline.append("$"+index(lem, tok[1:-1])[0])
				else:
					newline.append(tok)
			else:
				if tok in lem:
					newline.append("$"+index(lem, tok)[0])
				else:
					newline.append(tok)
		newline.append("|||")
		idx += 1
	out_action.write(" ".join(newline[:-1])+"\n")
			
if __name__ == "__main__":
	illform = []
	for line in open("illform"):
		line = line.strip()
		if line == "":
			continue
		illform.append(line.split()[-2])
	for line in open("manual_correct"):
		line = line.strip()
		if line == "" or line[0] == "#":
			continue
		illform.append(line)
	lines = []
	filename = ""
	out_input = open(sys.argv[1]+".oracle.input2", "w")
	out_action = open(sys.argv[1]+".oracle.action2", "w")
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			if filename in illform:
				lines = []
				continue
			idx = lines.index("Graph")
			
			assert idx % 2 == 0 and idx != 0
			lemmas = " ".join([ lines[i*2+1] for i in range(idx/2) ])
			words = " ".join([ lines[i*2] for i in range(idx/2) ])
			out_input.write("\n".join([words, lemmas]))
			out_input.write("\n\n")
			drg2oracle(lemmas, lines[idx+1:], out_action)
			out_input.flush()
			out_action.flush()
			lines = []
		else:
			if line[0] == "#":
				filename = line.split()[-2]
				continue
			lines.append(line)
	out_input.close()
	out_action.close()

			
