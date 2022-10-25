import json
from typing import Any
from functools import wraps


class ColorizeMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        color = cls.repr_color_code
        cls.__repr__ = ColorizeMixin.__color_repr(cls.__repr__, color)

    @staticmethod
    def __color_repr(func, color):
        @wraps(func)
        def wrapper(*args, **kwargs):
            base_repr_result = func(*args, **kwargs)
            color_code = f'\033[0;{color};1m'
            return color_code + base_repr_result + '\033[0;0;0m'
        return wrapper


class Base:
    def __init__(self, dict_: dict):
        for key in dict_:
            setattr(self, key, dict_[key])
        
    def __setattr__(self, __name: str, __value: Any) -> None:
        if isinstance(__value, dict):
            super().__setattr__('_' + __name, Base(__value))
        else:
            super().__setattr__('_' + __name, __value)

    def __getattr__(self, __name: str) -> Any:
        return super().__getattribute__('_' + __name)


class Advert(ColorizeMixin, Base):
    repr_color_code = 32

    def __init__(self, dict_: dict):
        if 'title' not in dict_:
            raise ValueError('title not in json')

        super(Advert, self).__init__(dict_)

    @property
    def price(self):
        if '_curr_price' in self.__dict__:
            return self._curr_price
        return 0

    @price.setter
    def _price(self, price):
        if price < 0:
            raise ValueError('Price must be >= 0')
        self.curr_price = price

    def __repr__(self) -> str:
        return f'{self._title} | {self._price} ₽'


lesson_str = """{
    "title": "python",
    "price": 0,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
}"""

lesson = json.loads(lesson_str)

lesson_ad = Advert(lesson)
print(lesson_ad)
print(lesson_ad.location.address)
