from odoo import fields, models, api


class wizard(models.TransientModel):
    _name = 'purchase.wizard'

    reason = fields.Text(string='Reason')

    def confirm(self):
        self.env['purchase.request'].create(
            {
                "reject_reason": self.reason,
                'state': 'reject'
            }

        )

