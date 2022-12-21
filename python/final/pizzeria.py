import random
from pizza import Pizza
from functools import wraps
from typing import Callable


def log(template: str) -> Callable:
    """Декорирует возвращаемое значение функции по шаблону template.
    template:
        func_name: название функции
        func_result: возвращаемое значение функции
        time: время выполнения функции
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(pizza: Pizza) -> str:
            log_time = random.randint(1, 59)
            mapping = {
                'time': log_time,
                'func_name': func.__name__,
                'func_result': func(pizza),
            }
            return template.format_map(mapping)
        return wrapper

    return decorator


@log('{func_result} за {time}с!')
def bake(pizza: Pizza) -> str:
    """Готовит пиццу."""

    return '🧑‍🍳 Приготовили'


@log('{func_result} за {time}c!')
def delivery(pizza: Pizza) -> str:
    """Доставляет пиццу."""

    return '🛵 Доставили'


@log('{func_result} за {time}с!')
def pickup(pizza: Pizza) -> str:
    """Самовывоз."""

    return '🏠 Забрали'


if __name__ == '__main__':
    print(bake(None))
    print(pickup(None))
    print(delivery(None))