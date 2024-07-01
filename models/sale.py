from odoo import api, fields, models

class SaleOrderAddons(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    business_model = fields.Selection(selection=[
        ('rt', 'Retail'),
        ('corp', 'Corporate'),
        ('sub', 'Subscription'),
    ], string='Business Model', required=True)

    @api.depends('business_model')
    def name_get(self):
        result = []
        for order in self:
            name = order.name
            if order.business_model:
                short_name = {
                    'rt': '[RT]',
                    'corp': '[CORP]',
                    'sub': '[SUB]',
                }.get(order.business_model, '')
                name = f'{short_name} - {name}'
            result.append((order.id, name))
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLine, self).default_get(fields)
        sale_order_id = self._context.get('default_order_id')
        if sale_order_id:
            sale_order = self.env['sale.order'].browse(sale_order_id)
            allowed_taxes = self.env['account.tax'].search([('business_model', '=', sale_order.business_model)])
            res['tax_id'] = [(6, 0, allowed_taxes.ids)]
        return res

    @api.onchange('order_id')
    def _onchange_order_id(self):
        if self.order_id:
            allowed_taxes = self.env['account.tax'].search([('business_model', '=', self.order_id.business_model)])
            self.tax_id = [(6, 0, allowed_taxes.ids)]