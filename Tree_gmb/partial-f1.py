
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

w = [[] for x in range(n)]

for i in range(n):
	for j in range(m):
		t1 = L1[i].split()
		t2 = L2[j].split()
		if t1[0] != t2[0] or t1[1] != t2[1]:
			w[i].append(0)
		else:
			if t1[1] == "DRS":
				if t1[2] == t2[2]:
					w[i].append(1)
				else:
					w[i].append(0.00001)
			else:
				c = 1
				if t1[2] == t2[2]:
					c += 1
				if len(t1) == 4 and len(t2) == 4 and t1[3] == t2[3]:
					c += 1
				w[i].append(2*c*1.0/(len(t1)-1+len(t2)-1))


ly = [0 for x in range(m)]
lx = [0 for x in range(n)]
for i in range(n):
	lx[i] = 0
	for j in range(m):
		if lx[i] < w[i][j]:
			lx[i] = w[i][j]
link = [-1 for x in range(m)]
visx = [False for x in range(n)]
visy = [False for x in range(m)]

def can(t):
	visx[t] = True
	for i in range(m):
		if (not visy[i]) and lx[t] + ly[i] == w[t][i]:
			visy[i] = True
			if link[i] == -1 or can(link[i]):
				link[i] = t
				return True
	return False

for i in range(n):
	flag = False
	while True:
		visx = [False for x in range(n)]
		visy = [False for x in range(m)]
		if can(i):
			break

		d = 10e10
		for j in range(n):
			if visx[j]:
				for k in range(m):
					if not visy[k]:
						d = min(d, lx[j] + ly[k] - w[j][k])
		if d == 10e10:
			flag = True
			break
		for j in range(n):
			if visx[j]:
				lx[j] -= d
		for j in range(m):
			if visy[j]:
				ly[j] += d
	if flag:
		break

visx = [False for x in range(n)]
visy = [False for y in range(m)]
p = 0
r = 0
c = 0
for t, f in enumerate(link):
	t1 = L1[f].split()
	t2 = L2[t].split()
	visx[f] = True
	visy[t] = True
	if t1[1] == "DRS":
		if t1[2] == t2[2]:
			c += 1
		p += 1
		r += 1
	else:
		c += 1
		if t1[2] == t2[2]:
			c += 1
		if len(t1) == 4 and len(t2) == 4 and t1[3] == t2[3]:
			c += 1
		p += len(t1) - 1
		r += len(t2) - 1

for i, t in enumerate(visx):
	if not t:
		p += len(L1[i].split()) - 1

for i, t in enumerate(visy):
	if not t:
		r += len(L2[i].split()) - 1

print "Clauses prod :",p
print "Clauses gold :",r

print "Matching clauses:", c
	
