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
		return True
	elif e_p.match(item):
		return True
	elif s_p.match(item):
		return True
	elif t_p.match(item):
		return True
	elif p_p.match(item):
		return True
	elif b_p.match(item):
		return True
	else:
		return False

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
	v = []
	idx = 0
	newline = []
	while idx < len(lines):
		toks = lines[idx].split()
		toks = rule_out_percent(toks)
		if len(toks) == 0:
			idx += 1
			continue
		for tok in toks:
			if is_var(tok):
				if tok not in v:
					newline.append(tok[0].upper())
					v.append(tok)
				else:
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
	lines = []
	out_input = open(sys.argv[1]+".oracle.input", "w")
	out_action = open(sys.argv[1]+".oracle.action", "w")
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
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
				continue
			lines.append(line)
	out_input.close()
	out_action.close()

			
