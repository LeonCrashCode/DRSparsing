from utils import equals
import json
import sys
def exist(supertag, supertag_cls):
	for i, tag in enumerate(supertag_cls,0):
		#if equals(supertag, tag[0]):
		if supertag == tag[0]:
			return True, i
	return False, -1

def main(filename):
	supertag_cls = []
	for line in open(filename):
		line = line.strip()
		if line.split()[0] == "===":
			sys.stderr.write(line+"\n")
			continue
		#supertag = json.loads(line.split("\t")[-1])
		supertag = "|||".join(line.split("\t")[-2:])
		f, i = exist(supertag, supertag_cls)
		if f:
			supertag_cls[i][-1] += 1
		else:
			supertag_cls.append([supertag, 1])

	supertag_cls = sorted(supertag_cls, key=lambda x:x[1], reverse=True)
	for tag, count in supertag_cls:
		#print json.dumps(tag), count
		print tag, count

if __name__ == "__main__":
	main(sys.argv[1])