import xlsxwriter
from libs.xlsx_format import XlsxFormat
from libs.constants import MULTILINE_STRING_KEYS

# TODO: Add auto format of row length
class XlsxWriter:
    def __init__(self, version: str) -> None:
        self.version: str = version

        # TODO: Consider refactor from methods to class level
        self.xlsx: xlsxwriter.Workbook | None = None
        self.format: XlsxFormat | None = None
        # self.xlsx = xlsxwriter.Workbook('test.xlsx')

    def write_new(self):
        self.xlsx = xlsxwriter.Workbook('test.xlsx')
        self.format: XlsxFormat = XlsxFormat(self.xlsx)
        self.generate_forecast()
        self.generate_events()
        self.generate_data_management()
        self.generate_algorithms_analysis()
        self.generate_version_analysis()
        self.generate_earnings()
        self.generate_logs()
        self.generate_configuration()

        # worksheet = xlsx.add_worksheet(name='test worksheet')

        # for number in range(20):
        #     worksheet.write(1, number, f'test data {number}')
        
        self.xlsx.close()

    def generate_forecast(self):
        worksheet = self.xlsx.add_worksheet(name='FORECAST')
        self.write_header(worksheet)

    def generate_events(self):
        worksheet = self.xlsx.add_worksheet(name='EVENTS')
        self.write_header(worksheet)

    def generate_data_management(self):
        worksheet = self.xlsx.add_worksheet(name='DATA MANAGEMENT')
        self.write_header(worksheet)

    def generate_algorithms_analysis(self):
        worksheet = self.xlsx.add_worksheet(name='ALGORITHMS ANALYSIS')
        self.write_header(worksheet)

    def generate_version_analysis(self):
        worksheet = self.xlsx.add_worksheet(name='VERSIONS ANALYSIS')
        self.write_header(worksheet)

    def generate_earnings(self):
        worksheet = self.xlsx.add_worksheet(name='EARNINGS')
        self.write_header(worksheet)
    
    def generate_logs(self):
        worksheet = self.xlsx.add_worksheet(name='LOGS')
        self.write_header(worksheet)

    def generate_configuration(self):
        worksheet = self.xlsx.add_worksheet(name='CONFIG')
        self.write_header(worksheet)

    def write_header(self, worksheet):
        worksheet.merge_range(f'A1:S1', f'Carrera XLSX v{self.version}', self.format.header)



    def write_data(self, data: dict):

        # TODO: Would be wise to backup data in folder called backups before updating in case of error

        self.write_update(path='data/locations/tracks.xlsx', data=data['tracks'])
        self.write_update(path='data/profiles/horses_t.xlsx', data=data['horses'])
        self.write_update(path='data/profiles/trainers_t.xlsx', data=data['trainers'])
        self.write_update(path='data/profiles/owners_t.xlsx', data=data['owners'])
        self.write_update(path='data/profiles/jockeys_t.xlsx', data=data['jockeys'])

    def write_update(self, path: str, data: list):
        self.xlsx = xlsxwriter.Workbook(path)
        self.format: XlsxFormat = XlsxFormat(self.xlsx)
        worksheet = self.xlsx.add_worksheet()

        ref_data = vars(data[0])

        # Write headers from list of keys
        worksheet.write_row(row=0, col=0, data=ref_data.keys())

        # Write entries from list of values
        for index, entry in enumerate(data):
            entry_as_dict = vars(entry)
            formatted = self.pack_multiline_string(entry_as_dict)
            worksheet.write_row(col=0, row=index+1, data=formatted.values())
        
        self.xlsx.close()
        print(f'[XlsxWriter:INFO] write {path} OK')

    def pack_multiline_string(self, entry: dict):

        for key, value in entry.items():
            if key in MULTILINE_STRING_KEYS:
                string = ''
                for mls in value:
                    string += f'{mls.to_string()};'
                entry[key] = string
        return entry
        # string = ''
        # for key, value in entry.items():
        #     if key in MULTILINE_STRING_KEYS:
        #         for mls_key, mls_value in value:
        #             string += f'{mls_key}={mls_value} '
        # return string