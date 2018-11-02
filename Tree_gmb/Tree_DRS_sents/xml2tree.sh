

for f in `ls -d data/*/*`
do
	echo $f
	python xml2tree.py $f/sentence.drs.xml > $f/sentence.tree
done	
