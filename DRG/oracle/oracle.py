import sys

def printout(line, L):
	print " ||| ".join(L[line]) + " TERM"

if __name__ == "__main__":
	L = {}
	tmpL = []
	cnt = 0
	total = 0
	prev = ""
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			if len(tmpL) == 0:
				continue
			L[tmpL[0]] = tmpL[3:]
			tmpL = []
		else:
			if line[0] == "#":
				continue
			tmpL.append(line)

	for line in open(sys.argv[2]):
		line = line.strip()
		if line[0] == "#":
			continue
		printout(line, L)

		

	#print cnt




