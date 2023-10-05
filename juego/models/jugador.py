# -*- coding: utf-8 -*-

from odoo import models, fields, api



# Crear una clase de Ciudad (cambiar nombre cuando sepa la tematica) y 1 jugador -> 1 ciudad
# Mirar lo de views.xml que es
# Cada vez que se crea una clase añadirlo con permisos a security
# si creo un nuevo archivo ponerlo en el init


class jugador(models.Model):
    _name = 'juego.jugador'
    _description = 'El jugador'

    nombre = fields.Char(required=True)
    planeta = fields.Many2one('juego.planeta')


class planeta(models.Model):
    _name = 'juego.planeta'
    _description = 'Uno de los planetas'

    nombre = fields.Char()
    jugador = fields.One2many('juego.jugador', required=True)
    soldados =
