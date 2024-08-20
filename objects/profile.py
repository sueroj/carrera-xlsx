from objects.multiline_string import MultilineString
from libs.constants import MULTILINE_STRING_KEYS



class Profile:
    def __init__(self):
        self.name: str = ''
        self.age: str = ''
        self.record: str = ''

    def unpack(self, props: tuple, data: tuple):
        print(f'[Profile:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        zipped_data = zip(props, data)
        for prop, value in zipped_data:
            setattr(self, prop, value)
        
        for key in MULTILINE_STRING_KEYS:
            if key in props:
                self._unpack_multiline_string(key)
        return self

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
        self.breeder: str = ''
        self.earnings: str = ''
        self.results: list[MultilineString] = []
        self.scratches: list[MultilineString] = []
        self.workouts: list[MultilineString] = []

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
