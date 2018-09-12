"""
	This file is only appied to notime nosense
	This drs2drg.py is to transform drs to the drg, which
	is compatible to tree evaluation.
"""
import sys
import types
import json
import re
from defination import DRSnode
from utils import normal_variables_for_tuples2
nosense = False
if len(sys.argv) >= 3 and sys.argv[2] == "nosense":
	nosense = True

noner = nosense

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

#p = re.compile("^v[0-9]+$")

def drg(node):

	#change ( to -lrb- and change ")" to "-rrb-"

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
	
	projections = {}
	def getb(n):
		if n.type == "dr":
			name = n.attrib["name"]
			if name in projections:
				assert n.attrib["label"] == projections[name]
			else:
				projections[name] = n.attrib["label"]
		for sn in n.expression:
			getb(sn)
	getb(node)

	k2b = {}
	def getk2b(n):
		if n.type == "constituent":
			klabel = n.attrib["label"]
			blabel = n.expression[0].attrib["label"]
			if klabel in k2b:
				assert blabel == k2b[klabel]
			else:
				k2b[klabel] = blabel
		for sn in n.expression:
			getk2b(sn)
	getk2b(node)
	

	declared_variable = []
	Tuples = []
	Flag = [True]
	c = [0]
	card = [0]
	time = [0]
	def travel(n):
		if n.type == "cond":
			for sn in n.expression:
				if sn.type == "rel" or sn.type == "eq": # rel
					a1 = sn.attrib["arg1"]
					a2 = sn.attrib["arg2"]
					#if p.match(a1) or p.match(a2):
					#	continue
					if a1 not in declared_variable:
						Tuples.append(" ".join([projections[a1], "REF", a1]))
						declared_variable.append(a1)
					if a2 not in declared_variable:
						Tuples.append(" ".join([projections[a2], "REF", a2]))
						declared_variable.append(a2)
					if sn.type == "rel":
						if nosense:
							Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "c"+str(c[0])]))
							Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
							Tuples.append(" ".join(["c"+str(c[0]), "ARG2", a2]))
							c[0] += 1
						else:
							assert False
							#Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["sense"]+"\"", a1, a2]))
					elif sn.type == "eq":
						Tuples.append(" ".join([n.attrib["label"], "EQU", "c"+str(c[0])]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG2", a2]))
						c[0] += 1
				elif sn.type == "named" or sn.type == "pred" or sn.type == "card" or sn.type == "timex": # named
					a1 = sn.attrib["arg"]
					#if p.match(a1):
					#	continue
					if a1 not in declared_variable:
						Tuples.append(" ".join([projections[a1], "REF", a1]))
						declared_variable.append(a1)
					if sn.type == "named":
						if noner:
							Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "c"+str(c[0])]))
							Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
							c[0] += 1
						else:
							assert False
							#Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["class"]+"\"", a1]))
					elif sn.type == "pred":
						if nosense:
							#Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], a1]))
							Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "c"+str(c[0])]))
							Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
							c[0] += 1
						else:
							assert False
							Tuples.append(" ".join([n.attrib["label"], sn.attrib["symbol"], "\""+sn.attrib["type"]+"."+sn.attrib["sense"]+"\"", a1]))
					elif sn.type == "card":
						assert sn.attrib["type"] == "eq"
						#sn.attrib["type"] = "EQU"
						#Tuples.append(" ".join([n.attrib["label"], sn.attrib["type"], a1, "\"CARD_NUMBER\""]))
						Tuples.append(" ".join([n.attrib["label"], "CARD", "c"+str(c[0])]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG2", "\"CARD_NUMBER"+str(card[0])+"\""]))
						c[0] += 1
						card[0] += 1
					else:
						assert sn.expression[0].type == "date"
						#Tuples.append(" ".join([n.attrib["label"], sn.expression[0].type, a1, "\"TIME_NUMBER\""]))
						#Tuples.append(" ".join([n.attrib["label"], "EQU", a1, "\"TIME_NUMBER\""]))
						Tuples.append(" ".join([n.attrib["label"], "TIMEX", "c"+str(c[0])]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG2", "\"TIME_NUMBER"+str(time[0])+"\""]))
						c[0] += 1
						time[0] += 1
				elif sn.type == "prop": # prop
					a1 = sn.attrib["argument"]
					#if p.match(a1):
					#	continue
					if a1 not in declared_variable:
						Tuples.append(" ".join([projections[a1], "REF", a1]))
						declared_variable.append(a1)
					assert len(sn.expression) == 1, "prop sub node"
					ssn = sn.expression[0]
					assert ssn.type == "drs" or ssn.type == "sdrs", "unrecognized type"
					#Tuples.append(" ".join([n.attrib["label"], "PRP", a1, ssn.attrib["label"]]))
					Tuples.append(" ".join([n.attrib["label"], "PRP", "c"+str(c[0])]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG2", ssn.attrib["label"]]))
					c[0] += 1

				elif sn.type in ["not", "pos", "nec"]:
					#assert len(sn.expression) == 1, "not | pos | nec sub node"
					if len(sn.expression) != 1:
						Flag[0] = False
						continue
					ssn = sn.expression[0]
					assert ssn.type == "drs" or ssn.type == "sdrs", "unrecognized type"
					#Tuples.append(" ".join([n.attrib["label"], sn.type.upper(), ssn.attrib["label"]]))
					Tuples.append(" ".join([n.attrib["label"], sn.type.upper(), "c"+str(c[0])]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG1", ssn.attrib["label"]]))
					c[0] += 1
				elif sn.type in ["imp", "or", "duplex"]:
					#for ssn in sn.expression:
					#	print ssn.type
					#assert len(sn.expression) == 2, "imp | or | duplex sub node"
					if len(sn.expression) != 2:
						Flag[0] = False
						continue
					ssn1 = sn.expression[0]
					ssn2 = sn.expression[1]
					#Tuples.append(" ".join([n.attrib["label"], sn.type.upper(), ssn1.attrib["label"], ssn2.attrib["label"]]))
					Tuples.append(" ".join([n.attrib["label"], sn.type.upper(), "c"+str(c[0])]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG1", ssn1.attrib["label"]]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG2", ssn2.attrib["label"]]))
					c[0] += 1
				else:
					print sn.type
					assert False, "unrecognized type"
		elif n.type == "sdrs":
			assert len(n.expression) == 2 #constituents and relations
			for sn in n.expression[0].expression:
				assert sn.type == "constituent" or sn.type == "sub"
				if sn.type == "sub":
					for ssn in sn.expression:
						assert len(ssn.expression) == 1
						a1 = ssn.attrib["label"]
						if a1 not in declared_variable:
							Tuples.append(" ".join([n.attrib["label"], "REF", a1]))
							declared_variable.append(a1)
						Tuples.append(" ".join([n.attrib["label"], "CONSTITUENT", "c"+str(c[0])]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
						Tuples.append(" ".join(["c"+str(c[0]), "ARG2", ssn.expression[0].attrib["label"]]))
						c[0] += 1
				elif sn.type == "constituent":
					assert len(sn.expression) == 1
					a1 = sn.attrib["label"]
					if a1 not in declared_variable:
						Tuples.append(" ".join([n.attrib["label"], "REF", a1]))
						declared_variable.append(a1)
					Tuples.append(" ".join([n.attrib["label"], "CONSTITUENT", "c"+str(c[0])]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
					Tuples.append(" ".join(["c"+str(c[0]), "ARG2", sn.expression[0].attrib["label"]]))
					c[0] += 1
					#Tuples.append(" ".join([n.attrib["label"], "DRS", sn.expression[0].attrib["label"]]))
		elif n.type == "constituent":
			pass
		#elif n.type == "sub":
		#	for sn in n.expression:
		#		assert len(sn.expression) == 1
		#		assert sn.expression[0].type == "drs" or sn.expression[0].type == "sdrs"
		#		Tuples.append(" ".join([n.attrib["label"], "DRS", sn.expression[0].attrib["label"]]))
		elif n.type == "relations":
			for sn in n.expression:
				a1 = sn.attrib["arg1"]
				a2 = sn.attrib["arg2"]
				Tuples.append(" ".join([sn.attrib["label"], sn.attrib["sym"], "c"+str(c[0])]))
				Tuples.append(" ".join(["c"+str(c[0]), "ARG1", a1]))
				Tuples.append(" ".join(["c"+str(c[0]), "ARG2", a2]))
				c[0] += 1
				#Tuples.append(" ".join([sn.attrib["label"], sn.attrib["sym"], k2b[a1], k2b[a2]]))
		for subnode in n.expression:
			travel(subnode)
	travel(node)
	return Flag[0], Tuples


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

			flag, Tuples = drg(target_DRSnode)

			#Tuples = redundent_ref(Tuples)
			normal_variables_for_tuples2(Tuples)

			#if flag and len(Tuples) != 0:
			if len(Tuples) != 0:
				print "\n".join(L[:-1])
				print "\n".join(Tuples)
				print 

			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	




