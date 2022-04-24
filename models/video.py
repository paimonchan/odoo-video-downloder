from odoo import models, fields

class Video(models.Model):
    _name = 'paimon.video'
    _order = 'create_date desc'

    name                        = fields.Char()
    url                         = fields.Char(required=True)
    thumbnail_url               = fields.Char()

    line_ids                    = fields.One2many('paimon.video.line', 'video_id',)
    state                       = fields.Selection([
                                    ('draft', 'Draft'),
                                    ('faile', 'Failed'),
                                    ('done', 'Done')
                                ])
    type                        = fields.Selection([
                                    ('youtube', 'Youtube')
                                ], default='youtube')
    
    def action_generate_download_link(self, cookie=str()):
        downloader = self.env['paimon.youtube.downloader']
        record = downloader.create(dict(
            youtube_url         = self.url,
            youtube_cookie      = cookie
        ))

        stream, detail = record.get_downloadable_video()

        if detail:
            self.name           = detail.title
            self.thumbnail_url  = detail.thumbnail
        
        self.write(dict(line_ids=[(5,)]))
        for stream_data in stream:
            if not stream_data.quality_label:
                continue
            self.env['paimon.video.line'].create(dict(
                video_id        = self.id,
                quality_label   = stream_data.quality_label,
                bitrate         = stream_data.bitrate,
                download_url    = stream_data.url
            ))

class VideoLine(models.Model):
    _name = 'paimon.video.line'
    _order = 'bitrate asc'

    quality_label               = fields.Char()
    bitrate                     = fields.Integer()
    download_url                = fields.Char()

    video_id                    = fields.Many2one('paimon.video', ondelete='cascade')

    def open(self):
        return dict(
            type                = 'ir.actions.act_url',
            url                 = self.download_url,
            target              = 'new',
        )