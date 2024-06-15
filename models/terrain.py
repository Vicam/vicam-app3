import math
from random import shuffle, randint, choice, random

# Assurez-vous que les classes Field et Duel ainsi que la base de données bdd sont correctement importées
# Ces importations dépendent de l'emplacement de ces classes dans votre projet
from models import Field, Duel

# Notez que "your_module" doit être remplacé par le nom du module où ces classes sont définies



class Terrain:
  def __init__(self, nb_fields, list_player, bdd):
    self.nb_fields = nb_fields
    self.list_player = list_player
    self.list_fields = self.get_fields()
    self.bdd = bdd


  def get_fields(self):
    list_fields = []
    nb_player = len(self.list_player)
    for id in range(self.nb_fields):
      field_per_front = self.nb_fields / nb_player
      part =  math.floor(id/field_per_front)
      left_player = self.list_player[part]
      right_player = self.list_player[0 if part+1 == nb_player else part+1]
      f = Field(id, left_player, right_player)
      list_fields.append(f)
      shuffle(list_fields)
    return list_fields

  def automatic_turn(self, print_level = 'all'):
    list_tour = []
    ready = True
    for f in self.list_fields:
      list_tour.append(f.turn)
    if min(list_tour) != max(list_tour):
        ready = False
    for f in self.list_fields:
      if ready == True:
        f.update_call()
        f.automatic_turn()
      else :
        if f.turn != max(list_tour):
          print(f"Field {f.id} n'a pas encore validé son tour")

  def manual_turn(self, id_field, vainqueur):
    self.list_field[id_field].manual_turn(vainqueur)

  def battle_turn(self):
    self.compute_priority()
    for f in self.list_fields:
      left_heros = []
      right_heros = []
      if f.statut == 'battle':
        print(f"----------------Zone {f.id}-----------------")
        left_army = int(f.left_player[1:])
        right_army = int(f.right_player[1:])
        if f.left_call == 'B':
          new_hero = self.get_priority_player(id_armee = left_army, filter = 'B')
          # print(f"ici left B : add {new_hero.name}")
          if new_hero is not None:
            left_heros.append(new_hero)
        if f.right_call == 'B':
          new_hero = self.get_priority_player(id_armee = right_army, filter = 'B')
          # print(f"ici right B : add {new_hero.name}")
          if new_hero is not None:
            right_heros.append(new_hero)
        if f.left_call in ['Team A+B', 'Team A']:
          new_hero_B = self.get_priority_player(id_armee = left_army, filter = 'B')
          new_hero_A = self.get_priority_player(id_armee = left_army, filter = 'A')
          if new_hero_B is not None:
            left_heros.append(new_hero_B)
          if new_hero_A is not None:
            left_heros.append(new_hero_A)
        if f.right_call in ['Team A+B', 'Team A']:
          new_hero_B = self.get_priority_player(id_armee = right_army, filter = 'B')
          new_hero_A = self.get_priority_player(id_armee = right_army, filter = 'A')
          if new_hero_B is not None:
            right_heros.append(new_hero_B)
          if new_hero_A is not None:
            right_heros.append(new_hero_A)
        if f.left_call == 'Team A':
            nb_hero = randint(0,3)
            for i in range(nb_hero):
              filter = 'A' if randint(0,1) == 1 else 'B'
              new_hero = self.get_priority_player(id_armee = left_army, filter = filter)
              if new_hero is not None:
                left_heros.append(new_hero)
        if f.right_call == 'Team A':
            nb_hero = randint(0,3)
            for i in range(nb_hero):
              filter = 'A' if randint(0,1) == 1 else 'B'
              new_hero = self.get_priority_player(id_armee = right_army, filter = filter)
              if new_hero is not None:
                right_heros.append(new_hero)
        # for hero in left_heros:
        #   print(f"left ({f.id}): {hero.name}")
        # for hero in right_heros:
        #   print(f"right ({f.id}): {hero.name}")
        while len(left_heros) > 0 and len(right_heros) > 0:
            left_hero, right_hero = choice(left_heros), choice(right_heros)
            print(f"============== ({left_hero.classe} vs {right_hero.classe}) ==============")
            print(f"""Héro {left_hero.name} armée {left_hero.armee} ({left_hero.classe})
                  vs Héro {right_hero.name} armée {right_hero.armee} ({right_hero.classe})""")
            d = Duel(left_hero, right_hero, details="public", max_manche=100)
            d.run_match()
            is_vainqueur_exist, vainqueur, looser = d.get_vainqueur()
            if looser in left_heros:
              left_heros.remove(looser)
            elif looser in right_heros:
              right_heros.remove(looser)
        # print("restant après combat.", "Nb héro left : ", len(left_heros), " Nb héro right : ", len(right_heros))
        if len(left_heros) > 0:
          f.manual_turn('left')
        elif len(right_heros) > 0:
          f.manual_turn('right')
        else :
          print('erreur ou match nul')
          f.manual_turn('nul')




  def compute_priority(self):
    shuffle(self.list_fields) # a testé
    for i, armee in self.bdd.dict_armee.items():
      taille = len(armee.dict_joueur)
      for i, joueur in armee.dict_joueur.items():
        joueur.priority = random()

  def get_priority_player(self, id_armee, filter):
    max_priority = 0
    joueur_selectionne = None
    armee = self.bdd.dict_armee[id_armee]
    for i, joueur in armee.dict_joueur.items():
      if (filter == 'B' and joueur.classe in ['C-', 'C', 'C+', 'B-', 'B', 'B+']) \
        or (filter == 'A' and joueur.classe in ['A-', 'A', 'A+', 'S-', 'S', 'S+']):
        if joueur.KO == 0:
          priority = joueur.priority
          if priority > max_priority:
            max_priority = priority
            joueur_selectionne = joueur
    # print("priority player  : ", joueur_selectionne.name if joueur_selectionne is not None else 'None',
    #       joueur_selectionne.armee if joueur_selectionne is not None else 'None', "filter : ", filter)
    if joueur_selectionne is not None:
      joueur_selectionne.priority = 0
    # print("après get ",self.bdd.dict_armee[id_armee].dict_joueur[joueur_selectionne.name].priority)
    return joueur_selectionne

  def print_status(self, print_level):
    for f in self.list_fields:
      f.print_status(print_level= print_level)