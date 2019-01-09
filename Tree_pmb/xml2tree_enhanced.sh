
readarray a < manual_correct

containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


for f in `ls -d ${1}/*/*`
do
	if containsElement $f ${a[@]}; then
		echo "skip $f"
	else
		if [ -f ${f}/en.drs.xml ]; then
			echo "processing $f"
			python xml2tree_enhanced.py $f/en.drs.xml > $f/sentence.tree.enhanced2
		fi
	fi
done	
