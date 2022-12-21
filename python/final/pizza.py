from enum import Enum
from functools import wraps
from typing import Dict


class Size(Enum):
    """Возможные размеры пицц."""

    L = 'L'
    XL = 'XL'


class EmojiMixin:
    """
    Миксин для добавления эмодзи к атрибуту name
    перед вызовом метода __str__.
    Для реализации используется __init_subclass__.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__str__ = EmojiMixin.__emojify_output(cls.__str__, cls.emoji)

    @staticmethod
    def __emojify_output(func, emoji):
        """Декорирует вызов функции с добавлением эмодзи к self.name."""

        @wraps(func)
        def wrapper(self):
            self.name += emoji
            func_result = func(self)
            self.name = self.name.removesuffix(emoji)
            return func_result
        return wrapper


class Pizza:
    """
    Класс для произвольной пиццы с названием pizza_name,
    рецептом recipe и размером size.
    """

    def __init__(self, pizza_name: str,
                 recipe: list[str], size: Size = Size.L) -> None:
        self.name = pizza_name
        self.recipe = recipe.copy()
        self.size = size

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        if not isinstance(value, Size):
            raise ValueError('Only items from enum Size are valid.')
        self._size = value

    def dict(self) -> dict:
        result = {
            'name': self.name,
            'recipe': self.recipe.copy(),
            'size': self.size,
        }
        return result

    def __eq__(self, other) -> bool:
        """
        Две пиццы равны, если совпадают их {ингредиенты, названия, размеры}.
        """

        if isinstance(other, Pizza):
            return self.dict() == other.dict()
        return False

    def __str__(self) -> str:
        return f'- {self.name}: {", ".join(self.recipe)}'

    @staticmethod
    def get_pizza_names() -> list[str]:
        """Возвращает названия всех производных пицц."""

        return [cls.__name__ for cls in Pizza.__subclasses__()]

    @staticmethod
    def get_pizzas() -> Dict:
        """Возвращает словарь {'название класса пиццы': класс пиццы}."""

        return {cls.__name__: cls for cls in Pizza.__subclasses__()}


class Margherita(Pizza, EmojiMixin):
    """Пицца маргарита."""

    emoji = '🧀'

    def __init__(self, size: Size = Size.L) -> None:
        name = 'Margherita'
        recipe = ['tomato sauce', 'mozzarella', 'tomatoes']
        super().__init__(name, recipe, size)


class Pepperoni(Pizza, EmojiMixin):
    """Пицца пепперони."""

    emoji = '🍕'

    def __init__(self, size: Size = Size.L) -> None:
        name = 'Pepperoni'
        recipe = ['tomato sauce', 'mozzarella', 'pepperoni']
        super().__init__(name, recipe, size)


class Hawaiian(Pizza, EmojiMixin):
    """Гавайская пицца."""

    emoji = '🍍'

    def __init__(self, size: Size = Size.L) -> None:
        name = 'Hawaiian'
        recipe = ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']
        super().__init__(name, recipe, size)


if __name__ == '__main__':
    pizza_hawaii = Hawaiian(Size('XL'))
    print(pizza_hawaii)
    print(pizza_hawaii.dict())
    print(pizza_hawaii.size.name)