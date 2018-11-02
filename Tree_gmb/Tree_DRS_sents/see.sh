

more +${1} ${2}.out | head -1 > ${2}.out.part

n=${1}

n=$((n*3-2))

more +${n} ${2}.in | head -3 > ${2}.in.part
