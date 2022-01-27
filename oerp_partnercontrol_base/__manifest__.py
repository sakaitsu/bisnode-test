# -*- coding: utf-8 -*-
{
    "name": "Odoo Bisnode Modul",
    "version": "14.0.0.0.0",
    "author": "Online ERP Hungary Kft.",
    "website": "https://online-erp.hu/",
    "category": "OERP",
    "summary": "Provide services from Bisnode - PartnerControl",
    "description": "This is a technical module. Please install autocomplete or monitor modules.",
    "depends": ["base", "base_setup"],
    "data": [
        "security/acl.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
