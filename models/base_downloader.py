from abc import abstractmethod
from .datas.streaming_data import StreamingData

class BaseDownloader:

    def __init__(self):
        self._streaming_datas = StreamingData()

    @abstractmethod
    def get_downloadable_video(self):
        pass

    @property
    def streaming_datas(self):
        return self._streaming_datas

    @streaming_datas.setter
    def streaming_datas(self, value):
        raise ValueError('cannot direct assign streaming_datas')