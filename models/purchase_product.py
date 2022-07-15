from email.policy import default

import required

from odoo import models, api, fields


class purchaseProduct(models.Model):
    _name = 'purchase.product'

    product_id = fields.Many2one('product.product', required=True)
    description = fields.Char(related='product_id.name', string="Description")
    quality = fields.Integer(default=1)
    cost = fields.Float(related='product_id.standard_price', string='Cost', readonly=True)
    total = fields.Float(string='Total', compute='get_cost', readonly=True)
    request_id = fields.Many2one('purchase.request')

    @api.depends('quality', 'cost')
    def get_cost(self):
        for record in self:
            record.total = record.quality * record.cost
