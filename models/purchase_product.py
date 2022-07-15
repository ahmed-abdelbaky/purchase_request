import required

from odoo import models, api, fields

product_id = fields.Many2one('product.product', required=True)
