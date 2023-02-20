# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

import random

#Lunes en clase restringir cantidad de edificios de CADA tipo a 10 para no tener infinitos y la producción sea realista.

class player(models.Model):
    _name = 'res.partner'
    _description = 'Player'
    _inherit = 'res.partner'

    image = fields.Image(max_width = 200, max_height = 200)
    name = fields.Char(string = "Name", required = True)
    password = fields.Char()

    is_player = fields.Boolean(default = False)

    location = fields.Integer(default = random.randint(1,999))

    mana = fields.Float(default = 0)
    gold = fields.Float(default = 100)
    evolver = fields.Float(default = 0)
    
    mana_production = fields.Integer(compute='_get_total_productions')
    gold_production = fields.Integer(compute='_get_total_productions')
    evolver_production = fields.Integer(compute='_get_total_productions')


    buildings = fields.One2many('white_clover.building', 'player')
    available_buildings = fields.Many2many('white_clover.building_type', compute="get_available_buildings")
    buildings_qty = fields.Integer(compute="get_buildings_qty")

    
    grimoires = fields.One2many('white_clover.grimoire', 'player')
    upgrade_grimoires = fields.Many2many('white_clover.grimoire',compute ="get_grimoires")

    grimoires_qty = fields.Integer(compute="get_grimoires_qty")
    
    @api.depends('buildings')
    def _get_total_productions(self):
        for c in self:
            c.mana_production = 0
            c.gold_production = 0
            c.evolver_production = 0
            if len(c.buildings) > 0:
                #print("ací arriba 37")
                c.mana_production = sum(c.buildings.mapped('mana_production'))
                #print("ací arriba 39")
                c.gold_production = sum(c.buildings.mapped('gold_production'))
                #print("ací arriba 41")
                c.evolver_production = sum(c.buildings.mapped('evolver_production'))
                #print("mana   ",c.mana)

    @api.depends('grimoires')
    def get_grimoires(self):
        for g in self:
            g.upgrade_grimoires = self.env['white_clover.grimoire'].search([('player','=',g.id)])

    @api.depends('grimoires')
    def get_grimoires_qty(self):
        for p in self:
            p.grimoires_qty = len(p.grimoires)
            
    @api.depends('buildings')
    def get_buildings_qty(self):
        for p in self:
            p.buildings_qty = len(p.buildings)

    @api.depends('gold')
    def get_available_buildings(self):
        for c in self:
            c.available_buildings = self.env['white_clover.building_type'].search([('gold_build_cost', '<=', c.gold)])
            

    @api.constrains('gold')
    def _check_gold(self):
        for record in self:
            if record.gold > 1000000:
                raise ValidationError("You have too much gold %s" % record.gold)
            
    @api.constrains('mana')
    def _check_mana(self):
        for record in self:
            if record.mana > 50000:
                raise ValidationError("You have too much mana %s" % record.mana)
            
    @api.constrains('evolver')
    def _check_evolver(self):
        for record in self:
            if record.evolver > 50000:
                raise ValidationError("You have too much evolver %s" % record.evolver)
            
            
            
    @api.model
    def produce(self):  # ORM CRON
        self.search([]).produce_player_resources()

    def produce_player_resources(self):
        for p in self:
            mana = p.mana + p.mana_production
            gold = p.gold + p.gold_production
            evolver = p.evolver + p.evolver_production

            p.write({
                "mana": mana,
                "gold": gold,
                "evolver": evolver
            })
            
    
    def distance(self,other_player):
        distance = 0
        if len(self) > 0 and len(other_player) > 0:
            distance = abs(self.location - other_player.location)
        return distance
            

    def create_grimoire(self):
        for p in self:
            print("hola")
            grimoiresList = self.env["white_clover.grimoire_type"].search([]).ids

            gid = random.choice(grimoiresList)


            if self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).name == "White grimoire":
                image = self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).image
                hp = random.betavariate(5,1.3)*15
                attack = random.betavariate(1.5,1.5)*10
                defense = random.betavariate(1.5,1.5)*10
                speed = random.betavariate(1.5,1.5)*10

            if self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).name == "Red grimoire":
                image = self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).image
                attack = random.betavariate(5,1.3)*20
                hp = random.betavariate(1.5,1.5)*10
                defense = random.betavariate(1.5,1.5)*10
                speed = random.betavariate(1.5,1.5)*10

            if self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).name == "Blue grimoire":
                image = self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).image
                defense = random.betavariate(5,1.3)*20
                attack = random.betavariate(1.5,1.5)*10
                hp = random.betavariate(1.5,1.5)*10
                speed = random.betavariate(1.5,1.5)*10

            if self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).name == "Green grimoire":
                image = self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).image
                speed = random.betavariate(5,1.3)*20
                attack = random.betavariate(1.5,1.5)*10
                defense = random.betavariate(1.5,1.5)*10
                hp = random.betavariate(1.5,1.5)*10

            name = self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).name 
            if p.gold >= 10000 and p.mana >= 8000 and p.evolver >= 5000 :
                self.env['white_clover.grimoire'].create({
                        "name": name,
                        "grimoire_type": self.env["white_clover.grimoire_type"].search([('id', '=', gid)], limit=1).id,
                        "player": p.id,
                        "hp": hp,
                        "image": image,
                        "defense": defense,
                        "attack": attack,
                        "speed":speed
                })
                p.gold -= 10000
                p.mana -= 8000
                p.evolver -= 5000


class building(models.Model):
    _name = 'white_clover.building'
    _description = 'Building'

    name = fields.Char(related = 'building_type.name')
    image = fields.Image(related = 'building_type.image')
    level = fields.Integer(default = 1)
    required_gold_levelup = fields.Float(compute='_get_required_gold_levelup')

    player = fields.Many2one('res.partner',ondelete="cascade")

    building_type = fields.Many2one('white_clover.building_type')
    
    mana_production = fields.Float(compute='_get_productions')
    gold_production = fields.Float(compute='_get_productions')
    evolver_production = fields.Float(compute='_get_productions')
    
    gold_build_cost = fields.Float(related = 'building_type.gold_build_cost')
    mana_build_cost = fields.Float(related = 'building_type.mana_build_cost')
    evolver_build_cost = fields.Float(related = 'building_type.evolver_build_cost')
    
    @api.constrains('level')
    def check_level(self):
        for record in self:
            if record.level > 10:
                raise ValidationError("Level can't be more than 10 %s" % record.level)
   
                 
    def _get_productions(self):
     for b in self:
        b.mana_production = 0
        b.gold_production = 0
        b.evolver_production = 0
         
        level = b.level

        mana_production = b.building_type.mana_production * level * 10
        gold_production = b.building_type.gold_production * level * 10
        evolver_production = b.building_type.evolver_production * level * 10




        if mana_production + b.player.mana >= 0 and gold_production + b.player.gold >= 0 and evolver_production + b.player.evolver >= 0:
            b.mana_production = mana_production
            b.gold_production = gold_production
            b.evolver_production = evolver_production      
    
        else:
            b.mana_production = 0
            b.gold_production = 0
            b.evolver_production = 0        


    
    
    def _get_required_gold_levelup(self):
        for c in self:
            c.required_gold_levelup = 4 ** c.level
    '''   SE PUEDE HACER DE LAS DOS FORMAS, pero hacemos la de levelupgrade
    def update_level(self):
        for b in self:
            if b.player.gold >= (b.gold_build_cost ** b.level):
                b.level += 1
                b.player.gold -= (b.gold_build_cost ** b.level)
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'You need '+str(b.gold_build_cost ** b.level)+' gold',
                        'type': 'danger',  # types: success,warning,danger,info
                        'sticky': False
                    }
                }
    '''

    def levelupgrade_building(self):
        for c in self:
            required_gold = c.required_gold_levelup  # Smartbutton
            available_gold = c.player.gold
            if (required_gold <= available_gold):
                c.level += 1
                c.player.gold = c.player.gold - required_gold
            else:
                raise ValidationError("You don't have enough gold")
            



class building_type(models.Model):
    _name = 'white_clover.building_type'

    name = fields.Char()
    buildings = fields.One2many('white_clover.building', 'building_type')
    image = fields.Image(max_width = 200, max_height = 200)
    
    
    mana_production = fields.Float(default = 0)
    gold_production = fields.Float(default = 0)
    evolver_production = fields.Float(default = 0)

    gold_build_cost = fields.Float(default = 100)
    mana_build_cost = fields.Float(default = 250)
    evolver_build_cost = fields.Float(default = 500)

    def create_building(self):
        for b in self:
            player = self.env['res.partner'].browse(self.env.context['ctx_player'])[0]
            if player.gold >= b.gold_build_cost:
                self.env['white_clover.building'].create({
                    "player": player.id,
                    "building_type": b.id
                })
                player.gold -= b.gold_build_cost
            
    
            
            

class grimoire(models.Model):
    _name = 'white_clover.grimoire'
    _description = 'Grimoire'

    name = fields.Char()

    image = fields.Image()
    
    level = fields.Integer(readonly = True)
    #level = fields.Integer(compute = "get_lvl")
    xp = fields.Float()
    
    def getGrimoireType(self):
        grimoiresList = self.env["white_clover.grimoire_type"].search([]).ids
        return random.choice(grimoiresList)


    grimoire_type = fields.Many2one('white_clover.grimoire_type')
    grimoire_type_write = fields.Many2one('white_clover.grimoire_type')


    player = fields.Many2one('res.partner')
    required_mana_levelup = fields.Float(compute='_get_required_mana_levelup')


    hp = fields.Integer(readonly = True)
    attack = fields.Integer(readonly = True)
    defense = fields.Integer(readonly = True)
    speed = fields.Integer(readonly = True)

    

    @api.onchange('grimoire_type')
    def _onchange_stats(self):
        if self.grimoire_type.name == "White grimoire":
            image = self.grimoire_type.image
            hp = random.betavariate(5,1.3)*15
            attack = random.betavariate(1.5,1.5)*10
            defense = random.betavariate(1.5,1.5)*10
            speed = random.betavariate(1.5,1.5)*10
            self.write({
                    "grimoire_type_write":self.grimoire_type.id,
                    "image":image,
                    "hp":hp,
                    "attack":attack,
                    "defense":defense,
                    "speed": speed})

        if self.grimoire_type.name == "Red grimoire":
            image = self.grimoire_type.image
            attack = random.betavariate(5,1.3)*20
            hp = random.betavariate(1.5,1.5)*10
            defense = random.betavariate(1.5,1.5)*10
            speed = random.betavariate(1.5,1.5)*10
            self.write({
                    "grimoire_type_write":self.grimoire_type.id,
                    "image":image,
                    "hp":hp,
                    "attack":attack,
                    "defense":defense,
                    "speed": speed})

        if self.grimoire_type.name == "Blue grimoire":
            image = self.grimoire_type.image
            defense = random.betavariate(5,1.3)*20
            attack = random.betavariate(1.5,1.5)*10
            hp = random.betavariate(1.5,1.5)*10
            speed = random.betavariate(1.5,1.5)*10
            self.write({
                    "grimoire_type_write":self.grimoire_type.id,
                    "image":image,
                    "hp":hp,
                    "attack":attack,
                    "defense":defense,
                    "speed": speed})

        if self.grimoire_type.name == "Green grimoire":
            image = self.grimoire_type.image
            speed = random.betavariate(5,1.3)*20
            attack = random.betavariate(1.5,1.5)*10
            defense = random.betavariate(1.5,1.5)*10
            hp = random.betavariate(1.5,1.5)*10
            self.write({
                    "grimoire_type_write":self.grimoire_type.id,
                    "image":image,
                    "hp":hp,
                    "attack":attack,
                    "defense":defense,
                    "speed": speed})
       #hacer que si speed de player1 duplica a la de player2 ataca 2 veces 
       
       
            
        


    #check_xp = fields.Integer()
    #check_lvl = fields.Integer(compute="check_level")
    
    @api.constrains('level')
    def _check_level(self):
        for record in self:
            if record.level > 100:
                raise ValidationError("You cant have more than 100 levels %s" % record.level)
            
        
    
    
    def _get_required_mana_levelup(self):
        for c in self:
            c.required_mana_levelup = 50 * c.level

    def levelupgrade_grimoire(self):
        for c in self:
            required_mana = c.required_mana_levelup  # Smartbutton
            available_mana = c.player.mana
            if (required_mana <= available_mana):
                c.level += 1
                if c.grimoire_type.name == "White grimoire":
                    c.hp += 2
                    c.attack += 1
                    c.defense += 1
                    c.speed  += 1
                if c.grimoire_type.name == "Red grimoire":
                    c.hp += 1
                    c.attack += 2
                    c.defense += 1
                    c.speed  += 1
                if c.grimoire_type.name == "Blue grimoire":
                    c.hp += 1
                    c.attack += 1
                    c.defense += 2
                    c.speed  += 1
                if c.grimoire_type.name == "Green grimoire":
                    c.hp += 1
                    c.attack += 1
                    c.defense += 1
                    c.speed  += 2
                    

                c.player.mana = c.player.mana - required_mana
            else:
                raise ValidationError("You don't have enough mana %s" % required_mana)       
       
    #igual hay que tocar este constrains porque el xp puede pasarse un poco y dar mas de nivel 100
    #@api.constrains('level')
    #def check_level(self):
     #   for b in self:
      #      if b.level > 100:
       #         raise ValidationError("Level cant be more than 100 levels")

    #hacer que los grimorios tengan tipos y cada grimorio hechizos que se pueden sustituir, un modelo nuevo que sea hechizo, hacer varios grimorios de demo 
    
    def invoke_grimoire(self):
        for b in self:
            player = self.env['res.partner'].browse(self.env.context['ctx_player'])[0]
            if player.gold >= 10000 and player.mana >= 8000 and player.evolver >= 5000 :
                self.env['white_clover.grimoire'].create({
                    "player": b.player.id,
                    "grimoire_type": b.id
                })
                player.gold -= 10000
                player.mana -= 8000
                player.evolver -= 5000
    
    
class grimoire_type(models.Model):
    _name = 'white_clover.grimoire_type'
    
    #name = fields.Selection([('1','Red Grimoire'),('2','Blue Grimoire'),('3','Green Grimoire'),('4','White Grimoire')],required =True)
    name = fields.Char(required=True)
    image = fields.Image(max_width = 200, max_height = 200)
    grimoires = fields.One2many('white_clover.grimoire', 'grimoire_type')

    hp = fields.Integer()
    attack = fields.Integer()
    defense = fields.Integer()
    speed = fields.Integer()


class battle(models.Model):
    _name = 'white_clover.battle'
    _description = 'Battles'
    
    name = fields.Char()
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_time')
    time = fields.Float(compute='_get_time')
    distance = fields.Float(compute='_get_time')
    progress = fields.Float()
    state = fields.Selection([('1', 'Preparation'), ('2', 'Send'), ('3', 'Finished')], default='1')
    player1 = fields.Many2one('res.partner',required = True)
    player2 = fields.Many2one('res.partner',required = True)
    grimoire_list = fields.One2many('white_clover.battle_grimoire_rel', 'battle_id')

    #esto lo haremos en un futuro al hacer la batalla
    #available_grimoires = fields.Many2many('white_clover.grimoire', compute = "get_available_grimoires")
    #total_power = fields.Float()  # ORM Mapped
    #winner = fields.Many2one()
    draft = fields.Boolean()
    
    
    @api.depends('grimoire_list', 'player1', 'player2')
    def _get_time(self):
        for b in self:
            b.time = 0
            b.distance = 0
            b.date_end = fields.Datetime.now()
            if len(b.player1) > 0 and len(b.player2) > 0 and len(b.grimoire_list) > 0 and len(
                    b.grimoire_list.grimoire_id) > 0:
                b.distance = b.player1.distance(b.player2)
                min_speed = b.grimoire_list.grimoire_id.sorted(lambda s: s.speed).mapped('speed')[0]
                b.time = b.distance / min_speed
                b.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(b.date_start) + timedelta(minutes=b.time))


    @api.onchange('player1')
    def onchange_player1(self):
        print(self)
        if len(self.player1) > 0:
            self.name = self.player1.name
            return {
                'domain': {               
                    'player2': [('id', '!=', self.player1.id)],
                }
            }


    @api.onchange('player2')
    def onchange_player2(self):
        print(self)
        if len(self.player2) > 0:
            self.name = self.player2.name
            return {
                'domain': {
                    'player1': [('id', '!=', self.player2.id)],
                }
            }



    def _get_grimoire_available(self):
        print(self)
        for b in self:
            b.grimoire_available = b.player1.grimoire.ids
            
            
    def launch_battle(self):
        print("launch")

    def execute_battle(self):
        print("execute")

    def back(self):
        print("back")

    def simulate_battle(self):
        print("simulate")

'''
    def launch_battle(self):
        print(self)
        for b in self:
            if len(b.heart1) == 1 and len(b.heart2) == 1 and len(b.cretures_list) > 0 and b.state == '1':

                b.date_start = fields.Datetime.now()
                b.progress = 0
                for s in b.creatures1_list:
                    creatures_available = \
                        b.creatures1_available.filtered(lambda s_a: s_a.creatures_id.id == s.creatures_id.id)[0]
                    creatures_available.qty -= s.qty
                b.state = '2'

    def back(self):
        print(self)
        for b in self:
            if b.state == '2':
                b.state = '1'
'''

class battle_grimoire_rel(models.Model):
    _name = 'white_clover.battle_grimoire_rel'
    _description = 'battle_grimoire_rel'

    name = fields.Char(related="grimoires_id.name")
    grimoires_id = fields.Many2one('white_clover.grimoire')
    battle_id = fields.Many2one('white_clover.battle')
    qty = fields.Integer()


class building_wizard(models.TransientModel):
    _name='white_clover.building_wizard'
    _description='Wizard pequeño para edificio'
    
    def get_default_building(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))
    
    player = fields.Many2one('res.partner', default = get_default_building, required = True)
    building_type = fields.Many2one('white_clover.building_type')
    
    def create_building_wizard(self):
        self.ensure_one()
        if self.player.gold >= self.building_type.gold_build_cost:
            self.env['white_clover.building'].create({
                "player":self.player.id,
                "building_type":self.building_type.id
            })
        self.player.gold -= 50
        
        
        
class player_wizard(models.TransientModel):
    _name='white_clover.player_wizard'
    _description='Wizard grande para players'
    
    image = fields.Image(max_width = 200, max_height = 200)
    name = fields.Char(string = "Name", required = True)
    password = fields.Char()
    state = fields.Selection([('1','Player'),('2','Grimoire'),('3','Create')],default='1')
    grimoires = fields.Many2many('white_clover.grimoire', 'player')
    
    
    def next(self):
        if self.state == '1':
            self.state = '2'
        elif self.state == '2':
            self.state = '3'
 

        return {
            'type':'ir.actions.act_window',
            'res_model':self._name,
            'res_id':self.id,
            'view_mode':'form',
            'target':'new', 
        }

    def back(self):
        if self.state == '2':
            self.state = '1'
        elif self.state == '3':
            self.state = '2'


        return {
            'type':'ir.actions.act_window',
            'res_model':self._name,
            'res_id':self.id,
            'view_mode':'form',
            'target':'new', 
        }
    
    
    
    
    def create_player_wizard(self):
        for i in self:
            grimoiresArr = []
        
        
        p = i.env['res.partner'].create({'name':i.name,'password':i.password, 'image':i.image,'grimoires':i.grimoires,'is_player':True})


        return {
            'type':'ir.actions.act_window',
            'res_model':'res.partner',
            'res_id':p.id,
            'view_mode':'form',
            'target':'current',
        }