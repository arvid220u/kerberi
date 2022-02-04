#!/usr/bin/env bash

N="$1"
BASE_F="../kerberi_stratified_"
GROUP_N="e3b0c44298fc1c149afb_"
EXT_F=".txt"

# iterate from 0 to N-1
for i in $(seq 0 $((N-1)))
do
    # create file names
    F_IN="$BASE_F$i$EXT_F"
    # iterate through lines in input file
    while read -r line
    do
        # if line is a kerberi, write to output file
        if [[ "$line" =~ ^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}$ ]]
        then
            blanche "$GROUP_N$i" -a "$line"
        fi
    done < "$F_IN"
done