import sys
import types
import json
import re
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

p = re.compile("^v[0-9]+$")

def drg(node):
	declared_variable = []
	def getb(arg):
		if arg in declared_variable:
			return None
		stack = []
		stack.append(node)
		while len(stack) != 0:
			if stack[0].type == "dr" and stack[0].attrib["name"] == arg:
				declared_variable.append(arg)
				return stack[0].attrib["label"]
			for subnode in stack[0].expression:
				stack.append(subnode)
			stack = stack[1:]
	Tuples = []
	def travel(n):
		if n.type == "cond":
			for sn in n.expression:
				if sn.type == "rel" or sn.type == "eq": # rel
					a1 = sn.attrib["arg1"]
					a2 = sn.attrib["arg2"]
					if p.match(a1) or p.match(a2):
						continue
					b1 = getb(a1)
					b2 = getb(a2)
					if b1:
						Tuples.append(" ".join([b1, "REF", a1]))
					if b2:
						Tuples.append(" ".join([b2, "REF", a2]))
					if sn.type == "rel":
						Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["sense"]+"\"", a1, a2]))
					elif sn.type == "eq":
						Tuples.append(" ".join([n.attrib["label"], "EQU",  a1, a2]))
				elif sn.type == "named" or sn.type == "pred" or sn.type == "card" or sn.type == "timex": # named
					a1 = sn.attrib["arg"]
					if p.match(a1):
						continue
					b1 = getb(a1)
					if b1:
						Tuples.append(" ".join([b1, "REF", a1]))
					if sn.type == "named":
						Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["class"]+"\"", a1]))
					elif sn.type == "pred":
						Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["type"]+"."+sn.attrib["sense"]+"\"", a1]))
					elif sn.type == "card":
						Tuples.append(" ".join([n.attrib["label"], sn.attrib["type"], a1, "\"NUMBER\""]))
					else:
						Tuples.append(" ".join([n.attrib["label"], sn.expression[0].type, a1, "\"DATE\""]))
				elif sn.type == "prop": # prop
					a1 = sn.attrib["argument"]
					if p.match(a1):
						continue
					b1 = getb(a1)
					if b1:
						Tuples.append(" ".join([b1, "REF", a1]))
					assert len(sn.expression) == 1, "prop sub node"
					ssn = sn.expression[0]
					assert ssn.type == "drs" or ssn.type == "sdrs", "unrecognized type"
					Tuples.append(" ".join([n.attrib["label"], "PRP", a1, ssn.attrib["label"]]))

				elif sn.type in ["not", "pos", "nec"]:
					assert len(sn.expression) == 1, "not | pos | nec sub node"
					ssn = sn.expression[0]
					assert ssn.type == "drs" or ssn.type == "sdrs", "unrecognized type"
					Tuples.append(" ".join([n.attrib["label"], sn.type.upper(), ssn.attrib["label"]]))
				else:
					print sn.type
					assert False, "unrecognized type"
		elif n.type == "sdrs":
			assert len(n.expression) == 2 #constituents and relations
			for sn in n.expression[0].expression:
				assert sn.type == "drs" or sn.type == "sub"
				Tuples.append(" ".join([n.attrib["label"], "DRS", sn.attrib["label"]]))
		elif n.type == "sub":
			for sn in n.expression:
				assert len(sn.expression) == 1
				assert sn.expression[0].type == "drs"
				Tuples.append(" ".join([n.attrib["label"], "DRS", sn.attrib["label"]]))
		for subnode in n.expression:
			travel(subnode)
	travel(node)


if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	print "#"," ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			if L[0] == "illegal":
				L = []
				continue
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)

			drg(target_DRSnode)
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	




