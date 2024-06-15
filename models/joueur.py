import base64
from math import floor
from random import randint

class Joueur:
  def __init__(self, name, classe, puissance, nb_atout=3, state=(0,0,0), deploye = 0, armee = 0):
    self.name = name
    self.classe = classe
    self.puissance = puissance
    self.puissance_encodee = self.encoder_puissance(puissance)
    self.puissance_public = 0
    self.state = state
    self.legere_blessure, self.blessure, self.KO = state
    self.nb_atout = nb_atout
    self.de = 0
    self.score = 0
    self.num_manche_atout = 0
    self.deploye = deploye
    self.armee = armee
    self.priority = 0

  def update_state(self, resultat):
    self.add_legere_blessure, self.add_blessure, self.add_KO = resultat
    self.legere_blessure += self.add_legere_blessure
    if self.legere_blessure > 1:
      self.legere_blessure = 0
      self.blessure += 1
    self.blessure += self.add_blessure
    if self.blessure > 1:
      self.KO = 1
    self.KO += self.add_KO
    self.state = (self.legere_blessure, self.blessure, self.KO)
    return self.state

  def attack(self, atout=False, puissance_adverse=0, num_manche=0):
    de = randint(1, 20)
    bonus_atout = 0
    bonus_superiorite = 0
    if atout:
      self.nb_atout += -1
      self.num_manche_atout = num_manche
      bonus_atout = 3
      if (self.puissance - puissance_adverse) > 0:
        bonus_superiorite = floor((self.puissance - puissance_adverse)/puissance_adverse/0.05)
      de_final = de + bonus_atout + bonus_superiorite
      if de_final > de:
        de = de_final
    score = self.puissance * (50 + de * 5) / 100
    self.de = de
    self.score = score

  def deploy(self, terrain):
    self.deploye = terrain

  def affect_armee(self, armee):
    self.armee = armee

  def encoder_puissance(self, puissance):
    # Convertit la puissance en bytes, encode en base64, puis convertit en string pour l'affichage
    puissance_bytes = str(puissance).encode('utf-8')
    puissance_encodee = base64.b64encode(puissance_bytes)
    return puissance_encodee.decode('utf-8')

  def display_state(self, details=0):
    text_zone = "disponible" if self.deploye == 0 else f" zone : {self.deploye}"
    if details == "base":
      if self.KO == 1:
        print(f"{self.name} : KO")
      else :
        print(f"{self.name} ({self.puissance_encodee}): {text_zone}")
    if details == "transparent":
      if self.KO == 1:
        print(f"{self.name} : KO")
      else :
        print(f"{self.name} ({self.puissance}): {text_zone}")
    if details == "public":
      if self.KO == 1:
        print(f"{self.name} : KO")
      else :
        text_puissance_public = f"> {self.puissance_public}"
        print(f"{self.name} ({text_puissance_public}): {text_zone}")