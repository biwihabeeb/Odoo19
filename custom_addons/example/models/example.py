# -*- coding: utf-8 -*-
from odoo import fields, models


class Example(models.Model):
    _name = "example"
    _description = "Example"

    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Partner")
    line_ids = fields.One2many('example.line', 'example_id', string="Example Lines")
    tags_ids = fields.Many2many("example.tag", string="Example Tags")

    def action_test(self):
        # self print("test",self.env.user)
        #  self.partner_id = self.env.user.partner_id
        #
        #  print(self.line_ids)
        #
        #  product = self.env['product.product'].search([], limit=1,order= "id desc")
        #  print(product.name)
        #
        #  self.line_ids = [fields.Command.create({
        #      'product_id': product.id,
        #      'quantity': 5,
        #      'price' : 50,
        #  }
        #
        #  )]

        # line = self.env['example.line'].search([('example_id', '=', self.id)], order="id asc", limit=1, offset=1)
        # line_all = self.env['example.line'].search([], order="id asc", limit=1, offset=1)
        # line = self.line_ids

        # print(line)
        #
        # print("lineall", line_all)
        # print("line1", line1)
        # if len(line) >= 2:
            # self.line_ids.create({
            #     'example_id': self.id,
            #     'product_id' : line[1].product_id.id,
            #     'price' : line[1].price,
            #     'quantity' : line[1].quantity,
            # })
            # line[1].copy()
        # qty>5
        # highest price
        # lowest qty first created qty= highest price
        # self.line_ids.sorted('quantity',reverse=True).sorted('id')[0].quantity=max(self.line_ids.filtered(lambda line: line.quantity >= 5).mapped('price'))
        # self.line_ids= [fields.Command.update( self.line_ids.sorted('quantity',reverse=True).sorted('id')[0].id,{
        #     'quantity':max(self.line_ids.filtered(lambda line: line.quantity >= 5).mapped('price')),
        # })]
        # line=self.line_ids.sorted('quantity',reverse=True)[0]
        # self.line_ids.sorted('quantity',reverse=True)[0].price = (line.price - (line.price * 0.05))
        # print("quantity",line.quantity)
        # self.line_ids=[fields.Command.update(line.id,{
        #     'price':(line.price-(line.price*0.05))
        # })]

        # line.write({
        #     'price': (line.price - (line.price * 0.05))
        # # })
        # line.price = (line.price - (line.price * 0.05))
        # self.line_ids=[fields.Command.delete(line.id)]

        # line.unlink()
        # tag=self.env.ref('example.model_example_tag_2')
        tag=self.tags_ids.search([('name','=','four')])
        print(tag.name)
        self.tags_ids=[fields.Command.delete(tag.id)]

        # self.line_ids=[fields.Command.unlink(line.id)]
        # line.write({'example_id':False})
        # unlinked=self.line_ids.search([('example_id','=',False)])
        # print(unlinked)
        # unlinked.write({'example_id':self.id})





