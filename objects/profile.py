from objects.record import Record
from objects.multiline_string import MultilineString
from libs.constants import MULTILINE_STRING_KEYS



class Profile:
    def __init__(self):
        self.name: str = ''
        self.age: str = ''
        self.record: Record = Record()

    def unpack(self, props: tuple, data: tuple):
        print(f'[Profile:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        zipped_data = zip(props, data)
        for prop, value in zipped_data:
            setattr(self, prop, value)
        
        for key in MULTILINE_STRING_KEYS:
            if key in props:
                self._unpack_multiline_string(key)
        return self
    
    def unpack_from_yaml(self, yaml_dict: dict):
        for key, val in yaml_dict.items():
            setattr(self, key, val)
        
        self._covert_dict_to_list('results')
        self._covert_dict_to_list('scratches')
        self._covert_dict_to_list('workouts')
        return self

    def _covert_dict_to_list(self, prop: str):
        value = getattr(self, prop, None)
        if value:
            value = [val for val in value.values()]
            setattr(self, prop, value)

    def _unpack_multiline_string(self, key: str):
        raw_string = getattr(self, key)
        lines = raw_string.split(';')
        
        data = []
        for line in lines:
            if line:
                data.append(MultilineString(line.strip()))
        setattr(self, key, data)

    def load_props(self, props: tuple):
        for prop in props:
            setattr(self, prop, '')

    
class Horse(Profile):
    def __init__(self):
        super().__init__()
        self.owner: str = ''
        self.trainer: str = ''
        self.earnings: str = ''
        self.speed_rating: str = 'NA'
        self.results: list[MultilineString] = []
        self.scratches: list[MultilineString] = []
        self.workouts: list[MultilineString] = []
        self.lasik: bool = False
        self.new_runner: bool = False

class Owner(Profile):
    def __init__(self):
        super().__init__()

class Trainer(Profile):
    def __init__(self):
        super().__init__()

class Jockey(Profile):
    def __init__(self):
        super().__init__()

class Breeder(Profile):
    def __init__(self):
        super().__init__()
