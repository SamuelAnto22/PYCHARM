# -*- coding: utf-8 -*-
# Este archivo define el modelo "liga.equipo" que representa a cada equipo de la liga.

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Modelo que almacena información de los equipos de fútbol.
class LigaEquipo(models.Model):

    # Identificador técnico del modelo en Odoo.
    _name = 'liga.equipo'

    # Descripción legible del modelo (usado en vistas y herramientas de desarrollo).
    _description = 'Equipo de la liga'

    # Orden por defecto en las vistas tipo tree o search.
    _order = 'nombre'

    # Indicamos qué campo se mostrará como el nombre del registro en campos Many2one.
    _rec_name = 'nombre'

    # === CAMPOS ===

    # Nombre del equipo, obligatorio.
    nombre = fields.Char('Nombre equipo', required=True, index=True)

    # Escudo del equipo, almacenado como imagen binaria. Se limitará visualmente a 50x50 píxeles.
    escudo = fields.Image('Escudo equipo', max_width=50, max_height=50)

    # Fecha en que se fundó el club.
    fecha_fundacion = fields.Date('Fecha fundación')

    # Descripción HTML del equipo (puede incluir imágenes, texto enriquecido).
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)

    # Número de partidos ganados, empatados y perdidos (se actualiza automáticamente).
    victorias = fields.Integer(default=0)
    empates = fields.Integer(default=0)
    derrotas = fields.Integer(default=0)

    # Campo computado: total de partidos jugados (sumando victorias + empates + derrotas).
    jugados = fields.Integer(compute="_compute_jugados", store=True)

    @api.depends('victorias', 'empates', 'derrotas')
    def _compute_jugados(self):
        for record in self:
            record.jugados = record.victorias + record.empates + record.derrotas

    # Campo computado: total de puntos según reglas de la liga.
    puntos = fields.Integer(compute="_compute_puntos", default=0, store=True)

    @api.depends('victorias', 'empates', 'derrotas', 'goles_a_favor', 'goles_en_contra')
    def _compute_puntos(self):
        for record in self:
            puntos = 0
            partidos = self.env['liga.partido'].search([])
            for partido in partidos:
                if partido.goles_casa is None or partido.goles_fuera is None:
                    continue

                if partido.equipo_casa == record:
                    diff = partido.goles_casa - partido.goles_fuera
                    if diff > 0:
                        puntos += 4 if diff >= 4 else 3
                    elif diff < 0:
                        puntos += -1 if abs(diff) >= 4 else 0
                    else:
                        puntos += 1
                elif partido.equipo_fuera == record:
                    diff = partido.goles_fuera - partido.goles_casa
                    if diff > 0:
                        puntos += 4 if diff >= 4 else 3
                    elif diff < 0:
                        puntos += -1 if abs(diff) >= 4 else 0
                    else:
                        puntos += 1

            record.puntos = puntos

    # Goles marcados y recibidos. Se actualizan desde los partidos.
    goles_a_favor = fields.Integer()
    goles_en_contra = fields.Integer()

    # === REGLAS DE VALIDACIÓN ===

    # Constraint SQL para evitar equipos duplicados por nombre
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El nombre del equipo debe ser único.'),
    ]

    # Constraint Python: la fecha de fundación debe ser anterior a la actual.
    @api.constrains('fecha_fundacion')
    def _check_fecha_fundacion(self):
        for record in self:
            if record.fecha_fundacion and record.fecha_fundacion > fields.Date.today():
                raise ValidationError('La fecha de fundación del club debe ser anterior a hoy.')
