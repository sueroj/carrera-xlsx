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
        self.parse_race_info()
        self.parse_horses()

    def parse_horses(self):
        
        # Split up horses in this race and parse each
        text_list = self.raw_data.split('Owner: ')
        horses_list = text_list[1::]
        for horse_info in horses_list:
            horse = Horse()
            owner = Owner()
            trainer = Trainer()
            jockey = Jockey()

            # Parse horse owner
            lines = horse_info.split(':')
            for line in lines:
                if 'Silks' in line:
                    horse.owner = re.sub(r'\s[\d|N][/\\\n\w]+Silks', '', line)
                    owner.name = horse.owner
            if not owner.name or 'Silks' in owner.name: # TODO: Move this to one centralized location for validation
                print('[EquibaseTextParser:WARN] Fail to parse owner: {owner.name}')
            
            # Split horse info into lines and continue parsing
            lines = horse_info.split('\n')
            for index, line in enumerate(lines):
                
                if 'Trainer:' in line:

                    # Parse horse trainer
                    match = re.search(r'Trainer:.+\(', line)
                    if match:
                        horse.trainer = match.group(0).replace('Trainer: ', '').replace(' (', '')
                        trainer.name = horse.trainer

                        # Parse horse record
                        match = re.search(r'\(.+\)', line)
                        if match:
                            trainer_record = match.group(0).strip('() ')
                            trainer.record.new(trainer_record)

                        # Parse jockey
                        match = re.search(r'%\s+.+', line)
                        if match:
                            jockey.name = match.group(0).replace('% ', '')
                            jockey_record = re.search(r'\(.+\)', lines[index+1]).group(0).strip('() ')
                            jockey.record.new(jockey_record)
            
                if 'Life:' in line:
                    split_line = line.split('$')

                    # Parse horse life earnings
                    line = split_line[1]
                    horse.earnings = re.search(r'^[\d,]+', line).group(0).replace(',', '')

                    # Parse horse record
                    line = split_line[0]
                    matches = re.findall(r'\d+', line)
                    if len(matches) == 5:
                        horse.speed_rating = matches[4]
                        horse.record.new_from_list(matches[0:4])
                    elif len(matches) == 4:
                        horse.record.new_from_list(matches)
                    else:
                        print(f'[EquibaseTextParser:WARN] Fail to parse horse record for horse: {horse.name}')
                    
                    # Update horse new runner status
                    if horse.speed_rating == 'NA':
                        horse.new_runner = True

                if 'GP:' in line:

                    # Parse horse name, which is on line starting with 'GP:' or next line
                    line = line.split('$')[2]
                    match = re.search(r'[a-zA-Z\' ]+\s', line)
                    if match:
                        horse.name = match.group(0)[0:-1]
                    else:  # If above fails, name could be on next line, try that
                        line = lines[index+1]
                        match = re.search(r'[a-zA-Z\' ]+\s', line)
                        if match:
                            horse.name = match.group(0)[0:-1]

                    # Parse horse lasik state
                    if '(L1)' in line or '(L)' in line:
                        horse.lasik = True

                # if 'A ' in line:                # TODO: Temporary add results directly to list, need to add parsing
                #     # Parse horse results
                #     horse.results.append(line)
                
                # if 'Workout(s):' in line:       # TODO: Temporary add workouts directly to list, need to add parsing
                #     # Parse horse workouts
                #     line = line.replace('Workout(s): ', '')
                #     horse.workouts.append(line)
            
            self.horses.append(horse)
            self.owners.append(owner)
            self.trainers.append(trainer)
            self.jockeys.append(jockey)
                    

            # TODO: STOPPED HERE - Continue with parsing the horse record from file. It is pretty tricky string to parse
            # Parse horse record    
            # match = re.findall(r'^\w+:\s.+\$[\d,]+', line)
            # if match:
            #     items = match[0].split('$')

            #     year, record_string = items[0].split(':')
            #     record_string = record_string.strip().split(' ')
            #     record_string = ''.join(record_string[0:3])
            #     cls = record_string[4]
            #     record.add(label=year, string=record_string)


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
