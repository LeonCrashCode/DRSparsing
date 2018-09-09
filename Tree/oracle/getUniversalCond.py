import sys
import re

ps = [ re.compile("^"+start+"[0-9]+?$") for start in ["X","E","S","P","K"]]
pps = [ re.compile("^"+start+"[0-9]+\($") for start in ["P","K"]]
def match(a):
	for p in ps+pps:
		if p.match(a):
			return True

D = {}
L = []
print "#", " ".join(sys.argv)
for line in open(sys.argv[1]):
	line = line.strip()
	if line[0] == "#":
		continue
	L.append(line)
	if len(L) == 3:
		lemmas = L[1].split()
		trees = L[2].split()
		for i in range(len(trees)):
			t = trees[i]
			if t in ["DRS(", "SDRS(", "POS(", "NEC(", "NOT(", "IMP(", "OR(", "DUPLEX(", ")"]:
				continue
			elif match(t):
				continue
			else:
				if t[:-1] not in lemmas:
					if t[:-1] not in D:
						D[t[:-1]] = 1
					else:
						D[t[:-1]] += 1
		L = []

for key in D.keys():
	#print key, D[key]
	print key
