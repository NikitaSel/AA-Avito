import sys
from datetime import datetime


def timed_output(function):

    original_write = sys.stdout.write

    def my_write(string_text):
        dt_now = datetime.now()
        dt_string = dt_now.strftime("%Y-%m-%d %H:%M:%S")

        if string_text != '\n':
            return original_write('[' + dt_string + ']' + ': ' + string_text)
        return original_write(string_text)
   
    def wrapper(text: str):
        sys.stdout.write = my_write

        ret_val = function(text)

        sys.stdout.write = original_write
        return ret_val
    return wrapper

@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


if __name__ == '__main__':
    print_greeting("Nikita")

    print('[2021-12-05 12:00:00]: Hello, Nikita!')