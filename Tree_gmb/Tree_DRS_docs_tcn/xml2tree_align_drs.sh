

for f in `ls -d data/*/*`
do
	echo $f
	python xml2tree_align_drs.py $f/en.drs.xml > $f/document.tree.tcn.align_drs
done	
