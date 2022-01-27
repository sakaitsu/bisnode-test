# -*- coding: utf-8 -*-
"""
@author: Online ERP Hungary Kft.
"""

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    pchu_partner_id = fields.Integer("PartnerControl ID")
    pchu_url = fields.Char("PartnerControl URL")

    pchu_vip = fields.Boolean("Monitoring", help="Very Important Partner. Choose to automatically monitor the partner.")
    pchu_last_update = fields.Datetime("PartnerControl Last Update Time", readonly=True)

    def open_bisnode_url(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": self.pchu_url,
        }
