from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread']
    _description = "Hospital Appointments"

    name = fields.Char(string="Reference",
            tracking=True,
            compute='_compute_reference'
    )
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one("res.partner", string="Doctor", tracking=True)
    consultation_id = fields.One2many("hospital.consultation", 'appointment_id', string='Medical Records')
    date = fields.Datetime(string='Appointment Date', required=True, tracking=True)
    reason = fields.Text(string='Reason for Visit')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')],
        string="Status",
        default='draft',
        tracking=True,
    )
    notes = fields.Text(string='Notes')
    active =  fields.Boolean(default=True)

    def confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def done(self):
        for rec in self:
            rec.state = 'done'

    def cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('patient_id.name')
    def _compute_reference(self):
        for record in self:
            if record.patient_id.name:
                record.name = f"{record.patient_id.name}'s Appointment"

    def consult(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Consult',
            'res_model': 'hospital.consultation',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_date': fields.Datetime.now(),
                'default_doctor_id': self.doctor_id.id,
            },
        }