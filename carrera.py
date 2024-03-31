from config import __version__
from libs.xlsx_writer import XlsxWriter
from libs.xlsx_reader import XlsxReader
from libs.xlsx_validate import XlsxValidate

""" Carrera Order/Structure

 PREDICTIONS
    - Algo bet predictions based on the UPCOMING EVENTS page
    - Shows odds, win/loss % predication
    - Show predictations for event for all algos simultaneously
 
 EVENTS
    - Lists upcoming events which algos will run against

 DATA MANAGEMENT
    - Lists imported/connected data
    - Source of data listed in directory /data
    - Each source is its own .xlsx, kept as database
    - e.g. horses.xlsx, cycling_athletes.xlsx, tennis_athletes.xlsx

 ALGORITHMS
    - Lists algorithms and display info/stats for analysis
 
 VERSIONS
    - Lists post-development version history and display info/stats for analysis
 
 EARNINGS
    - Display info/stats of bet earnings for analysis

 LOGS
    - Capture logs from output

 CONFIGURATION
    - Minor configurations page featuring options for adjustments (Bool Y/N, Int, and more)
"""

# # Symantic versioning (Major.minor.patch)
# __version__ = '0.1.0'


def main():
   print(f'[Carrera] Start Carrera, v{__version__}')
   carerra = CarreraXlsx()

   # Import xlsx data
   carerra.update()

   # Data Validate
   carerra.validate()

   # Algorithms Calc

   # Xlsx update: Predictions

   # Result Analysis and Metrics GUI

   print(f'[Carrera] Exit Carrera successfully')
      
class CarreraXlsx:
   def __init__(self) -> None:
      self.xlsx_reader = XlsxReader()
   
   def create(self):
      XlsxWriter(version=__version__).write_new()

   def test_read(self):
      XlsxReader().read()

   def update(self):
      self.xlsx_reader.import_data()
      self.xlsx_reader.update_data()
      
   def validate(self):
      XlsxValidate(self.xlsx_reader.data)
      

if __name__ == "__main__":
    main()