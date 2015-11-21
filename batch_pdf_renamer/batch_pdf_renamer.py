# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:38:10 2015

@author: monteiro
"""
import os
from PyPDF2 import PdfFileReader
import re

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

def get_metadata(x):
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