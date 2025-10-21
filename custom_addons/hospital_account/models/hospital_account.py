from odoo import fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class HospitalAccount(models.Model):
    _inherit = 'hospital.consultation'

    invoice_generated = fields.Boolean(string="Invoice Generated", default=False)

    def generate_invoice(self):
        self.ensure_one()

        if self.invoice_generated:
            raise UserError(_("An Invoice has already been generated for this consultation. You cannot generate another invoice"))
            
        self.env['account.move'].create({
            'name': f"{self.patient_id.name}'s Invoice",
            'partner_id': self.patient_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': datetime.now(),
            'invoice_line_ids': [(0, 0, {
                'name': 'Consultation Fee',
                'quantity': 1,
                'price_unit': 500.0,
            }),
            (0, 0, {
                'name': 'Medication',
                'quantity': 1,
                'price_unit': 1000.0,
            })
            ],
        })

        self.write({'invoice_generated': True})
        return super().generate_invoice()