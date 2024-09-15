# Copyright 2020 VERTS
# https://www.verts.co.in

from odoo import api, fields, tools, models,_
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date
import re
from odoo import http
from odoo.http import request, Response
from odoo.http import request,serialize_exception
from odoo.addons.web.controllers.main import ExcelExport
from odoo.exceptions import ValidationError
from odoo import api, models, fields, _
import werkzeug
import json
from lxml import etree



validClientIds = ['ODOO90bddb3e-cdd8-11ea-8954-48d2245123590']

class CrmLeadController(http.Controller):

    @http.route(['/crm_lead_web'], type='json', auth="public", methods=['POST'])
    def crm_lead_web(self, clientId, data):
        if (not clientId) or (clientId.isspace()) or (clientId not in validClientIds):
            return {"status": "Error", "msg": "INVALID CLIENT ID"}
        print("==========-------",data)
        try:
            medium_id = request.env['utm.medium'].search([('name','=','Website')])
            stage_id = request.env['crm.stage'].search([('name', '=', 'New')])
            description = data.get('description') if data.get('description') else ''
            if data:
                vals = {
                    'email_from': data.get('email') if data.get('email') else '',
                    'mobile': data.get('mobile') if data.get('mobile') else '',
                    'name':  data.get('name') if data.get('name') else '',
                    'contact_name': data.get('name') if data.get('name') else '',
                    'partner_name': data.get('company') if data.get('company') else '',
                    'city': data.get('city') if data.get('city') else '',
                    'state_id': data.get('state_id') if data.get('state_id') else '',
                    'country_id': data.get('country') if data.get('country') else '',
                    'stage_id': stage_id if stage_id else False,
                    'medium_id': medium_id if medium_id else False,
                    'description': description if description else False
                },
                if vals:
                    data = request.env['crm.lead'].sudo().create(vals)
                    if data:
                        return {'msg': 'Lead created successfully', 'status':'ok'}
                    else:
                        return {'msg': 'Unable to create the Lead', 'status':'error'}
        except Exception as e:
            msg = str(e)
            return {'msg': msg, 'status': 'error'}

    # @http.route(['/crm_lead_create'], type='json', auth="public", methods=['POST'])
    # def crm_lead_web(self, clientId, data):
    #     if (not clientId) or (clientId.isspace()) or (clientId not in validClientIds):
    #         return {"status": "Error", "msg": "INVALID CLIENT ID"}
    #     print("==========-------", data)
    #     try:
    #         if data:
    #             email = data.get('email', '')
    #             phone = data.get('phone', '')
    #
    #             # Check if lead with the same email or phone already exists
    #             existing_lead = request.env['crm.lead'].sudo().search(
    #                 ['|', ('email_from', '=', email), ('phone', '=', phone)], limit=1)
    #
    #             if existing_lead:
    #                 return {'msg': 'Lead with this email or phone already exists', 'status': 'error'}
    #             subscription= data.get('subscription', ''),
    #             notification_preferences= data.get('notification_preferences', ''),
    #             source=data.get('how_hear_about_us', '')
    #             function=data.get('job_title', '')
    #             industry= data.get('industry', '')
    #             interest= data.get('interests', '')
    #             notes = 'interest:' +interest + '\n \n \n' + "industry: " + industry + "\n" + " function: " + function + "\n" + " source: " + source + "\n" + " notification_preferences: " + notification_preferences + "\n" + " subscription: " + subscription
    #
    #             vals = {
    #                 'name': data.get('first_name', '') + ' ' + data.get('last_name', '') + data.get('postal_code', '') + data.get('country', ''),
    #                 'email_from': email,
    #                 'mobile': phone,
    #                 'street': data.get('address', '') + data.get('city', '') + data.get('state', ''),
    #                 # 'city': data.get('city', ''),
    #                 # 'state_id': data.get('state', ''),  # Assuming state is a char field, otherwise adjust accordingly
    #                 # 'zip': data.get('postal_code', ''),
    #                 # 'country_id': data.get('country', ''),
    #                 # Assuming country is a char field, otherwise adjust accordingly
    #                 'partner_name': data.get('company_name', ''),
    #                 # 'function': data.get('job_title', ''),
    #                 # 'industry': data.get('industry', ''),
    #                 # 'description': data.get('interests', ''),
    #                 # 'source_id': data.get('how_hear_about_us', ''),
    #                 # Assuming source_id is a char field, otherwise adjust accordingly
    #                 'website': data.get('website', ''),  # Assuming username as website for example purpose
    #                 'type': 'lead',  # Assuming type is lead, change if necessary
    #                 'notes': notes,
    #                 # 'subscription': data.get('subscription', ''),  # Adding subscription field
    #                 # 'notification_preferences': data.get('notification_preferences', ''),
    #             }
    #
    #             # try:
    #     #     if data:
    #     #         vals = {
    #     #             'email_from': data.get('email') if data.get('email') else '',
    #     #             'phone': data.get('mobile') if data.get('mobile') else '',
    #     #             'name': data.get('name') if data.get('name') else '',
    #     #             'partner_id': data.
    #     #         },
    #             if vals:
    #                 data = request.env['crm.lead'].sudo().create(vals)
    #                 if data:
    #                     return {'msg': 'Lead created successfully', 'status': 'ok'}
    #                 else:
    #                     return {'msg': 'Unable to create the Lead', 'status': 'error'}
    #     except Exception as e:
    #         msg = str(e)
    #         return {'msg': msg, 'status': 'error'}

    @http.route(['/crm_lead_create'], type='json', auth="public", methods=['POST'])
    def crm_lead_web(self, clientId, data):
        if (not clientId) or (clientId.isspace()) or (clientId not in validClientIds):
            return {"status": "Error", "msg": "INVALID CLIENT ID"}
        print("==========-------", data)
        try:
            if data:
                email = data.get('email', '')
                phone = data.get('phone', '')

                # Check if lead with the same email or phone already exists
                existing_lead = request.env['crm.lead'].sudo().search(
                    ['|', ('email_from', '=', email), ('phone', '=', phone)], limit=1)
                print('lead exist', existing_lead)
                if existing_lead:
                    return {'msg': 'Lead with this email or phone already exists', 'status': 'error'}

                function = data.get('job_title', '')
                industry = data.get('industry', '')
                interest = data.get('interest', '')  # Updated from 'interests' to 'interest'
                notes = (
                    f"interest: {interest}\n\n\n"
                    f"industry: {industry}\n"
                    f"function: {function}\n"
                )
                if data.get('level_of_contact') == 'select':
                    data['level_of_contact'] = ''

                # Updated 'vals' dictionary to include missing fields
                vals = {
                    'name': f"{data.get('first_name', '')} {data.get('last_name', '')}",
                    'email_from': email,
                    'mobile': phone,
                    'street': f"{data.get('address', '')}, {data.get('city', '')}, {data.get('state', '')}, {data.get('country', '')},{data.get('postal_code', '')}",
                    'partner_name': data.get('company_name', ''),
                    'business_name': data.get('business_name', ''),
                    'function': function,
                    'industry': industry,
                    'interest': interest,
                    'website': data.get('website', ''),
                    'type': 'lead',
                    'description': notes,
                    'type_of_registration': data.get('business_type', ''),  # Added business type
                    'level_of_contact': data.get('level_of_contact', '') ,  # Added level of contact
                    'hear_about_us': data.get('hear_about_us', ''),
                    'company_id':1,
                }

                if vals:
                    print('vals is here',vals)
                    new_lead = request.env['crm.lead'].sudo().create(vals)
                    if new_lead:
                        return {'msg': 'Lead created successfully', 'status': 'ok'}
                    else:
                        return {'msg': 'Unable to create the Lead', 'status': 'error'}
        except Exception as e:
            msg = str(e)
            return {'msg': msg, 'status': 'error'}

    @http.route(['/helpdesk_create'], type='json', auth="public", methods=['POST'])
    def helpdesk_create_web(self, clientId, data):
        if (not clientId) or (clientId.isspace()) or (clientId not in validClientIds):
            return {"status": "Error", "msg": "INVALID CLIENT ID"}
        print("==========-------", data)
        try:
            if data:
                vals = {
                    'partner_name': data.get('name') if data.get('name') else '',
                    'name': data.get('mobile') if data.get('mobile') else '',
                    'partner_email': data.get('email') if data.get('email') else '',
                    'description': data.get('message') if data.get('message') else '',
                },
                if vals:
                    data = request.env['helpdesk.ticket'].sudo().create(vals)
                    if data:
                        return {'msg': 'Record created successfully', 'status': 'ok'}
                    else:
                        return {'msg': 'Unable to create the record', 'status': 'error'}
        except Exception as e:
            msg = str(e)
            return {'msg': msg, 'status': 'error'}


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    interest = fields.Selection([
        ('want_to_get_featured_on_biz_bracket', 'Want to get featured on Biz Bracket'),
        ('exploring_a_feature_for_my_company', 'Exploring a feature for my company'),
        ('partner_with_biz_bracket', 'Partner with Biz Bracket'),
        ('business_consultation', 'Business Consultation'),
        ('other', 'Other'),
    ], string="Interest")

    level_of_contact = fields.Selection([
        ('ceo', 'CEO'),
        ('director', 'Director'),
        ('manager', 'Manager'),
        ('executive', 'Executive'),
    ], string="Level of Contact")

    industry = fields.Selection([
        ('agriculture', 'Agriculture'),
        ('automotive', 'Automotive'),
        ('aviation', 'Aviation'),
        ('banking_and_finance', 'Banking and Finance'),
        ('biotechnology', 'Biotechnology'),
        ('chemicals', 'Chemicals'),
        ('construction_and_real_estate', 'Construction and Real Estate'),
        ('consulting_services', 'Consulting Services'),
        ('consumer_goods_fmcg', 'Consumer Goods (FMCG)'),
        ('e_commerce', 'E-commerce'),
        ('education', 'Education'),
        ('energy_renewable_and_non_renewable', 'Energy (Renewable and Non-Renewable)'),
        ('entertainment_and_media', 'Entertainment and Media'),
        ('event_management', 'Event Management'),
        ('fashion_and_apparel', 'Fashion and Apparel'),
        ('food_and_beverages', 'Food and Beverages'),
        ('healthcare_and_pharmaceuticals', 'Healthcare and Pharmaceuticals'),
        ('hospitality_and_tourism', 'Hospitality and Tourism'),
        ('information_technology_it', 'Information Technology (IT)'),
        ('insurance', 'Insurance'),
        ('logistics_and_supply_chain', 'Logistics and Supply Chain'),
        ('manufacturing', 'Manufacturing'),
        ('mining_and_metals', 'Mining and Metals'),
        ('retail', 'Retail'),
        ('telecommunications', 'Telecommunications'),
        ('textiles', 'Textiles'),
        ('transportation', 'Transportation'),
        ('waste_management_and_recycling', 'Waste Management and Recycling'),
        ('water_resources_and_irrigation', 'Water Resources and Irrigation'),
        ('legal_and_professional_services', 'Legal and Professional Services'),
        ('others', 'Others'),
    ], string="Industry")

    hear_about_us = fields.Selection([
        ('google', 'Google'),
        ('social_media', 'Social Media'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ], string="How did you hear about us?")

    type_of_registration = fields.Selection([
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('company', 'Company'),
    ], string="Type of Registration")

    business_name = fields.Char("Business Name")
    membership_id = fields.Many2one('user.membership.type', 'Membership')

    def create_customer(self):
        if self:
            if self.email or self.mobile:
                vals = {
                    'partner_id': self.id,
                    'login': self.email if self.email else self.mobile,
                }
                users = self.env['res.users'].create(vals)


class CrmLeadMembershipType(models.Model):
    _name = "user.membership.type"

    name = fields.Char('Name')
    annual_subscription = fields.Float('Monthly/Yearly Subcription Amount')
    type = fields.Selection([('monthly','Monthly'),('yearly','Yearly')])






