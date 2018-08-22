import sys
import types
import json
import re
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

p = re.compile("^v[0-9]+$")
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
						#last_drs = get_last_drs(n.expression[i].expression[0])
						#change_label(last_drs, last_drs.attrib["label"], n.expression[i].expressionp[1].attrib["label"])
						#last_drs.expression[0] += n.expression[i].expression[1].expression[0]
						#last_drs.expression[1] += n.expression[i].expression[1].expression[1]
						#n.expression[i] = n.expression[i].expression[0]
						pass
					elif n.expression[i].expression[0].type == "sdrs" and n.expression[i].expression[1].type == "sdrs":
						print "illegal"
						#print "sdrs sdrs"
						pass
					else:
						print "illegal"
						#print "no"
						pass

	return travel(node)




if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
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
			L.append(line)
	#print cnt




