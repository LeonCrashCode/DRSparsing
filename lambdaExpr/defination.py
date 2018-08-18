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
		self.text = node.text.strip()
		self.attrib = node.attrib
		self.indexs = get_index(node)
		for cnode in node:
			if cnode.tag == "indexlist":
				continue
			subnode = DRSnode()
			subnode.init_from_xml(cnode)
			self.expression.append(subnode)
	def unserialization(self, d):
		self.type = d["type"]
		self.text = d["text"]
		self.attrib = d["attrib"]
		self.indexs = d["indexs"]
		for item in d["expression"]:
			node = DRSnode()
			node.unserialization(item)
			self.expression.append(node)
	def serialization(self):
		return {"type": self.type, "text": self.text, "attrib": self.attrib, "indexs": self.indexs, "expression": [expr.serialization() for expr in self.expression]}


	def add_variable(self, to, flag):
		if not flag:
			return
		if self.type == "drs":
			node = DRSnode()
			node.type = "dr"
			node.attrib = {"name": to, "label": self.attrib["label"]}
			self.expression[0].expression.insert(0, node)
			flag = False
		for i in range(len(self.expression)):
			self.expression[i].add_variable(to, flag)

