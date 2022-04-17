from dataclasses import dataclass
from ..commons.data import Data
from ..commons.field import Field

@dataclass
class VideoDetailData(Data):
    video_id            = Field(str, 0)
    title               = Field(str, 0)
    length              = Field(str, 0)
    thumbnail           = Field(str, 0)
    description         = Field(str, 0)
    is_private          = Field(bool, False)