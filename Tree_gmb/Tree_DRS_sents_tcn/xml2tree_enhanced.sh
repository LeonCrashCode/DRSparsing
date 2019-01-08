

for f in `ls -d data/*/*`
do
	echo $f
	python xml2tree_enhanced.py $f/sentence.drs.xml > $f/sentence.tree.enhanced2
done	
