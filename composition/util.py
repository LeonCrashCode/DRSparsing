import re
import types


var_p = re.compile("\$m*?[vxestpkb][0-9]+?\$")

def is_var(arg):
		if type(arg) != types.StringType:
			return False
		elif var_p.match(arg):
			return True
		else:
			return False

def get_tuple(st, split_tag):
	cnt = 0
	cnt1 = 0
	cnt2 = 0
	indexs = []
	for i in range(len(st)):
		if st[i] == "(":
			cnt += 1
		elif st[i] == "[":
			cnt1 += 1
		elif st[i] == ")":
			cnt -= 1
		elif st[i] == "]":
			cnt1 -= 1
		if cnt == 0 and cnt1 == 0 and cnt2 % 2 == 0 and st[i] == split_tag:
			indexs.append(i)
	assert cnt == 0 and cnt1 == 0 and cnt2 % 2 == 0
	indexs.append(len(st))
	return indexs
