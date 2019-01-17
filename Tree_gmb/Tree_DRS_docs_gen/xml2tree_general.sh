
readarray a < manual_correct

containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


for f in `ls -d data/*/*`
do
	if containsElement $f ${a[@]}; then
		echo "skip $f"
	else
		echo "processing $f"
		python xml2tree_general.py $f/en.drs.xml > $f/en.tree.general
	fi
done	
