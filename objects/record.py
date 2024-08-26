



class Record:
    def __init__(self) -> None:
        self.starts: str = ''
        self.wins: str = ''
        self.places: str = ''
        self.shows: str = ''

    def __str__(self):
        return f'{self.starts}-{self.wins}-{self.places}-{self.shows}'

    def new(self, record_string: str):
        record_string = record_string.split('-')
        self.starts = record_string[0]
        self.wins = record_string[1]
        self.places = record_string[2]
        self.shows = record_string[3]

    def new_from_list(self, record_list: list):
        self.starts = record_list[0]
        self.wins = record_list[1]
        self.places = record_list[2]
        self.shows = record_list[3]
    