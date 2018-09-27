
for f in `seq -f 'p%02g' 0 99`
do 
	for d in `ls -d ${1}/${f}/*`
	do
		echo ${d}
		python preprocessCLF.py ${d}/en.drs.xml ${d}/en.drs.clf > ${d}/en.clf
	done
done
