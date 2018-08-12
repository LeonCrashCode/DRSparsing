class var(object):
	def __init__(self, node):
		self.type = "var"
		assert node.tag == "var"
		self.label = node.text
	def serialization(self):
		return {"type": self.type, "label": self.label}

	