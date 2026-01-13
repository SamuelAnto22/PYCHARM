
from odoo import models, fields

class InstitutoCiclo(models.Model):
    _name = 'instituto.ciclo'
    _description = 'Ciclo Formativo'

    name = fields.Char(string="Nombre del Ciclo", required=True)
    codigo = fields.Char(string="Código")
    modulo_ids = fields.One2many('instituto.modulo', 'ciclo_id', string="Módulos")

class InstitutoModulo(models.Model):
    _name = 'instituto.modulo'
    _description = 'Módulo Profesional'

    name = fields.Char(string="Nombre del Módulo", required=True)
    ciclo_id = fields.Many2one('instituto.ciclo', string="Ciclo Formativo")
    profesor_id = fields.Many2one('instituto.profesor', string="Profesor")
    alumno_ids = fields.Many2many('instituto.alumno', string="Alumnos Matriculados")

class InstitutoAlumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Alumno'

    name = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    dni = fields.Char(string="DNI")
    modulo_ids = fields.Many2many('instituto.modulo', string="Módulos Matriculados")

class InstitutoProfesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Profesor'

    name = fields.Char(string="Nombre", required=True)
    especialidad = fields.Char(string="Especialidad")
    modulo_ids = fields.One2many('instituto.modulo', 'profesor_id', string="Módulos que Imparte")