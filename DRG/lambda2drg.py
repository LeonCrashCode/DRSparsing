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
	def travel(n):
		if n.type == "cond":
			for sn in n.expression:
				if sn.type == "rel": # rel
					a1 = sn.attrib["arg1"]
					a2 = sn.attrib["arg2"]
					if p.match(a1) or p.match(a2):
						continue
					b1 = getb(a1)
					b2 = getb(a2)
					if b1:
						print b1, "REF", a1
					if b2:
						print b2, "REF", a2
					print n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["sense"]+"\"", a1, a2
				elif sn.type == "named": # named
					a1 = sn.attrib["arg"]
					if p.match(a1):
						continue
					b1 = getb(a1)
					if b1:
						print b1, "REF", a1
					print n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["class"]+"\"", a1
				elif sn.type == "pred": # pred
					a1 = sn.attrib["arg"]
					if p.match(a1):
						continue
					b1 = getb(a1)
					if b1:
						print b1, "REF", a1
					print n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["type"]+"."+sn.attrib["sense"]+"\"", a1
				elif sn.type == "card": # card
					a1 = sn.attrib["arg"]
					if p.match(a1):
						continue
					b1 = getb(a1)
					if b1:
						print b1, "REF", a1
					print n.attrib["label"], sn.attrib["type"], a1, "NUMBER"
				elif sn.type == "eq": # eq
					a1 = sn.attrib["arg1"]
					a2 = sn.attrib["arg2"]
					if p.match(a1) or p.match(a2):
						continue
					b1 = getb(a1)
					b2 = getb(a2)
					if b1:
						print b1, "REF", a1
					if b2:
						print b2, "REF", a2
					print n.attrib["label"], "eq",  a1, a2
				elif sn.type == "prop": # prop
					a1 = sn.attrib["argument"]
					if p.match(a1)
						continue
					b1 = getb(a1)
					if b1:
						print b1, "REF", a1
					for ssn in sn.expression:
						if ssn.type == "drs"

					print n.attrib["label"], "prop",  a1
				else:
					print sn.type
					assert False, "unrecognized type"
		for subnode in n.expression:
			travel(subnode)

	travel(node)

if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)

			drg(target_DRSnode)
			L = []
		else:
			L.append(line)
	




