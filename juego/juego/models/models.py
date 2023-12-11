# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class jugador(models.Model):
    _name = 'juego.jugador'
    _description = 'El jugador'

    nombre = fields.Char()
    planetas = fields.One2many('juego.planetas', 'jugador')
    oro = fields.Integer(default=50)

    @api.constrains('nombre')
    def _jnombre_vacio(self):
        for n in self:
            if not n.nombre:
                raise ValidationError("El nombre no puede estar vacio")

    @api.model
    def actualizar_oro(self):
        for j in self:
            oro_generado = 0
            for p in j.planetas:
                for e in p.edificios:
                    oro_generado += e.produccion_oro

            j.write({'oro': j.oro + oro_generado})


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
            if e.edificios:
                e.num_edificios = len(e.edificios)
            else:
                e.num_edificios = 0

    @api.constrains('nombre')
    def _pnombre_vacio(self):
        for n in self:
            if not n.nombre:
                raise ValidationError("El nombre del planeta no puede estar vacio")


class edificio(models.Model):
    _name = 'juego.edificio'
    _description = 'Edificio'

    planeta = fields.Many2one('juego.planetas')
    tipo = fields.Selection([('1', 'soldado generico'), ('2', 'mina de oro'), ('3', 'soplador de aire'),
                             ('4', 'amongus'), ('5', 'torre laser'), ('6', 'torre de comando'), ('7', 'alfredo'),
                             ('8', 'destructor 3000')])
    nivel = fields.Integer(default=1)
    vida = fields.Float(compute='_tipos')
    max_vida = fields.Float(compute='_tipos')
    atq = fields.Float(compute='_tipos')
    produccion_oro = fields.Float(compute='_tipos')
    porcentaje_nivel = fields.Float(default=0)

    @api.model
    def create(self, values):
        edificioCreado = super(edificio, self).create(values)
        jugador = edificioCreado.planeta.jugador
        if jugador:
            jugador.write({'oro': jugador.oro - 15})

        return edificioCreado

    @api.constrains('nivel')
    def _check_nivel_limit(self):  # Nivel 99 es el maximo
        for e in self:
            if e.nivel > 99:
                raise ValidationError('El nivel del edificio no puede superar 99')

    @api.model
    def subir_nivel(self):
        for e in self.search([('porcentaje_nivel', '<', 100)]):
            e.porcentaje_nivel += 1 / (e.nivel + 1)
            if e.porcentaje_nivel >= 100 & e.nivel < 99:
                e.porcentaje_nivel = 0
                e.nivel += 1
            elif e.porcentaje_nivel >= 100 & e.nivel == 99:
                e.porcentaje_nivel = 100  # se queda en 100% para dar a entender que es el nivel maximo

    @api.depends('tipo', 'nivel')  # estadisticas segun el tipo
    def _tipos(self):
        for e in self:
            if e.tipo and e.nivel:
                if e.tipo == '1':
                    e.max_vida = e.nivel * 100
                    e.vida = e.max_vida
                    e.atq = e.nivel * 10
                    e.produccion_oro = 0
                elif e.tipo == '2':
                    e.max_vida = e.nivel * 120
                    e.vida = e.max_vida
                    e.atq = 0
                    e.produccion_oro = e.nivel * 20
                elif e.tipo == '3':
                    e.max_vida = e.nivel * 120
                    e.vida = e.max_vida
                    e.atq = e.nivel * 30
                    e.produccion_oro = 0
                elif e.tipo == '4':
                    e.max_vida = e.nivel * 80
                    e.vida = e.max_vida
                    e.atq = e.nivel * 20
                    e.produccion_oro = 0
                elif e.tipo == '5':
                    e.max_vida = e.nivel * 150
                    e.vida = e.max_vida
                    e.atq = e.nivel * 15
                    e.produccion_oro = e.nivel
                elif e.tipo == '6':
                    e.max_vida = e.nivel * 80
                    e.vida = e.max_vida
                    e.atq = e.nivel * 5
                    e.produccion_oro = e.nivel * 0.5
                elif e.tipo == '7':
                    e.max_vida = e.nivel * 90
                    e.vida = e.max_vida
                    e.atq = e.nivel * 30
                    e.produccion_oro = e.nivel * 0.25
                elif e.tipo == '8':
                    e.max_vida = e.nivel * 400
                    e.vida = e.max_vida
                    e.atq = e.nivel * 40
                    e.produccion_oro = 0
            else:
                e.max_vida = None
                e.vida = None
                e.atq = None
                e.produccion_oro = None


class batalla(models.Model):
    _name = 'juego.batalla'
    _description = 'Una batalla'

    nombre = fields.Char()
    fecha_inicio = fields.Datetime(default=lambda self: fields.Datetime.now())
    fecha_final = fields.Datetime(compute='_get_fecha_final')
    fecha_restante = fields.Char(compute='_get_fecha_final')
    fecha_progreso = fields.Float(compute='_get_fecha_final')
    jugador1 = fields.Many2one('juego.jugador', string='Jugador 1')
    jugador2 = fields.Many2one('juego.jugador', string='Jugador 2')
    ganador = fields.Many2one('juego.jugador', string='Ganador', readonly=True)
    finalizada = fields.Boolean(default=False)

    @api.depends('fecha_inicio')
    def _get_fecha_final(self):
        for b in self:
            inicio = fields.Datetime.from_string(b.fecha_inicio)
            final = inicio + timedelta(hours=2)
            restante = final - datetime.now()
            tiempo_pasado = (datetime.now() - inicio).total_seconds() / 60
            b.fecha_final = fields.Datetime.to_string(final)
            b.fecha_restante = "{:02}:{:02}:{:02}".format(restante.seconds // 3600, (restante.seconds // 60) % 60,
                                                          restante.seconds % 60)
            b.fecha_progreso = (tiempo_pasado * 100) / (2 * 60)

    def _calcular_ganador(self):
        edificios_jugador1 = self.jugador1.planetas.mapped('edificios')
        edificios_jugador2 = self.jugador2.planetas.mapped('edificios')

        fuerza_jugador1 = sum(edificio.atq + edificio.vida for edificio in edificios_jugador1)
        fuerza_jugador2 = sum(edificio.atq + edificio.vida for edificio in edificios_jugador2)

        if fuerza_jugador1 > fuerza_jugador2:
            self.ganador = self.jugador1
        elif fuerza_jugador2 > fuerza_jugador1:
            self.ganador = self.jugador2
        else:
            self.ganador = None

    @api.depends('fecha_progreso')
    def finalizar_batalla(self):
        for f in self:
            if not f.finalizada and f.fecha_progreso == 100:
                f.calcular_ganador()
                f.finalizada = True

    def forzar_finalizar_batalla(self):  # para llamarlo con un boton en la interfaz para no tener que esperarse
        for f in self:
            if not f.finalizada:
                f.calcular_ganador()
                f.finalizada = True