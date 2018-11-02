

for f in `ls -d data/*/*`
do
	echo $f
	python xml2tree.py $f/en.drs.xml > $f/document.tree
done	
