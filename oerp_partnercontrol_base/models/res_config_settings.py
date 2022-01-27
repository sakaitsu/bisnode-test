# -*- coding: utf-8 -*-
"""
@author: Online ERP Hungary Kft.
"""

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # autocomplete
    module_oerp_partnercontrol_autocomplete = fields.Boolean("Bisnode AutoComplete Integration")
    pchu_username = fields.Char("User Name", config_parameter="partnercontrol.username", default="")
    pchu_password = fields.Char("Password", config_parameter="partnercontrol.password", default="")
    pchu_long_name = fields.Boolean(
        "Import With Long Name?", config_parameter="partnercontrol.long_name", default=False
    )
    pchu_use_odoo_autocompolete = fields.Boolean(
        "Enable Odoo IAP Autocomplete?", config_parameter="partnercontrol.call_odoo_autocomplete", default=False
    )

    # monitoring
    module_oerp_partnercontrol_monitor = fields.Boolean("PartnerControl Monitoring Integration")
    pchu_servicecd = fields.Char("Service Code", config_parameter="partnercontrol.servicecd", default="")

    # disable clearbit
    module_oerp_partner_autocomplete_noclearbit = fields.Boolean("Disable ClearBit AutoComplete Results")
