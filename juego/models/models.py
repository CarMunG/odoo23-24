# -*- coding: utf-8 -*-

#  Proyecto Carlos Muñoz Gimeno

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

#  PRIMER TRIMESTRE

class jugador(models.Model):
    _name = 'juego.jugador'
    _description = 'El jugador'

    nombre = fields.Char()
    planetas = fields.One2many('juego.planetas', 'jugador')
    oro = fields.Integer(default=50)

    @api.model
    def actualizar_oro(self):  # Cron que recoge el Oro de los Edificios y se lo da al Jugador
        for p in self.planetas:
            for e in p.edificios:
                self.oro += e.produccion_oro

    @api.constrains('nombre')
    def _j_nombre_vacio(self):  # Restriccion para que no tenga el nombre vacio
        for n in self:
            if not n.nombre:
                raise ValidationError("El nombre no puede estar vacio")


class planetas(models.Model):
    _name = 'juego.planetas'
    _description = 'Uno de los planetas'

    nombre = fields.Char()
    jugador = fields.Many2one('juego.jugador')
    edificios = fields.One2many('juego.edificio', 'planeta')
    num_edificios = fields.Integer(compute='_get_cant_edif')

    @api.depends('edificios')
    def _get_cant_edif(self):  # Devuelve la cantidad de Edificios que tiene un Planeta para mostrarlos en su view
        for e in self:
            if e.edificios:
                e.num_edificios = len(e.edificios)
            else:
                e.num_edificios = 0

    @api.constrains('nombre')
    def _p_nombre_vacio(self):  # Restriccion para que no tenga el nombre vacio
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
    def create(self, values):  # Cuando se crea un nuevo edificio le quita 15 de oro al Jugador
        edificio_creado = super(edificio, self).create(values)
        jugador = edificio_creado.planeta.jugador
        if jugador:
            jugador.write({'oro': jugador.oro - 15})  # Cuesta 15 de Oro crear cada Edificio

        return edificio_creado

    @api.constrains('nivel')
    def _check_nivel_limit(self):  # Restriccion para que el nivel no supere el limite
        for e in self:
            if e.nivel > 99:  # Nivel 99 es el maximo
                raise ValidationError('El nivel del edificio no puede superar 99')

    @api.model
    def subir_nivel(self):  # Cron que sube el % de nivel de cada Edificio
        for e in self.search([('porcentaje_nivel', '<', 100)]):
            e.porcentaje_nivel += 1 / (e.nivel + 1)
            if e.porcentaje_nivel >= 100 & e.nivel < 99:
                e.porcentaje_nivel = 0
                e.nivel += 1
            elif e.porcentaje_nivel >= 100 & e.nivel == 99:
                e.porcentaje_nivel = 100  # se queda en 100% para dar a entender que es el nivel maximo

    @api.depends('tipo', 'nivel')  # Da estadisticas al Edificio segun el tipo
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
            else:  # Si no selecciona ningun tipo se vacian las estadisticas
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
    jugador_1 = fields.Many2one('juego.jugador')
    jugador_2 = fields.Many2one('juego.jugador')
    ganador = fields.Many2one('juego.jugador', string='Ganador', readonly=True)
    finalizada = fields.Boolean(default=False)

    @api.depends('fecha_inicio')
    def _get_fecha_final(self):  # Calcula la fecha final, restante y el % que a progresado la batalla
        for b in self:
            inicio = fields.Datetime.from_string(b.fecha_inicio)
            final = inicio + timedelta(hours=2)
            restante = final - datetime.now()
            tiempo_pasado = (datetime.now() - inicio).total_seconds() / 60
            b.fecha_final = fields.Datetime.to_string(final)
            b.fecha_restante = "{:02}:{:02}:{:02}".format(restante.seconds // 3600, (restante.seconds // 60) % 60,
                                                          restante.seconds % 60)
            b.fecha_progreso = (tiempo_pasado * 100) / (2 * 60)

    def calcular_ganador(self):  # Calcula el ganador dependiendo de la vida y ataque de los Edificios de los Jugadores
        edificios_jugador1 = self.jugador_1.planetas.mapped('edificios')
        edificios_jugador2 = self.jugador_2.planetas.mapped('edificios')

        fuerza_jugador1 = sum(edificio.atq + edificio.vida for edificio in edificios_jugador1)
        fuerza_jugador2 = sum(edificio.atq + edificio.vida for edificio in edificios_jugador2)

        if fuerza_jugador1 > fuerza_jugador2:
            self.ganador = self.jugador_1
        elif fuerza_jugador2 > fuerza_jugador1:
            self.ganador = self.jugador_2
        else:
            self.ganador = None

        self.ganador.write({'oro': self.ganador.oro + 350})  # El jugador que gana consigue 350 de oro

        for edificio_ganador in self.ganador.planetas.mapped('edificios'):  # Los edificios del ganador suben un 50%
            edificio_ganador.porcentaje_nivel += 50

    @api.depends('fecha_progreso')  # Cron que comprueba si llega a 100% para acabar la batalla
    def finalizar_batalla(self):
        for f in self:
            if not f.finalizada and f.fecha_progreso == 100:
                f.calcular_ganador()
                f.finalizada = True

    def forzar_finalizar_batalla(self):  # para llamarlo con un boton en la view para no tener que esperarse
        for f in self:
            if not f.finalizada:
                f.calcular_ganador()
                f.finalizada = True
            else:  # Salta un error si la Batalla ya ha sido finalizada
                raise ValidationError("La batalla ya ha sido finalizada")

#  SEGUNDO TRIMESTRE
    class wizard(models.TransientModel):  # Pensar de que hacerlo
        # Copiar los atributos de lo que sea, pero NO los One2many
        # Cambiar el nombre de los permisos en security cuando cambie el nombre y eso, tambien en views y vistas
        _name = 'juego.wizard'

        def crear_x(self):  # Cambiar el nombre de la funcion cuando eso y tambien cambiarla en vistas.xml
            self.env["juego.x"].create({
                "nombre variable": self.variable,  # Cambiar el nombre de a las cosas que va a crear
                "nombre variable 2": self.variable2
            })
