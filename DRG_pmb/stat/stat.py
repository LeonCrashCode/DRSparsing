import sys


def is_realword(item):
	if item[0] == "\"" and item[-1] == "\"":
		return True
	else:
		return False

node = {}
edge = {}
var = {}
def add(k,d):
	if k in d:
		d[k] += 1
	else:
		d[k] = 1
def stat(lines, lemmas):
	lemmas = lemmas.split()
	for line in lines:
		acts = line.split()
		for act in acts:
			toks = act.split("_")
			if toks[1] == "NODE":
				t = "_".join(toks[2:])
				if is_realword(t):
					if t[1:-1] in lemmas:
						add("LEMMA", node)
					else:
						add(t, node)
				else:
					add(t, node)
			elif toks[1] == "EDGE":
				add("_".join(toks[2:4]), edge)
				t = "_".join(toks[4:])
				if is_realword(t):
					pass
				else:
					typ = t[0]
					idx = int(t[1:])
					if typ in var:
						var[typ] = max(var[typ], idx)
					else:
						var[typ] = idx
if __name__ == "__main__":
	lines = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			idx = lines.index("Graph")
			lemmas = lines[idx-1]
			stat(lines[idx+1:], lemmas)
			lines = []
		else:
			lines.append(line)
	out = open("node", "w")
	for key in node.keys():
		out.write(key+" "+str(node[key])+"\n")
	out.close()

	out = open("edge", "w")
	for key in edge.keys():
		out.write(key+" "+str(edge[key])+"\n")
	out.close()

	out = open("var", "w")
	for key in var.keys():
		out.write(key+" "+str(var[key])+"\n")
	out.close()