#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Requires:
    - gspread
    - Scholar Tools - pubmed and crossref - TODO add links
    - pyperclip


from sheets_scripts import main
pmid = '35645033'
main.pubmed_to_entry(pmid)
main.pubmed_to_entry()

main.doi_to_entry()


from sheets_scripts import main
file = main.JimSpreadSheet('Urodynamics - Uroflow')
sheet = file.get_sheet('main')






"""

#https://stackoverflow.com/questions/68819546/how-can-you-programmatically-format-content-to-paste-into-google-spreadsheets

#Standard
#--------------------
from datetime import datetime



#Third
#---------------------
import pyperclip
import pandas as pd

from pubmed import API as PubmedAPI
pubmed_api = PubmedAPI(verbose=True)

from crossref.api import API as CrossrefAPI
crossref_api = CrossrefAPI()


#Local
#----------------------
from . import gsheet


class JimSpreadSheet:
    
    def __init__(self,name,client=None):
        
        if client is None:
            client = gsheet.Client()
        
        self.client = client
        self.file = client.open(name)
        
        
    def get_sheet(self,name):
        
        return JimWorkSheet(self.file.get_worksheet(name))  

class JimWorkSheet:
    
    def __init__(self,sheet):
        self.sheet = sheet
        
    def get_entries(self):
        pass

    
#pyperclip.copy("a\tb\tc")

def doi_to_entry(doi):
    
    d = crossref_api.doi_info(doi)
    
    cells = []
    
    #0 - 1st entry
    #0 - year component
    
    if 'published-print' in d:
        year = d['published-print']['date-parts'][0][0]
    else:
        year = d['published']['date-parts'][0][0]
    
    cells.append(str(year))
    
    #Author string
    #1 - last
    #2 - last, last
    #3 - last, last, last
    #4 - last et al. (last)
    
    n_authors = len(d.author)
    if n_authors == 1:
        author_str = d.author[0]['family']
    elif n_authors == 2:
        author_str = d.author[0]['family'] + ', ' + d.author[1]['family']
    elif n_authors == 3:
        author_str = d.author[0]['family'] + ', ' + d.author[1]['family'] + ', ' + d.authors[2]['family']
    else:
        author_str = d.author[0]['family'] + ' et al. (' + d.author[-1]['family'] + ')'
    
    cells.append(author_str)
    
    cells.append(d.title[0])
    
    cells.append(d['container-title'][0])
    
    cells.append(doi)
    
    now = datetime.now()

    current_date = now.strftime("%m/%d/%Y")
    
    cells.append(current_date)
    
    final_string = "\t".join(cells)
    
    pyperclip.copy(final_string)
    
    print(cells[0])
    print(cells[1])


def pubmed_to_entry(pmid):
    
    #- retrieve info
    #- 
    
    pmid = str(pmid)
    
    summary = pubmed_api.pubmed.summary(pmid)
    d = summary.docs[0]
    
    #cells
    #-------
    #0) year
    #1) authors
    #2) title
    #3) journal
    #4) pmid
    #5) 
    cells = []
    cells.append(str(d.sort_pub_date.year))
    
    #Author string
    #1 - last
    #2 - last, last
    #3 - last, last, last
    #4 - last et al. (last)
    
    n_authors = len(d.authors)
    if n_authors == 1:
        author_str = d.authors[0].last
    elif n_authors == 2:
        author_str = d.authors[0].last + ', ' + d.authors[1].last
    elif n_authors == 3:
        author_str = d.authors[0].last + ', ' + d.authors[1].last + ', ' + d.authors[2].last
    else:
        author_str = d.authors[0].last + ' et al. (' + d.authors[-1].last + ')'
    
    cells.append(author_str)
    
    cells.append(d.title)
    
    cells.append(d.source)
    
    cells.append(pmid)
    
    now = datetime.now()

    current_date = now.strftime("%m/%d/%Y")
    
    cells.append(current_date)
    
    final_string = "\t".join(cells)
    
    pyperclip.copy(final_string)
    
    print(cells[0])
    print(cells[1])

    
    


