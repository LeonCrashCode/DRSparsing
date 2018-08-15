from utils import get_index

class DRSnode(object):
	def __init__(self):
		self.type = ""
		self.text = ""
		self.attrib = {}
		self.expression = []
		self.indexs = []
	def init_from_xml(self, node):
		self.type = node.tag
		self.text = node.text
		self.attrib = node.attrib
		self.indexs = get_index(node)
		for cnode in node:
			if cnode.tag == "indexlist":
				continue
			subnode = DRSnode()
			subnode.init_from_xml(cnode)
			self.expression.append(subnode)
	def serialization(self):
		return {"type": self.type, "text": self.text, "attrib": self.attrib, "indexs": self.indexs, "expression": [expr.serialization() for expr in self.expression]}

