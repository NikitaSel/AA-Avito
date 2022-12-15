from typing import Generic, Sequence, Callable
from utils import T, SeqFlowMixin
from functools import partial


class Seq(SeqFlowMixin, Generic[T]):
    def __init__(self, seq: Sequence[T]) -> None:
        self.seq = seq
        self._transformes_list = []
        super().__init__()

    def map(self, func: Callable) -> None:
        map = partial(self._map, func)
        self._transformes_list.append(map)
        return self

    def filter(self, func: Callable) -> None:
        filter = partial(self._filter, func)
        self._transformes_list.append(filter)
        return self

    def take(self, num_elements: int) -> list:
        ret_val = []

        elements = self._take()

        i = 0
        while i < num_elements:
            elem = next(elements)
            ret_val.append(elem)
            i += 1

        self._drop_transformes_list()

        return ret_val

    def _drop_transformes_list(self):
        self._transformes_list = []


if __name__ == '__main__':

    test_seq = ('1', '2', '3', '4', '5', '6')

    seq = Seq(test_seq)

    print(seq.map(int).filter(lambda x: x % 2).take(3)) # --> [1, 3, 5]



    test_seq_2 = [[1, 1, 2], [2, 3, 2, 4]]

    seq = Seq(test_seq_2)

    print(seq.map(set).filter(lambda x: 1 in x).map(list).take(1)) # --> [[1, 2]]