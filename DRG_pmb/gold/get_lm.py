import sys
import re

p = re.compile(" |~")
#re.split(' |~',str)

raws = []
lines = []
for line in open(sys.argv[1]):
	line = line.strip()
	if line == "":
		raws.append(p.split(lines[0]))
		lines = []
	else:
		lines.append(line)

drss = []
lines = []
for line in open(sys.argv[2]):
	line = line.strip()
	if line == "":
		drss.append(lines)
		lines = []
	else:
		lines.append(line)

assert len(raws) == len(drss)

for i in range(len(raws)):
	print " ".join(raws[i]), "$$$"," ||| ".join(drss[i])