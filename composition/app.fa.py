import sys
import string
import re
import types

class util:
	def __init__(self):
		self.v_v = re.compile("\$m*?v[0-9]+?\$")
		self.x_v = re.compile("\$m*?x[0-9]+?\$")
		self.e_v = re.compile("\$m*?e[0-9]+?\$")
		self.s_v = re.compile("\$m*?s[0-9]+?\$")
		self.t_v = re.compile("\$m*?t[0-9]+?\$")
		self.p_v = re.compile("\$m*?p[0-9]+?\$")
		self.k_v = re.compile("\$m*?k[0-9]+?\$")
		self.b_v = re.compile("\$m*?b[0-9]+?\$")

	def is_v(self, arg):
		if self.v_v.match(arg):
			return True
		return False
	def is_x(self, arg):
		if self.x_v.match(arg):
			return True
		return False
	def is_e(self, arg):
		if self.e_v.match(arg):
			return True
		return False
	def is_s(self, arg):
		if self.s_v.match(arg):
			return True
		return False
	def is_t(self, arg):
		if self.t_v.match(arg):
			return True
		return False
	def is_p(self, arg):
		if self.p_v.match(arg):
			return True
		return False
	def is_k(self, arg):
		if self.k_v.match(arg):
			return True
		return False
	def is_b(self, arg):
		if self.b_v.match(arg):
			return True
		return False

	def is_var(self, arg):
		if type(arg) != types.StringType:
			return False
		elif self.is_v(arg):
			return True
		elif self.is_x(arg):
			return True
		elif self.is_e(arg):
			return True
		elif self.is_s(arg):
			return True
		elif self.is_t(arg):
			return True
		elif self.is_p(arg):
			return True
		elif self.is_k(arg):
			return True
		elif self.is_b(arg):
			return True
		else:
			return False

	def mark_var(self, st):
		if type(st) == types.StringType:
			if self.is_var(st):
				return "$m"+st[1:-1]+"$"
			else:
				return st
		i = 0
		n_st = []
		while i < len(st):
			n_st.append(self.mark_var(st[i]))
			i += 1
		return n_st
	def mark_var_part(self, st):
		if type(st) == types.StringType:
			if self.is_var(st):
				if self.is_v(st) or self.is_b(st):
					return st
				else:
					return "$mm"+st[1:-1]+"$"
			else:
				return st
		i = 0
		n_st = []
		while i < len(st):
			n_st.append(self.mark_var_part(st[i]))
			i += 1
		return n_st
	def back_var(self, st):
		self.vl = []
		self.xl = []
		self.el = []
		self.sl = []
		self.tl = []
		self.pl = []
		self.kl = []
		self.bl = []
		self.make_var_list(st)
		#print self.bl
		return self.normalize(st)
	def make_var_list(self, st):
		if type(st) == types.StringType:
			if self.is_v(st):
				if st not in self.vl:
					self.vl.append(st)
			elif self.is_x(st):
				if st not in self.xl:
					self.xl.append(st)
			elif self.is_e(st):
				if st not in self.el:
					self.el.append(st)
			elif self.is_s(st):
				if st not in self.sl:
					self.sl.append(st)
			elif self.is_t(st):
				if st not in self.tl:
					self.tl.append(st)
			elif self.is_p(st):
				if st not in self.pl:
					self.pl.append(st)
			elif self.is_k(st):
				if st not in self.kl:
					self.kl.append(st)
			elif self.is_b(st):
				if st not in self.bl:
					self.bl.append(st)
			else:
				return
		for item in st:
			self.make_var_list(item)
	def normalize(self, st):
		if type(st) == types.StringType:
			if self.is_v(st):
				return "$v"+str(self.vl.index(st)+1)+"$"
			elif self.is_x(st):
				return "$x"+str(self.xl.index(st)+1)+"$"
			elif self.is_e(st):
				return "$e"+str(self.el.index(st)+1)+"$"
			elif self.is_s(st):
				return "$s"+str(self.sl.index(st)+1)+"$"
			elif self.is_t(st):
				return "$t"+str(self.tl.index(st)+1)+"$"
			elif self.is_p(st):
				return "$p"+str(self.pl.index(st)+1)+"$"
			elif self.is_k(st):
				return "$k"+str(self.kl.index(st)+1)+"$"
			elif self.is_b(st):
				return "$b"+str(self.bl.index(st)+1)+"$"
			else:
				return st
		i = 0
		n_st = []
		while i < len(st):
			n_st.append(self.normalize(st[i]))
			i += 1
		return n_st

	def get_tuple(self, supertag, split_tag):
		cnt = 0
		cnt1 = 0
		cnt2 = 0
		indexs = []
		for i in range(len(supertag)):
			if supertag[i] == "(":
				cnt += 1
			elif supertag[i] == "[":
				cnt1 += 1
			elif supertag[i] == ")":
				cnt -= 1
			elif supertag[i] == "]":
				cnt1 -= 1
			if cnt == 0 and cnt1 == 0 and cnt2 % 2 == 0 and supertag[i] == split_tag:
				indexs.append(i)
		assert cnt == 0 and cnt1 == 0 and cnt2 % 2 == 0
		indexs.append(len(supertag))
		return indexs

class DRS:
	def __init__(self):
		self.util = util()
		self.outp = 99
		self.supertag = []
		self.supertag_serialize = ""
	def struct_init(self, supertag):
		assert type(supertag) == types.ListType
		self.supertag = supertag
	def string_init(self, supertag):
		assert type(supertag) == types.StringType
		self.supertag_serialize = supertag
	def back_var(self):
		self.supertag = self.util.back_var(self.supertag)
	def mark_var(self):
		self.supertag = self.util.mark_var(self.supertag)
	def unserialize(self):
		assert self.supertag_serialize != ""
		self.supertag = self.unserializing(self.supertag_serialize)
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
		assert len(self.supertag) != 0

		self.supertag_serialize = ""
		self.serializing(self.supertag)

	def serializing(self, supertag):
		if type(supertag) == types.StringType:
			self.supertag_serialize += supertag
			return

		assert len(supertag) >= 2
		if supertag[0] == "drs":
			assert len(supertag) == 4
			self.supertag_serialize += supertag[1]+":"
			self.supertag_serialize += "drs("
			self.drs_domain_serialize(supertag[2])
			self.supertag_serialize += ","
			self.drs_conds_serialize(supertag[3])
			self.supertag_serialize += ")"
		elif supertag[0] == "sdrs":
			assert len(supertag) == 4
			self.supertag_serialize += "sdrs("
			self.sdrs_domain_serialize(supertag[2])
			self.supertag_serialize += ","
			self.sdrs_conds_serialize(supertag[3])
			self.supertag_serialize += ")"
		else:
			if supertag[1] != "":
				self.supertag_serialize += supertag[1]+":"
			self.supertag_serialize += supertag[0]+"("
			for item in supertag[2:]:
				self.serializing(item)
				self.supertag_serialize += ","
			self.supertag_serialize = self.supertag_serialize.strip(",")+")"
	def drs_domain_serialize(self, supertag):
		self.supertag_serialize += "["
		assert len(supertag) % 3 == 0
		i = 0
		while i < len(supertag):
			self.supertag_serialize += "" + supertag[i] + ":"
			i += 1
			self.supertag_serialize += "[" + supertag[i] + "]:"
			i += 1
			self.supertag_serialize += supertag[i] + ","
			i += 1
		self.supertag_serialize = self.supertag_serialize.strip(",") + "]"
	def drs_conds_serialize(self, supertag):
		self.supertag_serialize += "["
		assert len(supertag) % 3 == 0
		i = 0
		while i < len(supertag):
			self.supertag_serialize += "" + supertag[i] + ":"
			i += 1
			self.supertag_serialize += "[" + supertag[i] + "]:"
			i += 1
			self.serializing(supertag[i])
			self.supertag_serialize += ","
			i += 1
		self.supertag_serialize = self.supertag_serialize.strip(",") + "]"
	def sdrs_domain_serialize(self, supertag):
		self.supertag_serialize += "["
		i = 0
		while i < len(supertag):
			self.serializing(supertag[i])
			self.supertag_serialize += ","
			i += 1
		self.supertag_serialize = self.supertag_serialize.strip(",") + "]"
	def sdrs_conds_serialize(self, supertag):
		self.supertag_serialize += "["
		assert len(supertag) % 2 == 0
		i = 0
		while i < len(supertag):
			self.supertag_serialize += "[" + supertag[i] + "]:"
			i += 1
			self.serializing(supertag[i])
			self.supertag_serialize += ","
			i += 1
		self.supertag_serialize = self.supertag_serialize.strip(",") + "]"

	### application
	def reduction(self):
		while True:
			self.have_reduced = False
			self.supertag = self.reduction_proc(self.supertag)
			#self.serialize()
			#print self.supertag_serialize
			if self.have_reduced == False:
				break
		
	def reduction_proc(self, st):
		if type(st) == types.StringType:
			return st
		if len(st) == 0:
			return st
		new_st = []
		if (st[0] == "app") and type(st[2]) == types.ListType and st[2][0] == "lam":
			self.have_reduced = True
			new_st = self.application(st[2], st[3])
		else:
			for item in st:
				new_st.append(self.reduction_proc(item))
		return new_st

	def replace(self, st1, lam):
		if type(st1) == types.StringType:
			if st1 == "sub":
				self.sub_flag = True
			if st1 == lam:
				if type(self.st2) == types.ListType and self.replace_flag and self.sub_flag == False:
					self.st2 = self.util.mark_var_part(self.st2)
					#print "==="
					pass
				self.replace_flag = True
				#print self.st2
				return self.st2
			return st1

		i = 0
		n_st = []
		while i < len(st1):
			n_st.append(self.replace(st1[i], lam))
			i += 1
		return n_st

	def application(self, st1, st2):
		assert len(st1) == 4
		self.st2 = st2
		self.replace_flag = False
		self.sub_flag = False
		st = self.replace(st1[3], st1[2])
		return st

	# merge
	def get_structure(self, st):
		if type(st) == types.StringType or len(st) == 0:
			return ""
		if st[0] == "drs":
			return "drs()"

		struct = ""
		if type(st[0]) == types.StringType:
			struct += st[0]+"("
			if st[0] == "alfa":
				struct = st[0] + "_" +st[2]+"("
		else:
			struct += "list("
		
		if st[0] != "sdrs":
			for item in st:
				struct += self.get_structure(item)
		else:
			for item in st[:-1]:
				struct += self.get_structure(item)
		struct += ")"
		return struct
	def merge(self):
		self.supertag = self.merge_proc(self.supertag)
		self.supertag = self.merge_time(self.supertag)
	def merge_time_value(self, tv1, tv2):
		assert tv1[0] == "+" and tv2[0] == "+"
		assert len(tv1) == 9 and len(tv2) == 9
		ntv = "+"
		i = 1
		while i < 9:
			if tv1[i] == "X" and tv2[i] == "X":
				ntv += "X"
			elif tv1[i] != "X" and tv2[i] == "X":
				ntv += tv1[i]
			elif tv1[i] == "X" and tv2[i] != "X":
				ntv += tv2[i]
			else:
				assert False, "conflict time"
			i += 1
		return ntv
	def merge_time(self, st):
		if type(st) == types.StringType or len(st) == 0:
			return st
		i = 0
		while i < len(st):
			st[i] = self.merge_time(st[i])
			i += 1
		if st[0] == "drs":
			n_conds = []
			i = 0
			while i < len(st[3]):
				bi = st[3][i]
				ii = st[3][i+1]
				ci = st[3][i+2]
				if ci[0] == "timex":
					j = 0
					while j < len(n_conds):
						bj = n_conds[j]
						ij = n_conds[j+1]
						cj = n_conds[j+2]
						if cj[0] == "timex" and bj == bi and cj[2] == ci[2]:
							break
						j += 3
					if j == len(n_conds):
						n_conds.append(bi)
						n_conds.append(ii)
						n_conds.append(ci)
					else:
						n_conds[j+1] += ","+ii
						n_conds[j+2][3] = self.merge_time_value(ci[3], cj[3])
				else:
					n_conds.append(bi)
					n_conds.append(ii)
					n_conds.append(ci)
				i += 3
			st[3] = n_conds
		return st
	def merge_proc(self, st):
		if type(st) == types.StringType or len(st) == 0:
			return st

		i = 0
		while i < len(st):
			st[i] = self.merge_proc(st[i])
			i += 1
		if st[0] != "merge" and st[0] != "alfa":
			return st

		struct = self.get_structure(st)
		print struct
		if struct == "merge(drs()merge(drs()app()))":
			# merge(drs1()merge(drs2()app())) -> merge(drs12()app())
			st[2] = self.drs_combine(st[2], st[3][2])
			st[3] = st[3][3]
			st = st[:4]
		elif struct == "merge(drs()drs())":
			# merge(drs1()drs2()) -> drs12()
			st = self.drs_combine(st[2], st[3])
		elif struct == "alfa_def(drs()merge(drs()app()))":
			# alfa_def(drs1()merge(drs2()app())) -> merge(drs12()app())
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
			pass
		elif struct == "alfa_pro(drs()alfa_def(drs()app()))":
			# alfa_pro(drs1()alfa_def(drs2()app())) -> alfa_def(drs21()app())
			st[4][3] = self.drs_combine(st[3], st[4][3], "2:")
			st = st[4]
		elif struct == "merge(drs()merge(sdrs(list(lab(drs())lab(drs())))app()))":
			# merge(drs1()merge(sdrs(list(lab(drs2())lab(drs3())))app())) -> sdrs(list(lab(drs12())lab(merge(drs3()app()))))
			st[3][2][2][0][3] = self.drs_combine(st[2], st[3][2][2][0][3])
			st[3][2][2][1][3] = ["merge", "", st[3][2][2][1][3], st[3][-1]]
			st = st[3][2]
		elif struct == "alfa_def(drs()alfa_def(drs()app()))":
			# alfa_def(drs1()alfa_def(drs2()app())) -> alfa_def(drs12()app())
			st[4][3] = self.drs_combine(st[3], st[4][3], "1:1/0,2/1")
			st = st[4]
			pass
		elif struct == "merge(drs()merge(merge(drs()app())drs()))":
			# merge(drs1()merge(merge(drs2()app())drs3())) -> merge(drs12()merge(app()drs3()))
			st[2] = self.drs_combine(st[2], st[3][2][2])
			st[3] = ["merge", "", st[3][2][3], st[3][-1]]
			st = st[0:4]
		elif struct == "alfa_def(drs()drs())":
			# alfa_def(drs()drs()) -> drs12()
			st = self.drs_combine(st[3], st[4], "1:1/0,2/1")
		elif struct == "merge(drs()alfa_def(drs()app()))":
			# merge(drs1()alfa_def(drs2()app())) -> merge(drs12()app())
			st[2] = self.drs_combine(st[2], st[3][3], "1:")
			st[3] = st[3][4]
			st = st[0:4]
		elif struct == "alfa_ref(drs()merge(drs()app()))":
			# alfa_ref(drs1()merge(drs2()app())) -> merge(drs12(),app())
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
		elif struct == "alfa_ref(drs()merge(drs()merge(app()app())))":
			# alfa_ref(drs()merge(drs()merge(app()app()))) -> merge(drs12()merge(app()app()))
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
		elif struct == "alfa_pro(drs()merge(drs()merge(app()app())))":
			# alfa_pro(drs()merge(drs()merge(app()app()))) -> merge(drs12()merge(app()app()))
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
		elif struct == "alfa_pro(drs()merge(drs()app()))":
			# alfa_pro(drs()merge(drs()app())) -> merge(drs12()app())
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
		elif struct == "alfa_def(drs()merge(drs()merge(app()merge(drs()app()))))":
			# alfa_def(drs()merge(drs()merge(app()merge(drs()app())))) -> merge(drs12()merge(app()merge(drs3()app()))
			st[4][2] = self.drs_combine(st[3], st[4][2], "1:1/0,2/1")
			st = st[4]
		elif struct == "merge(drs()merge(drs()merge(app()app())))":
			st[3][2] = self.drs_combine(st[2], st[3][2], "1:2/1")
			st = st[3]
		elif struct == "merge(merge(drs()app())drs())":
			# merge(merge(drs1()app())drs2()) -> merge(drs1()merge(app()drs2()))
			st[2][3] = ["merge", "", st[2][3], st[-1]]
			st = st[2]
		elif struct == "merge(drs()merge(drs()merge(app()drs())))":
			# merge(drs()merge(drs()merge(app()drs()))) -> merge(drs12()merge(app()drs3()))
			st[3][2] = self.drs_combine(st[2], st[3][2], "1:2/1")
			st = st[3]
		elif struct == "merge(drs()merge(merge(drs()app())merge(drs()app())))":
			# merge(drs()merge(merge(drs()app())merge(drs()app()))) -> merge(drs12()merge(app()merge(drs()app())))
			
		"""
		if new_st[0] == "merge" and len(new_st) == 3:
			new_st = new_st[2]
		if new_st[0] == "merge":
			new_st = self.merge_drs(new_st)
		if new_st[0] == "merge" and len(new_st) == 3:
			new_st = new_st[2]
		"""
		return st
	def merge_drs(self, st):
		new_st = [st[0], st[1]] #["merge", ""]

		i = 2
		while i < len(st):
			item = st[i]
			assert type(item) == types.ListType
			if item[0] == "drs":
				if type(new_st[-1]) == types.ListType and new_st[-1][0] == "drs":
					new_st[-1] = self.drs_combine(new_st[-1], item)
				else:
					new_st.append(item)
			elif item[0] == "merge":
				for item2 in item[2:]:
					if type(item2) == types.ListType and item2[0] == "drs":
						if type(new_st[-1]) == types.ListType and new_st[-1][0] == "drs":
							new_st[-1] = self.drs_combine(new_st[-1], item2)
						else:
							new_st.append(item2)
					else:
						new_st.append(item2)
			else:
				new_st.append(item)
			i += 1
		new_new_st = [new_st[0], new_st[1]]
		i = 2
		if new_st[2][0] == "drs":
			new_new_st.append(new_st[2])
			i += 1
		while i < len(new_st):
			if new_st[i][0] == "app" and i + 1 < len(new_st) and new_st[i+1][0] == "drs":
				new_new_st.append(["merge", "", new_st[i], new_st[i+1]])
				i += 2
			else:
				new_new_st.append(new_st[i])
				i += 1
		return new_new_st
	def drs_combine(self, drs1, drs2, opt="1:2/1"):
		assert drs1[0] == "drs" and drs2[0] == "drs"
		if opt == "1:2/1":
			p1 = drs1[1]
			p2 = drs2[1]
			drs2[2] = self.change_b(drs2[2], p2, p1)
			drs2[3] = self.change_b(drs2[3], p2, p1)
			drs1[2] += drs2[2]
			drs1[3] += drs2[3]
			return drs1
		elif opt == "1:1/0,2/1":
			p1 = drs1[1]
			p2 = drs2[1]
			drs1[2] = self.change_b(drs1[2], p1, "$b"+str(self.outp)+"$")
			drs1[3] = self.change_b(drs1[3], p1, "$b"+str(self.outp)+"$")
			drs2[2] = self.change_b(drs2[2], p2, p1)
			drs2[3] = self.change_b(drs2[3], p2, p1)
			drs1[2] += drs2[2]
			drs1[3] += drs2[3]
			self.outp += 1
			return drs1
		elif opt == "2:":
			drs2[2] = drs1[2] + drs2[2]
			drs2[3] = drs1[3] + drs2[3]
			return drs2
		elif opt == "1:":
			drs1[2] += drs2[2]
			drs1[3] += drs2[3]
			return drs1

	def change_b(self, l, v_from, v_to):
		if type(l) == types.StringType:
			if l == v_from:
				return v_to
			else:
				return l
		n_l = []
		for item in l:
			n_l.append(self.change_b(item, v_from, v_to))
		return n_l
	
L = []
total = 0
correct1 = 0
correct2 = 0
correct3 = 0
correct4 = 0
n = 0
drs0 = DRS()
drs1 = DRS()
drs2 = DRS()
drs  = DRS()
for line in open("fa"):
	line = line.strip()
	if line == "":
		if "sdrs" in L[0] or "sdrs" in L[1] or "sdrs" in L[2]:
			L = []
			continue
		#if "alfa" in L[0] or "alfa" in L[1] or "alfa" in L[2]:
		#	L = []
		#	continue
		if "XXX" in L[0] or "XXX" in L[1] or "XXX" in L[2]:
			L = []
			continue
		drs0.string_init(L[0])
		drs1.string_init(L[1])
		drs2.string_init(L[2])
		drs0.unserialize()
		drs1.unserialize()
		drs2.unserialize()
		drs0.back_var()
		drs1.back_var()
		drs2.back_var()
		drs0.serialize()
		drs1.serialize()
		drs2.mark_var()
		drs2.serialize()
		#drs1.serialize()
		#drs2.serialize()
		#print drs1.supertag_serialize
		
		drs.struct_init(["app", "", drs1.supertag, drs2.supertag])
		drs.reduction()
		drs.merge()
		drs.back_var()
		drs.serialize()
		if drs.supertag_serialize != drs0.supertag_serialize and len(drs.supertag_serialize) != len(drs0.supertag_serialize):
			print "L1", drs1.supertag_serialize
			print "L2", drs2.supertag_serialize
			print "L0", drs0.supertag_serialize
			print "SU", drs.supertag_serialize
			print
			assert False, "not correct" 
		#print drs.supertag
		#exit(1)
		n += 1
		if n % 1000 == 0:
			print n
		L = []
	else:
		L.append(line)

