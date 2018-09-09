import sys

if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			docid = int(L[0].split("/")[1][1:])
			if sys.argv[2] == "train":
				if docid <= 99 and docid >= 20:
					print L[0]
			if sys.argv[2] == "dev":
				if docid <= 19 and docid >= 10:
					print L[0]
			if sys.argv[2] == "test":
				if docid <= 9 and docid >= 0:
					print L[0]
			#print cnt, total
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	#print cnt




