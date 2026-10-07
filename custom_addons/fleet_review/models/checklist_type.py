# -*- coding: utf-8 -*-

from odoo import fields, models

class ChecklistType(models.Model):
    _name = 'checklist.type'
    _rec_name = 'name'

    name = fields.Char()