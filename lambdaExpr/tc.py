import sys
import types
import json
from utils import normal_variables
from utils import 
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tc1(node):

	node = replace_attrib(node, "v1", "x1")

	node_app = DRSnode()
	node_app.type = "app"
	node_var1 = DRSnode()
	node_var1.type = "var"
	node_var1.text = "v1"
	node_var2 = DRSnode()
	node_var2.type = "var"
	node_var2.text = "x1"
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_lam.expression.append(node_app)

	return normal_variables(node_lam, "v")

if __name__ == "__main__":
	L = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			output = ftr(source_DRSnode)
			
			if L[3] == json.dumps(output.serialization()):
				exit(1)
		else:
			L.append(line)
	




