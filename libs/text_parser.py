import re
from objects.profile import Horse, Owner, Trainer, Jockey
from objects.record import Record
from libs.constants import TEXT_PARSER_FILENAME


class TextParser:
    def __init__(self, raw_data: str) -> None:
        self.raw_data = ''.join([line for line in raw_data])
        self.raw_data_lines = [line.strip('\n') for line in raw_data]

class EquibaseTextParser(TextParser):
    def __init__(self, raw_data: str) -> None:
        super().__init__(raw_data)
        self.track: str = ''
        self.date: str = ''
        self.race_number: str = ''
        self.race_name: str = f''
        self.race_rating: str = ''
        self.race_purse: str = ''
        self.track_record: str = ''
        self.track_record_holder: str = ''
        self.track_record_weight: str = ''
        
        self.horses: list[Horse] = []
        self.owners: list[Owner] = []
        self.trainers: list[Trainer] = []
        self.jockeys: list[Jockey] = []
        self.parse()

    def parse(self):
        # self.raw_data = ''.join([line for line in self.raw_data])
        # self.raw_data = [line.strip('\n') for line in self.raw_data]
        self.parse_race_info()
        self.parse_horses()
        return self

    def parse_horses(self):
        
        # TODO: STOPPED HERE> USe python regex tool for this
        # Split up horses in this race
        match = re.findall(r'.+Owner:.+Trainer\s\(', self.raw_data, flags=re.DOTALL)
        if match:
            pass

        # horse = None

        # for index, line in enumerate(self.raw_data):
        #     if 'Owner: ' in line:
        #         horse = Horse()
        #         owner = Owner()
        #         trainer = Trainer()
        #         jockey = Jockey()
        #         record = Record()
            
        #     if horse:
        #         # Parse horse owner
        #         match = re.search(r'Owner:.+\s', line)
        #         if match:
        #             horse.owner = match.group(0).replace('Owner: ', '').strip()
        #             owner.name = horse.owner
                
        #         # Parse horse trainer
        #         match = re.search(r'Trainer:.+\(', line)
        #         if match:
        #             horse.trainer = match.group(0).replace('Trainer: ', '').replace(' (', '')
        #             trainer.name = horse.trainer

        #             match = re.search(r'\(.+\)', line)
        #             if match:
        #                 trainer.record = match.group(0).replace('(', '').replace(')', '').strip()

        #             match = re.search(r'%\s+.+', line)
        #             if match:
        #                 jockey.name = match.group(0).replace('% ', '')
        #                 jockey_record = re.search(r'\(.+\)', self.raw_data[index+1])
        #                 if jockey_record:
        #                     jockey.record = jockey_record.group(0).replace('(', '').replace(')', '').strip()

        #         # Parse horse name


        #         # TODO: STOPPED HERE - Continue with parsing the horse record from file. It is pretty tricky string to parse
        #         # Parse horse record    
        #         match = re.findall(r'^\w+:\s.+\$[\d,]+', line)
        #         if match:
        #             items = match[0].split('$')

        #             year, record_string = items[0].split(':')
        #             record_string = record_string.strip().split(' ')
        #             record_string = ''.join(record_string[0:3])
        #             cls = record_string[4]
        #             record.add(label=year, string=record_string)


                            
        #         # Parse horse results
                            
        #         # Parse horse workouts

        #         # Match last line of information for a horse
        #         # This indicates to save this horse and prepare for next
        #         match = re.search(r'Trainer.+\(Last', line)
        #         if match:
        #             self.horses.append(horse)
        #             horse = None


    def parse_race_info(self):
        header = self.raw_data_lines[0:14]
        self.track = header.pop(0)

        for index, line in enumerate(header):
            
            # Parse race date
            match = re.search(r'\d.+APPROX', line)
            if match:
                self.date = match.group(0).replace(' APPROX', '')

            # Parse race number
            match = re.search(r'\d\s(equi)', line)
            if match:
                self.race_number = match.group(0).replace(' equi', '')
                self.race_name = f'Race {self.race_number}'

            # Parse race rating
            match = re.search(r'Race Rating', line)
            if match:
                self.race_rating = header[index+1]

            # Parse race purse
            match = re.search(r'Purse.+\(', line)
            if match:
                self.race_purse = match.group(0).replace('Purse $', '').replace('. (', '')

            # Parse track record information
            match = re.search(r'Track Record:', line)
            if match:
                # Parse track record holder
                match = re.search(r'Record:.+?\(', line)
                if match:
                    self.track_record_holder = match.group(0).replace('Record: ', '').replace('(', '')

                # Parse track record holder weight
                match = re.search(r',\d+\slbs', line)
                if match:
                    self.track_record_weight = match.group(0).replace(',', '').replace(' lbs', '')
                
                # Parse track record (as fastest time)
                match = re.search(r';\s.+\s', line)
                if match:
                    self.track_record = match.group(0).replace('; ', '').strip()
        print(f'[EquibaseTextParser:INFO] import {self.track} {self.race_name} from {TEXT_PARSER_FILENAME}')


