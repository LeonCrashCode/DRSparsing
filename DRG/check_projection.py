import sys
import types
import re

px = re.compile("^x[0-9]+?$")
pt = re.compile("^t[0-9]+?$")

def check(L):

	"""
	variable = {}
	for tuples in L:
		tuples = tuples.split()
		if tuples[1] == "REF":
			variable[tuples[2]] = tuples[0]
	"""
	cond_variable = {}
	for tuples in L:
		tuples = tuples.split()
		if tuples[1] == "REF":
			continue
		if len(tuples) == 3:
			if tuples[-1] in cond_variable:
				print tuples
				assert cond_variable[tuples[-1]] == tuples[0]
			else:
				cond_variable[tuples[-1]] = tuples[0]

if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			print L[0]
			check(L[3:])
			#print cnt, total
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	#print cnt




