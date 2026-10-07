# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        # print(self.order_line.mapped('product_id.project_id').name)
        project = None
        for line in self.order_line:
            # print(line.product_id)
            if line.product_id.project_id:
                project = line.product_id.project_id
                break
        # print(project)
        if not project:
            return super().button_confirm()

        total_qty = sum(self.order_line.mapped('product_uom_qty'))
        total_price = sum(self.order_line.mapped('price_subtotal'))
        stage = self.env['project.task.type'].search([
            ('name','=','In Progress')
        ])
        create_task = self.env['project.task'].create({
            'project_id': project.id,
            'name': "Purchase confirmed - %s" % self.name,
            'stage_id': stage.id,
            # 'description': f"Product total Quantity: {total_qty}, Product total Price: ${total_price}",
            'description': "Product total Quantity: %s,\nProduct total Price: $ %s" % (total_qty, total_price),

        })

        products = []

        for line in self.order_line:
            # print(line.product_id.name)
            products.append(line.product_id.name)
            self.env['project.task'].create({
                'name': line.product_id.name,
                'parent_id': create_task.id,
            })
        print(products)
        self.message_post(
            body=f"Project Task Created for linked materials:\n%s" % "\n".join(products)
        )
        return super().button_confirm()

