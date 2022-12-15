from typing import TypeVar, Any


T = TypeVar("T")


class SeqFlowMixin:

    def _map(self, func: callable, elem: Any):
        yield func(elem)

    def _filter(self, func: callable, elem: Any):
        if func(elem):
            yield elem

    def _take(self):

        for elem in self.seq:

            for transform in self._transformes_list[:-1]:
                try:
                    elem = next(transform(elem))
                except StopIteration:
                    break
            else:
                yield from self._transformes_list[-1](elem)