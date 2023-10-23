import sys
from datetime import datetime


original_write = sys.stdout.write

def my_write(string_text):
    dt_now = datetime.now()
    dt_string = dt_now.strftime("%Y-%m-%d %H:%M:%S")

    if string_text != '\n':
        return original_write('[' + dt_string + ']' + ': ' + string_text)
    return original_write(string_text)


if __name__ == '__main__':

    sys.stdout.write = my_write

    print('1, 2, 3')

    sys.stdout.write = original_write

    print('[2021-12-05 12:00:00]: 1, 2, 3')