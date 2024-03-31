



class MultilineString:
    def __init__(self, line: str) -> None:
        self._line = line
        self._parse_entries()
        self._format()
    
    def _parse_entries(self):
        entries = self._line.split(',')

        for entry in entries:
            try:
                k, value = entry.strip().split('=')
                setattr(self, k, value)
            except ValueError:
                exit(f'[MutlilineString:ERROR] Error parsing multiline string in line, check for commas: {self._line}')

    def _format(self):
        pass
