# -*- coding: utf-8 -*-
"""
@author: Online ERP Hungary Kft.
"""

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.country.state"

    city_ids = fields.One2many("res.city", "state_id", string="City's")
