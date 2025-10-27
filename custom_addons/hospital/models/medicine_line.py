from odoo import fields, models, api

class HospitalMedicineLine(models.Model):
    _name = "hospital.medicine.line"
    _description = "Medicine Line for Prescription"

    name = fields.Char(String='Description')
    product_id = fields.Many2one('product.product', string='Medicine', required=True)
    quantity = fields.Float(string='Quantity', defualt=1.0, required=True)
    price_unit = fields.Float(string='Price Unit', required=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)


    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
            
