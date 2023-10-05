# -*- coding: utf-8 -*-

from odoo import models, fields, api


class edificio_tipo(models.Model):
    _name = 'juego.edificio_tipo'
    _description = 'Tipo edificio'

    nombre = fields.Char()
    atq = fields.Integer()
    produccion_oro = fields.Float()


#    produccion_(otro recurso pa dar a las tropas) = fields.Float()


class edificio(models.Model):
    _name = 'juego.edificio'
    _description = 'Edificio'

    nombre = fields.Char(related='tipo.nombre')
    tipo = fields.Many2one('juego.edificio_tipo', ondelete='restrict')
    nivel = fields.Float(default=1)
    vida = fields.Integer()
#   ciudad(cambiar nombre cuando sepa tematica) = fields.One2many('juego."ciudad"', ondelete='cascade')

