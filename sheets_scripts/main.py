#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:25:00 2022

@author: jim

from sheets_scripts import main
pmid = '35645033'
main.pubmed_to_entry(pmid)



gspread


Filepath (including name) pointing to a credentials .json file. Defaults to DEFAULT_CREDENTIALS_FILENAME:
    %APPDATA%gspreadcredentials.json on Windows
    ~/.config/gspread/credentials.json everywhere else



#rm authorized_user.json

https://github.com/burnash/gspread/issues/932



"""

#https://stackoverflow.com/questions/68819546/how-can-you-programmatically-format-content-to-paste-into-google-spreadsheets

from datetime import datetime

import pyperclip

import pandas as pd

import gspread
#https://docs.gspread.org/en/latest/api/client.html

#An alternative: pygsheets


#https://developers.google.com/drive/api/v2/reference/parents/list


#https://developers.google.com/drive/api/guides/search-files

#https://stackoverflow.com/questions/46545336/search-files-recursively-using-google-drive-rest
#
#folders = service.files().list(q="mimeType='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false",fields="nextPageToken, files(id, name)",pageSize=400).execute()
#
#https://developers.google.com/drive/api/v3/reference/files



"""
in https://github.com/burnash/gspread/blob/master/gspread/client.py

DRIVE_FILES_API_V3_URL = 


res = gc.request("get",DRIVE_FILES_API_V3_URL,)

page_token = ""
while page_token is not None:
    if page_token:
        params["pageToken"] = page_token

    res = self.request("get", url, params=params).json()
    files.extend(res["files"])
    page_token = res.get("nextPageToken", None)


"""

#Improvements
#- could track folder name relative to parent
#- could limit search depth, e.g., only go down 1 folder


#TODO: They actually recommend getting all folders first and then filtering parents


def read_sheet(gc):
    pass



"""
folders = list_all_folders(gc)
childs_ids = filter_by_super_parent(folders,folder_id)

"""


def list_all_folders(gc):
    """
    
    gc = gspread.oauth()


    Parameters
    ----------
    gc : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    #Documentation:
    #https://developers.google.com/drive/api/v3/reference/drives/list
    #
    #
    #Properties of the folders: (adjust below)
    #https://developers.google.com/drive/api/guides/ref-search-terms#drive_properties
    
    
    url = "https://www.googleapis.com/drive/v3/files"
        
    folders = []
    
    q="mimeType='application/vnd.google-apps.folder' and trashed = false"
    
    params = {
        "q": q,
        "pageSize": 1000,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
        "fields": "nextPageToken,files(id,name,parents)",
    }
    
    page_token = ""
    while page_token is not None:
        if page_token:
            params["pageToken"] = page_token

        res = gc.request("get", url, params=params).json()
        folders.extend(res["files"])
        page_token = res.get("nextPageToken", None)
        
    return folders

def filter_by_super_parent(folders,folder_id):
    
    
    #TODO: Support max depth as well
    
    #Populate child_map
    #------------------
    #key: id of parent
    #value: list of ids of childen
    
    child_map = {}  
    for folder in folders:
        child_map[folder['id']] = []
    
     
    for folder in folders:
        #Currently assuming single parent
        #
        #Why is parents not present in all :/
        
        if 'parents' in folder:
            parent = folder['parents'][0]
            try:
                child_map[parent].append(folder['id'])
            except:
                child_map[parent] = []
                child_map[parent].append(folder['id'])
                
            
    child_ids = child_map[folder_id]
    next_index = 0
    while next_index < len(child_ids):
        next_folder_id = child_ids[next_index]
        next_children = child_map[next_folder_id]
        child_ids.extend(next_children)
        next_index += 1
        
    return child_ids



def list_folders_recursive(gc,folder_id):
    """
    
    TODO: Support max depth

    Parameters
    ----------
    gc : TYPE
        DESCRIPTION.
    folder_id : TYPE
        DESCRIPTION.

    Returns
    -------
    folders : TYPE
        DESCRIPTION.

    """
    
    
    
    folders = list_folders(gc,folder_id)
    i = 0
    while i < len(folders):
        next_folder = folders[i]['id']
        folders.extend(list_folders(gc,next_folder))
        i += 1
        
    return folders

def list_folders(gc,folder_id):
    
    url = "https://www.googleapis.com/drive/v3/files"
        
    folders = []
    
    q="mimeType='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false"
    
    params = {
        "q": q,
        "pageSize": 1000,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
        "fields": "nextPageToken,files(id,name)",
    }
    
    page_token = ""
    while page_token is not None:
        if page_token:
            params["pageToken"] = page_token

        res = gc.request("get", url, params=params).json()
        folders.extend(res["files"])
        page_token = res.get("nextPageToken", None)
    
    return folders





    """
    
    
    res = gc.request("get", DRIVE_FILES_API_V3_URL, params=params).json()
    
    folders = service.files().list(,
                                   fields="nextPageToken, files(id, name)",pageSize=400).execute()
    
    
    
    all_folders = gc.get('files', [])
    all_files = check_for_files(folder_id)
    n_files = len(all_files)
    n_folders = len(all_folders)
    if n_folders != 0:
        for i,folder in enumerate(all_folders):
            folder_name =  folder['name']
            new_pattern = subfolder_pattern
            new_sub_patterns[subfolder_pattern] = folder['id']
            print('New Pattern:', new_pattern)
            all_files = check_for_files(folder['id'])
            n_files =len(all_files)
            new_folder_tree = new_pattern 
            if n_files != 0:
                for file in all_files:
                    file_name = file['name']
                    new_file_tree_pattern = subfolder_pattern + "/" + file_name
                    new_sub_patterns[new_file_tree_pattern] = file['id']
                    print("Files added :", file_name)
            else:
                print('No Files Found')
    else:
        all_files = check_for_files(folder_id)
        n_files = len(all_files)
        if n_files != 0:
            for file in all_files:
                file_name = file['name']
                subfolders[folder_tree + '/'+file_name] = file['id']
                new_file_tree_pattern = subfolder_pattern + "/" + file_name
                new_sub_patterns[new_file_tree_pattern] = file['id']
                print("Files added :", file_name)
    return new_sub_patterns 
    """


"""
def check_for_files(folder_id):
    other_files = service.files().list(q="mimeType!='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false",fields="nextPageToken, files(id, name)",pageSize=400).execute()
    all_other_files = other_files.get('files', [])   
    return all_other_files

def get_folder_tree(folder_id):
    sub_folders = check_for_subfolders(folder_id)

    for i,sub_folder_id in enumerate(sub_folders.values()):
        folder_tree = list(sub_folders.keys() )[i]
        print('Current Folder Tree : ', folder_tree)
        folder_ids.update(sub_folders)
        print('****************************************Recursive Search Begins**********************************************')
        try:
            get_folder_tree(sub_folder_id)
        except:
            print('---------------------------------No furtherance----------------------------------------------')
    return folder_ids 

folder_ids = get_folder_tree(folder_id)
"""





from pubmed import API
api = API(verbose=True)

#pyperclip.copy("a\tb\tc")


def get_sheets_list():
    
    gc = gspread.oauth()
    
    temp = gc.list_spreadsheet_files()
    #
    # - id
    # - name
    # - createdTime
    # - modifiedTime
    
    df = pd.DataFrame(temp)
    
    df = df.sort_values(by='name',axis='columns')
    
    pass


def pubmed_to_entry(pmid):
    
    #- retrieve info
    #- 
    
    summary = api.pubmed.summary(pmid)
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

    
    


