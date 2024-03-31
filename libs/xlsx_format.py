from xlsxwriter import Workbook


class XlsxFormat:
    # Cell background colors
    HEADER_BG_COLOR = '#f5dc85'
    INFO_BG_COLOR = 'e6e6e6'
    WARNING_BG_COLOR = '#ffcccc'
    ERROR_BG_COLOR = '#ffcccc'
    GREY_CELL_BG_COLOR = '#e6e6e6'

    # Font colors
    RED_NOTE_COLOR = '#af0e0e'

    # Font sizes
    DEFAULT_FONT_SIZE = 10
    SMALL_FONT_SIZE = 8

    def __init__(self, workbook: Workbook) -> None:
        self.header = workbook.add_format({'align': 'center', 'bold': True, 'border': True, 'bg_color': self.HEADER_BG_COLOR})
        self.default_font_size = workbook.add_format({'font_size': self.DEFAULT_FONT_SIZE})
        self.info = workbook.add_format({'align': 'center', 'bold': True, 'border': True, 'bg_color': self.INFO_BG_COLOR})
        self.warning = workbook.add_format({'align': 'center', 'bold': True, 'border': True, 'bg_color': self.WARNING_BG_COLOR})
        self.error = workbook.add_format({'align': 'center', 'bold': True, 'border': True, 'bg_color': self.ERROR_BG_COLOR})
