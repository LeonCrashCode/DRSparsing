import sys
import re

from number import getCard
from number import getTimex

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

out1 = open("number", "w")
out2 = open("time", "w")
def get_in(filename):
	words = []
	lines = []
	for line in open(filename):
		line = line.strip().decode("UTF-8")
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
		line = line.strip().decode("UTF-8")
		trees.append(line.split())
	return trees

def getLem(w, t):
	t = t[0]
	tag = None
	if t == "a":
		tag = wordnet.ADJ
	elif t == "v":
		tag = wordnet.VERB
	elif t == "n":
		tag = wordnet.NOUN
	elif t == "r":
		tag = wordnet.ADV
	else:
		assert False, "unrecognized tag"

	lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(w[:-1].lower(), tag)+"("
		
def ground(l):
	i = 0
	n_l = []
	while i < len(l):
		if l[i] == "Named(":
			idx = l[i:].index(")")
			assert idx == 4
			n_l += l[i:i+idx+1]
			i = i + idx + 1
		elif l[i] in ["DRS(", "SDRS(", "NEC(", "POS(", "NOT(", "DUP(", "OR(", "IMP(", ")"]:
			n_l.append(l[i])
			i += 1
		elif re.match("^[PK][0-9]+\($", l[i]):
			n_l.append(l[i])
			i += 1
		elif re.match("^[XESTPKB][0-9]+$", l[i]):
			n_l.append(l[i])
			i += 1
		elif l[i] == "Card(":
			idx = l[i:].index(")")
			n_l.append(l[i])
			n_l.append(l[i+1])
			n_l.append(l[i+2])
			value = getCard(l[i+3:i+idx])
			n_l.append(value)
			n_l.append(")")
			i = i + idx + 1
		elif re.match("^T[yx][mx][dx]\($", l[i]):
			idx = l[i:].index(")")
			n_l.append("Timex(")
                        n_l.append(l[i+1])
			n_l.append(l[i+2])
                        value = getTimex(l[i], l[i+3:i+idx])
                        n_l.append(value)
                        n_l.append(")")
                        i = i + idx + 1
		elif l[i][-1] == "(":
			if re.match("^[anvr]\.[0-9][0-9]$", l[i+3]):
				lem = getLem(l[i], l[i+3])
				idx = l[i:].index(")")
				n_l.append(lem)
				n_l = n_l + l[i+1:i+idx+1]
				i = i + idx + 1
			else:
				idx = l[i:].index(")")
                                n_l = n_l + l[i:i+idx+1]
                                i = i + idx + 1
		else:
			assert False, "unrecognized token"
	return n_l
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
				trees[i][j] = lemmas[i][cur][idx]
			elif trees[i][j] == "@P(":
				trees[i][j] = "P"+str(p)+"("
				p += 1
			elif trees[i][j] == "@K(":
                                trees[i][j] = "K"+str(k)+"("
                                k += 1
			j += 1
		trees[i] = ground(trees[i])
		i += 1

if __name__ == "__main__":
	words = get_in(sys.argv[1])
	trees = get_out(sys.argv[2])

	out_tree(words, trees)
	
	for i in range(len(words)):
		#print "#", " ||| ".join([" ".join(word) for word in words[i]]).encode("UTF-8")
		print " ".join(trees[i]).encode("UTF-8")
