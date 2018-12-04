
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
	line = line.split()
	new_line = []
	for item in line:
		if item in m:
			new_line.append(m[item])
		else:
			new_line.append(item)
	L1.append(" ".join(new_line))

L2 = []
for line in open(sys.argv[3]):
	line = line.strip()
	if line == "":
		continue
	if line in L2:
		continue
	L2.append(line)

n = len(L1)
m = len(L2)

visx = [False for x in range(n)]
visy = [False for x in range(m)]
fc = 0
fp = 0
fr = 0
for i, t1 in enumerate(L1):
	t1 = t1.split()
	maxf = -1
	maxj = -1
	maxc = 0
	maxp = 0
	maxr = 0
	#print t1
	for j, t2 in enumerate(L2):
		if visy[j] == True:
			continue
		t2 = t2.split()
		if t1[0] != t2[0] or t1[1] != t2[1]:
			continue
		else:
			c = 0
			p = 0
			r = 0
			if t1[1] == "DRS":
				if t1[2] == t2[2]:
					c = 1
				p += 1
				r += 1
			else:
				c = 1
				if t1[2] == t2[2]:
					c += 1
				if len(t1) == 4 and len(t2) == 4 and t1[3] == t2[3]:
					c += 1
				p += len(t1) - 1
				r += len(t2) - 1
			if maxf < 2*c*1.0/(p+r):
				maxj = j
				maxf = 2*c*1.0/(p+r)
				maxc = c
				maxp = p
				maxr = r
	if maxf != -1:
		#print L2[maxj].split()
		visx[i] = True
		visy[maxj] = True
		fc += maxc
		fp += maxp
		fr += maxr

for i in range(n):
	if not visx[i]:
		fp += len(L1[i].split()) - 1
for i in range(m):
	if not visy[i]:
		fr += len(L2[i].split()) - 1

print "Clauses prod :",fp
print "Clauses gold :",fr

print "Matching clauses:", fc

