from utils import get_index
from domain import domain
from var import var
from relations import relations

class alfa(object):
	def __init__(self, node):
		self.type = "alfa"
		assert node.tag == "alfa"
		self.label = node.attrib["type"]
		self.expression = []
		for subnode in node:
			if subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "label": self.label, "expression": [expr.serialization() for expr in self.expression]}


class app(object):
	def __init__(self, node):
		self.type = "app"
		self.expression = []
		assert node.tag == "app"
		for subnode in node:
			if subnode.tag == "var":
				self.expression.append(var(subnode))
			elif subnode.tag == "lam":
				self.expression.append(lam(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}


class cond(object):
	def __init__(self, node):
		self.type = "cond"
		assert node.tag == "cond"
		assert len(node) == 1
		subnode = node[0]
		self.expression = []
		self.pointer = node.attrib["label"]
		if True:
			if subnode.tag in ["pred", "rel", "named", "eq", "card", "timex"]:
				self.expression.append(commonR(subnode))
			elif subnode.tag in ["not", "nec", "pos"]:
				self.expression.append(scoped1R(subnode))
			elif subnode.tag in ["imp", "or", "duplex"]:
				self.expression.append(scoped2R(subnode))
			elif subnode.tag == "prop":
				self.expression.append(prop(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "pointer": self.pointer, "expression": [expr.serialization() for expr in self.expression]}

class conds(object):
	def __init__(self, node):
		self.type = "conds"
		assert node.tag == "conds"
		self.expression = []
		for subnode in node:
			if subnode.tag == "cond":
				self.expression.append(cond(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

class constituent(object):
	def __init__(self, node):
		self.type = "constituent"
		assert node.tag == "constituent"
		assert len(node) == 1
		self.label = node.attrib["label"]
		self.expression = []
		for subnode in node:
			if subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "label": self.label, "expression": [expr.serialization() for expr in self.expression]}


class constituents(object):
	def __init__(self, node):
		self.type = "constituents"
		assert node.tag == "constituents"
		self.expression = []
		for subnode in node:
			if subnode.tag == "constituent":
				self.expression.append(constituent(subnode))
			elif subnode.tag == "sub":
				self.expression.append(sub(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

class drs(object):
	def __init__(self, node):
		self.type = "drs"
		assert node.tag == "drs"
		self.expression = []
		for subnode in node:
			if subnode.tag == "domain":
				self.expression.append(domain(subnode))
			elif subnode.tag == "conds":
				self.expression.append(conds(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

class lam(object):
	def __init__(self, node):
		self.type = "lam"
		assert node.tag == "lam"
		self.expression = []
		for subnode in node:
			if subnode.tag == "var":
				self.expression.append(var(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "lam":
				self.expression.append(lam(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

class merge(object):
	def __init__(self, node):
		self.type = "merge"
		assert node.tag == "merge"
		self.expression = []
		for subnode in node:
			if subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

class prop(object):
	def __init__(self, node):
		self.type = "prop"
		self.indexs = get_index(node)
		self.expression = []
		self.label = node.attrib["argument"]
		assert len(node) == 2
		for subnode in node[1:]:
			if subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "label": self.label, "expression": [expr.serialization() for expr in self.expression]}

class commonR(object):
	def __init__(self, node):
		self.type = node.tag
		self.indexs = get_index(node)
		self.attrib = node.attrib
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "attrib":self.attrib}

class scoped1R(object):
	def __init__(self, node):
		self.type = node.tag
		self.indexs = get_index(node)
		self.expression = None
		assert len(node) == 2
		for subnode in node[1:]:
			if subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "expression": [expr.serialization() for expr in self.expression]}


class scoped2R(object):
	def __init__(self, node):
		self.type = node.tag
		self.indexs = get_index(node)
		self.expression = []
		assert len(node) == 3
		for subnode in node[1:]:
			if subnode.tag == "drs":
				self.expression.append(drs(subnode))
			elif subnode.tag == "app":
				self.expression.append(app(subnode))
			elif subnode.tag == "merge":
				self.expression.append(merge(subnode))
			elif subnode.tag == "alfa":
				self.expression.append(alfa(subnode))
			elif subnode.tag == "sdrs":
				self.expression.append(sdrs(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "indexs": self.indexs, "expression": [expr.serialization() for expr in self.expression]}

class sdrs(object):
	def __init__(self, node):
		self.type = "sdrs"
		assert node.tag == "sdrs"
		self.expression = []
		for subnode in node:
			if subnode.tag == "relations":
				self.expression.append(relations(subnode))
			elif subnode.tag == "constituents":
				self.expression.append(constituents(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}


class sub(object):
	def __init__(self, node):
		self.type = "sub"
		assert node.tag == "sub"
		self.expression = []
		for subnode in node:
			if subnode.tag == "constituent":
				self.expression.append(constituent(subnode))
			else:
				print subnode.tag
				assert False, "unrecognized node"
	def serialization(self):
		return {"type": self.type, "expression": [expr.serialization() for expr in self.expression]}

	