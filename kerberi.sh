#!/usr/bin/env bash

OUT="kerberi.txt"
LISTS="lists.txt"
TMP="$OUT-tmp.txt"

echo "clearing $OUT and $LISTS"
rm $OUT
rm $LISTS
echo "writing output to $OUT"

for LIST in $@
do
	echo "$LIST" >> $LISTS
done

while read -r LIST
do
	echo "searching through $LIST"
	blanche $LIST | while read -r listelem
	do
		if [[ "$listelem" =~ ^LIST.* ]]
		then
			echo $listelem | cut -d':' -f 2 >> $LISTS
		else
			echo "$listelem" >> $OUT
		fi
	done
done < $LISTS

# deduplicate
sort -u "$OUT" > "$TMP"
mv "$TMP" "$OUT"

# remove non-kerberoses
awk '!/@/' < $OUT > $TMP
mv "$TMP" "$OUT"

echo "output written to $OUT"
echo "$(wc -l < $OUT) kerberi found"
