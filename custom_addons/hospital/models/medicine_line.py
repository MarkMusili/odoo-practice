from typing_extensions import ReadOnly
from odoo import fields, models, api

class HospitalMedicineLine(models.Model):
    _name = "hospital.medicine.line"
    _description = "Medicine Line for Prescription"

    name = fields.Char(string='Description')
    product_id = fields.Many2one('product.product', string='Medicine', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Float(string='Price Unit')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True, readonly=True)

    consultation_id = fields.Many2one('hospital.consultation', string="Consultation")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id:
                if not record.name:
                    record.name = record.product_id.display_name
                record.price_unit = record.product_id.list_price



    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
