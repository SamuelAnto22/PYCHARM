# -*- coding: utf-8 -*-
from odoo import models, fields


class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Asistente para crear nuevos partidos'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local', required=True)
    goles_casa = fields.Integer(string='Goles local', default=0)
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante', required=True)
    goles_fuera = fields.Integer(string='Goles visitante', default=0)

    def add_liga_partido(self):
        liga_partido_model = self.env['liga.partido']
        for wiz in self:
            liga_partido_model.create({
                'equipo_casa': wiz.equipo_casa.id,
                'goles_casa': wiz.goles_casa,
                'equipo_fuera': wiz.equipo_fuera.id,
                'goles_fuera': wiz.goles_fuera,
            })
