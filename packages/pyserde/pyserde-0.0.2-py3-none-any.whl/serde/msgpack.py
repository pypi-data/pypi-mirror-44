from typing import Any, Tuple, Type

import msgpack
from dataclasses import astuple

from .core import FROM_TUPLE, T
from .de import Deserializer
from .se import Serializer


class MsgPackSerializer(Serializer):
    def serialize(self, obj: Any) -> str:
        return msgpack.packb(astuple(obj))


class MsgPackDeserializer(Deserializer):
    def deserialize(self, s: bytes) -> Tuple:
        return msgpack.unpackb(s, raw=False, use_list=False)


def to_msgpack(obj: Any, serializer=MsgPackSerializer) -> bytes:
    return obj.__serde_serialize__(serializer)


def from_msgpack(c: Type[T], s: str, de: Type[Deserializer] = MsgPackDeserializer) -> Type[T]:
    dct = de().deserialize(s)
    return getattr(c, FROM_TUPLE)(dct)
