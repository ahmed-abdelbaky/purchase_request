from odoo import models, fields, api


class purchase_request(models.Model):
    _name = 'purchase.request'
    _description = 'purchase_request.purchase_request'

    name = fields.Char(required=True)
    request_id = fields.Many2one("res.users", string="request by", required=True, default=lambda self: self.env.user)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date()
    reject_reason = fields.Text(string="Reject Reason")
    product_ids = fields.One2many('purchase.product', 'request_id', string="Purchase Request Line")
    total_price = fields.Float(string="Total Price", compute="get_total", store=True)
    state = fields.Selection(
        [
            ('draft', 'Reset to draft'),
            ('to_be_approve', 'Submit for Approval'),
            ('approve', 'Approve'),
            ('reject', 'Reject'),
            ('cancel', 'Cancel')
        ], string="status", default='draft'
    )

    def set_draft(self):
        self.state = 'draft'

    def to_be_approve(self):
        self.state = 'to_be_approve'

    def set_cancel(self):
        self.state = 'to_be_approve'

    def set_approve(self):
        self.state = 'approve'
        template_id = self.env.ref("purchase_request.email_template").id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        ctx = {
            'default_model': 'purchase.request',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_borders'
        }
        return ctx


    def set_reject(self):
        self.state = 'reject'

    @api.depends("product_ids.cost")
    def get_total(self):

        for record in self:
            comm = 0.0
            for line in record.product_ids:
                comm += line.cost
                record.total_price = comm
