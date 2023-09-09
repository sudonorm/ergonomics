import json
import os
import sys
import warnings
warnings.filterwarnings("ignore")
import datetime
import time
from typing import List, Union, Dict, Any

import dropbox
from io import StringIO, BytesIO
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS", None)

class DBXUpDown:
    """This class contains functions which can be used to download and upload a JSON file to a Dropbox account
    """
    
    def __init__(self):

        self.dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        if DROPBOX_ACCESS_TOKEN is None:
            sys.exit("ERROR: Looks like you didn't add your access token. Add your Dropbox token to the instance of your class and try again.")

    def dataframe_to_bytes(self, df:pd.DataFrame, encoding:str = 'utf-8') -> bytes:
        data = df.to_json()
        data = bytes(data, encoding=encoding)
        return data

    def dictionary_to_bytes(self, data_dict:Dict, encoding:str = 'utf-8') -> bytes:
        data_dict = str(data_dict)
        data = bytes(data_dict, encoding=encoding)
        return data
    
    def default(self, o: Any) -> datetime.datetime.isoformat:
        '''
        Convert datetime and date objects into isoformat so they can be serialized.
        '''
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    def add_to_dropbox_using_stream(self, data: Dict, filename_with_extension: str) -> None:
        """Add a JSON file to Dropbox
        """
        
        pa_th = '/{}'.format(filename_with_extension)
        while '//' in pa_th:
            pa_th = pa_th.replace('//', '/')
        
        try:
            with StringIO() as stream:
                json.dump(data, stream, indent=4, default=self.default)

                stream.seek(0)
            
                self.dbx.files_upload(
                    f=stream.read().encode(),
                    path=pa_th,
                    mode=dropbox.files.WriteMode.overwrite
                )
                
        except Exception as e:
            sys.exit(f'{"ERROR: the following exception occured: "}{e}')
    
    def add_to_dropbox(self, data: bytes, filename_with_extension: str) -> None:
        """Add a bytes file to Dropbox
        """
        
        pa_th = '/{}'.format(filename_with_extension)
        while '//' in pa_th:
            pa_th = pa_th.replace('//', '/')
        
        print(pa_th)
        try:
            self.dbx.files_upload(
                f=data,
                path=pa_th,
                mode=dropbox.files.WriteMode.overwrite
                )
                
        except Exception as e:
            sys.exit(f'{"ERROR: the following exception occured: "}{e}')

    def get_from_dropbox(self, filename_with_extension: str) -> Dict:
        """Download a file from Dropbox.
        Return the bytes of the file, or None if it doesn't exist.
        """
        
        # dbx = dropbox.Dropbox(self.token)
        pa_th = '/{}'.format(filename_with_extension)
        while '//' in pa_th:
            pa_th = pa_th.replace('//', '/')
        
        try:
            md, res = self.dbx.files_download(pa_th)
        except:
            return None
        data = res.content
        return data

    def download_from_dropbox(self, path_to_files:str = '', encoding:str = 'utf-8') -> List:

        """This function can be used to download all the json files in a dropbox folder

        Returns:
            List: list of dictionaries
        """
        files = self.dbx.files_list_folder(path_to_files, recursive=False)
        output_files_list = []
        # dbx.files_list_folder_continue(files.cursor)
        for file in files.entries:
            from ast import literal_eval
            if isinstance(file, dropbox.files.FileMetadata):
                output_data = literal_eval(self.get_from_dropbox(file.path_display).decode(encoding))
                output_files_list.append(output_data)
        
        return output_files_list

    def get_or_create_file(self, dataTemplate:Dict, filename_with_extension:str) -> Union[Dict, bool]:
        """This function will try to get a JSON file from Dropbox and 
        if it does not exist, it will add this to Dropbox
        """
        
        newDump = False
        dataTemplate = self.data_template()
        bytes_data = self.get_from_dropbox(filename_with_extension)

        if bytes_data == None:
            self.add_to_dropbox_using_stream(dataTemplate, filename_with_extension)
            newDump = True
            return dataTemplate, newDump
        
        else:
            with BytesIO(bytes_data) as stream:
                data = json.load(stream)
            return data, newDump