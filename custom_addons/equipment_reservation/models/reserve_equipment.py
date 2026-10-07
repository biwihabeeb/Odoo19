# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ReserveEquipment(models.Model):
    _name = 'reserve.equipment'


    name = fields.Char(
        string='Reference ID',
        default='New',

    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
    )

    start_date = fields.Date(
        string='Start Date',
        required=True,
    )

    end_date = fields.Date(
        string='End Date',
        required=True,
    )

    purpose = fields.Text(
        string='Purpose',
    )
    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('using', 'In use'),
            ('returned', 'Returned'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
    )

    equipment_line_ids = fields.One2many(
        'reserve.equipment.line',
        inverse_name='reservation_id'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name','New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('reserve.equipment') or 'New'
        return super(ReserveEquipment, self).create(vals_list)

    def action_approve_equipment(self):
        if self.status == 'draft':
            request = self.search([
                # ('start_date','=', self.start_date),
                # # ('end_date','=', self.end_date),
                ('start_date','<=',self.end_date),
                ('end_date','>=',self.start_date),
                ('status','in',['approved','using']),
                ('id','!=',self.id),
            ])
            # print(request)
            approved_equipments = request.equipment_line_ids.mapped('equipment_id').ids
            requested_equipments = self.equipment_line_ids.mapped('equipment_id').ids
            print('requested_equipments:',requested_equipments)
            print('approved_equipments:',approved_equipments)
            if request:
                for rec in requested_equipments:
                    if rec in approved_equipments:
                        raise ValidationError("Reservation of equipment cannot be approved for the specified date. Please reschedule")
            self.status = 'approved'


    def action_start_equipment_use(self):
        if self.status == 'approved':
            self.status = 'using'


    def action_return_equipment(self):
        if self.status == 'using':
            self.status = 'returned'

    def action_cancel_request(self):
        self.status = 'cancel'


    def action_set_to_draft(self):
        self.status = 'draft'
