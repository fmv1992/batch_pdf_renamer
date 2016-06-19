# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:38:10 2015

@author: Felipe M. Vieira <fmv1992@gmail.com>

Description:
helper functions to main program
"""
import os
import re
try:
    from unidecode import unidecode
except ImportError:
    unidecode = lambda x: re.sub('[^a-zA-Z0-9_\-]', '', x)
import logging
from PyPDF2 import PdfFileReader
import isbnlib



def scan_pdf_files_in_folder(x):
    """Scan for pdf files."""
    if os.path.isfile(x):
        return [x]
    elif os.path.isdir(x):
        list_of_pdfs = []
        for (rootpath, subdir, filenames) in os.walk(x):
            for file in filenames:
                if file.endswith('.pdf'):
                    list_of_pdfs.append(os.path.join(rootpath, file))
        return list_of_pdfs
    else:
        raise Exception(x, 'is neither a file nor folder.')


def get_metadata_from_file(x):
    """Get metadata for file x.
    Returns a tuple (author, title)"""
    pdf_file = open(x, 'rb')
    pdfobj = PdfFileReader(pdf_file)
    dictinfo = pdfobj.getDocumentInfo()
    try:
        author = dictinfo['/Author']
    except:
        author = None
    try:
        title = dictinfo['/Title']
    except:
        title = None
    pdf_file.close()
    return (author, title)

def clear_string(x):
    """Manipulates the author string."""
    # allow only a small subset of common characters
    x = unidecode(x).lower()
    # clears the double _ _
    x = re.sub('[^a-z0-9_]+', '_', x)
    # removes the _ at the end of string
    x = re.sub('_\Z', '', x)
    return(x.lower())

def check_valid_isbn(x):
    """Check if it is a ISBN. Returns the isbn if it is valid. None otherwise.
    """
    for i in range(len(x)):
        if isbnlib.is_isbn10(x[i:i+10]):
            return x[i:i+10]
        elif isbnlib.is_isbn13(x[i:i+13]):
            return x[i:i+13]
    return None


def get_isbn_from_file(x):
    """Gets the isbn from file."""
    pdf_file = open(x, 'rb')
    try:
        pdfobj = PdfFileReader(pdf_file)
        # loose expectation of what a isbn specification might be
        isbn_general = re.compile('(isbn|standard.{0,10}book).{10,150}',
                                    flags=re.IGNORECASE|re.DOTALL)
        for i in range(10):
            pageobj = pdfobj.getPage(i)
            general_match = isbn_general.search(pageobj.extractText().lower())
            if general_match:
                only_numbers = re.sub('[^0-9]', '', general_match.group(0))
                valid_isbn = check_valid_isbn(only_numbers)
                if valid_isbn:
                    return valid_isbn
    except:
        pass
    return None

def get_metadata_from_valid_isbn(isbn):
    """ """
    metadata = None
    servers = ('wcat', 'goob', 'openl', 'merge')
    for server in servers:
        try:
            metadata = isbnlib.meta(isbn, server)
            if metadata is not None:
                break
        except:
            pass
    else:
        return None
    authors_string = ''
    for author in metadata['Authors']:
        authors_string += author + ' '
    return (authors_string[:-1], metadata['Title'])


def do_rename(src, dst, safelogfile=None, dry_run=False):
    """Do the rename and add the name to the logfile."""
    unix_command = 'mv \'' + \
                   os.path.dirname(src) + '/' + dst + '\' \'' + \
                   src + '\'\n'
    full_source_name = src
    full_dest_name = os.path.dirname(src) + '/' + dst
    if full_source_name != full_dest_name:
        if dry_run is False:
            os.rename(full_source_name, full_dest_name)
            if safelogfile:
                safelogfile.write(unix_command)
        logging.info('%s -> %s', os.path.basename(full_source_name),
                     os.path.basename(full_dest_name))
    return None
