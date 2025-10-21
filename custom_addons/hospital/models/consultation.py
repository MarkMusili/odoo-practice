from odoo import api, fields, models

class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Electronic Medical Records"
    _inherit = ['mail.thread']

    name = fields.Char(
        string="Title",
        tracking=True,
        compute="_compute_title"
    )
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one("res.partner", string="Doctor", tracking=True)
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')
    date = fields.Datetime(string='Date', required=True, tracking=True)
    symptoms = fields.Text(string="Patient Symptoms", tracking=True)
    diagnosis = fields.Text(string="Diagnosis", tracking=True)
    treatment_plan = fields.Text(string="Summary of Treatment")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string="Status")

    def confirm(self):
        for record in self:
            record.state = 'in_progress'

    def done(self):
        for record in self:
            record.state = 'done'

    def generate_invoice(self):
        for record in self:
            return True

    def reset(self):
        for record in self:
            record.state = 'in_progress'

    @api.depends('patient_id.name')
    def _compute_title(self):
        for record in self:
            record.name = f"{record.patient_id.name}'s Consultation"