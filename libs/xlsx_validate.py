



class XlsxValidate:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.cross_reference_data()

    def cross_reference_data(self):
        self.check_property_by_name(data_key='horses', prop='owner')
        self.check_property_by_name(data_key='horses', prop='trainer')
        self.check_property_by_name(data_key='tracks', prop='region')

        self.check_results(data_key='horses', prop='track')
        self.check_results(data_key='horses', prop='jockey')
        # self.check_results(data_key='horses', prop='form_note')

        # self.check_notes()

    def check_property_by_name(self, data_key: str, prop: str):
        # Create list of property to check
        properties = []
        for obj in self.data[data_key]:
            value = getattr(obj, prop, None)
            if value:
                properties.append(value)

        # Check against loaded properties (read from /data .xlsx)
        try:
            loaded_props = []
            for obj in self.data[f'{prop}s']:
                loaded_props.append(obj.name)
        except Exception as err:
            raise LookupError(f'[XlsxValidate:ERROR] No data named {prop}s was loaded from .xlsx, ensure data .xlsx exists with at least one entry')

        for string in properties:
            if string not in loaded_props:
                print(f'[XlsxValidate:WARNING] {prop} "{string}" not found in /data .xlsx')

    def check_results(self, data_key: str, prop: str):
        # Create list of result values to check
        properties = []
        for obj in self.data[data_key]: 
            for attr in ['results', 'scratches', 'workouts']:
                item_list = getattr(obj, attr)
                for item in item_list:
                    value = getattr(item, prop)
                    if value not in properties:
                        properties.append(value)

        # Check against loaded properties (read from /data .xlsx)
        try:
            loaded_props = []
            for obj in self.data[f'{prop}s']:
                loaded_props.append(obj.name)
        except Exception as err:
            raise LookupError(f'[XlsxValidate:ERROR] No data named {prop}s was loaded from .xlsx, ensure data .xlsx exists with at least one entry')

        for string in properties:
            if string not in loaded_props:
                print(f'[XlsxValidate:WARNING] {prop} "{string}" not found in {prop}s.xlsx')

    def check_notes(self):
        """Check and validate notes which are basically weighted enums (i.e. algorithm params) for the app"""
        
        # Check all notes in data objects
        for key, items in self.data:
            for item in items:
                _dict = item.__dict__()
                for key in _dict.keys():
                    if '_note' in key:
                        pass


        # Check all notes in data objects multiline strings


