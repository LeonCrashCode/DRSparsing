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
	node_var2.text = "x0"
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_merge = DRSnode()
	node_merge.type = "merge"

	node.modify_attrib("v1", "x0")
	node.add_variable("x0", True)

	node_merge.expression.append(node.expression[1])
	node_merge.expression.append(node_app)
	node.expression[1] = node_merge

	normal_variables(node)

	return node

def tc2(node): #N->NP. alfa def

	node_app = DRSnode()
	node_app.type = "app"
	node_var1 = DRSnode()
	node_var1.type = "var"
	node_var1.text = "v1"
	node_var2 = DRSnode()
	node_var2.type = "var"
	node_var2.text = "x0"
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_merge = DRSnode()
	node_merge.type = "alfa"
	node_merge.attrib = {"type": "def"}

	node.modify_attrib("v1", "x0")
	node.add_variable("x0", True)
	
	node_merge.expression.append(node.expression[1])
	node_merge.expression.append(node_app)
	node.expression[1] = node_merge

	normal_variables(node)
	return node

def tc2_s(node): #N->NP. alfa def

	node_app = DRSnode()
	node_app.type = "app"
	node_var1 = DRSnode()
	node_var1.type = "var"
	node_var1.text = "v1"
	node_var2 = DRSnode()
	node_var2.type = "var"
	node_var2.text = "s0"
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_merge = DRSnode()
	node_merge.type = "alfa"
	node_merge.attrib = {"type": "def"}

	node.modify_attrib("v1", "s0")
	node.add_variable("s0", True)
	
	node_merge.expression.append(node.expression[1])
	node_merge.expression.append(node_app)
	node.expression[1] = node_merge

	normal_variables(node)

	return node


if __name__ == "__main__":
	L = []
	eq = 0
	total = 0
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			total += 1
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)
			normal_variables(target_DRSnode)
			target = json.dumps(target_DRSnode.serialization())

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc1(source_DRSnode)
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc2(source_DRSnode)
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc2_s(source_DRSnode)
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			print "\n".join(L)
			print
			L = []
		else:
			L.append(line)
	print eq, total
	




