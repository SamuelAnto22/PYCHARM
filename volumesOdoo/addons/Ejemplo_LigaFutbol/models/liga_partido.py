# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Modelo que representa un partido entre dos equipos
class LigaPartido(models.Model):
    _name = 'liga.partido'
    _description = 'Un partido de la liga'

    # Equipo local (relación Many2one con liga.equipo)
    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local')

    # Goles anotados por el equipo local
    goles_casa = fields.Integer()

    # Equipo visitante (relación Many2one con liga.equipo)
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante')

    # Goles anotados por el visitante
    goles_fuera = fields.Integer()

    # === VALIDACIONES ===

    # Valida que el equipo local no esté vacío ni sea el mismo que el visitante
    @api.constrains('equipo_casa')
    def _check_equipo_local(self):
        for record in self:
            if not record.equipo_casa:
                raise ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos deben ser diferentes.')

    # Valida que el equipo visitante no esté vacío ni sea igual al local
    @api.constrains('equipo_fuera')
    def _check_equipo_visitante(self):
        for record in self:
            if not record.equipo_fuera:
                raise ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos deben ser diferentes.')

    # === LÓGICA DE CLASIFICACIÓN ===

    # Recalcula la clasificación de todos los equipos
    def actualizoRegistrosEquipo(self):
        for equipo in self.env['liga.equipo'].search([]):
            # Resetea estadísticas
            equipo.victorias = equipo.empates = equipo.derrotas = 0
            equipo.goles_a_favor = equipo.goles_en_contra = 0

            for partido in self.env['liga.partido'].search([]):
                # Si el equipo jugó como local
                if partido.equipo_casa == equipo:
                    if partido.goles_casa > partido.goles_fuera:
                        equipo.victorias += 1
                    elif partido.goles_casa < partido.goles_fuera:
                        equipo.derrotas += 1
                    else:
                        equipo.empates += 1
                    equipo.goles_a_favor += partido.goles_casa
                    equipo.goles_en_contra += partido.goles_fuera

                # Si el equipo jugó como visitante
                if partido.equipo_fuera == equipo:
                    if partido.goles_fuera > partido.goles_casa:
                        equipo.victorias += 1
                    elif partido.goles_fuera < partido.goles_casa:
                        equipo.derrotas += 1
                    else:
                        equipo.empates += 1
                    equipo.goles_a_favor += partido.goles_fuera
                    equipo.goles_en_contra += partido.goles_casa

    # Cada vez que se modifica un campo de goles o equipos, actualiza la clasificación
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        self.actualizoRegistrosEquipo()

    # Al crear un partido, actualiza clasificación
    @api.model
    def create(self, values):
        record = super().create(values)
        self.actualizoRegistrosEquipo()
        return record

    # Al borrar un partido, también actualiza clasificación
    def unlink(self):
        res = super().unlink()
        self.actualizoRegistrosEquipo()
        return res

    # === ACCIONES ===

    # Suma 2 goles a todos los equipos locales en todos los partidos disputados
    def action_sumar_goles_casa(self):
        for partido in self.env['liga.partido'].search([]):
            if partido.goles_casa is None:
                partido.goles_casa = 2
            else:
                partido.goles_casa += 2
        self.actualizoRegistrosEquipo()
        return True

    # Suma 2 goles a todos los equipos visitantes en todos los partidos disputados
    def action_sumar_goles_fuera(self):
        for partido in self.env['liga.partido'].search([]):
            if partido.goles_fuera is None:
                partido.goles_fuera = 2
            else:
                partido.goles_fuera += 2
        self.actualizoRegistrosEquipo()
        return True
