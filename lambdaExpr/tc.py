import sys
import types
import json
from utils import normal_variables
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tc1(node): #N->NP, merge

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

	node_merge = DRSnode()
	node_merge.type = "merge"

	node.modify_attrib("v1", "x0")
	node.add_variable("x0", True)
	node = normal_variables(node, "x")

	node_merge.expression.append(node.expression[1])
	node_merge.expression.append(node_app)
	node.expression[1] = node_merge

def tc2(node): #N->NP. alfa def

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

	node_merge = DRSnode()
	node_merge.type = "alfa"
	node_merge.attrib = {"type": "def"}

	node.modify_attrib("v1", "x0")
	node.add_variable("x0", True)
	node = normal_variables(node, "x")

	node_merge.expression.append(node.expression[1])
	node_merge.expression.append(node_app)
	node.expression[1] = node_merge




if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			source1 = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode1 = DRSnode()
			source_DRSnode1.unserialization(source1)
			tc1(source_DRSnode1)

			source2 = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode2 = DRSnode()
			source_DRSnode2.unserialization(source2)
			tc2(source_DRSnode2)
			#print json.dumps(output.serialization())

			if L[3] == json.dumps(source_DRSnode1.serialization()) or L[3] == json.dumps(source_DRSnode2.serialization()):
				eq += 1
			else:
				#print "\n".join(L)
				print 
			total += 1
			L = []
		else:
			L.append(line)
	print eq, total
	




