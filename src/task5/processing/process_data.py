from processing.data_generator.extract_mines_aspects import (
    extract_mines_aspects,
)
from processing.data_generator.get_spreadsheet_data import (
    get_data_from_spreadhseet,
)


def process_data():
    spreadsheet_data = get_data_from_spreadhseet()
    print(extract_mines_aspects(spreadsheet_data))
