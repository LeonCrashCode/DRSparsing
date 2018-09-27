
cat data/silver/p0[2-9]/*/en.clf > tmp0

for i in `seq 1 9`
do
cat data/silver/p${i}[0-9]/*/en.clf > tmp${i}
done

cat tmp* > trn.clf
rm tmp*
