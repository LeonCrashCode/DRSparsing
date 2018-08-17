import sys
import types
import json
from utils import normal_variables
from utils import equals
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def btr(node):
	node_lam = DRSnode()
	node_lam.type = "lam"

	node_var = DRSnode()
	node_var.type = "var"
	node_var.text = "v0"
	node_lam.expression.append(node_var)


	node_app = DRSnode()
	node_app.type = "app"
	node_var = DRSnode()
	node_var.type = "var"
	node_var.text = "v0"
	node_app.expression.append(node_var)
	node_app.expression.append(node)

	node_lam.expression.append(node_app)

	return normal_variables(node_lam, "v")

if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)
			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			output = btr(source_DRSnode)
			
			if equals(target, output.serialization()):
				eq += 1
			total += 1
			L = []	
		else:
			L.append(line)
	print eq, total
	




