import sys

print "#", " ".join(sys.argv)
L = []
tmp = []
for line in open(sys.argv[1]):
	line = line.strip()
	if line == "":
		L.append(tmp[1].split())
		tmp = []
	else:
		if line[0] == "#":
			continue
		tmp.append(line)

D = {}
i = 0
for line in open(sys.argv[2]):
	line = line.strip()
	if line[0] == "#":
		continue
	for item in line.split("|||"):
		item = item.split()
		if item[1] in ["DRS", "NEC", "POS", "NOT", "DUPLEX", "IMP", "OR", "SUB"]:
			continue
		if item[1] not in L[i]:
			if item[1] not in D:
				D[item[1]] = 1
			else:
				D[item[1]] += 1
	i += 1

for key in D.keys():
	print key