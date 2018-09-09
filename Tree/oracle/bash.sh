python filelist.py  ../tree.notime train > trn.filelist
python filelist.py  ../tree.notime dev > dev.filelist
python filelist.py  ../tree.notime test > tst.filelist

for part in trn dev tst
do
python oracle.py ../tree.notime ../supertag ${part}.filelist > ${part}.oracle
done


