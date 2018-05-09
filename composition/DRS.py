import sys
import string
import re
import types
from util import get_tuple as get_tuple

class DRS:
	def __init__(self):
		self.st = []
		self.st_serialize= ""
	def struct_init(self, st):
		assert type(st) == types.ListType
		self.st = st
	def string_init(self, st):
		assert type(st) == types.StringType
		self.st_serialize = st
	def back_var(self):
		self.st = self.util.back_var(self.st)
	def mark_var(self):
		self.st = self.util.mark_var(self.st)
	def unserialize(self):
		assert self.st_serialize != ""
		self.st = self.unserializing(self.st_serialize)
	def unserializing(self, s):
		inter_rep = []
		idx = s.find("(")

		if idx == -1:
			return s

		name = s[:idx]
		content = s[idx+1:-1]

		idx = name.find(":")
		point = ""
		if idx != -1:
			point = name[:idx]
			name = name[idx+1:]

		inter_rep.append(name)
		inter_rep.append(point)
		indexs = self.util.get_tuple(content, ",")
		if name == "drs":
			assert len(indexs) == 2
			inter_rep.append(self.drs_domains_unserialize(content[0:indexs[0]]))
			inter_rep.append(self.drs_conds_unserialize(content[indexs[0]+1:]))
		elif name == "sdrs":
			assert len(indexs) == 2
			inter_rep.append(self.sdrs_domains_unserialize(content[0:indexs[0]]))
			inter_rep.append(self.sdrs_conds_unserialize(content[indexs[0]+1:]))
		else:
			prev = 0
			for idx in indexs:
				inter_rep.append(self.unserializing(content[prev:idx]))
				prev = idx + 1
		return inter_rep
	def drs_domains_unserialize(self, content):
		domains = []
		if content == "[]":
			return domains
		content = content[1:-1]
		indexs = self.util.get_tuple(content, ",")
		prev = 0
		for idx in indexs:
			indexs2 = self.util.get_tuple(content[prev:idx],":")
			assert len(indexs2) == 3
			domains.append(content[prev:idx][0:indexs2[0]])
			domains.append(content[prev:idx][indexs2[0]+2:indexs2[1]-1])
			domains.append(content[prev:idx][indexs2[1]+1:indexs2[2]])
			prev = idx + 1
		return domains
	def drs_conds_unserialize(self, content):
		conds = []
		if content == "[]":
			return conds
		content = content[1:-1]
		indexs = self.util.get_tuple(content, ",")
		prev = 0
		for idx in indexs:
			indexs2 = self.util.get_tuple(content[prev:idx], ":")
			assert len(indexs2) == 3
			conds.append(content[prev:idx][0:indexs2[0]])
			conds.append(content[prev:idx][indexs2[0]+2:indexs2[1]-1])
			conds.append(self.unserializing(content[prev:idx][indexs2[1]+1: indexs2[2]]))
			prev = idx + 1
		return conds
	def sdrs_domains_unserialize(self, content):
		domains = []
		if content == "[]":
			return domains
		content = content[1:-1]
		indexs = self.util.get_tuple(content, ",")
		prev = 0
		for idx in indexs:
			domains.append(self.unserializing(content[prev:idx]))
			prev = idx + 1
		return domains
	def sdrs_conds_unserialize(self,content):
		conds = []
		if content == "[]":
			return conds
		content = content[1:-1]
		indexs = self.util.get_tuple(content, ",")
		prev = 0
		for idx in indexs:
			indexs2 = self.util.get_tuple(content[prev:idx], ":")
			assert len(indexs2) == 2
			conds.append(content[prev:idx][1:indexs2[0]-1])
			conds.append(self.unserializing(content[prev:idx][indexs2[0]+1:]))
			prev = idx + 1
		return conds
	def serialize(self):
		assert len(self.st) != 0

		self.st_serialize = ""
		self.serializing(self.st)

	def serializing(self, st):
		if type(st) == types.StringType:
			self.st_serialize += st
			return

		assert len(st) >= 2
		if st[0] == "drs":
			assert len(st) == 4
			self.st_serialize += st[1]+":"
			self.st_serialize += "drs("
			self.drs_domain_serialize(st[2])
			self.st_serialize += ","
			self.drs_conds_serialize(st[3])
			self.st_serialize += ")"
		elif st[0] == "sdrs":
			assert len(st) == 4
			self.st_serialize += "sdrs("
			self.sdrs_domain_serialize(st[2])
			self.st_serialize += ","
			self.sdrs_conds_serialize(st[3])
			self.st_serialize += ")"
		else:
			if st[1] != "":
				self.st_serialize += st[1]+":"
			self.st_serialize += st[0]+"("
			for item in st[2:]:
				self.serializing(item)
				self.st_serialize += ","
			self.st_serialize = self.st_serialize.strip(",")+")"
	def drs_domain_serialize(self, st):
		self.st_serialize += "["
		assert len(st) % 3 == 0
		i = 0
		while i < len(st):
			self.st_serialize += "" + st[i] + ":"
			i += 1
			self.st_serialize += "[" + st[i] + "]:"
			i += 1
			self.st_serialize += st[i] + ","
			i += 1
		self.st_serialize = self.st_serialize.strip(",") + "]"
	def drs_conds_serialize(self, st):
		self.st_serialize += "["
		assert len(st) % 3 == 0
		i = 0
		while i < len(st):
			self.st_serialize += "" + st[i] + ":"
			i += 1
			self.st_serialize += "[" + st[i] + "]:"
			i += 1
			self.serializing(st[i])
			self.st_serialize += ","
			i += 1
		self.st_serialize = self.st_serialize.strip(",") + "]"
	def sdrs_domain_serialize(self, st):
		self.st_serialize += "["
		i = 0
		while i < len(st):
			self.serializing(st[i])
			self.st_serialize += ","
			i += 1
		self.st_serialize = self.st_serialize.strip(",") + "]"
	def sdrs_conds_serialize(self, st):
		self.st_serialize += "["
		assert len(st) % 2 == 0
		i = 0
		while i < len(st):
			self.st_serialize += "[" + st[i] + "]:"
			i += 1
			self.serializing(st[i])
			self.st_serialize += ","
			i += 1
		self.st_serialize = self.st_serialize.strip(",") + "]"
