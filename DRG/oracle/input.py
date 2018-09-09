import sys

def printout(line, L):
	for it in L[line]:
		it = it.split()[0]
		if it in ["(", "[", "{"]:
			it = "-LRB-"
		if it in [")", "]", "}"]:
			it = "-RRB-" 
		print it,
	print

	for it in L[line]:
		it = it.split()[1]
		if it in ["(", "[", "{"]:
			it = "-lrb-"
		if it in [")", "]", "}"]:
			it = "-rrb-" 
		print it,
	print
	print

if __name__ == "__main__":
	L = {}
	cnt = 0
	total = 0
	prev = ""
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if len(line.split()) == 3:
			prev = " ".join(line.split()[1:])
			L[prev] = []
		else:
			L[prev].append(line)

	for line in open(sys.argv[2]):
		line = line.strip()
		if line[0] == "#":
			continue
		printout(line, L)

		

	#print cnt




