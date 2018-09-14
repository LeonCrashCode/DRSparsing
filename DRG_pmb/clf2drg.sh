
for d in `ls -d ${1}/*/*`
do
echo ${d}
python clf2drg.py ${d}
done
