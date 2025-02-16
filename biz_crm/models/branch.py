from odoo import _, api, fields, models, tools
from odoo.exceptions import AccessError


class BranchMaster(models.Model):
    _name = "branch.master"
    _description = "Branch"
    _order = "id desc"


    branch_name = fields.Char(string="Name")
    branch_code = fields.Char(string="Code")
    city_id = fields.Many2one(comodel_name='res.city', string='City ID')
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state',
        string="State", domain="[('country_id', '=?', country_id)]"
    )
