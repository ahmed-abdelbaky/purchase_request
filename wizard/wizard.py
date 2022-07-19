from email.policy import default

from odoo import fields, models, api


class wizard(models.TransientModel):
    _name = 'purchase.wizard'

    def _default_sessions(self):
        return self.env['purchase.request'].browse(self._context.get('active_ids'))

    reason_ids = fields.Many2one('purchase.request', default=_default_sessions)
    reason = fields.Text(string='Reason')

    def confirm(self):
        self.reason_ids.reject_reason = self.reason,
        self.reason_ids.state = 'reject'

