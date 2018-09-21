
for f in `seq -f 'p%02g' 0 99`
do 
	for d in `ls -d data/${f}/*`
	do
		echo ${d}
		python drs2drg.py ${d}/en.drs.xml > ${d}/en.drg2
	done
done
