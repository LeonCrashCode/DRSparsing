import sys

L1 = [[]]
for line in open(sys.argv[1]):
	line = line.strip()
	L1[-1].append(line)
	if len(L1[-1]) == 3:
		L1.append([])
L1.pop()
L2 = [[]]
for line in open(sys.argv[2]):
	line = line.strip()
	L2[-1].append(line)
	if len(L2[-1]) == 3:
		L2.append([])
L2.pop()
i = 0
j = 0
while i < len(L1) and j < len(L2):
	if L1[i][0] == L2[j][0]:
		print L1[i][2]
		i += 1
		j += 1
	else:
		print i*3,j*3
		exit(1)
