from collections import UserDict
from typing import Any

class DuplicateKeyError(KeyError):
    def __init__(self, key, value):
        msg = f'key {key} already exists with value {value}'
        super(DuplicateKeyError, self).__init__(msg)

class UniqueKeyDict(UserDict):
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if __key in self:
            raise DuplicateKeyError(__key, self[__key])
        return super().__setitem__(__key, __value)