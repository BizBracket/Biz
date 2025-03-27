from odoo import _, api, fields, models, tools
from odoo.exceptions import AccessError
import odoo

class BranchMaster(models.Model):
    _name = "branch.master"

    name = fields.Char('Branch', required=True)
    description = fields.Text('Description')
    company_id = fields.Many2one(
        'res.company', 'Company', required=True, copy=False,
        default=lambda self: self.env.user.company_id)
    street = fields.Char('Street', size=64)
    street2 = fields.Char('Street2', size=64)
    zip_id = fields.Many2one('pin.code.master', 'Zip')
    city_id = fields.Many2one(comodel_name='res.city', string='City')
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    email = fields.Char('Email', size=64)
    website = fields.Char('Website', size=64)
    phone = fields.Char('Phone', size=64)
    pan_no = fields.Char('PAN No.', size=64)
    cin_no = fields.Char('CIN No.', size=64)
    gstin_no = fields.Char('GSTIN', size=64)
    branch_code = fields.Char('Branch Code')
    branch_format = fields.Char('Branch Format')
    logo_branch = fields.Binary("Branch Logo", attachment=True)
    branch_code_prefix = fields.Char('Branch Code Prefix')
    branch_code_seq = fields.Integer('Branch Code seq', copy=False, default=1)



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
        print(self.city_id, "self.city_idself.city_idself.city_id")
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



class ResUsers(models.Model):
    _inherit = "res.users"

    branch_ids = fields.Many2many('branch.master', 'branch_relation_rel', 'user_id', 'branch_id', string='Branches',
                                  required=False)


class areas_basic_masters(models.Model):
    _name = "areas.basic.masters"
    _description = "Areas Basic Masters"

    name = fields.Char('Area Name', required=True)
    city_id = fields.Many2one('res.city', 'City')
    pin_code_id = fields.Many2one('pin.code.master', 'Pincode')


class PinCodeMaster(models.Model):
    _name = "pin.code.master"
    _description = "Pincode Master"

    name = fields.Char('Pin Code', required=True)
    area_id = fields.Many2one('areas.basic.masters', string='Area')
    city_id = fields.Many2one('res.city', string='City')
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")


