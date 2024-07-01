from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    business_model = fields.Selection(selection=[
        ('rt', 'Retail'),
        ('corp', 'Corporate'),
        ('sub', 'Subscription'),
    ], string='Business Model')
