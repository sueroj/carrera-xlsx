



class Location:
    def __init__(self):
        pass
        # print(f'[Location:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        # zipped_data = zip(props, data)
        # for prop, value in zipped_data:
        #     setattr(self, prop, value)

        # self._unpack_multiline_string()

        # self.load_props(props)
        # self.load_data(data)

    # def _unpack_multiline_string(self):
    #     for key in ['results', 'scratches', 'workouts']:
    #         raw_string = getattr(self, key)
    #         lines = raw_string.split(';')
            
    #         data = []
    #         for line in lines:
    #             if line:
    #                 data.append(MultilineString(line.strip()))
    #         setattr(self, key, data)
    
    def unpack_from_xlsx(self, props: tuple, data: tuple):
        print(f'[Location:INFO] Incoming data props length: {len(props)}, data length: {len(data)}')
        zipped_data = zip(props, data)
        for prop, value in zipped_data:
            setattr(self, prop, value)
        return self


    def load_props(self, props: tuple):
        for prop in props:
            setattr(self, prop, '')

    def load_data(self, data: tuple):
        print(f'[Profile] load data: {data}')
    
class Track(Location):
    def __init__(self, props: tuple, data: tuple):
        super().__init__(props, data)