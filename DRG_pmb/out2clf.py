import sys
import re

def read_input(filename):
	o = [[]]
	for line in open(filename):
		line = line.strip()
		if line == "":
			o.append([])
		else:
			o[-1].append(line)
	return o[:-1]

def read_output(filename):
	o = []
	for line in open(filename):
		line = line.strip()
		o.append(line)
	return o

def addsense(output):
	output = output.split()
	if output[-1] == "<END>":
		output.pop()
	if output[-1] == "|||":
		output.pop()
	output = " ".join(output)
	output = output.split("|||")
	for i in range(len(output)):
		toks = output[i].split()
		if toks[1] in ["REF", "DRS", "PRP", "NOT", "NEC", "POS", "IMP", "DUP", "OR", "EQU", "NEQ", "APX", "LES", "LEQ", "TPR", "TAB"]:
			continue
		if len(toks) == 4:
			continue
		output[i] = " ".join([toks[0], toks[1], "\"n.01\"", toks[2]])
	return " ||| ".join(output)

def out2clf(output, input):
	vs = ["B", "X", "E", "S", "T", "P"]
	count = [0 for i in range(6)] # b x e s t p
	p = re.compile("^\$[0-9]+$")
	input = input.split()
	output = output.split()
	if output[-1] == "<END>":
		output.pop()
	if output[-1] == "|||":
		output.pop()
	cnt = 0
	for item in output:
		cnt += 1
		if item == "|||":
			cnt = 0
			print
		elif item in vs:
			idx = vs.index(item)
			print item.lower()+str(count[idx]),
			count[idx] += 1
		elif p.match(item):
			if cnt == 2:
				print input[int(item[1:])],
			else:
				print "\""+input[int(item[1:])]+"\"",
		else:
			print item,


if __name__ == "__main__":
	inputs = read_input(sys.argv[1])
	outputs = read_output(sys.argv[2])

	print "#", " ".join(sys.argv)
	#print len(inputs)
	#print len(outputs)
	assert len(inputs) == len(outputs)

	for i in range(len(inputs)):
		outputs[i] = addsense(outputs[i])
		out2clf(outputs[i], inputs[i][1])
		print
		print 