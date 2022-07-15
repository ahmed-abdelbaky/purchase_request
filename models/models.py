from email.policy import default

import required

from odoo import models, fields, api


class purchase_request(models.Model):
    _name = 'purchase.request'
    _description = 'purchase_request.purchase_request'

    name = fields.Char(required=True)
    request_id = fields.Many2one("res.users", string="request by", required=True)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date()
    reject_reason = fields.Text(Readonly=True, string="Reject Reason")
    product_ids = fields.One2many('purchase.product', 'request_id', string="Purchase Request Line")
    total_price = fields.Float(string="Total Price", compute="get_total", store=True)

    @api.depends("product_ids.cost")
    def get_total(self):

        for record in self:
            comm = 0.0
            for line in record.product_ids:
                comm += line.cost
                record.total_price = comm
