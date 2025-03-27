from odoo import api, fields, tools, models,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_get_master_branch(self):
        if self.env.user.branch_ids:
            for branch in self.env.user.branch_ids:
                master_branch_id = branch.id
                return master_branch_id

    branch_id = fields.Many2one('branch.master', string='Branch', default=_default_get_master_branch)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('order_id.partner_id')
    def _compute_tax_id(self):
        """Apply different tax based on whether the customer's state matches the company's state."""
        # super(SaleOrderLine)._compute_tax_id()
        for line in self:
            company_state = line.order_id.company_id.state_id
            customer_state = line.order_id.partner_id.state_id

            if company_state and customer_state:
                if company_state == customer_state:
                    # Apply local tax if states match
                    tax = self.env['account.tax'].search([('name', 'in', ('CGST output 9%', 'SGST output  9%'))])
                else:
                    # Apply out-of-state tax if states are different
                    tax = self.env['account.tax'].search([('name', '=', 'IGST output  18%')], limit=1)

                # Assign tax to the order line
                line.tax_id = [(6, 0, tax.ids)] if tax else [(5, 0, 0)]  # Clear if no tax found




class Customer(models.Model):
    _inherit = 'res.partner'


    city_id = fields.Many2one(comodel_name='res.city', string='City')
    pin_code = fields.Many2one('pin.code.master', 'Zip')

    @api.onchange('zip_id')
    def on_change_zip_id(self):
        if self.zip_id:
            self.city_id = self.zip_id.city_id.id
            self.state_id = self.zip_id.state_id.id
            self.country_id = self.zip_id.country_id.id
        elif self.city_id == None and self.zip_id == None:
            self.city_id = ""
            self.zip_id = ""
            self.state_id = ""
            self.country_id = ""

    @api.onchange('city_id')
    def on_change_city_id(self):
        res = {}
        if self.city_id:
            self.country_id = self.city_id.country_id
            self.state_id = self.city_id.state_id
            if self.zip_id.city_id != self.city_id:
                self.zip_id = None
            res = {'domain': {'zip_id': [('city_id', '=', self.city_id.id)]}}
        else:
            self.city_id = None
            self.country_id = None
            self.state_id = None
            res = {'domain': {'zip_id': [(1, '=', 1)]}}
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _default_get_master_branch(self):
        if self.env.user.branch_ids:
            for branch in self.env.user.branch_ids:
                master_branch_id = branch.id
                return master_branch_id

    pin_code = fields.Many2one('pin.code.master', 'Zip')
    branch_id = fields.Many2one('branch.master', string='Branch', default=_default_get_master_branch)
    city_id = fields.Many2one(comodel_name='res.city', string='City')

