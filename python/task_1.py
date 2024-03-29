import os
import csv
from collections.abc import Iterable


READ_FROM = '/Users/nikitaseleznev/Downloads/Corp_Summary.csv'
SAVE_TO = '/Users/nikitaseleznev/Downloads/summary_report.csv'


class Utils:
    @staticmethod
    def is_correct_path(file_path: str) -> bool:
        """
        Check if a path exists or not

        Parameters
        ----------
        file_path : str
        Any valid string path is acceptable. The string could be a URL.

        Returns
        -------
        True if a path is correct else False
        """
        is_correct = False

        if not isinstance(file_path, str):
            return is_correct

        is_correct = os.path.exists(file_path)

        return is_correct

    @staticmethod
    def is_correct_filename_extension(file_path: str) -> bool:
        """
        Check if a filename extension is csv

        Parameters
        ----------
        file_path : str
        Any valid string path is acceptable. The string could be a URL.

        Returns
        -------
        True if a filename extension is csv else False
        """

        filename_extension = file_path[file_path.rfind('.') + 1:]

        if filename_extension != 'csv':
            return False
        return True

    @staticmethod
    def correct_input(input_:str) -> str:
        """
        Check if a input is correct and if not offers to enter again

        Parameters
        ----------
        input_ : str
        Supposed four options: 1, 2, 3, exit

        Returns
        -------
        Correct input
        """

        correct_input = list(map(str, range(1, 4))) + ['exit']

        while True:
            if input_ not in correct_input:
                print('Incorrect input, supposed only four options: 1, 2, 3, exit')
                input_ = input()
            else:
                break

        return input_

    @staticmethod
    def is_columns_in_csv(columns: Iterable, header: Iterable) -> bool:
        """
        Check if the columns are in the header

        Parameters
        ----------
        columns : Iterable
        header: Iterable

        Returns
        -------
        True if columns are in the header else False
        """

        is_columns_in_csv = (len(set(columns) - set(header)) == 0)

        if not is_columns_in_csv:
            return False
        return True

    @staticmethod
    def print_command_information() -> None:
        """
        Prints command information
        """

        print('1 - Displays command hierarchy.')
        print('2 - Displays a summary report by department.')
        print('3 - Saves the summary report.')
        print('4 - Exit.')

    @staticmethod
    def get_command_hierarchy(reader: Iterable) -> dict:
        """
        Builds a command hierarchy

        Parameters
        ----------
        reader: Iterable

        Returns
        -------
        Command hierarchy in dict 
        """

        if not isinstance(reader, Iterable):
            raise 'Function only accepts Iterable objects'

        header = next(reader)

        name2num = {name: ind for ind, name in enumerate(header)}

        if not Utils.is_columns_in_csv(['Департамент', 'Отдел'], header):
            raise ValueError(f'csv file has to contain the folowing colunms: Департамент, Отдел]')

        command_hierarchy = {}

        for row in reader:
            dep, team = row[name2num['Департамент']], row[name2num['Отдел']]

            if dep not in command_hierarchy:
                command_hierarchy[dep] = set()

            command_hierarchy[dep] |= set([team])

        return command_hierarchy

    @staticmethod
    def print_command_hierarchy_helper(command_hierarchy: dict) -> tuple([int, int]):
        """
        Сalculates the minimum size of cells in a table

        Parameters
        ----------
        command_hierarchy: dict

        Returns
        -------
        Length of first and second column
        """

        max_len_dep = max(map(len, command_hierarchy.keys()))
        max_len_team = max(map(lambda x: max(map(len, x)), command_hierarchy.values()))

        max_len_num_dep = len(str(len(command_hierarchy.keys()))) + len('. ')
        max_len_num_team = len(str(len(command_hierarchy.values()))) + len('. ')

        max_len_dep = max(max_len_dep, len('Департамент'))
        max_len_team = max(max_len_team, len('Отдел'))

        llen, rlen = max_len_dep + max_len_num_dep, max_len_team + max_len_num_team

        return llen, rlen

    @staticmethod
    def print_command_hierarchy(reader: Iterable) -> True:
        """
        Prints a command hierarchy

        Parameters
        ----------
        reader: Iterable

        Returns
        -------
        Bool: True
        """
        command_hierarchy = Utils.get_command_hierarchy(reader)

        llen, rlen = Utils.print_command_hierarchy_helper(command_hierarchy)

        print(f"%-{llen}s %-{rlen}s" % ('Департамент', 'Отдел'))

        for i, dep in enumerate(command_hierarchy.keys()):
            for j, team in enumerate(command_hierarchy[dep]):
                if j == 0:
                    print(f"%-{llen}s %-{rlen}s" % ('-'*llen, '-'*rlen))
                    print(f"%-{llen}s %-{rlen}s" % (f'{i}. ' + dep, f'{j}. ' + team))
                    continue
                print(f"%-{llen}s %-{rlen}s" % (' ', f'{j}. ' + team))

        return True

    @staticmethod
    def get_summary_report(reader: Iterable) -> dict:
        """
        Builds a summary report

        Parameters
        ----------
        reader: Iterable

        Returns
        -------
        Summary report in dict 
        """

        if not isinstance(reader, Iterable):
            raise 'Function only accepts Iterable objects'

        header = next(reader)

        name2num = {name: ind for ind, name in enumerate(header)}

        if not Utils.is_columns_in_csv(['Департамент', 'Оклад'], header):
            raise ValueError(f'csv file has to contain the folowing colunms: Департамент, Оклад]')

        summary_report = {}

        for row in reader:
            dep, curr_salary = row[name2num['Департамент']], int(row[name2num['Оклад']])

            if dep not in summary_report:
                summary_report[dep] = dict()        

            min_max_sal = summary_report[dep].get('min_max_sal',  (curr_salary, curr_salary))
            summary_report[dep]['min_max_sal'] = (
                                                  min(min_max_sal[0], curr_salary), 
                                                  max(min_max_sal[1], curr_salary)
                                                 )

            summary_report[dep]['number'] = summary_report[dep].get('number', 0) + 1

        return summary_report

    @staticmethod
    def print_summary_report_helper(summary_report: dict) -> tuple([int, int, int]):
        """
        Сalculates the minimum size of cells in a table for print_summary_report function

        Parameters
        ----------
        summary_report: dict

        Returns
        -------
        Length of first, middle, second column
        """

        max_len_dep = max(map(len, summary_report.keys()))

        max_len_number = max([len(str(summary_report[dep]['number'])) for dep in summary_report])

        max_len_min_max_sal = max(
                                  [len(
                                       str(summary_report[dep]['min_max_sal'][0]) +\
                                       ' - ' + \
                                       str(summary_report[dep]['min_max_sal'][1])
                                   ) for dep in summary_report]
                              )
        max_len_num_dep = len(str(len(summary_report.keys()))) + len('. ')

        max_len_dep = max(max_len_dep, len('Департамент'))
        max_len_number = max(max_len_number, len('Численность'))
        max_len_min_max_sal = max(max_len_min_max_sal, len('Вилка ЗП'))

        llen, mlen, rlen = max_len_dep + max_len_num_dep, max_len_number, max_len_min_max_sal

        return llen, mlen, rlen

    @staticmethod
    def print_summary_report(reader: Iterable) -> True:
        """
        Prints a summary report

        Parameters
        ----------
        reader: Iterable

        Returns
        -------
        Bool: True
        """
        summary_report = Utils.get_summary_report(reader)

        llen, mlen, rlen = Utils.print_summary_report_helper(summary_report)

        print(f"%-{llen}s %-{mlen}s %-{rlen}s" % ('Департамент', 'Численность', 'Вилка ЗП'))

        for i, (dep, rep) in enumerate(summary_report.items()):
            number = rep['number']
            min_max_sal = str(rep['min_max_sal'][0]) + ' - ' + str(rep['min_max_sal'][1])

            print(f"%-{llen}s %-{mlen}s %-{rlen}s" % ('-'*llen, '-'*mlen, '-'*rlen))
            print(f"%-{llen}s %-{mlen}s %-{rlen}s" % (f'{i}. ' + dep, number, min_max_sal))

        return True

    @staticmethod
    def save_summary_report(reader: Iterable, file_path: str = SAVE_TO, delimiter: str = ';') -> True:
        """
        Saves a summary report

        Parameters
        ----------
        reader: Iterable
        file_path: str. Path to save a summary report
        delimiter: str

        Returns
        -------
        Bool: True
        """

        if not isinstance(file_path, str):
            raise ValueError(f'Incorrect path: {file_path}')

        if not Utils.is_correct_filename_extension(file_path):
            raise ValueError('Only csv files are supported')

        summary_report = Utils.get_summary_report(reader)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)

            writer.writerow(['Департамент', 'Численность', 'Вилка ЗП'])

            for dep, rep in summary_report.items():
                min_max_sal = str(summary_report[dep]['min_max_sal'][0]) +\
                                       ' - ' + \
                                       str(summary_report[dep]['min_max_sal'][1])

                writer.writerow([dep, summary_report[dep]['number'], min_max_sal])

        return True

    @staticmethod
    def exit() -> False:
        """
        Exit the progaram

        Returns
        -------
        Bool: False
        """

        print('Program completed')
        return False

    @staticmethod
    def case2func(reader: Iterable, case: str) -> bool:
        """
        Uses required function depending on user's input

        Parameters
        ----------
        reader: Iterable
        case : str. Supposed to be only one of these elements: [1, 2, 3, exit]

        Returns
        -------
        Bool
        """
        correct_cases = list(map(str, range(1, 4))) + ['exit']

        case2num = {case: ind for ind, case in enumerate(correct_cases)}

        optional_funcs = [Utils.print_command_hierarchy,
                          Utils.print_summary_report,
                          Utils.save_summary_report,
                          Utils.exit]

        if case2num[case] < case2num['exit']:
            return optional_funcs[case2num[case]](reader)
        else:
            return optional_funcs[case2num[case]]()

    @staticmethod
    def read(file_path: str, delimiter: str = ';', case='exit') -> bool:
        """
        Reads a file and does one of four requests:

            1 - Displays command hierarchy.
            2 - Displays a summary report by department: name, headcount, "fork" of salaries in the form of min - max, average salary.
            3 - Saves the summary report from the previous paragraph as a csv file.
            4 - Exit.

        Parameters
        ----------
        file_path: str. Path to save a summary report
        delimiter: str
        case: str. Supposed to be only one of these elements: [1, 2, 3, exit]

        Returns
        -------
        Bool: True
        """

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            return Utils.case2func(reader, case)


def read_csv(file_path: str = READ_FROM, delimiter: str = ';') -> None:
    """
    Reads a file and does requests until exit:

        1 - Displays command hierarchy.
        2 - Displays a summary report by department: name, headcount, "fork" of salaries in the form of min - max, average salary.
        3 - Saves the summary report from the previous paragraph as a csv file.
        4 - Exit.

    Parameters
    ----------
    file_path: str. Path to save a summary report
    delimiter: str

    Returns
    -------
    Bool: True

    """

    if not Utils.is_correct_path(file_path):
        raise ValueError(f'Incorrect path: {file_path}')

    if not Utils.is_correct_filename_extension(file_path):
        raise ValueError('Only csv files are supported')

    Utils.print_command_information()

    input_ = Utils.correct_input(input())

    while Utils.read(file_path, delimiter, input_):
        input_ = Utils.correct_input(input())


if __name__ == '__main__':
    read_csv()
