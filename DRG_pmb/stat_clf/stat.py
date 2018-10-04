import sys
import re
x_p = re.compile("^x[0-9]+$")
e_p = re.compile("^e[0-9]+$")
s_p = re.compile("^s[0-9]+$")
t_p = re.compile("^t[0-9]+$")
p_p = re.compile("^p[0-9]+$")
b_p = re.compile("^b[0-9]+$")

cpy1_p = re.compile("^\"\$[0-9|,]+\"")
cpy2_p = re.compile("^\$[0-9|,]+")

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

node = {}
edge = {}
var = {}
max_tuple_cnt = 0
def add(k,d):
	if k in d:
		d[k] += 1
	else:
		d[k] = 1
def stat(line):
	line = line.split("|||")
	global max_tuple_cnt
	max_tuple_cnt = max(len(line), max_tuple_cnt)
	for l in line:
		toks = l.split()
		assert len(toks) in [3,4]
		for tok in toks:
			if tok in ["X", "E", "S", "T", "P", "B"]:
				pass
			elif is_var(tok):
				typ = tok[0]
				idx = int(tok[1:])
				if typ in var:
					var[typ] = max(var[typ], idx)
				else:
					var[typ] = idx
			elif cpy1_p.match(tok) or cpy2_p.match(tok):
				pass
			else:
				add(tok, node)


	
if __name__ == "__main__":
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		stat(line)
	out = open("node", "w")
	for key in node.keys():
		out.write(key+" "+str(node[key])+"\n")
	out.close()
	out = open("var", "w")
	for key in var.keys():
		out.write(key+" "+str(var[key])+"\n")
	out.close()

	print max_tuple_cnt