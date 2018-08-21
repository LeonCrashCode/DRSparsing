import sys
import types
import json
import re
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

p = re.compile("^v[0-9]+$")

def unlambda(node):
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
				elif sn.type == "named" or sn.type == "pred" or sn.type == "card": # named
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
					else:
						Tuples.append(" ".join([n.attrib["label"], sn.attrib["type"], a1, "\"NUMBER\""]))
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
				print sn.expression[0].type
				assert sn.expression[0].type == "drs"
				Tuples.append(" ".join([n.attrib["label"], "DRS", sn.attrib["label"]]))
		for subnode in n.expression:
			travel(subnode)

	travel(node)

def have_complex_app(node):
	stack = []
	stack.append(node)
	while len(stack) != 0:
		if stack[0].type == "app":
			assert len(stack[0].expression) == 2
			if stack[0].expression[0].type != "var" or stack[0].expression[1].type != "var":
				return True
		for subnode in stack[0].expression:
			stack.append(subnode)
		stack = stack[1:]
	return False

def rule_out_app(node):
	
	def travel(n):
		l = []
		for i, sn in enumerate(n.expression):
			if sn.type == "app":
				l.append(i)
		n.expression = [i for j, i in enumerate(n.expression) if j not in l]
		for sn in n.expression:
			travel(sn)
	travel(node)

def rule_out_lam(node):

	while True:
		if node.type == "lam":
			node = node.expression[1]
			continue
		return node



def have_complex_merge(node):
	stack = []
	stack.append(node)
	while len(stack) != 0:
		if stack[0].type == "merge":
			if len(stack[0].expression) != 1:
				print json.dumps(stack[0].expression[0].serialization())
				print json.dumps(stack[0].expression[1].serialization())
				return True
		for subnode in stack[0].expression:
			stack.append(subnode)
		stack = stack[1:]
	return False



if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)

			if have_complex_app(target_DRSnode):
				cnt += 1
			else:
				
				if "alfa" in L[3]:
					cnt += 1
				
				else:
					#print L[3]
					rule_out_app(target_DRSnode)
					#print json.dumps(target_DRSnode.serialization())
					target_DRSnode = rule_out_lam(target_DRSnode)
					L[3] = json.dumps(target_DRSnode.serialization())
					print "\n".join(L)
					print
				
			#print cnt, total
			L = []
		else:
			L.append(line)
	#print cnt
	




