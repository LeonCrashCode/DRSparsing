

for f in `ls -d ${1}/*/*`
do
	if [ -f ${f}/en.drs.xml ]; then
		echo $f
    	python xml2tree.py $f/en.drs.xml > $f/en.tree
	fi
	
done	
