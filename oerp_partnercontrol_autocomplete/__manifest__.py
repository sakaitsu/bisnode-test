# -*- coding: utf-8 -*-
{
    "name": "Bisnode - AutoComplete",
    "version": "14.0.1.0.0",
    "author": "Online ERP Hungary Kft.",
    "website": "https://online-erp.hu/",
    "category": "OERP",
    "summary": "Autocomplete company data",
    "description": "Import data from Bisnode",
    "depends": [
        "base",
        "base_address_city",
        "oerp_partnercontrol_base",
        "partner_autocomplete",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/partnercontrol_autocomplete_assets.xml",
    ],
    "external_dependencies": {
        "python": ["zeep"],
        "bin": [],
    },
    "auto_install": False,
    "installable": True,
    "application": False,
}
