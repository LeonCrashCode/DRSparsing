import sys
import re

def get_in(filename):
	words = []
	lines = []
	for line in open(filename):
		line = line.strip()
		if line == "":
			words.append(lines[0].split("|||"))
			for i in range(len(words[-1])):
				words[-1][i] = words[-1][i].strip().split()
			lines = []
		else:
			lines.append(line)
	return words

def get_out(filename):
	trees = []
	for line in open(filename):
		line = line.strip()
		trees.append(line.split())
	return trees

def out_tree(lemmas, trees):
	assert len(lemmas) == len(trees)

	i = 0
	cur = 0
	while i < len(lemmas):
		j = 0
		k = 1
		p = 1
		while j < len(trees[i]):
			if re.match("^DRS-[0-9]+\($", trees[i][j]):
				cur = int(trees[i][j][4:-1])
				trees[i][j] = "DRS("
				assert cur < len(lemmas[i])
			elif re.match("^\$[0-9]+\($",trees[i][j]):
				idx = int(trees[i][j][1:-1])
				trees[i][j] = lemmas[i][cur][idx]+"("
			elif re.match("^\$[0-9]+$", trees[i][j]):
				idx = int(trees[i][j][1:])
				trees[i][j] = '"'+lemmas[i][cur][idx]+'"'
			elif re.match("^[anvr]\.[0-9][0-9]$", trees[i][j]):
				trees[i][j] = '"'+trees[i][j] + '"'
			elif trees[i][j] == "@P(":
				trees[i][j] = "P"+str(p)+"("
				p += 1
			elif trees[i][j] == "@K(":
                                trees[i][j] = "K"+str(k)+"("
                                k += 1
			j += 1
		i += 1

if __name__ == "__main__":
	words = get_in(sys.argv[1])
	trees = get_out(sys.argv[2])

	out_tree(words, trees)
	
	for i in range(len(words)):
		print "#", " ||| ".join([" ".join(word) for word in words[i]])
		print " ".join(trees[i])
