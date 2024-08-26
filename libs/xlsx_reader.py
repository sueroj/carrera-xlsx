import os
import yaml
import openpyxl

from config import __version__
from objects.profile import Profile, Horse, Owner, Trainer, Jockey
from objects.location import Location, Track
from libs.xlsx_writer import XlsxWriter
from libs.text_parser import EquibaseTextParser
from libs.constants import TEXT_PARSER_FILENAME


# Reference: Prints all data in xlsx as dict, row by row (There is another prop for column by column)
    # for value in worksheet.values:
    #     print(value)
class XlsxReader:
    def __init__(self) -> None:
        self.data: dict = {}

    def import_data(self): 
        self._import_from_xlsx(key_name='horses', path='profiles/horses', loader=Horse)
        self._import_from_xlsx(key_name='owners', path='profiles/owners', loader=Owner)
        self._import_from_xlsx(key_name='trainers', path='profiles/trainers', loader=Trainer)
        self._import_from_xlsx(key_name='jockeys', path='profiles/jockeys', loader=Jockey)

        self._import_from_xlsx(key_name='tracks', path='locations/tracks', loader=Track)
        self._import_from_xlsx(key_name='regions', path='locations/regions', loader=Location)

        self._import_from_text_file()

        # TODO: STOPPED HERE. Continue notes format. Use .xlsx or other like enums?
        #  continue with imports and validate

    # TODO: NEED to validate types here, make sure types are right to prevent errors
    # TODO: Could use some refactoring
    # TODO: XlsxLogger module could simplify logging actions for the LOGS page

    def _import_from_xlsx(self, key_name: str, path: str, loader: object):
        print(f'[XlsxReader:INFO] import from xlsx {path} start')

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

            objects = [loader().unpack(props=header_row, data=entry) for entry in entries]
            self.data.update({key_name: objects})
            print(f'[XlsxReader:INFO] import {path} OK with {len(entries)} entries')


    def _import_from_yaml(self, key_name: str, path: str, loader: object):
        print(f'[XlsxReader:INFO] import from yaml {path} start')

        if not os.path.exists(f'data/{path}.yaml'):
            print(f'[XlsxReader:ERROR] data/{path}.yaml not found. Data cannot be imported')
            return

        # Import yaml file data and convert from dict to list
        yaml_file = open(f'data/{path}.yaml', 'r')
        data = yaml.load(stream=yaml_file, Loader=yaml.Loader)
        data = [loader().unpack_from_yaml(val) for val in data.values()]

        if data:
            self.data.update({key_name: data})
            print(f'[XlsxReader:INFO] import {path} OK with {len(data)} entries')
        else:
            print(f'[XlsxReader:WARNING] No data in data/{path}.yaml')

    def _import_from_text_file(self):
        print(f'[XlsxReader:INFO] checking {TEXT_PARSER_FILENAME} file')

        with open(TEXT_PARSER_FILENAME, 'r') as data_file:
            raw_data = data_file.readlines()
        
        if not len(raw_data) > 0:
            print(f'[XlsxReader:INFO] no data found in {TEXT_PARSER_FILENAME} file')
            return
        else:
            parsed_data = EquibaseTextParser(raw_data)

            # TODO: Implement a checks for updating data.
            #  i.e. once parsed, check data for existing horse, if exists, add parsed to existing record
            #  maybe just update the results only if name is matched.

            # TODO: These functions req rewrite be more abstract
            self.extend_horse_data(incoming_data=parsed_data)
            self.extend_track_data(incoming_data=parsed_data)

            print(f'[XlsxReader:INFO] parse {TEXT_PARSER_FILENAME} OK')

    def extend_horse_data(self, incoming_data: EquibaseTextParser):
        # TODO: This func req rewrite be more abstract
        existing_horses = [horse.name for horse in self.data['horses']]

        for horse in incoming_data.horses:
            if not horse.name in existing_horses:
                self.data['horses'].append(horse)
                existing_horses.append(horse.name)
                print(f'[XlsxReader:INFO] {horse.name}, data extension with new horse OK')
            else:
                print(f'[XlsxReader:INFO] Horse {horse.name} already exists -- update required')                
                # TODO: Else update record here

    def extend_track_data(self, incoming_data: EquibaseTextParser):
        existing_tracks = [track.abbreviation for track in self.data['tracks']]

        if incoming_data.track not in existing_tracks:
            new_track = Track()
            new_track.abbreviation = incoming_data.track
            new_track.record_speed = incoming_data.track_record
            new_track.record_holder = incoming_data.track_record_holder
            new_track.record_weight = incoming_data.track_record_weight
            self.data['tracks'].append(new_track)
            print(f'[XlsxReader:INFO] {new_track.abbreviation}, data extension with new track OK')


    def update_data(self):
        print(f'[XlsxReader:INFO] Check data for data update START')

        # self.update_locations()
        # update_owners()
        pass

        print(f'[XlsxReader:INFO] Check data for data update OK')

    # def update_owners(self):
    #     # TODO: Before any updates, check if prop file exists, if yes, open to import
    #     if os.path.exists('data/profiles/owners.xlsx'):
    #         xlsx = openpyxl.open(filename='data/profiles/owners.xlsx')
    #     else:
        
    def update_locations(self):
        # Get list of known tracks by their abbreviation
        tracks = [track.abbreviation for track in self.data['tracks']]

        # Check results and update new tracks
        result_tracks = []
        for obj in self.data['horses']:
            for result in obj.results:
                if result['track'] not in result_tracks:
                    result_tracks.append(result['track'])

        for _track in result_tracks:
            if _track not in tracks:
                track = Track()
                track.abbreviation = _track
                self.data['tracks'].append(track)
