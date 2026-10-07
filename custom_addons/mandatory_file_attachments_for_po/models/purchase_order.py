# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    no_attachments_warning_message = fields.Text(
        compute="_compute_no_attachments_warning_message",
        default=False
    )


    def _compute_no_attachments_warning_message(self):
        attachments = self.env['ir.attachment'].search([('res_id', '=', self.id)])
        if not attachments:
            self.no_attachments_warning_message = "WARNING: Requires at least one file attachment to confirm the Purchase Order."
        else:
            self.no_attachments_warning_message = False
        # print(self.no_attachments_warning_message)


    def button_confirm(self):
        is_required = self.env['ir.config_parameter'].sudo().get_param('purchase.attachment_required')
        # print(self.message_attachment_count)
        # print(is_required)
        print(self.env['ir.attachment'].search([('res_id','=',self.id)]).mapped('mimetype'))
        attachments = self.env['ir.attachment'].search([
            ('res_id','=',self.id),
        ])
        # print(attachments.filtered(lambda attachment: 'png' in attachment.mimetype or 'jpeg' in attachment.mimetype or 'pdf' in attachment.mimetype).mapped('display_name'))
        if is_required:
            if not attachments:
                raise ValidationError("Purchase Order Requires at least one file attachment to confirm the order.")
            else:
                if not attachments.filtered(lambda attachment: 'png' in attachment.mimetype or 'jpeg' in attachment.mimetype or 'pdf' in attachment.mimetype):
                    raise ValidationError("Attach Valid files (.jpg/.png/.pdf)")


        return super().button_confirm()