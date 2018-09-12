import sys
import os
def change(a):
	if a in ["("]:
		return "-LRB-"
	elif a in [")"]:
		return "-RRB-"
	return a
for root, dirs, files in os.walk("data_sentence"):
	if len(root.split("/")) != 3:
		continue

	Ldrs = []
	out = open(root+"/sentence.sent_drs", "w")
	for line in open(root+"/sentence.drs"):
		line = line.strip()
		Ldrs.append(line)

	cnt = 0
	for line in open(root+"/sentence.logic"):
		line = line.strip()
		if cnt % 2 == 0:
			out.write(" ".join([ change(x.split()[0]) for x in line.split("|||")]) + "\n")
			out.write(" ".join([ change(x.split()[1]).lower() for x in line.split("|||")]) + "\n")
			out.write(Ldrs[cnt/2] + "\n")
		cnt += 1
	out.close()
	assert cnt/2 == len(Ldrs)


