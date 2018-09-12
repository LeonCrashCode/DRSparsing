import sys
import os
import xml.etree.ElementTree as ET
filename = ""
der = 0
import json
from defination import DRSnode

def add_pointer(node, start):

	index = [start]
	def travel(n):
		if n.type == "sdrs" or n.type == "sub":
			n.attrib["label"] = "b"+str(index[0])
			index[0] += 1
			for drel in n.expression[1].expression:
				drel.attrib["label"] = n.attrib["label"]
		for sn in n.expression:
			travel(sn)
	travel(node)



def process_drs(parent, out):
	assert parent.tag == "drs"

	supertag = DRSnode()
	supertag.init_from_xml(parent)
	add_pointer(supertag, 1000)
	out.write(json.dumps(supertag.serialization())+"\n")
for root, dirs, files in os.walk("data_sentence"):
	if len(root.split("/")) != 3:
		continue
	tree = ET.parse(root+"/sentence.drs.xml.notime.index_normalized")
	filename = root
	root = tree.getroot()
	out = open(filename+"/sentence.drs","w")
	print filename
	for child in root:
		process_drs(child, out)


