#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Client Permissions Setup
------------------------
https://docs.gspread.org/


Step 1:
Enable permissions.  Note, I believe a service account is specific to Google
Cloud. Thus I followed the directions for end users.

Current instructions at:
https://docs.gspread.org/en/v5.7.0/oauth2.html#enable-api-access-for-a-project

Step 2:
Ensure the crendentials.json file is saved to:
    mac: ~/.config/gspread/credentials.json
    win: %APPDATA%\gspread\credentials.json
    
Step 3:
    When you load the client for the first time it will launch a browser
    to complete Oauth.
    
Examples
----------------------
from sheets_scripts import gsheet
gc = gsheet.Client()
file = gc.open('Urodynamics - Uroflow')
main = file.get_worksheet('main')


folder = gc.get_folder_by_name('Topic_Notes')


folders = gc.get_folder_list(parent_id=folder['id'])

folders = gc.get_folder_list(max_depth=2)


Models
------
Client
  - Spreadsheet
      - Worksheet
          - Cell


"""

#Standard
#---------------------------
import os
import string


#Third
#---------------------------
import gspread
from gspread.utils import ExportFormat


#Local
#---------------------------
from . import utils
fstr = utils.float_or_none_to_string
cld = utils.get_list_class_display
from .utils import get_truncated_display_string as td
from .utils import quotes

class Client():
    
    """
    Improvements
    ------------
    1. Fix expiration issue
    2. Allow loading from different location
    
    
    """
    
    def __init__(self):
        
        #Note this may fail and requires deleting authorized json file
        #
        #https://github.com/burnash/gspread/issues/932
        #
        #TODO: Make this deletion automatic. Any other way to fix this?
        #
        #   Not sure how to interpret GitHub issue.
        
        self.h = gspread.oauth()
        self.ff = FolderFunctions(self)
       
        
    def get_folder_by_name(self,name):
        """
        Parameters
        ----------
        name - string
            Name of the folder
            
        Returns
        -------
        folder : dictionary
            .parents - list
            .id - string
            .name - string
        
        """
        temp =  self.ff.get_folder_by_name(name)
        if len(temp) == 1:
            return temp[0]
        elif len(temp) == 0:
            return temp
            
        
    def get_folder_list(self,parent_id=None,max_depth=None):
        """
        
        

        Parameters
        ----------
        parent_id : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        folders : TYPE
            DESCRIPTION.

        """
        if (parent_id is None) and (max_depth is not None):
            parent_id = 'root'
        
        if parent_id is None:
            folders = self.ff.list_all_folders()
        else:
            folders = self.ff.list_sub_folders(parent_id,max_depth=max_depth)
        
        return folders
        
    def get_spreasheet_list(self):
        """
        
        Features
        --------
        - at folder
        - recursive
        - max_depth
        - info to get

        Returns
        -------
        None.

        """
        pass
        
    def open(self,file_name):
        """
        
        TODO
        
        title (str) – A title of a spreadsheet.

        folder_id (str) – (optional) If specified can be used to filter spreadsheets by parent folder ID.

        Parameters
        ----------
        file_name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        h_file = self.h.open(file_name)
        return Spreadsheet(h_file)
        
    
    def open_by_key(self,file_id):
    
        h_file = self.h.open_by_key(file_id)
        
        return Spreadsheet(h_file)
    
    def open_by_url(self,file_url):
        pass
        
    def __repr__(self):
        
        """
        'auth',
        'copy',
        'create',
        'del_spreadsheet',
        'export',
        'import_csv',
        'insert_permission',
        'list_permissions',
        'list_spreadsheet_files',
        'login',
        'open',
        'open_by_key',
        'open_by_url',
        'openall',
        'remove_permission',
        'request',
        'session',
        'set_timeout',
        'timeout']
        """
        
        pv = ['h',cld(self.h),
              'methods','------------',
              'open','opens file',
              'open_by_key','opens file by specifying ID',
              'open_by_url','open by specifying specifc URL']

        return utils.display_class(self, pv)



class Spreadsheet:
    
    """
    https://docs.gspread.org/en/latest/api/models/spreadsheet.html
    
    """
    
    def __init__(self,h):
        self.h = h
      
    @property
    def creation_time(self):
        return self.h.creationTime
    
    @property
    def id(self):
        return self.h.id
    
    @property
    def last_update_time(self):
        return self.h.lastUpdateTime
    
    @property
    def locale(self):
        return self.h.locale
    

    
    #skipping: sheet1
    
    @property
    def timezone(self):
        return self.h.timezone
    
    @property
    def title(self):
        return self.h.title
    
    @property
    def sheet_names(self):
        temp = self.h.worksheets()
        return [x.title for x in temp]
    
    @property
    def updated(self):
        return self.h.updated
    
    @property
    def url(self):
        return self.h.url
    
    
    #---------------------------------
    
    def export(self,file_path=None,root=None,format='pdf'):
        """
        
        Either saves a file OR returns bytes.
        
        Parameters
        ----------
        file_path : None
            This should be a full file path. If specifed the file is saved at
            the specified location.
        root : default None
            This is only a folder path. If specified the current name of the 
            sheet is added to the folder path.
        format :
            - 'pdf'
            - 'excel'
            - 'csv'
            - 'tsv'
            - 'open_office_sheet'
            - 'zipped_html'
            

        Returns
        -------
        bytes
        
        
        Example
        -------
        root = '/Users/jim/Desktop'
        file.export(root=file_path,format='excel')

        """
        
        #TODO: Switch on format
        
        
        if format == 'pdf':
            format = ExportFormat.PDF
            ext = 'pdf'
        elif format == 'excel':
            format = ExportFormat.EXCEL
            ext = 'xlsx'
        elif format == 'csv':
            format = ExportFormat.CSV
            ext = 'csv'
        elif format == 'open_office_sheet':
            format = ExportFormat.OPEN_OFFICE_SHEET
        elif format == 'ods':
            format = ExportFormat.TSV
            ext = 'tsv'
        elif format == 'zipped_html':
            format = ExportFormat.ZIPPED_HTML
            ext = 'zip'
        else:
            raise Exception('Unrecognized format option')
        
        
        bytes = self.h.export(format)
        
        if root is not None:
            file_name = self.title + '.' + ext
            file_path = os.path.join(root,file_name)
        
        if file_path is not None:
            with open(file_path, 'wb') as f: 
                f.write(bytes)
        else:
            return bytes

    
    def get_all_worksheets(self):
        
        temp = self.h.worksheets()        
        return [Worksheet(x,self) for x in temp]
    
    
    def get_worksheet(self,index_or_title):
        """
        
        get_worksheet(self,index)
        get_worksheet(self,title)

        Parameters
        ----------
        index : TYPE
            An index of a worksheet. Indexes start from zero.

        Returns
        -------
        None.

        """
        
        #Note, unfortunately ID is an int with overlapping values
        #ID=0 is valid
        if isinstance(index_or_title,int):
            index = index_or_title
            temp = self.h.get_worksheet(index)
        else:
            title = index_or_title
            temp = self.h.worksheet(title)
        
        return Worksheet(temp,self)

    
    def get_worksheet_by_id(self,id):
        
        temp = self.h.get_worksheet_by_id(id)
        
        return Worksheet(temp,self)    
    
    def __repr__(self):
        """
        
        'accept_ownership',
        'add_worksheet',
        'batch_update',
        'client',

        'del_worksheet',
        'duplicate_sheet',
        'export',
        'fetch_sheet_metadata',
        'list_named_ranges',
        'list_permissions',
        'list_protected_ranges',

        'named_range',
        'remove_permissions',
        'reorder_worksheets',
        'share',
        'sheet1',
        'transfer_ownership',
        'update_locale',
        'update_timezone',
        'update_title',
        'values_append',
        'values_batch_clear',
        'values_batch_get',
        'values_batch_update',
        'values_clear',
        'values_get',
        'values_update',
        'worksheet',
        'worksheets']


        """
        
        pv = ['h',cld(self.h),
              'id',self.id,
              'title',self.title,
              'sheet_names',td(str(self.sheet_names)),
              'creation_time',self.creation_time,
              'last_update_time',self.last_update_time,
              'locale',self.locale,
              'timezone',self.timezone,
              'updated',self.updated,
              'url',td(self.url),
              'methods','------------',
              'get_worksheet','get sheet by index',
              'get_worksheet_by_id','get sheet by ID',
              'get_worksheet_by_title','get sheet by name']

        return utils.display_class(self, pv)

class Worksheet:
    
    def __init__(self,h,parent):
        self.h = h
        self.parent = parent
        
    def acell(self,label,value_render_option='FORMATTED_VALUE'):
        """
        

        Parameters
        ----------
        label : TYPE
            DESCRIPTION.
        value_render_option : Tdefault FORMATTED_VALUE
            - 'FORMATTED_VALUE'
            - 'UNFORMATTED_VALUE'
            - 'FORMULA'

        Returns
        -------
        None.

        """
        
        return self.h.acell(label,value_render_option=value_render_option)

        
    def add_rows(self,n_rows):
        """
        
        Parameters
        ----------
        n_rows : int
            Number of new rows to add.

        Returns
        -------
        None.

        """
        pass
        
    def append_row(self):
        """
        
        #append_row(values, value_input_option='RAW', insert_data_option=None, 
        #           table_range=None, include_values_in_response=False)
        
        value_input_option : 
            - 'RAW'
            - 'USER_ENTERED' - as if user typed in entry
        insert_data_option :
            - 'OVERWRITE'
            - 'INSERT_ROWS'
        table_range :
            (optional) The A1 notation of a range to search for a logical table 
            of data. Values are appended after the last row of the table. 
            Examples: A1 or B2:D4
            ????? What is this?
        include_values_in_response : 
                
        
            

        Returns
        -------
        None.

        """
        pass
    

    def append_rows(self):
        """
        
        #append_rows(values, value_input_option='RAW', insert_data_option=None, 
        #           table_range=None, include_values_in_response=False)

        Returns
        -------
        None.

        """
        pass
    
    
        
    @property    
    def id(self):
        return self.h.id
    
    @property
    def index(self):
        return self.h.index
    
    @property    
    def col_count(self):
        return self.h.col_count
    
    @property
    def row_count(self):
        return self.h.row_count
    
    @property
    def frozen_col_count(self):
        return self.h.frozen_col_count
    
    @property
    def frozen_row_count(self):
        return self.h.frozen_row_count
    
    @property
    def is_sheet_hidden(self):
        return self.h.isSheetHidden
    
    @property
    def tab_color(self):
        return self.h.tab_color
    
    @property
    def title(self):
        return self.h.title
    
    @property
    def updated(self):
        return self.h.updated
    
    @property
    def url(self):
        return self.h.url
    
    
        
        
        #col_count
        #frozen_col_count
        #frozen_row_count
        #id
        #index
        #isSheetHidden
        #row_count
        #tab_color
        #title
        #updated
        #url    
        
    def add_cols(self):
        pass
    
    def add_rows(self):
        pass
    
    def append_row(self):
        #https://docs.gspread.org/en/latest/api/models/worksheet.html#gspread.worksheet.Worksheet.append_row
        pass
    
    def append_rows(self):
        #https://docs.gspread.org/en/latest/api/models/worksheet.html#gspread.worksheet.Worksheet.append_rows
        pass
    
    def get_cell(self):
        pass
    
    def get_range(self):
        #https://docs.gspread.org/en/latest/api/models/worksheet.html#gspread.worksheet.Worksheet.append_rows
        pass
        
    def get_col_values(self,col_id,render_option='FORMATTED_VALUE'):
        
        """
        Parameters
        ----------
        col_id : index_1b or string
            First column is column 1 or 'A'
        render_option :
            - 'FORMATTED_VALUE'
            - 'UNFORMATTED_VALUE'
            - 'FORMULA'
            
            
        
            
        """
        #UNFORMATTED_VALUE
        #FORMULA
        
        if isinstance(col_id,str):
            col_id = col_string_to_index(col_id)
            
        return self.h.col_values(col_id,render_option)
    
    
    def __repr__(self):
        
        """
        'acell',
        'X add_cols',
        'add_dimension_group_columns',
        'add_dimension_group_rows',
        'add_protected_range',
        'X add_rows',
        'batch_clear',
        'batch_format',
        'batch_get',
        'batch_update',
        'cell',
        'clear',
        'clear_basic_filter',
        'clear_note',
        'client',
        'col_count',
        'X col_values',
        'columns_auto_resize',
        'copy_range',
        'copy_to',
        'cut_range',
        'define_named_range',
        'delete_columns',
        'delete_dimension',
        'delete_dimension_group_columns',
        'delete_dimension_group_rows',
        'delete_named_range',
        'delete_protected_range',
        'delete_row',
        'delete_rows',
        'duplicate',
        'export',
        'find',
        'findall',
        'format',
        'freeze',
        'frozen_col_count',
        'frozen_row_count',
        'get',
        'get_all_cells',
        'get_all_records',
        'get_all_values',
        'get_note',
        'get_values',
        'hide',
        'hide_columns',
        'hide_rows',
        'id',
        'index',
        'insert_cols',
        'insert_note',
        'insert_row',
        'insert_rows',
        'isSheetHidden',
        'list_dimension_group_columns',
        'list_dimension_group_rows',
        'merge_cells',
        'range',
        'resize',
        'row_count',
        'row_values',
        'rows_auto_resize',
        'set_basic_filter',
        'show',
        'sort',
        'spreadsheet',
        'tab_color',
        'title',
        'unhide_columns',
        'unhide_rows',
        'unmerge_cells',
        'update',
        'update_acell',
        'update_cell',
        'update_cells',
        'update_index',
        'update_note',
        'update_tab_color',
        'update_title',
        'updated',
        'url']
        """
        
        #col_count
        #frozen_col_count
        #frozen_row_count
        #id
        #index
        #isSheetHidden
        #row_count
        #tab_color
        #title
        #updated
        #url
        
        pv = ['h',cld(self.h),
              'parent',cld(self.parent),
              'id',self.id,
              'index',self.index,
              'col_count',self.col_count,
              'row_count',self.row_count,
              'frozen_col_count',self.frozen_col_count,
              'frozen_row_count',self.frozen_row_count,
              'is_sheet_hidden',self.is_sheet_hidden,
              'tab_color',self.tab_color,
              'title',self.title,
              'updated',self.updated,
              'url',td(self.url),
              'methods','------------',
              'open','opens file',
              'open_by_key','opens file by specifying ID',
              'open_by_url','open by specifying specifc URL']

        return utils.display_class(self, pv)        
    
class Cell:
    
    def __init__(self):
        pass
        
class FolderFunctions:
    
    def __init__(self,client):
        self.parent = client
        self.client = client.h
        self.url = "https://www.googleapis.com/drive/v3/files"
        
        
    def filter_by_super_parent(folders,folder_id):
        
        #TODO: Old code, clean up
        
        
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
    
    def get_folder_by_name(self,name):
        
        folders = []
        
        q="mimeType='application/vnd.google-apps.folder' and name='" + name + "'"
        
        #TODO: Could make these optional ...
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

            res = self.client.request("get", self.url, params=params).json()
            folders.extend(res["files"])
            page_token = res.get("nextPageToken", None)
            
        return folders

    def list_sub_folders(self,folder_id,max_depth=None):
        
        """
        - max_depth
        - approach???
           - multi-requests - DONE
           - all folders then filter
           
           
        
        """
        
        #This approach does a query per folder
        #------------------------------------------
        depth = 1
        folders = self._list_folders(folder_id,'',depth)
        i = 0
        while i < len(folders):
            next_folder = folders[i]['id']
            depth = folders[i]['depth'] + 1
            if (max_depth is None) or (depth <= max_depth):
                #print('-------------')
                #print(depth)
                #print(max_depth)
                starting_path = folders[i]['path']
                new_folders = self._list_folders(next_folder,starting_path,depth)
                folders.extend(new_folders)
                
            i += 1
            
        return folders
    
    def _list_folders(self,folder_id,starting_path,depth):
        """
        
        Helper function for list_sub_folders
        
        

        Parameters
        ----------
        folder_id : TYPE
            DESCRIPTION.
        starting_path : TYPE
            DESCRIPTION.
        depth : TYPE
            DESCRIPTION.

        Returns
        -------
        folders : TYPE
            DESCRIPTION.

        """
                    
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
    
            res = self.client.request("get", self.url, params=params).json()
            
            temp_folders = res["files"]
            for entry in temp_folders:
                folder_path = starting_path + '/' + entry['name']
                entry['path'] = folder_path
                entry['depth'] = depth

            folders.extend(temp_folders)
            page_token = res.get("nextPageToken", None)
        
        return folders
    
    def list_all_folders(self):        
        #Documentation:
        #https://developers.google.com/drive/api/v3/reference/drives/list
        #
        #
        #Properties of the folders: (adjust below)
        #https://developers.google.com/drive/api/guides/ref-search-terms#drive_properties
        
        
        
            
        folders = []
        
        q="mimeType='application/vnd.google-apps.folder' and trashed=false"
        
        #TODO: Could make these optional ...
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

            res = self.client.request("get", self.url, params=params).json()
            folders.extend(res["files"])
            page_token = res.get("nextPageToken", None)
            
        return folders
  
#https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
def index_to_col_string(index_1b):
    """
    
    

    Parameters
    ----------
    index_1b : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
        
        
    Examples
    --------
    from sheets_scripts import gsheet
    print(gsheet.index_to_col_string(1))
    print(gsheet.index_to_col_string(27))
    print(gsheet.index_to_col_string(26+26*26+1))
    

    """
    #Call is recursive so do 0-based
    return n2a(index_1b-1)

def n2a(n,b=string.ascii_uppercase):
    d, m = divmod(n,len(b))
    return n2a(d-1,b)+b[m] if d else b[m]

def col_string_to_index(a):
    """
    Returns
    -------
    int : 1 based
    
    Example
    -------
    from sheets_scripts import gsheet
    i1 = 1413
    col_string = gsheet.index_to_col_string(i1)
    i2 = gsheet.col_string_to_index(col_string)
    print(f'i1:{i1}  i2:{i2}  c:"{col_string}"')
    
    
    """
    value = 0 
    a2 = a[::-1]
    for i,c in enumerate(a2):
        value += (ord(c)-64)*(26**(i))
    return value
    #for i,
    




