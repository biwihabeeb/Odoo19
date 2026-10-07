# -*- coding: utf-8 -*-

from odoo import fields,models

class LibraryGenres(models.Model):
    _name = 'library.genres'
    _description = 'Genres'

    # genre_id = fields.Id()
    name = fields.Char(
        string="Genre"
    )
