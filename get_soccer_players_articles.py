#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys


DEBUG = True

#Returns a list of Wiki IDs read from input file path "filein" 
def load_wiki_ids(filein):
    with open(filein) as i:
        return [l.strip() for l in i.readlines()]

#Prints article present in path "corpus_dir" if its ID is present in "soccer_ids" list
def extract_soccer_articles(soccer_ids, corpus_dir, output_dir):
    #For loop walks through all the subdirectories and file in root directory-"corpus_dir" 
    for path, subdirs, files in os.walk(corpus_dir):
        for name in files:
            f = os.path.join(path, name)
            with open(f) as i:
                 #Read the contents in file to "content" 
                 content = ''.join(i.readlines())
            #Extract the "current_id" from text line having format for eg. id="336" 
            match = re.search('id="([^"]+)"', content)
            current_id = match.group(1)
            if DEBUG:
                print "File = [%s] - Wiki ID = [%s]" % (f, current_id)
            if current_id in soccer_ids:
                #copy the file to "output_dir"
                shutil.copy(f, output_dir)
                if DEBUG:
                    print "MATCHED! [%s]" % content
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: %s <SOCCER_IDS> <CORPUS_DIR> <OUTPUT_DIR>" % __file__
        sys.exit(1)
    else:
        ids = load_wiki_ids(sys.argv[1])
        extract_soccer_articles(ids, sys.argv[2], sys.argv[3])
