from logging import raiseExceptions
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'image.mixin']
    _description = "Patient Data"

    name = fields.Char(string="Patient Name", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string='Age', compute="_compute_age")
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], string='Blood Type')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    emergency_contact = fields.Char(string='Emergency Contact')
    active =  fields.Boolean(default=True)

    appointments_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    appointment_count = fields.Integer(compute='_compute_appointment_count')
    consultation_ids = fields.One2many('hospital.consultation', 'patient_id', string='Patient Records')
    allergies = fields.Many2many('hospital.patient.allergy', string="Allergies")
    chronic_conditions = fields.Many2many('hospital.patient.chronic_condition', string="Chronic Conditions")


    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])

    def book_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Book Appointment',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.id,
                'default_date': fields.Datetime.now(),
            },
        }

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list',
            'domain': [('patient_id', '=', self.id)],
        }

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                record.age = relativedelta(today, record.date_of_birth).years
            else:
                record.age = 0

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('name'):
                partner_vals = {
                    'name': val.get('name'),
                    'is_company': False,
                }
                if val.get('email'):
                    partner_vals['email'] = val['email']
                if val.get('phone'):
                    partner_vals['phone'] = val['phone']
                if val.get('address'):
                    partner_vals['street'] = val['address']

                partner = self.env['res.partner'].create(partner_vals)
                val['partner_id'] = partner.id
        return super().create(vals)
