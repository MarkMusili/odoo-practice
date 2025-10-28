from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    consultation_id = fields.Many2one('hospital.consultation', string="Consultation")

class HospitalAccount(models.Model):
    _inherit = 'hospital.consultation'

    invoice_generated = fields.Boolean(string="Invoice Generated", default=False)
    invoice_line_ids = fields.One2many('account.move.line', 'consultation_id', string="Invoice Lines")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.depends('invoice_line_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('invoice_line_ids.consultation_id', '=', record.id)])

    def _prepare_invoice(self):
        return {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id,
            'invoice_date': datetime.now(),
            'invoice_origin': f"Consultation - {self.name}",
            'invoice_line_ids': []
        }

    def _prepare_invoice_line(self, medicine_line):
        return {
            'consultation_id': self.id,
            'product_id': medicine_line.product_id.id,
            'name': medicine_line.name,
            'quantity': medicine_line.quantity,
            'price_unit': medicine_line.product_id.list_price
        }

    def _create_invoice(self):
        self.ensure_one()
        invoice_vals = self._prepare_invoice()

        consultation_fee = (0, 0, {
                    'consultation_id': self.id,
                    'name': 'Consultation Fee',
                    'quantity': 1.0,
                    'price_unit': 500.0
                })

        invoice_line_vals = []
        for medicine_line in self.medicine_line_ids:
            line_vals = self._prepare_invoice_line(medicine_line)
            invoice_line_vals.append((0, 0, line_vals))

        invoice_vals['invoice_line_ids'] = invoice_line_vals + [consultation_fee]

        invoice = self.env['account.move'].create(invoice_vals)


    def generate_invoice(self):
        return self._create_invoice()

    def action_view_invoices(self):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [
            ('invoice_line_ids.consultation_id', '=', self.id)
        ]

        action.pop('res_id', None)
        return action