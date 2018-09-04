import sys
import types
import json
import re
from defination import DRSnode
from utils import normal_variables

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())



if __name__ == "__main__":
	L = []
	cnt = 0
	total = 0
	print "#", " ".join(sys.argv)
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)
			
			normal_variables(target_DRSnode)

			L[3] = json.dumps(target_DRSnode.serialization())
			print "\n".join(L)
			print
			#print cnt, total
			L = []
		else:
			if line[0] == "#":
				continue
			L.append(line)
	#print cnt




