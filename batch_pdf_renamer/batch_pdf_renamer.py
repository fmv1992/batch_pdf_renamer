# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:38:10 2015

@author: monteiro
"""
import os
from PyPDF2 import PdfFileReader
import re
import isbnlib

def scan_pdf_files_in_folder(x):
    """Scan for pdf files."""
    # if is file
    if os.path.isfile(x):
        return [x]
    # if is folder
    elif os.path.isdir(x):
        list_of_pdfs = []
        for (rootpath, subdir, filenames) in os.walk(x):
            for file in filenames:            
                if '.pdf' in file:
                    list_of_pdfs.append(rootpath + '/' + file)
        return list_of_pdfs
    else:
        raise Exception(str(x, 'is neither a file nor folder.'))

def get_metadata_from_file(x):
    """Get metadata for file x.
    Returns a tuple (author, title)"""
    pdf_file = open(x, 'rb')
    pdfobj = PdfFileReader(pdf_file)
    dictinfo = pdfobj.getDocumentInfo()
    #print(dictinfo)
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
    
def work_on_author(x):
    """Manipulates the author string."""
    # allow only a small subset of common characters
    x = re.sub('[^a-zA-Z0-9_\-]', '_', x)
    # clears the double _ _
    x = re.sub('__', '_', x)
    # removes the _ at the end of string
    x = re.sub('_\Z', '', x)
    return(x.lower())

def work_on_title(x):
    """Manipulates the title string."""
    # allow only a small subset of common characters
    x = re.sub('[^a-zA-Z0-9_\-]', '_', x)
    # clears the double _ _
    x = re.sub('__', '_', x)
    # removes the _ at the end of string
    x = re.sub('_\Z', '', x)
    return(x.lower())

def process_raw_isbn(x):
    """Check if it is a ISBN"""
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
        isbn_general = re.compile('[Ii][Ss][Bb][Nn].{13,100}', re.DOTALL)
        isbn10 = re.compile('')
        isbn13 = re.compile('')
        for i in range(10):
            pageobj = pdfobj.getPage(i)
            general_match = re.search(isbn_general, pageobj.extractText())
            if general_match:
                only_numbers = re.sub('[^0-9]', '', general_match.group(0))
                valid_isbn = process_raw_isbn(only_numbers)
                if valid_isbn:
                    return valid_isbn
    except:
        pass
    return None
                
def get_metadata_from_valid_isbn(isbn):
    """ """
    try:
        metadata = isbnlib.meta(isbn, 'merge')
        authors_string = ''
        for author in metadata(['Authors']):
            authors_string += authors_string + ' '
        return (authors_string[:-1], metadata['Title'])
    except:
        return None
            
    return None