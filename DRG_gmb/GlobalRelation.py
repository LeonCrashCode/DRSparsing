import os
import sys
import re

D = {}
def RelationReader(filename):
	lines = []
	for line in open(filename):
		line = line.strip()
		if line == "" or line[0] == "#":
			continue
		lines.append(line)
	idx = lines.index("Graph")
	lines = lines[idx+1:]
	for line in lines:
		tok = line.split()[1]
		if tok in ["REF", "Named", "Pred", "NOT", "DRS", "POS", "NEC", "IMP", "OR", "DUPLEX", "PRP"]:
			pass
		elif tok.isupper():
			pass
		else:
			if tok in D:
				D[tok] += 1
			else:
				D[tok] = 1

if __name__ == "__main__":
	print "#", " ".join(sys.argv)
	for root, dirs, files in os.walk(sys.argv[1]):
		if len(root.split("/")) != 3:
			continue
		path = root

		sys.stderr.write(path+"\n")
		if not os.path.exists(path+"/en.clf"):
			pass
		else: 
			RelationReader(path+"/en.clf")

	keys = D.keys()
	keys.sort()
	rare_cnt = 0
	for key in keys:
		if D[key] <= 10:
			rare_cnt += D[key]
		else:
			#print key, D[key]
			print key
	#print "__RARE__", rare_cnt
	print "__RARE__"
	#print "\n".join([key+" "+str(D[key]) for key in keys])
