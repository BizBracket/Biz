# helpdesk_task_converter/wizard/convert_task_wizard.py

from odoo import _, api, fields, models

class ConvertTaskWizard(models.TransientModel):
    _name = 'convert.task.wizard'
    _description = 'Convert Helpdesk Ticket to Task Wizard'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)

    @api.model
    def default_get(self, fields):
        res = super(ConvertTaskWizard, self).default_get(fields)
        if self.env.context.get('default_ticket_id'):
            res['ticket_id'] = self.env.context['default_ticket_id']
        return res

    def action_create_task(self):
        self.ensure_one()
        task_vals = {
            'name': self.ticket_id.name,
            'project_id': self.project_id.id,
            'description': self.ticket_id.description,
            'company_id': self.ticket_id.company_id.id,
            'partner_id': self.ticket_id.partner_id.id if self.ticket_id.partner_id else None,
            'heldesk_ticket_id': self.ticket_id.id

        }
        task = self.env['project.task'].create(task_vals)
        self.ticket_id.is_task_created = True
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
