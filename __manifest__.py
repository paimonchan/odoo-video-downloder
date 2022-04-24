# -*- coding: utf-8 -*-
{
    'name': "Odoo Video Downloader",
    'summary': """Odoo Video Downloader""",
    'description': """Video Downloader""",
    'author': "Paimon",
    'category': 'other',
    'version': '1.0.1',
    'depends': ['base'],
    'data': [
        'security/youtube_downloader.xml',
        'security/video_popup.xml',
        'security/video_line.xml',
        'security/video.xml',
        'views/video_popup.xml',
        'views/video.xml',
        'views/menu.xml',
    ],
}
