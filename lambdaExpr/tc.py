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

	node.modify_attrib("v1", "x0")
	node.add_variable("x0")
	
	return normal_variables(node, "x")

if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			output = ftr(source_DRSnode)
			
			if L[3] == json.dumps(output.serialization()):
				eq += 1
			total += 1
		else:
			L.append(line)
	print eq, total
	




