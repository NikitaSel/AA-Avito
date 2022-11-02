import csv

from udict import UniqueKeyDict
from functools import partial
from F import (
    print_command_hierarchy, 
    print_summary_report,
    save_summary_report,

    print_command_information,
    is_correct_path,
    is_correct_filename_extension,
    correct_input
)


READ_FROM = '/Users/nikitaseleznev/Downloads/Corp_Summary.csv'
SAVE_TO = '/Users/nikitaseleznev/Downloads/summary_report.csv'

CASE2FUNC = UniqueKeyDict()
CASE2FUNC['1'] = print_command_hierarchy
CASE2FUNC['2'] = print_summary_report
CASE2FUNC['3'] = partial(save_summary_report, file_path=SAVE_TO)


def read(file_path: str, case: str, delimiter: str = ';') -> None:
    """
    Reads a file and does one of four requests:

        1 - Displays command hierarchy.
        2 - Displays a summary report by department: name, headcount, "fork" of salaries in the form of min - max, average salary.
        3 - Saves the summary report from the previous paragraph as a csv file.
        exit - Exit.

    Parameters
    ----------
    file_path: str. Path to save a summary report
    delimiter: str
    case: str. Supposed to be only one of these elements: [1, 2, 3]

    Returns
    -------
    None
    """

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        CASE2FUNC[case](reader)


def read_csv(file_path: str = READ_FROM, delimiter: str = ';') -> None:
    """
    Reads a file and does requests until exit:

        1 - Displays command hierarchy.
        2 - Displays a summary report by department: name, headcount, "fork" of salaries in the form of min - max, average salary.
        3 - Saves the summary report from the previous paragraph as a csv file.
        exit - Exit.

    Parameters
    ----------
    file_path: str. Path to save a summary report
    delimiter: str

    Returns
    -------
    None

    """

    if not is_correct_path(file_path):
        raise ValueError(f'Incorrect path: {file_path}')

    if not is_correct_filename_extension(file_path):
        raise ValueError('Only csv files are supported')

    print_command_information()

    while (input_ := correct_input(input())) != 'exit':
        read(file_path, input_, delimiter)
    else:
        print("Program completed")

if __name__ == '__main__':
    read_csv()
