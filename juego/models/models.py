# -*- coding: utf-8 -*-

# Cada vez que se crea una clase añadirlo con permisos a security
# si creo un nuevo archivo ponerlo en el init
# todas las clases ponerlas en el views.xml
# poner cosas de Demo en demo.xml
# Crear botones y cosas en views.xml
# Si algo da error y no sabes que es, entra sin update y desinstala->instala el modulo

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class jugador(models.Model):
    _name = 'juego.jugador'
    _description = 'El jugador'

    nombre = fields.Char(required=True)
    planetas = fields.One2many('juego.planetas', 'jugador')

    @api.constrains('nombre')
    def _nombre_vacio(self):
        for n in self:
            if n.nombre == "":
                raise ValidationError("El nombre no puede estar vacio")


class planetas(models.Model):
    _name = 'juego.planetas'
    _description = 'Uno de los planetas'

    nombre = fields.Char()
    jugador = fields.Many2one('juego.jugador')
    edificios = fields.One2many('juego.edificio', 'planeta')
    num_edificios = fields.Integer(compute='_get_cant_edif')

    @api.depends('edificios')
    def _get_cant_edif(self):
        for e in self:
            e.num_edificios = len(e.edificios)


class edificio(models.Model):
    _name = 'juego.edificio'
    _description = 'Edificio'

    nombre = fields.Char()
    planeta = fields.Many2one('juego.planetas')
    tipo = fields.Selection([('1', 'soldado generico'), ('2', 'torre laser'), ('3', 'soplador de aire'),
                             ('4', 'amongus'), ('5', 'mina de oro'), ('6', 'torre de comando'), ('7', 'alfredo'),
                             ('8', 'destructor 3000')])
    nivel = fields.Float(default=1)
    vida = fields.Integer(compute='_tipos', store=True)
    max_vida = fields.Integer(compute='_tipos', store=True)
    atq = fields.Integer(compute='_tipos', store=True)
    produccion_oro = fields.Integer(compute='_tipos', store=True)

# La funcion deberia cambiar dinamicamente los objetos esos, pero no lo hace

    @api.model
    def create(self, values):
        record = super(edificio, self).create(values)
        record._tipos()
        return record

    @api.onchange('tipo', 'nivel')
    def _tipos(self):
        for e in self:
            if e.tipo and e.nivel:
                if e.tipo == '1':
                    e.max_vida = e.max_vida * (e.nivel / 3)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel / 5)
                    e.produccion_oro = e.produccion_oro * 0
                elif e.tipo == '2':
                    e.max_vida = e.max_vida * (e.nivel / 4)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel / 2)
                    e.produccion_oro = e.produccion_oro * 1
                elif e.tipo == '3':
                    e.max_vida = e.max_vida * (e.nivel / 2)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel / 6)
                    e.produccion_oro = e.produccion_oro * 0
                elif e.tipo == '4':
                    e.max_vida = e.max_vida * (e.nivel / 4)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel / 4)
                    e.produccion_oro = e.produccion_oro * 0
                elif e.tipo == '5':
                    e.max_vida = e.max_vida * (e.nivel / 3)
                    e.vida = e.max_vida
                    e.atq = e.atq * 0
                    e.produccion_oro = e.produccion_oro * e.nivel
                elif e.tipo == '6':
                    e.max_vida = e.max_vida * (e.nivel / 2)
                    e.vida = e.max_vida
                    e.atq = e.atq * 0
                    e.produccion_oro = e.produccion_oro * 0.5
                elif e.tipo == '7':
                    e.max_vida = e.max_vida * (e.nivel / 2)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel / 3)
                    e.produccion_oro = e.produccion_oro * 0.25
                elif e.tipo == '8':
                    e.max_vida = e.max_vida * (e.nivel * 4)
                    e.vida = e.max_vida
                    e.atq = e.atq * (e.nivel * 4)
                    e.produccion_oro = e.produccion_oro * 0
            else:
                e.max_vida = None
                e.vida = None
                e.atq = None
                e.produccion_oro = None


class batalla(models.Model):
    _name = 'juego.batalla'
    _description = 'Batalla'

    nombre = fields.Char()
    fecha_inicio = fields.Datetime()
    fecha_final = fields.Datetime()
