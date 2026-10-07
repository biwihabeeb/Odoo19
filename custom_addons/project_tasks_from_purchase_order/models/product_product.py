# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    project_id = fields.Many2one(
        comodel_name='project.project'
    )