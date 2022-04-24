from odoo import models, fields

class VideoPopup(models.TransientModel):
    _name = 'paimon.video.popup'

    url                         = fields.Char(required=True)
    cookie                      = fields.Char()

    def confirm(self):
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