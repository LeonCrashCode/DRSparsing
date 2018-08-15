import sys
import types
import json
from utils import normal_variables
from defination import DRSnode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

def ftr(expre):
	expre_lam = DRSnode()
	expre_lam.type = "lam"

	expre_v1 = DRSnode()
	expre_v1.type = "var"
	expre_v1.text = "v0"

	expre_lam.expression.append(expre_v1)

	expre_app = DRSnode()
	expre_app.type = "app"
	expre_app.expression.append(expre_v1)
	expre_app.expression.append(expre)

	expre_lam.expression.append(expre_app)


	return normal_variables(expre_lam.serialization(), "v")

if __name__ == "__main__":
	L = []
	for line in open(sys.argv[1]):
		line = line.strip()
		if line == "":
			target = json.loads(L[3], object_hook=ascii_encode_dict)
			target_DRSnode = DRSnode()
			target_DRSnode.unserialization(target)
			source = json.loads(L[5], object_hook=ascii_encode_dict)
			source_DRSnode = DRSnode()
			source_DRSnode.unserialization(source)
			output = ftr(source_DRSnode)
			print json.dumps(output)
			exit(1)
		else:
			L.append(line)
	




