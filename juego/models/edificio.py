# -*- coding: utf-8 -*-

from odoo import models, fields, api


class edificio_tipo(models.Model):
    _name = 'juego.edificio_tipo'
    _description = 'Tipo edificio'

    nombre = fields.Char()
    atq = fields.Integer()
    produccion_oro = fields.Float()
    max_vida = fields.Float()


#    produccion_(otro recurso pa dar a las tropas) = fields.Float()


class edificio(models.Model):
    _name = 'juego.edificio'
    _description = 'Edificio'

    nombre = fields.Char(related='tipo.nombre')
    tipo = fields.Many2one('juego.edificio_tipo', ondelete='restrict')
    nivel = fields.Float(default=1)
    vida = fields.Integer()
    planeta = fields.One2many('juego.planeta', ondelete='cascade')
    max_vida = fields.Integer()
    atq = fields.Integer()
    produccion_oro = fields.Integer()

    @api_depends(tipo, nivel):
    def _aumentar_estadisticas(self):
        for e in self:
            e.max_vida = e.tipo.max_vida*(e.nivel/3)
            e.vida = e.tipo.max_vida
            e.atq = e.tipo.atq*(e.nivel/5)
            e.produccion_oro = e.tipo.produccion_oro*()




