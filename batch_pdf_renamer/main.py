# -*- coding: utf-8 -*-
"""
Created on ??

@author: monteiro
"""
# imports
import logging
import argparse
from batch_pdf_renamer import *

# parsing
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='puts the program in verbose mode',
                    action="store_true", default=False)
parser.add_argument('--dry-run', help='makes no actual changes, just print    \
                                      them to stdout',
                    action="store_true", default=False)
parser.add_argument('--input', help='input file or folder to work on',
                    action="store", default='', required=True)
args = parser.parse_args()

# logging
if args.verbose is True:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %H:%M:%S')

# sample log                        
logging.info('File %s already exists. Skipping.', 'string')

# scan for pdfs
all_pdf_paths = scan_pdf_files_in_folder(args.input)
# extract metadata
for each_pdf in all_pdf_paths:
    # get metadata
    try:
        get_metadata(each_pdf)
        metadata = get_metadata(each_pdf)
        if metadata[0] is None or metadata[1] is None:
            pass
        elif metadata[0] == '' or metadata[1] == '':
            pass
        else:
            # do the renaming
            new_filename = work_on_title(metadata[0]) + '_-_' + \
                           work_on_author(metadata[1]) + '.pdf'
            print(each_pdf, '---TO---', new_filename, '\n\n')
    except:
        pass