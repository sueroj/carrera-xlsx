import os
import openpyxl

from config import __version__
from objects.profile import Profile, Horse
from objects.location import Location, Track
from libs.xlsx_writer import XlsxWriter


# Reference: Prints all data in xlsx as dict, row by row (There is another prop for column by column)
    # for value in worksheet.values:
    #     print(value) 

class XlsxReader:
    def __init__(self) -> None:
        self.data: dict = {}

    def import_data(self): 
        self._import(key_name='horses', path='profiles/horses', loader=Horse)
        self._import(key_name='owners', path='profiles/owners', loader=Profile)
        self._import(key_name='trainers', path='profiles/trainers', loader=Profile)
        self._import(key_name='jockeys', path='profiles/jockeys', loader=Profile)

        self._import(key_name='tracks', path='locations/tracks', loader=Track)
        self._import(key_name='regions', path='locations/regions', loader=Location)

        # TODO: STOPPED HERE. Continue notes format. Use .xlsx or other like enums?
        #  continue with imports and validate


    # TODO: Could use some refactoring
    # TODO: XlsxLogger module could simplify logging actions for the LOGS page
    def _import(self, key_name: str, path: str, loader: any):
        print(f'[XlsxReader:INFO] import {path} start')

        if not os.path.exists(f'data/{path}.xlsx'):
            print(f'[XlsxReader:ERROR] data/{path}.xlsx not found. Data cannot be imported')
            return

        xlsx = openpyxl.open(filename=f'data/{path}.xlsx')
        worksheet = xlsx['Sheet1']
        all_rows= [row for row in worksheet.values]

        if all_rows:
            header_row = all_rows[0]
            entries = all_rows[1::]

            # TODO: Debug for xlsx object printout
            # print(header_row)
            # print(entries)

            objects = [loader(props=header_row, data=entry) for entry in entries]
            self.data.update({key_name: objects})
            print(f'[XlsxReader:INFO] import {path} OK with {len(entries)} entries')
        else:
            print(f'[XlsxReader:WARNING] No data in data/{path}.xlsx')


    def update_data(self):
        self.update_locations()
        # update_owners()

    # def update_owners(self):
    #     # TODO: Before any updates, check if prop file exists, if yes, open to import
    #     if os.path.exists('data/profiles/owners.xlsx'):
    #         xlsx = openpyxl.open(filename='data/profiles/owners.xlsx')
    #     else:
        
    def update_locations(self):
        # Get list of known tracks by their abbreviation
        tracks = [track.abbreviation for track in self.data['tracks']]

        result_tracks = []
        for obj in self.data['horses']:
            for result in obj.results:
                if result.track not in result_tracks:
                    result_tracks.append(result.track)

        for location in result_tracks:
            if location not in tracks:
                track = Profile()
                setattr(track, 'abbreviation', location)
                self.data['tracks'].append(track)

        xlsx_writer = XlsxWriter(version=__version__)
        xlsx_writer.update_data()
      

