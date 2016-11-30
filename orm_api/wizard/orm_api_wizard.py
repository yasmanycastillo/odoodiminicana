# -*- encoding:utf-8 -*-
from openerp import fields, models, api


class OrmApiWizard(models.TransientModel):
    """Wizard example"""
    _name = 'orm_api.wizard_report'

    student = fields.Many2one('orm_api.student', 'Estudiantes')

    def _get_data(self):
        """Obtencion de datos para el reporte"""
        Student = self.env['orm_api.student'].search([])
        resultado = []

        for line in Student:
            data = {
                'nombre': 'Fulano' if not line.name else line.name,
                'apellido': line.lastname,
                'genero': line.gender,
            }
            resultado.append(data)

        return resultado

    def _format_report(self, data):
        # from ipdb import set_trace;set_trace() # BREAK DOWN
        return self.pool['report'].get_action(
            self._cr, self._uid, [], 'orm_api.partner_report', data=data)

    @api.multi
    def print_report(self):
        # self.ensure_one()
        resultado = {}
        resultado['form'] = self._get_data()
        # from ipdb import set_trace;set_trace() # BREAK DOWN
        return self._format_report(resultado)


