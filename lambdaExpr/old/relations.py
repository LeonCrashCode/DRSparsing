from utils import get_index
class drel(object):
	def __init__(self, node):
		self.type = node.tag
		self.indexs = get_index(node)
		self.attrib = node.attrib
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "attrib": self.attrib}
class relations(object):
	def __init__(self, node):
		self.type = "relations"
		assert node.tag == "relations"
		self.expression = []
		for subnode in node:
			assert subnode.tag == "drel"
			self.expression.append(drel(subnode))
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}
