import sys
import re

ec = ["K15", "P10", "X40", "E15", "S15"]
for line in open("ErrorCond"):
	line = line.strip()
	ec.append(line.split()[0]+"(")


L = []
print "#", " ".join(sys.argv)

def have_ec(trees):
	for t in trees:
		if t in ec:
			return True

	return False

for line in open(sys.argv[1]):
	line = line.strip()
	if line[0] == "#":
		continue
	L.append(line)
	if len(L) == 3:
		trees = L[2].split()
		if not have_ec(trees):
			print "\n".join(L)
		L = []

