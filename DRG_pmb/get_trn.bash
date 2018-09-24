
cat data/silver/p0[2-9]/*/en.drg > tmp0

for i in `seq 1 9`
do
cat data/silver/p${i}[0-9]/*/en.drg > tmp${i}
done

cat tmp* > trn.drg
rm tmp*
