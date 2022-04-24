from abc import abstractmethod
from ..datas.video_stream_data import VideoStreamData
from ..datas.video_detail_data import VideoDetailData

class BaseDownloader:

    def __init__(self):
        self._video_stream_datas = VideoStreamData()
        self._video_detail_datas = VideoDetailData()

    @property
    def video_stream_datas(self):
        return self._video_stream_datas

    @video_stream_datas.setter
    def video_stream_datas(self, value):
        raise ValueError('cannot direct assign video_stream_datas')

    @property
    def video_detail_datas(self):
        return self._video_detail_datas

    @video_detail_datas.setter
    def video_detail_datas(self, value):
        raise ValueError('cannot direct assign video_detail_datas')

    @abstractmethod
    def get_downloadable_video(self):
        pass
