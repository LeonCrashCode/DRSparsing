

for f in `ls -d data/*/*`
do
	echo $f
	python xml2tree_align.py $f/en.drs.xml > $f/document.tree.align 
done	
