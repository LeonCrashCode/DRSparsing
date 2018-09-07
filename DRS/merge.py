"""
this file is to output the completed drs without "merge" and v variables,
ignoring merge sdrs and sdrs
making sure complex condition, "not", "pos" and "nec", have and only have one drs
"imp", "or" and "duplex" have and only have two drs
"""
import sys
import types
import json
import re
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

pv= re.compile("^v[0-9]+$")
pp= re.compile("^p[0-9]+$")
def merge(node):

	def change_label(n, fr, to):
		if "label" in n.attrib and n.attrib["label"] == fr:
			n.attrib["label"] = to
		for sn in n.expression:
			change_label(sn, fr, to)

	def get_first_drs(n):
		
		first_drs = []
		def travel(nn):
			if len(first_drs) == 1:
				return
			for sn in nn.expression:
				travel(sn)

			if nn.type == "drs" and len(first_drs) == 0:
				first_drs.append(nn)

		travel(n)
		assert len(first_drs) == 1
		return first_drs[0]

	def travel(n):
		for i in range(len(n.expression)):
			travel(n.expression[i])
			if n.expression[i].type == "merge":
				if len(n.expression[i].expression) == 1:
					#print "only one"
					n.expression[i] = n.expression[i].expression[0]
				elif len(n.expression[i].expression) == 2:
					if n.expression[i].expression[0].type == "drs" and n.expression[i].expression[1].type == "drs":
						#print "drs drs"
						change_label(n.expression[i].expression[0], n.expression[i].expression[0].attrib["label"], n.expression[i].expression[1].attrib["label"])
						n.expression[i].expression[1].expression[0].expression += n.expression[i].expression[0].expression[0].expression #merge.drs.domains.expression
						n.expression[i].expression[1].expression[1].expression += n.expression[i].expression[0].expression[1].expression #merge.drs.conds.expression
						n.expression[i] = n.expression[i].expression[1]
					elif n.expression[i].expression[0].type == "drs" and n.expression[i].expression[1].type == "sdrs":
						#exit(1)
						#print "drs sdrs"
						first_drs = get_first_drs(n.expression[i].expression[1])
						change_label(n.expression[i].expression[0], n.expression[i].expression[0].attrib["label"], first_drs.attrib["label"])
						first_drs.expression[0].expression = n.expression[i].expression[0].expression[0].expression + first_drs.expression[0].expression
						first_drs.expression[1].expression = n.expression[i].expression[0].expression[1].expression + first_drs.expression[1].expression
						n.expression[i] = n.expression[i].expression[1]
						pass
					elif n.expression[i].expression[0].type == "sdrs" and n.expression[i].expression[1].type == "drs":
						#print "sdrs drs"
						last_drs = get_last_drs(n.expression[i].expression[0])
						change_label(last_drs, last_drs.attrib["label"], n.expression[i].expressionp[1].attrib["label"])
						last_drs.expression[0] += n.expression[i].expression[1].expression[0]
						last_drs.expression[1] += n.expression[i].expression[1].expression[1]
						n.expression[i] = n.expression[i].expression[0]
						pass
					elif n.expression[i].expression[0].type == "sdrs" and n.expression[i].expression[1].type == "sdrs":
						print "illegal"
						#print "sdrs sdrs"
						pass
					else:
					    #print n.expression[i].expression[0].type, n.expression[i].expression[1].type
						print "illegal"
						#print "no"
						pass
		if (n.type in ["not", "pos", "nec"]) and len(n.expression) != 1:
			print "illegal"
		if (n.type in ["imp", "or", "duplex"]) and len(n.expression) != 2:
			print "illegal"

	travel(node)

	def travel2(n): # erase v variable
		if n.type == "conds":
			newlist = []
			for sn in n.expression:
				ssn = sn.expression[0]
				if ssn.type in ["rel", "eq"] and (pv.match(ssn.attrib["arg1"]) or pv.match(ssn.attrib["arg2"])):
					continue
				if ssn.type in ["named", "pred", "card", "timex"] and pv.match(ssn.attrib["arg"]):
					continue
				newlist.append(sn)
			n.expression = newlist
		for sn in n.expression:
			travel2(sn)
	travel2(node)

	variable = []
	def travel3(n): # make sure prop variable is started with "p"
		if n.type == "prop":
			if pp.match(n.attrib["argument"]):
				pass
			elif n.attrib["argument"] not in variable:
				variable.append(n.attrib["argument"])
		for sn in n.expression:
			travel3(sn)

	travel3(node)

	def travel4(n):
		if n.type == "dr" and (n.attrib["name"] in variable):
			n.attrib["name"] = "p"+str(1000+variable.index(n.attrib["name"]))
		if ("arg" in n.attrib) and (n.attrib["arg"] in variable):
			n.attrib["arg"] = "p"+str(1000+variable.index(n.attrib["arg"]))
		if ("arg1" in n.attrib) and (n.attrib["arg1"] in variable):
			n.attrib["arg1"] = "p"+str(1000+variable.index(n.attrib["arg1"]))
		if ("arg2" in n.attrib) and (n.attrib["arg2"] in variable):
			n.attrib["arg2"] = "p"+str(1000+variable.index(n.attrib["arg2"]))
		if ("argument" in n.attrib) and (n.attrib["argument"] in variable):
			n.attrib["argument"] = "p"+str(1000+variable.index(n.attrib["argument"]))
		for sn in n.expression:
			travel4(sn)

	travel4(node)

if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
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
			#print "\n".join(L)
			#print
			dummy_node = DRSnode()
			dummy_node.expression.append(target_DRSnode)
			merge(dummy_node)

			L[3] = json.dumps(dummy_node.expression[0].serialization())
			print "\n".join(L)
			print
			#print cnt, total
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	#print cnt




