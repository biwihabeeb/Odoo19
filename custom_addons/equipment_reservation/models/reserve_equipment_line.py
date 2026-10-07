# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ReserveEquipmentLine(models.Model):
    _name = 'reserve.equipment.line'
    _rec_name = 'equipment_id'

    equipment_id = fields.Many2one(
        'product.product',
        string='Equipment',
    )

    reservation_id = fields.Many2one(
        'reserve.equipment',
        string='Reservation ID',
    )