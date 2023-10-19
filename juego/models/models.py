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
    jugador = fields.Many2one('juego.jugador')
    edificios = fields.One2many('juego.edificio', 'planeta')


class edificio(models.Model):
    _name = 'juego.edificio'
    _description = 'Edificio'

    nombre = fields.Char(related='tipo.nombre')
    planeta = fields.Many2one('juego.planeta', ondelete='cascade')
    #   Pensar nombres que ponerles
    tipo = fields.Selection([('1', 'sad'), ('2', 'patata'), ('3', 'sdioa'), ('4', 'ewqe')])
    nivel = fields.Float(default=1)
    vida = fields.Integer()
    max_vida = fields.Integer()
    atq = fields.Integer()
    produccion_oro = fields.Integer()


@api_depends('tipo', 'nivel')
def _tipos(self):
    for e in self:
#       Poner estadisticas distintas dependiendo del tipo
        if e.tipo == '1':
            e.max_vida = e.max_vida * (e.nivel / 3)
            e.vida = e.max_vida
            e.atq = e.atq * (e.nivel / 5)
            e.produccion_oro = e.produccion_oro * ()
        elif e.tipo == '2':
            e.max_vida = e.max_vida * (e.nivel / 3)
            e.vida = e.max_vida
            e.atq = e.atq * (e.nivel / 5)
            e.produccion_oro = e.produccion_oro * ()
        elif e.tipo == '3':
            e.max_vida = e.max_vida * (e.nivel / 3)
            e.vida = e.max_vida
            e.atq = e.atq * (e.nivel / 5)
            e.produccion_oro = e.produccion_oro * ()
        elif e.tipo == '4':
            e.max_vida = e.max_vida * (e.nivel / 3)
            e.vida = e.max_vida
            e.atq = e.atq * (e.nivel / 5)
            e.produccion_oro = e.produccion_oro * ()
