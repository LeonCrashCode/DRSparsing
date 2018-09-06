import sys

m = -1
D = {}
for line in open(sys.argv[1]):
	line = line.strip()
	l = len(line.split())
	m = max(m, l)
	if l in D:
		D[l] += 1
	else:
		D[l] = 1 

print m

L = [(key, D[key]) for key in D.keys()]

L.sort()

for item in L:
	print item[0], item[1]



