# -*- coding: utf-8 -*-

# Cada vez que se crea una clase añadirlo con permisos a security
# si creo un nuevo archivo ponerlo en el init
# todas las clases ponerlas en el views.xml
# poner cosas de Demo en demo.xml
# Crear botones y cosas en views.xml
# Si algo da error y no sabes que es, entra sin update y desinstala->instala el modulo
# Hacer un Crono Job pa que se actualicen las weas cada minuto

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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
    vida = fields.Integer(compute='_tipos')
    max_vida = fields.Integer(compute='_tipos')
    atq = fields.Integer(compute='_tipos')
    produccion_oro = fields.Integer(compute='_tipos')

    @api.depends('tipo', 'nivel')
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
    fecha_inicio = fields.Datetime(default=lambda self: fields.Datetime.now())
    fecha_final = fields.Datetime(compute='_get_fecha_final')
    fecha_restante = fields.Char(compute='_get_fecha_final')
    fecha_progreso = fields.Float(compute='_get_fecha_final')

    @api.depends('fecha_inicio')
    def _get_fecha_final(self):
        for b in self:
            inicio = fields.Datetime.from_string(b.fecha_inicio)
            final = inicio + timedelta(hours=2)
            restante = relativedelta(final, datetime.now()).total_seconds() / 60
            tiempo_pasado = (datetime.now()-inicio).total_seconds()
            b.fecha_final = fields.Datetime.to_string(final)
            b.fecha_restante = str(restante.hours) + ":" + str(restante.minutes) + ":" + str(restante.seconds)
            b.fecha_progreso = (tiempo_pasado*100)/(b.fecha_final*60)
