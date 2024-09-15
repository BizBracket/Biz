# License AGPL-3.0

{
    "name": "Helpdesk Management",
    "summary": """
        Helpdesk""",
    "version": "16.0.2.2.0",
    "license": "AGPL-3",
    "category": "After-Sales",
    "author": "Chevron",
    "website": "",
    "depends": ["mail", "portal", "project"],
    "data": [
        "data/helpdesk_data.xml",
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
        "views/helpdesk_ticket_templates.xml",
        "views/helpdesk_ticket_menu.xml",
        "views/helpdesk_ticket_team_views.xml",
        "views/helpdesk_ticket_stage_views.xml",
        "views/helpdesk_ticket_category_views.xml",
        "views/helpdesk_ticket_channel_views.xml",
        "views/helpdesk_ticket_tag_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_dashboard_views.xml",
        "wizard/convert_task_wizard_views.xml",
    ],
    "demo": ["demo/helpdesk_demo.xml"],
    "development_status": "Beta",
    "application": True,
    "installable": True,
}
