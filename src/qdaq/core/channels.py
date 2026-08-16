'''
Contains base classes for data channels management
'''

from enum import Enum
from dataclasses import dataclass


class ChannelKind(Enum):
    SCALAR = 'scalar'
    ARRAY = 'array'
    SPECTRAL_IMAGE = 'spectral_image'

@dataclass
class ChannelSpec:
    name: str
    kind: ChannelKind
    unit: str | None = None
    metadata: str | None = None
