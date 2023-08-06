# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# © 2015 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    is_insurance_plan = fields.Boolean(
        string='Insurance Plan',
        help='Check this if the product is an insurance plan',
    )
