import sys
import types
import json
import re
from defination import DRSnode
from utils import normal_variables
nosense = False
if len(sys.argv) >= 3 and sys.argv[2] == "nosense":
	nosense = True

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tree(node):
	
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
		elif n.type == "conds":
			for sn in n.expression:
				travel(sn)
		elif n.type == "cond":
			

	variable = []
	px = re.compile("^x[0-9]+?$")
	pt = re.compile("^t[0-9]+?$")
	def travel(n):
		if n.type == "dr":
			name = n.attrib["name"]
			if pt.match(name) and (name not in variable):
				variable.append(name)
		if n.type == "cond":
			for sn in n.expression:
				if sn.type == "eq":
					a1 = sn.attrib["arg1"]
					a2 = sn.attrib["arg2"]
					if px.match(a1) and (a2 in variable) and (a1 not in variable):
						variable.append(a1)
					if px.match(a2) and (a1 in variable) and (a2 not in variable):
						variable.append(a2)
		for sn in n.expression:
			travel(sn)

	while True:
		l = len(variable)
		travel(node)
		if l == len(variable):
			break


	def travel2(n):
		if n.type == "domain":
			newlist = []
			for sn in n.expression:
				if sn.attrib["name"] in variable:
					continue
				newlist.append(sn)
			n.expression = newlist
			return
		if n.type == "conds":
			newlist = []
			for sn in n.expression:
				ssn = sn.expression[0]
				if ssn.type == "rel" and ((ssn.attrib["arg1"] in variable) or (ssn.attrib["arg2"] in variable) or ("temp_" in ssn.attrib["symbol"])):
					continue
				if ssn.type == "eq" and ((ssn.attrib["arg1"] in variable) or (ssn.attrib["arg2"] in variable)):
					continue
				if ssn.type in ["named", "pred"] and ((ssn.attrib["arg"] in variable) or ("temp_" in ssn.attrib["symbol"])):
					continue
				if ssn.type in ["card", "timex"] and (ssn.attrib["arg"] in variable):
					continue
				newlist.append(sn)
			n.expression = newlist
		for sn in n.expression:
			travel2(sn)

	travel2(node)

	exist_variable = []
	def travel3(n):
		if n.type == "cond":
			sn = n.expression[0]
			if sn.type in ["rel", "eq"]:
				a1 = sn.attrib["arg1"]
				a2 = sn.attrib["arg2"]
				if a1 not in exist_variable:
					exist_variable.append(a1)
				if a2 not in exist_variable:
					exist_variable.append(a2)
			if sn.type in ["named", "pred", "card", "timex"]:
				a1 = sn.attrib["arg"]
				if a1 not in exist_variable:
					exist_variable.append(a1)
		for sn in n.expression:
			travel3(sn)

	travel3(node)

	def travel4(n):
		if n.type == "domain":
			newlist = []
			for sn in n.expression:
				if sn.attrib["name"] in exist_variable:
					newlist.append(sn)
			n.expression = newlist
		else:
			for sn in n.expression:
				travel4(sn)



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

			L[3] = tree(target_DRSnode)
			#normal_variables(target_DRSnode)

			print "\n".join(L)
			print 

			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	




