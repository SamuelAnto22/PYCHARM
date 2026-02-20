# -*- coding: utf-8 -*-
from odoo import models, fields

# ==============================================================
#  MODELO TRANSIENTE (WIZARD)
# ==============================================================
# Este modelo es temporal. Los datos se guardan sólo mientras
# el asistente (wizard) está abierto. Luego, Odoo borra el registro.
# Muy útil para pantallas interactivas, confirmaciones o creación rápida.
# ==============================================================

class LigaEquipoWizard(models.TransientModel):
    _name = 'liga.equipo.wizard'
    _description = 'Asistente para crear nuevos equipos'

    # --------------------------------------------------------------
    # CAMPOS DEL WIZARD
    # --------------------------------------------------------------

    # Nombre del equipo a crear
    nombre = fields.Char(string='Nombre del equipo', required=True)

    # Descripción (HTML enriquecido)
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)

    # --------------------------------------------------------------
    # MÉTODO PRINCIPAL DEL WIZARD
    # --------------------------------------------------------------
    def add_liga_equipo(self):
        """
        Método que se ejecuta cuando el usuario pulsa el botón "Añadir"
        dentro del wizard. Crea un nuevo registro en el modelo liga.equipo.
        """

        # Obtenemos la referencia al modelo destino (liga.equipo)
        liga_equipo_model = self.env['liga.equipo']

        # self puede contener varios registros del wizard (aunque normalmente será uno)
        for wiz in self:
            # Creamos el nuevo equipo con los datos introducidos en el wizard
            liga_equipo_model.create({
                'nombre': wiz.nombre,
                'descripcion': wiz.descripcion,
            })

        # Al no devolver nada, Odoo simplemente cierra el wizard al terminar.
        # (Se podría devolver una acción si quisiéramos abrir el equipo creado).
