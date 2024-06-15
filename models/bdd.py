import base64
from random import randint

# Assurez-vous d'importer les classes Joueur et Armee depuis leurs modules respectifs
from models import Joueur, Armee  # Remplacez 'your_module' par le nom correct du module

class BDD:
  def __init__(self):
    self.tour = 0
    self.dict_joueur = {}
    self.dict_armee = {}
    self.ref_classe = {
        'S+': {'force_base': 125, 'force_alea_min': 15, 'force_alea_max': 20},
        'S': {'force_base': 120, 'force_alea_min': 14, 'force_alea_max': 20},
        'S-': {'force_base': 115, 'force_alea_min': 13, 'force_alea_max': 20},
        'A+': {'force_base': 110, 'force_alea_min': 12, 'force_alea_max': 20},
        'A': {'force_base': 110, 'force_alea_min': 11, 'force_alea_max': 20},
        'A-': {'force_base': 110, 'force_alea_min': 10, 'force_alea_max': 20},
        'B+': {'force_base': 110, 'force_alea_min': 7, 'force_alea_max': 15},
        'B': {'force_base': 110, 'force_alea_min': 6, 'force_alea_max': 15},
        'B-': {'force_base': 110, 'force_alea_min': 5, 'force_alea_max': 15},
        'C+': {'force_base': 50, 'force_alea_min': 3, 'force_alea_max': 10},
        'C': {'force_base': 50, 'force_alea_min': 2, 'force_alea_max': 10},
        'C-': {'force_base': 50, 'force_alea_min': 1, 'force_alea_max': 10},
    }

  def init(self, info_init, init_type):
      for key, value in info_init.items():
        if init_type == 'new':
          puissance = self.compute_puissance(classe = value.classe, tour=value.tour,
                                            nb_bonus = value.bonus, puissance_base = value.puissance_base)
        elif init_type == 'existing encode':
          puissance_encodee = value.puissance
          puissance_bytes = puissance_encodee.encode('utf-8')
          puissance_decodee = base64.b64decode(puissance_bytes)
          puissance = int(puissance_decodee.decode('utf-8'))
        elif init_type == 'existing':
          puissance = value.puissance
        new_joueur = Joueur(key, value.classe, puissance, nb_atout=3, state=(0,0,0), deploye = 0, armee = value.armee)
        self.dict_joueur[key] = new_joueur
        if value.armee not in self.dict_armee:
          self.dict_armee[value.armee] = Armee(value.armee)
        self.dict_armee[value.armee].add_joueur(new_joueur)


  def compute_puissance(self, classe, tour, nb_bonus, puissance_base=0):
    info = self.ref_classe.get(classe)
    force_base = info.get('force_base')
    puissance = 0
    taux_bonus = 1 + nb_bonus*0.02
    if puissance_base == 0:
      puissance_base_new = info.get('force_base') * taux_bonus
      puissance_random = randint(info.get('force_alea_min'), info.get('force_alea_max')) * taux_bonus * 5
      puissance += puissance_base_new + puissance_random
      for i in range(tour):
        puissance_random = randint(info.get('force_alea_min'), info.get('force_alea_max')) * taux_bonus * 5
        puissance += puissance_random
    else :
      puissance = puissance_base
      puissance_random = randint(info.get('force_alea_min'), info.get('force_alea_max')) * taux_bonus * 5
      puissance += puissance_random
    return puissance

  def instruction_gpt(self, all_instruct):
    for armee, instruct in all_instruct.items():
      for joueur, zone in instruct.items():
        bdd.dict_armee[armee].dict_joueur[joueur].deploy(zone)