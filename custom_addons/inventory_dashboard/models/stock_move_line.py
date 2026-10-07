# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta, date

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def get_incoming_stock(self, filter):
        domain = [
            ("picking_code", "=", "incoming"),
            ('location_dest_id', '=', self.env.ref("stock.stock_location_stock")),
            ('state', 'in', ['assigned', 'waiting', 'confirmed']),
            ('company_id','=',self.env.company.id),
            ]
        is_group_user = self.env.user.has_group('stock.group_stock_manager')
        # print("wkehl ", self.env.company.name)

        year = int(filter['year'])
        if filter['period'] == '1' and filter['week']:
            week = int(filter['week'])
            print('W',week)
            if filter['month']:
                month = int(filter['month'])
                print(filter['month'])
            else:
                month = date.today().month
                print('M',month)
            start_date = datetime(year, month, 1 + (week - 1) * 7).date()
            end_date = start_date + timedelta(days=7)
            print('Filter by week', start_date, end_date)
            domain += [('create_date','>=', start_date),('create_date','<',end_date)]
        elif filter['period'] == '2' and filter['month']:
            month = int(filter['month'])
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month + 1, 1).date()
            print('Filter by month', start_date, end_date)
            domain += [('create_date','>=', start_date),('create_date','<',end_date)]

        if not is_group_user:
            domain.append(('create_uid','=',self.env.uid))
            incoming_stock = self.search_read(
                domain,
                fields=['product_id','quantity','product_uom_id','location_id','state','picking_id'],

            )
        else:
            incoming_stock = self.search_read(
                domain,
                fields=['product_id', 'quantity', 'product_uom_id', 'location_id', 'state','picking_id'],
                # limit=10
            )
        picking_ids = []
        for rec in incoming_stock:
            picking_ids.append(rec['picking_id'])
        # incoming_stock_qty = sum(incoming_stock.mapped('quantity'))
        # print(incoming_stock)
        # incoming_stock.append(picking_ids)
        return incoming_stock

    @api.model
    def get_outgoing_stock(self, filter):
        domain = [
            ("picking_code", "=", "outgoing"),
            ('location_id', '=', self.env.ref("stock.stock_location_stock")),
            ('state', 'in', ['assigned', 'waiting', 'confirmed']),
            ('company_id', '=', self.env.company.id),
        ]
        is_group_user = self.env.user.has_group('stock.group_stock_manager')

        year = int(filter['year'])
        if filter['period'] == '1' and filter['week']:
            week = int(filter['week'])
            print('W', week)
            if filter['month']:
                month = int(filter['month'])
                print(filter['month'])
            else:
                month = date.today().month
                print('M', month)
            start_date = datetime(year, month, 1 + (week - 1) * 7).date()
            end_date = start_date + timedelta(days=7)
            print('Filter by week', start_date, end_date)
            domain += [('create_date', '>=', start_date), ('create_date', '<', end_date)]
        elif filter['period'] == '2' and filter['month']:
            month = int(filter['month'])
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month + 1, 1).date()
            print('Filter by month', start_date, end_date)
            domain += [('create_date', '>=', start_date), ('create_date', '<', end_date)]

        if is_group_user:
            outgoing_stock = self.search_read(
                domain,
                fields=['product_id', 'quantity', 'product_uom_id', 'location_dest_id', 'state','picking_id'],
                # limit=10
            )
        else:
            domain.append(('create_uid', '=', self.env.uid))
            outgoing_stock = self.search_read(
                domain,
                fields=['product_id', 'quantity', 'product_uom_id', 'location_dest_id', 'state','picking_id'],
                # limit=10
            )


        print('OUTGOING STOCK')
        key = []
        res = {}
        result = []
        ids = []
        picking_ids = []
        for record in outgoing_stock:
            ids.append(record['id'])
            picking_ids.append(record['picking_id'][0])
            if record['product_id'][1] in key:
                res[record['product_id'][1]] += record['quantity']
            else:
                key.append(record['product_id'][1])
                res[record['product_id'][1]] = record['quantity']
            # print(record['product_id'][1])
        for key in res:
            result.append({'product':key, 'quantity':res[key]})

        print('OUT',outgoing_stock)
        result.append(ids)
        result.append(picking_ids)
        return result

    @api.model
    def get_internal_transfers(self, filter):
        domain = [
            ("picking_code", "=", "internal"),
            ('company_id', '=', self.env.company.id),

        ]
        is_group_user = self.env.user.has_group('stock.group_stock_manager')

        year = int(filter['year'])
        if filter['period'] == '1' and filter['week']:
            week = int(filter['week'])
            print('W', week)
            if filter['month']:
                month = int(filter['month'])
                print(filter['month'])
            else:
                month = date.today().month
                print('M', month)
            start_date = datetime(year, month, 1 + (week - 1) * 7).date()
            end_date = start_date + timedelta(days=7)
            print('Filter by week', start_date, end_date)
            domain += [('create_date', '>=', start_date), ('create_date', '<', end_date)]
        elif filter['period'] == '2' and filter['month']:
            month = int(filter['month'])
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month + 1, 1).date()
            print('Filter by month', start_date, end_date)
            domain += [('create_date', '>=', start_date), ('create_date', '<', end_date)]

        if is_group_user:
            internal_transfers = self.search_read(
                domain,
                fields=['product_id', 'location_id', 'location_dest_id', 'state', 'quantity', 'product_uom_id','picking_id'],
            )
        else:
            domain.append(('create_uid', '=', self.env.uid))
            internal_transfers = self.search_read(
                domain,
                fields=['product_id', 'location_id', 'location_dest_id', 'state', 'quantity', 'product_uom_id','picking_id'],
            )

        key = []
        res = {}
        result = []
        ids = []
        picking_ids = []
        for record in internal_transfers:
            ids.append(record['id'])
            print('PICKING ID', record['picking_id'])
            if record['picking_id']:
                picking_ids.append(record['picking_id'][0])
            if record['product_id'][1] in key:
                res[record['product_id'][1]] += record['quantity']
            else:
                key.append(record['product_id'][1])
                res[record['product_id'][1]] = record['quantity']
            # print(record['product_id'][1])
        for key in res:
            result.append({'product': key, 'quantity': res[key]})
        result.append(ids)
        result.append(picking_ids)
        return result