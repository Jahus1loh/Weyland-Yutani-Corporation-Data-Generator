from processing.data_analysis.analyze_data import analyze_data
from processing.generate_data.generate_data import generate_data
from processing.get_generator_data.extract_mines_aspects import (
    extract_mines_aspects,
)
from processing.get_generator_data.get_spreadsheet_data import (
    get_data_from_spreadhseet,
)


def process_data():
    spreadsheet_data = get_data_from_spreadhseet()
    extracted_data = extract_mines_aspects(spreadsheet_data)
    generated_data = generate_data(extracted_data)
    analyze_data(generated_data)
    # print(analyze_data(generated_data))
