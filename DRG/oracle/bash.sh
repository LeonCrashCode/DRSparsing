mkdir ${1}
python filelist.py  ../${1} train > ${1}/trn.filelist
python filelist.py  ../${1} dev > ${1}/dev.filelist
python filelist.py  ../${1} test > ${1}/tst.filelist

for part in trn dev tst
do
python input.py ../supertag ${1}/${part}.filelist > ${1}/${part}.input
python oracle.py ../${1} ${1}/${part}.filelist > ${1}/${part}.oracle
done


