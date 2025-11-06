# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

logger = logging.getLogger(__name__)

class HospitalDashboard(http.Controller):
    @http.route('/hospital_dashboard/data', type='json', auth='user')
    def get_hospital_data(self):
        Patient = request.env['hospital.patient']
        Appointment = request.env['hospital.appointment']

        return {
            "total_patients": Patient.search_count([]),
            "total_appointments": Appointment.search_count([]),
            "patients_by_gender": {
                "male": Patient.search_count([('gender', '=', 'male')]),
                "female": Patient.search_count([('gender', '=', 'female')])
            }
        }