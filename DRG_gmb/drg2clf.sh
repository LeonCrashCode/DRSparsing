
for f in `seq -f 'p%02g' 0 99`
do 
	for d in `ls -d data/${f}/*`
	do
		echo ${d}
		python drg2clf.py ${d}/en.drg2 > ${d}/en.clf
	done
done
