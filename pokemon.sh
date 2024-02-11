#!/bin/bash
cat topics.txt | while read n;
do
	python3 search.py $n
done
#EOF