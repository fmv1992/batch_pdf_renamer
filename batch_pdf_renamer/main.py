# -*- coding: utf-8 -*-
"""
Created on ??

@author: monteiro
"""
# imports
import logging
import argparse
from batch_pdf_renamer import *  # the module uses all functions
from datetime import datetime as dt

# parsing
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='puts the program in verbose mode',
                    action="store_true", default=False)
parser.add_argument('--dry-run', help='makes no actual changes, just print    \
                                      them to stdout',
                    action="store_true", default=False)
parser.add_argument('--input', help='input file or folder to work on',
                    action="store", default='', required=True)
parser.add_argument('--restore-file', help='log file for easy undo',
                    action="store",
                    default=str(os.path.dirname(os.path.dirname(
                                os.path.abspath(__file__))) +
                                '/' + 'restorelog.txt'),
                    required=False)
args = parser.parse_args()

# logging
if args.verbose is True:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %H:%M:%S')
# safety file for undoing                        
if not os.path.isfile(args.restore_file):
    raise Exception(str(args.restore_file + ' does not exist yet.'))
else:
    safe_log_file = open(str(os.path.dirname(os.path.dirname(
                                os.path.abspath(__file__))) +
                                '/' + 'restorelog.txt'), 'at')
    safe_log_file.write(str(dt.now()) + '\n')
# sample log                        
logging.info('File %s already exists. Skipping.', 'string')


def do_rename(src, dst):
    """Do the rename and add the name to the logfile."""
    unix_command = 'mv \'' + \
                   os.path.dirname(src) + '/' + dst + '\' \'' + \
                   src + '\'\n' 
    safe_log_file.write(unix_command)
    full_source_name = src
    full_dest_name = os.path.dirname(src) + '/' + dst
    if full_source_name != full_dest_name:
        os.rename(full_source_name, full_dest_name)
    return None

# scan for pdfs
all_pdf_paths = scan_pdf_files_in_folder(args.input)
# extract metadata
all_changes = 5 * '\n'
for each_pdf in all_pdf_paths:
    # get metadata from isbn
    valid_isbn = get_isbn_from_file(each_pdf)
    if valid_isbn:
        metadata = get_metadata_from_valid_isbn(valid_isbn)
        if metadata:
            new_filename = work_on_title(metadata[0]) + '_-_' + \
                               work_on_author(metadata[1]) + '.pdf'
            print(str(os.path.basename((each_pdf)) + ' -> ' + new_filename + '\n'))
            do_rename(each_pdf, new_filename)
            continue
    else:
        #print('could not get a valid isbn for', each_pdf)
        pass
    # get metadata from file
    try:
        metadata = get_metadata_from_file(each_pdf)
        if metadata[0] is None or metadata[1] is None:
            pass
        elif metadata[0] == '' or metadata[1] == '':
            pass
        else:
            # do the renaming
            new_filename = work_on_title(metadata[0]) + '_-_' + \
                           work_on_author(metadata[1]) + '.pdf'
            print(str(os.path.basename((each_pdf)) + ' -> ' + new_filename + '\n'))
            do_rename(each_pdf, new_filename)
    except:
        pass
safe_log_file.close()