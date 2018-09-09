import sys
import types
import json
import re
from defination import DRSnode
from utils import normal_variables_for_trees
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tree(node):
	
	def travel2(n):
		if ("symbol" in n.attrib) and (n.attrib["symbol"] in ["(", "[", "{"]):
			n.attrib["symbol"] = "-lrb-"
		if ("symbol" in n.attrib) and (n.attrib["symbol"] in [")", "]", "}"]):
			n.attrib["symbol"] = "-rrb-"
		if ("sym" in n.attrib) and (n.attrib["sym"] in ["(", "[", "{"]):
			n.attrib["sym"] = "-lrb-"
		if ("sym" in n.attrib) and (n.attrib["sym"] in [")", "]", "}"]):
			n.attrib["sym"] = "-rrb-"
		for sn in n.expression:
			travel2(sn)
	travel2(node)

	tree = []
	def travel(n):
		if n.type == "drs":
			tree.append("DRS(")
			assert len(n.expression) == 2
			travel(n.expression[1])
			tree.append(")")
		elif n.type == "sdrs":
			tree.append("SDRS(")
			assert len(n.expression) == 2
			travel(n.expression[0])
			travel(n.expression[1])
			tree.append(")")
		elif n.type == "sub":
			for sn in n.expression:
				travel(sn)
		elif n.type == "constituents":
			for sn in n.expression:
				travel(sn)
		elif n.type == "constituent":
			tree.append(n.attrib["label"].upper()+"(")
			assert len(n.expression) == 1
			travel(n.expression[0])
			tree.append(")")
		elif n.type == "relations":
			for sn in n.expression:
				tree.append(sn.attrib["sym"]+"(")
				tree.append(sn.attrib["arg1"].upper())
				tree.append(sn.attrib["arg2"].upper())
				tree.append(")")
		elif n.type == "conds":
			for sn in n.expression:
				travel(sn)
		elif n.type == "cond":
			assert len(n.expression) == 1 # cond
			sn = n.expression[0]
			if sn.type in ["rel"]:
				tree.append(sn.attrib["symbol"]+"(")
				tree.append(sn.attrib["arg1"].upper())
				tree.append(sn.attrib["arg2"].upper())
			elif sn.type == "eq":
				tree.append("EQ(")
				tree.append(sn.attrib["arg1"].upper())
				tree.append(sn.attrib["arg2"].upper())
			elif sn.type in ["named", "pred"]:
				tree.append(sn.attrib["symbol"]+"(")
				tree.append(sn.attrib["arg"].upper())
			elif sn.type == "card":
				tree.append("CARD(")
				tree.append(sn.attrib["arg"].upper())
				tree.append("CARD_NUMBER")
			elif sn.type == "timex":
				tree.append("TIMEX(")
				tree.append(sn.attrib["arg"].upper())
				tree.append("TIME_NUMBER")
			elif sn.type == "prop":
				tree.append(sn.attrib["argument"].upper()+"(")
				assert len(sn.expression) == 1
				travel(sn.expression[0])
			elif sn.type in ["pos", "nec", "not"]:
				tree.append(sn.type.upper()+"(")
				assert len(sn.expression) == 1
				travel(sn.expression[0])
			elif sn.type in ["imp", "or", "duplex"]:
				tree.append(sn.type.upper()+"(")
				assert len(sn.expression) == 2
				travel(sn.expression[0])
				travel(sn.expression[1])
			else:
				print sn.type
				assert False, "unrecognized type"
			tree.append(")")
	travel(node)

	return tree

if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	print "#"," ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)

			L[3] = tree(target_DRSnode)
			normal_variables_for_trees(L[3])
			L[3] = " ".join(L[3])
			#normal_variables(target_DRSnode)

			if L[3] != "DRS( )":
				print "\n".join(L)
				print 

			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	




