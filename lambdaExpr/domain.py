from utils import get_index
class dr(object):
	def __init__(self, node):
		self.type = "dr"
		assert node.tag == "dr"
		self.indexs = get_index(node)
		self.label =  node.attrib["label"]
		self.name = node.attrib["name"]
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "label": self.label, "name": self.name}


class domain(object):
	def __init__(self, node):
		self.type = "domain"
		assert node.tag == "domain"
		self.expression = []
		for subnode in node:
			assert subnode.tag == "dr"
			self.expression.append(dr(subnode))
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}


	