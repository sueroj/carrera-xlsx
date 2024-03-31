from objects.multiline_string import MultilineString



class Profile:
    def __init__(self, props: tuple, data: tuple):
        print(f'[Profile:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        zipped_data = zip(props, data)
        for prop, value in zipped_data:
            setattr(self, prop, value)

    def _unpack_multiline_string(self):
        for key in ['results', 'scratches', 'workouts']:
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
    def __init__(self, props: tuple, data: tuple):
        super().__init__(props, data)
        self._unpack_multiline_string()

class Owner(Profile):
    def __init__(self, props: tuple, data: tuple):
        super().__init__(props, data)