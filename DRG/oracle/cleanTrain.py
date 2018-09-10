import sys

out_input = open(sys.argv[1] + ".clean", "w")
out_oracle = open(sys.argv[2] +".clean", "w")
ec = []
for line in open("ErrorCond"):
	line = line.strip()
	if line[0] == "#":
		continue
	ec.append(line.split()[0])

out_input.write("# "+" ".join(sys.argv)+"\n")
out_oracle.write("# "+" ".join(sys.argv)+"\n")
L = []
tmp = []
for line in open(sys.argv[1]):
	line = line.strip()
	if line == "":
		L.append(tmp)
		tmp = []
	else:
		if line[0] == "#":
			continue
		tmp.append(line)

def match(line):
	for item in line.split("|||"):
		item = item.split()
		if item[1] in ec:
			return True
	return False

i = 0
for line in open(sys.argv[2]):
	line = line.strip()
	if line[0] == "#":
		continue
	if not match(line):
		out_input.write("\n".join(L[i])+"\n\n")
		out_oracle.write(line+"\n")
		out_input.flush()
		out_oracle.flush()
	i += 1
out_input.close()
out_oracle.close()

