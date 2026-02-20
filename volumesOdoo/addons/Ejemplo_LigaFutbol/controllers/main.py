# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# ============================
#  Controlador público HTTP
# ============================

# Esta clase maneja rutas web personalizadas que devuelven información de equipos en formato JSON
class Main(http.Controller):

    # ------------------------------------------------------
    # Ruta: /ligafutbol/equipo/json
    # - Tipo: HTTP GET
    # - Autenticación: Ninguna ("auth='none'")
    # - Propósito: Devolver la lista de equipos y sus estadísticas en JSON
    # ------------------------------------------------------
    @http.route('/ligafutbol/equipo/json', type='http', auth='none', csrf=False)
    def obtenerDatosEquiposJSON(self):
        """
        Esta función se ejecuta cuando accedemos a la URL:
            http://localhost:8069/ligafutbol/equipo/json
        Y devuelve la información de los equipos en formato JSON.
        No requiere autenticación.
        """

        # Obtenemos todos los registros del modelo liga.equipo usando sudo() para evitar restricciones
        equipos = request.env['liga.equipo'].sudo().search([])

        # Lista para almacenar la información que enviaremos en JSON
        listaDatosEquipos = []

        for equipo in equipos:
            # Convertimos los datos del equipo a una lista simple de valores
            listaDatosEquipos.append([
                equipo.nombre,
                str(equipo.fecha_fundacion),
                equipo.jugados,
                equipo.puntos,
                equipo.victorias,
                equipo.empates,
                equipo.derrotas,
            ])

        # Convertimos la lista a formato JSON (cadena de texto)
        json_result = json.dumps(listaDatosEquipos)

        # Devolvemos la respuesta al navegador
        return json_result

    # ------------------------------------------------------
    # Ruta: /eliminarempates
    # - Tipo: HTTP GET
    # - Autenticación: Ninguna ("auth='none'")
    # - Propósito: Eliminar partidos empatados y devolver cuántos se borraron
    # ------------------------------------------------------
    @http.route('/eliminarempates', type='http', auth='none', csrf=False)
    def eliminarEmpates(self):
        partidos = request.env['liga.partido'].sudo().search([])
        empatados = partidos.filtered(lambda p: p.goles_casa == p.goles_fuera)
        cantidad = len(empatados)
        if cantidad:
            empatados.unlink()
        return str(cantidad)
