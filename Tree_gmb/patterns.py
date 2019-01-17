import re

drs_n = re.compile("^DRS\-[0-9]+\($")
vb = re.compile("^B[0-9]+$")
vp = re.compile("^P[0-9]+$")
vk = re.compile("^K[0-9]+$")
bp = re.compile("^P[0-9]+\($")
bk = re.compile("^K[0-9]+\($")
vall = re.compile("^[XESTPK][0-9]+$")
