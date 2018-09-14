import os
import sys
import re

def clear(item):
	items = item.split("|||")
	newitems = []
	for item in items:
		if len(item) >= 2 and item[0] == "\"" and item[-1] == "\"":
			item = item[1:-1]
		if len(item) == 0:
			print item
		assert len(item) > 0, "empty item"
		newitems.append(item)
	return "|||".join(newitems)
def drg2act(lines, out):
	out.write(lines[0]+"\n")
	out.write(lines[1]+"\n")
	act = []
	v = []
	for line in lines[2:]:
		l, c, r = line.split()
		l = clear(l)
		c = clear(c)
		r = clear(r)
		if l not in v:
			if l in ["now", "speaker", "hearer"]:
				act.append("ADD_NODE_"+l.upper())
			else:
				act.append("ADD_NODE_"+l[0].upper())
			v.append(l)
			for edge in lines[2:]:
				el, ec, er = edge.split()
				el = clear(el)
				ec = clear(ec)
				er = clear(er)
				if el == l and er in v:
					act.append("ADD_EDGE_OUT "+ec+" "+er)
				elif er == l and el in v:
					act.append("ADD_EDGE_IN "+ec+" "+el)
			if act[-1].split()[0] == "ADD_NODE":
				act.append("NO_EDGE_ADDED")
		if r not in v:
			if r in ["now", "speaker", "hearer"]:
				act.append("ADD_NODE_"+r.upper())
			else:
				act.append("ADD_NODE_"+r[0].upper())
			v.append(r)
			for edge in lines[2:]:
				el, ec, er = edge.split()
				el = clear(el)
				ec = clear(ec)
				er = clear(er)
				if el == r and er in v:
					act.append("ADD_EDGE_OUT "+ec+" "+er)
				elif er == r and el in v:
					act.append("ADD_EDGE_IN "+ec+" "+el)
			if act[-1].split()[0] == "ADD_NODE":
				act.append("NO_EDGE_ADDED")
	out.write("\n".join(act))
	out.write("\n\n")
	out.flush()

cnt = 0
if __name__ == "__main__":
	lines = []
	out = open(sys.argv[1].split(".")[0]+".act","w")
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			if len(lines) > 2:
				drg2act(lines, out)
			lines = []
		else:
			lines.append(line)
	out.close()
			
