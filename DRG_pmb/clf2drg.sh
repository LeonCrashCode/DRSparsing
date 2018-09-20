
for f in `seq -f 'p%02g' 0 99`
do 
	for d in `ls -d ${1}/${f}/*`
	do
		echo ${d}
		python clf2drg.py ${d}
	done
done
