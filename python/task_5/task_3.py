import os
import sys


def redirect_output(filepath):
    def out_wrapper(function):
        def wrapper():
            original_out = sys.stdout

            with open(filepath, 'w') as output:
                sys.stdout = output

                ret_val = function()

            sys.stdout = original_out
            return ret_val
        return wrapper
    return out_wrapper

@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


if __name__ == '__main__':
    calculate()