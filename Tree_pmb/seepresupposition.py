

import sys
import re


lines = []
for line in open(sys.argv[1]):
	line = line.strip()
	if line[0] == "#":
		continue
	line  = line.split("%")[0].strip()
	if line == "":
		continue

	lines.append(line)

d = {}
for line in lines:
	line = line.split()
	if line[1] == "REF":
		if line[2] in d and line[0] not in d[line[2]]:
			d[line[2]].append(line[0])
		else:
			d[line[2]] = [line[0]]

for line in lines:
	line = line.split()
	if re.match("^\"[anrv]\.[0-9][0-9]\"$", line[2]):
	#	print "Pred"
		if line[0] not in d[line[3]] or len(d[line[3]])>1:
			print "Pred", line
	if line[1] == "Name":
	#	print "Name"
		if line[0] not in d[line[2]]:
			print "Name", line
