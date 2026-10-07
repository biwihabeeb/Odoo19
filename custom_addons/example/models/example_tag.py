# -*- coding: utf-8 -*-
from odoo import fields, models
import random

class ExampleTag(models.Model):
    _name = "example.tag"

    name=fields.Char(string="Name")
    color=fields.Integer(default=lambda self:random.randint(1,11),string="Color")