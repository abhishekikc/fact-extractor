#!/bin/bash

set -e

cd ..
# Download latest Italian Wikipedia dump
wget http://download.wikimedia.org/itwiki/latest/itwiki-latest-pages-articles.xml.bz2
# Extract text
bzcat itwiki-latest-pages-articles.xml.bz2 | scripts/lib/WikiExtractor.py
# Split extraction by article
cat extracted/*/* | csplit --suppress-matched -z -f 'corpus/doc_' - '/</doc>/' {*}
# Build a single big file
find extracted -type f -exec cat {} \; > all-extracted.txt
# Extract verbs with TreeTagger
# N.B. treetagger segfaults with the single big file, run it over each article instead
#cat all-extracted.txt | treetagger/cmd/tree-tagger-italian | grep VER | sort -u > verbi.txt
find extracted -type f -exec bash -c "cat '{}' | treetagger/cmd/tree-tagger-italian | grep VER >> verbi.txt" \;
sort -u verbi.txt > unique-sorted-verbs.txt
# Extract vocabulary
python scripts/bag_of_words.py all-extracted.txt
# POS tagging + chunker with TextPro
perl textpro.pl -verbose -html -l ita -c token+sentence+pos+chunk -o . ~/srl/training/itwiki/gold
