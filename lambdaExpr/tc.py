import sys
import types
import json
from utils import normal_variables
from utils import get_last_drs_node
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def tc1(node, start): #N->NP, merge
	v = start + "0"

	node_app = DRSnode()
	node_app.type = "app"
	node_var1 = DRSnode()
	node_var1.type = "var"
	node_var1.text = "v1"
	node_var2 = DRSnode()
	node_var2.type = "var"
	node_var2.text = v
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_merge = DRSnode()
	node_merge.type = "merge"

	node.modify_attrib("v1", v)
	node.add_variable(v, True)

	node_last, idx = get_last_drs_node(node)
	node_merge.expression.append(node_last.expression[idx])
	node_merge.expression.append(node_app)
	node_last.expression[idx] = node_merge

	normal_variables(node)

	return node

def tc2(node, start): #N->NP. alfa def
	v = start + "0"

	node_app = DRSnode()
	node_app.type = "app"
	node_var1 = DRSnode()
	node_var1.type = "var"
	node_var1.text = "v1"
	node_var2 = DRSnode()
	node_var2.type = "var"
	node_var2.text = v
	node_app.expression.append(node_var1)
	node_app.expression.append(node_var2)

	node_merge = DRSnode()
	node_merge.type = "alfa"
	node_merge.attrib = {"type": "def"}

	node.modify_attrib("v1", v)
	node.add_variable(v, True)
	
	node_last, idx = get_last_drs_node(node)
	node_merge.expression.append(node_last.expression[idx])
	node_merge.expression.append(node_app)
	node_last.expression[idx] = node_merge

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
			source_DRSnode = tc1(source_DRSnode, "x")
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc1(source_DRSnode, "s")
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc2(source_DRSnode, "x")
			change = json.dumps(source_DRSnode.serialization())

			if target == change:
				eq += 1
				L = []
				continue

			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			source_DRSnode = tc2(source_DRSnode, "s")
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
	




