import sys
import types
import re

px = re.compile("^x[0-9]+?$")
pt = re.compile("^t[0-9]+?$")

def simplify_time(L):
	variable = []

	while True:
		l = len(variable)
		for tuples in L:
			tuples = tuples.split()
			for tup in tuples:
				if pt.match(tup):
					if tup not in variable:
						variable.append(tup)
		for tuples in L:
			tuples = tuples.split()
			if tuples[1] == "EQU":
				if px.match(tuples[-1]) and pt.match(tuples[-2]):
					if tuples[-1] not in variable:
						variable.append(tuples[-1])
				if px.match(tuples[-2]) and pt.match(tuples[-1]):
					if tuples[-2] not in variable:
						variable.append(tuples[-2])
		if len(variable) == l:
			break

	new_L = []
	for tuples in L:
		tuples = tuples.split()
		if "temp_" in tuples[1]:
			continue
		elif tuples[-1] in variable:
			continue
		elif tuples[-2] in variable:
			continue
		else:
			new_L.append(" ".join(tuples))

	variable = []
	for tuples in new_L:
		tuples = tuples.split()
		if tuples[1] == "REF":
			continue
		for tup in tuples[2:]:
			if tup not in variable:
				variable.append(tup)

	new_new_L = []
	for tuples in new_L:
		tuples = tuples.split()
		if tuples[1] == "REF" and tuples[-1] not in variable:
			continue
		else:
			new_new_L.append(" ".join(tuples))
	return new_new_L

if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1

			newL = simplify_time(L[3:])
			print "\n".join(L[:3])
			print "\n".join(newL)
			print 
			#print cnt, total
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	#print cnt




