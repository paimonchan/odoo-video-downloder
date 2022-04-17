from dataclasses import dataclass
from ..commons.data import Data
from ..commons.field import Field

@dataclass
class StreamingData(Data):
    bitrate             = Field(int, 0)
    width               = Field(int, 0)
    height              = Field(int, 0)
    content_length      = Field(str, str())
    quality_label       = Field(str, str())