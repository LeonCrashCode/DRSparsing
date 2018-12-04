
import sys

m = {}
for line in open(sys.argv[1]):
	line = line.strip().split()
	m[line[0]] = line[1]

L1 = []
for line in open(sys.argv[2]):
	line = line.strip()
	if line == "":
		continue
	if line in L1:
		continue
	L1.append(line)

L2 = []
for line in open(sys.argv[3]):
	line = line.strip()
	if line == "":
		continue
	if line in L2:
		continue
	L2.append(line)

c = 0
l1 = len(L1)
l2 = len(L2)
for item in L1:
	item = item.split()
	n_item = []
	for ite in item:
		if ite in m:
			n_item.append(m[ite])
		else:
			n_item.append(ite)
	n_item = " ".join(n_item)
	if n_item in L2:
		c += 1

print "Clauses prod :",l1
print "Clauses gold :",l2

print "Matching clauses:", c

