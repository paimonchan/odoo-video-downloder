import re
import json
from werkzeug import urls
from odoo import models, fields
from odoo.exceptions import UserError
from urllib.parse import urlparse, parse_qs
from .base_downloader import BaseDownloader
from .datas.video_stream_data import VideoStreamData
from .datas.video_detail_data import VideoDetailData

class YoutubeDownloader(models.TransientModel, BaseDownloader):
    _name = 'paimon.youtube.downloader'

    youtube_url         = fields.Char(required=True)
    youtube_cookie      = fields.Char(default=str())

    def extract_video_id(self):
        """
        case url
         o> http://youtu.be/2Pdl4afH7_I
         o> http://www.youtube.com/watch?v=2Pdl4afH7_I&feature=feedu
         o> http://www.youtube.com/watch/2Pdl4afH7_I
         o> http://www.youtube.com/embed/2Pdl4afH7_I
         o> http://www.youtube.com/v/2Pdl4afH7_I?version=3&amp;hl=en_US
        """
        url = urlparse(self.youtube_url)
        if url.hostname == 'youtu.be':
            return url.path[1:]
        if url.path == '/watch':
            return parse_qs(url.query)['v'][0]
        if url.path[:7] == '/watch/':
            return url.path.split('/')[2]
        if url.path[:7] == '/embed/':
            return url.path.split('/')[2]
        if url.path[:3] == '/v/':
            return url.path.split('/')[2]
        return False
    
    def extract_video_stream(self, metadata):
        if not metadata:
            return dict()
        streaming_data = metadata.get('streamingData') or dict()
        adaptive_formats = streaming_data.get('adaptiveFormats') or []
        video_stream_datas = VideoStreamData.empty()
        for adaptive in adaptive_formats:
            streaming_data_id = VideoStreamData.create(dict(
                url             = adaptive.get('url'),
                bitrate         = adaptive.get('bitrate'),
                width           = adaptive.get('width'),
                height          = adaptive.get('height'),
                content_length  = adaptive.get('contentLength'),
                quality_label   = adaptive.get('qualityLabel'),
            ))
            video_stream_datas |= streaming_data_id
            # return streaming_data_ids
        return video_stream_datas
    
    def check_playable(self, metadata):
        def _check_status(status):
            if status == 'OK'                   : return
            if status == 'LOGIN_REQUIRED'       : raise UserError('This Is Private Video')
            
            raise UserError('Video Not Playable')
        
        playability_status = metadata.get('playabilityStatus') or dict()
        status = playability_status.get('status') or False
        _check_status(status)

    def contsruct_header(self):
        header = {
            'Cookie'            : self.youtube_cookie
        }
        return header

    def get_video_metadata(self):
        metadata_url = 'https://www.youtube.com/watch'
        pattern = 'ytInitialPlayerResponse\s*=\s*({.+?})\s*;'
        video_id = self.extract_video_id()
        params = dict(
            v                   = video_id,
            gl                  = 'US',
            hl                  = 'en',
            has_verified        = 1,
            bpctr               = 9999999999
        )

        header = self.contsruct_header()
        response = self.env['paimon.request'].GET(metadata_url, params, header)
        regex = re.compile(r'{}'.format(pattern))
        response_text = regex.search(response)
        if response_text:
            player_response = json.loads(response_text.group(1))
            self.check_playable(player_response)
            return player_response
        return False
    
    def get_video_info(self):
        info_url = 'https://www.youtube.com/get_video_info?'
        video_id = self.extract_video_id()
        params = dict(
            video_id            = video_id,
            html5               = 1,
            eurl                = 'https://youtube.googleapis.com/v/{}'.format(video_id),
            el                  = 'detailpage',
            c                   = 'TVHTML5',
            cver                = '6.20180913'
        )

        response = self.env['paimon.request'].GET(info_url, params)
        return response
    
    def get_downloadable_video(self):
        metadata = self.get_video_metadata()
        self._streaming_datas = streaming_data_ids
        return self.streaming_datas        self._video_stream_datas = self.extract_video_stream(metadata)