from odoo import models, fields, api
import random

class PatientChronicCondition(models.Model):
    _name = "hospital.patient.chronic_condition"
    _description = "Patient chronic conditions"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(default=0)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'color' not in vals or vals['color'] == 0:
                vals['color'] = random.randint(1, 11)
        return super().create(vals_list)