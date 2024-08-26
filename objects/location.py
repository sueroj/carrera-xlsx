



class Location:
    def __init__(self):
        self.name: str = ''
        self.abbreviation: str = ''
        self.region: str = ''
        self.types: str = ''
        self.record_speed: str = ''
        self.notes: str = ''

    def unpack(self, props: tuple, data: tuple):
        print(f'[Location:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        zipped_data = zip(props, data)
        for prop, value in zipped_data:
            setattr(self, prop, value)
        return self
    
    def unpack_from_yaml(self, yaml_dict: dict):
        for key, val in yaml_dict.items():
            setattr(self, key, val)
        return self

    def load_props(self, props: tuple):
        for prop in props:
            setattr(self, prop, '')

    def load_data(self, data: tuple):
        print(f'[Profile] load data: {data}')
    
class Track(Location):
    def __init__(self):
        super().__init__()
        self.record_holder: str = ''
        self.record_weight: str = ''
