# -*- coding: utf-8 -*-
from stdnum import do

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FleetServiceOrder(models.Model):
    _name = 'fleet.service.order'

    name = fields.Char(
        string="Service Order",
        default='New',
        readonly = True,
    )

    technician_id = fields.Many2one(
        'hr.employee',
        domain=[
            ('is_available_technician', '=', True),
            # ('vehicle_ids','in',vehicle_id),
        ]
    )

    allowed_vehicle_ids = fields.Many2many(
        'fleet.vehicle',
        compute='_compute_allowed_vehicle_ids',
    )

    vehicle_id  = fields.Many2one(
        'fleet.vehicle',
        # domain=
    )


    service_date = fields.Date()
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
    )
    # — Selection: Draft, Confirmed, In
    # Progress, Done, Cancelled
    part_ids = fields.One2many(
        'fleet.service.order.part',
        inverse_name='order_id',
    )
    # — One2many → fleet.service.order.part
    checklist_ids = fields.One2many(
        'fleet.service.order.checklist',
        inverse_name='order_id',

    )

    parts_total = fields.Float(
        string="Sub Total",
        compute='_compute_parts_total',
    )

    labour_cost = fields.Float(
        string="Labour Cost",
    )

    grand_total = fields.Float(
        string="Total Amount",
        compute='_compute_grand_total',
    )

    checklist_progress = fields.Float(
        string="Checklist Progress",
        compute='_compute_checklist_progress',
        # store=True,
    )

    type_ids = fields.Many2many(
        'checklist.type'
    )

    @api.onchange('technician_id')
    def _compute_allowed_vehicle_ids(self):
        self.allowed_vehicle_ids = self.env['hr.employee'].search([
            ('id','=',self.technician_id.id),
        ]).mapped('vehicle_ids')


    @api.depends('part_ids')
    def _compute_parts_total(self):
        sub_total = 0
        if self.part_ids:
            for rec in self.part_ids:
                sub_total += rec.quantity * rec.unit_price
            self.parts_total = sub_total
        else:
            self.parts_total = 0.0

    @api.depends('parts_total','labour_cost')
    def _compute_grand_total(self):
        self.grand_total = self.parts_total + self.labour_cost

    @api.depends('checklist_ids.is_done')
    def _compute_checklist_progress(self):
        # print('_compute_checklist_progress')
        for rec in self:
            # print(self.checklist_ids)

            checklist_done = len(rec.checklist_ids.search([
                ('order_id','=',rec.id),
                ('is_done','=',True),
            ]))
            checklist_total = len(rec.checklist_ids.search([
                ('order_id','=',rec.id),
            ]))
            rec.checklist_progress = 0.0
            if checklist_total != 0:
                rec.checklist_progress = (checklist_done / checklist_total) * 100
            else:
                rec.checklist_progress = 0


    @api.model_create_multi
    def create(self, vals_list):
        """Generate sequence for book records"""
        print('vals_list', vals_list)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.service.order') or 'New'
        return super(FleetServiceOrder, self).create(vals_list)

    def button_confirm(self):
        if self.part_ids:
            self.state = 'confirmed'
        else:
            raise ValidationError('No Parts added. Please add parts to proceed')




    def button_generate_checklist(self):
        if self.state == 'confirmed' and not self.checklist_ids:
            checklist = self.mapped('type_ids')
            print('checklist_tasks', checklist)
            self.update({
                'checklist_ids': [
                    fields.Command.create({
                        'order_id': self.id,
                        'task_name': task.name,
                        'is_done': False,
                    }) for task in checklist
                ]
            })
        elif self.checklist_ids:
            print('checklist_tasks', self.checklist_ids)
            return {
                'type': "ir.actions.client",
                'tag': "display_notification",
                'params': {
                    'title': "Warning!",
                    'message': "Checklist lines already exist.",
                    'type': "warning",
                    'sticky': False,
                }
            }


        # pass

    def button_start_service(self):
        if self.technician_id and self.state == 'confirmed':
            self.state = 'in_progress'
            if self.checklist_progress == 100.0:
                self.state = 'done'
        else:
            raise ValidationError('Please add the responsible Technician')


    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.state == 'in_progress' and rec.checklist_progress == 100.0:
                rec.write({
                    'state': 'done',
                })
        return res


    def button_cancel(self):
        if self.state in ['draft', 'in_progress','confirmed']:
            self.state = 'cancel'
        else:
            raise ValidationError('Services that are completed cannot be cancelled')
        pass
