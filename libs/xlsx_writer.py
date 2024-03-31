import xlsxwriter
from libs.xlsx_format import XlsxFormat

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



    def update_data(self):

        self.write_update(path='data/locations/tracks.xlsx', data=self.data['tracks'])

    def write_update(self, path: str, data: list):
        self.xlsx = xlsxwriter.Workbook(path)
        self.format: XlsxFormat = XlsxFormat(self.xlsx)

        ref_data = data[0].__dict__()
        for key in ref_data.keys():
            pass
        self.xlsx.close()