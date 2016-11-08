# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import openerp.addons.decimal_precision as dp


class Student(models.Model):
    _name = "orm_api.student"
    _order = "credit"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    @api.depends('name', 'lastname')
    def _get_full_name(self):

        for rec in self:
            if not rec.name and not rec.lastname:
                rec.fullname = ""
            else:
                rec.fullname = u"{} {}".format(rec.name, rec.lastname)

    def _get_today(self):
        return fields.Date.today()

    def _get_gender(self):
        return [('m', 'Hombre'), ('f', 'Mujer')]

    name = fields.Char(string="Nombre", help="Es un tooltip de ayuda", copy=False, size=11)
    lastname = fields.Char(string="Apellido", help="Es un tooltip de ayuda", copy=False)
    fullname = fields.Char(compute=_get_full_name)
    fullname2 = fields.Char()
    date = fields.Date(string=u"Fecha", default=_get_today)
    gender = fields.Selection(_get_gender, string="Sexo")
    married = fields.Boolean("Casado")
    credit = fields.Float(digits=dp.get_precision('precio de producto'))
    colegio_id = fields.Many2one("orm_api.colegios")
    phone_ids = fields.One2many("orm_api.phone", "student_id")
    tags = fields.Many2many("orm_api.student.tags")
    state = fields.Selection([('draft', "Borrador"),('ac','Aceptado')], default="draft")


    @api.multi
    def state_toggle(self):
        self.state = "draft" if self.state == "ac" else "ac"


    @api.onchange("name", "lastname")
    def onchange_fullname2(self):
        if not self.name and not self.lastname:
            self.fullname2 = ""
        else:
            self.fullname2 = u"{} {}".format(self.name, self.lastname)

    @api.constrains("credit")
    def more_than_two(self):
        if self.credit < 100:
            raise exceptions.ValidationError("El credito debe ser mayor que 100")
        
    @api.model
    def create(self, vals):
        return super(Student, self).create(vals)
    
    @api.multi
    def write(self, vals):
        return super(Student, self).write(vals)

    @api.multi
    def unlink(self):
        return super(Student, self)


    @api.multi
    def create_auto_data(self):
        for a in range(1000):
            self.env["orm_api.colegios"].create({"name": "Cole {}".format(a)})

        # create on one2many
        self.write({"phone_ids": [(0, False, {"name": "809 597 2221"}),
                                  (0,False, {"name": "809 444 444"})]})

        return True

    def custom_search(self):

        self.search([('name','=','eneldo'),('lastname','ilike','serrata')])


class Colegios(models.Model):
    _name = "orm_api.colegios"

    name = fields.Char(string="Colegio", required=True, size=10)
    phone = fields.Char(string="Telefono", required=True, size=10)
    active = fields.Boolean()
    sequence = fields.Integer()


class Phone(models.Model):
    _name = "orm_api.phone"

    name = fields.Char("Telefono")
    student_id = fields.Many2one("orm_api.student")


class StudentTag(models.Model):
    _name = "orm_api.student.tags"

    name = fields.Char()


class CrmLead(models.Model):
    _inherit = "res.partner"

    student_id = fields.Many2one("orm_api.student")
