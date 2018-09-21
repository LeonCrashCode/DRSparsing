
for f in `seq -f 'p%02g' 0 99`
do 
	for d in `ls -d ${1}/${f}/*`
	do
		echo ${d}
		python drg2clf.py  ${d}/en.drg > ${d}/en.clf
	done
done
