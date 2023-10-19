# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Cada vez que se crea una clase añadirlo con permisos a security
# si creo un nuevo archivo ponerlo en el init
# todas las clases ponerlas en el views.xml
# poner cosas de Demo en demo.xml

class jugador(models.Model):
    _name = 'juego.jugador'
    _description = 'El jugador'

    nombre = fields.Char(required=True)
    planetas = fields.One2many('juego.planeta', 'jugador')

    @api.constrains('nombre')
    def _nombre_vacio(self):
        for n in self:
            if n.nombre == "":
                raise ValidationError("El nombre no puede estar vacio")

class planeta(models.Model):
    _name = 'juego.planeta'
    _description = 'Uno de los planetas'

    nombre = fields.Char()
    jugador = fields.Many2one('juego.jugador', ondelete="cascade")
    edificios = fields.One2many('juego.edificio', 'planeta')


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


def _calcular_estadisticas(self):
    for e in self:
        e.max_vida = e.tipo.max_vida * (e.nivel / 3)
        e.vida = e.tipo.max_vida
        e.atq = e.tipo.atq * (e.nivel / 5)
        e.produccion_oro = e.tipo.produccion_oro * ()

@api.depends('tipo', 'nivel')
def _aumentar_estadisticas(self):
    for e in self:





class edificio_tipo(models.Model):
    _name = 'juego.edificio_tipo'
    _description = 'Tipo edificio'

    nombre = fields.Char()
    planeta = fields.Many2one('juego.planeta', ondelete="cascade")
    atq = fields.Integer()
    produccion_oro = fields.Float()
    max_vida = fields.Float()


#    produccion_(otro recurso pa dar a las tropas) = fields.Float()