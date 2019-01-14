

for d in `ls -d ${1}/*`
do
	echo ${d}
	for f in `ls -d ${d}/*`
	do
                	if [ -f ${f}/en.drs.clf ]; then
                        	echo "processing $f"
                        	python seepresupposition.py $f/en.drs.clf
                	fi

	done
done

