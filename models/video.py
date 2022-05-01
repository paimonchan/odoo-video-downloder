from odoo import models, fields

class Video(models.Model):
    _name = 'paimon.video'
    _order = 'write_date desc'

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
    next_refresh_date           = fields.Datetime()
    
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

class VideoPopup(models.TransientModel):
    _name = 'paimon.video.popup'

    url                         = fields.Char(required=True)
    cookie                      = fields.Char()

    def confirm(self):
        video_id = self.env['paimon.video'].search([('url', '=', self.url)], limit=1)
        if not video_id:
            video_id = self.env['paimon.video'].create(dict(
                url                 = self.url,
            ))
        video_id.action_generate_download_link(self.cookie or str())

        return dict(
            name                ='Delivery',
            type                ='ir.actions.act_window',
            res_model           ='paimon.video',
            view_mode           ='kanban,form',
            view_type           ='form',
            target              ='current',
        )