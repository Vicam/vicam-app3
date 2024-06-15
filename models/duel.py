import base64
from math import floor
from random import randint

# Assurez-vous que les classes Joueur sont importées depuis leurs modules respectifs
from models import Joueur  # Remplacez 'your_module' par le nom correct du module


class Duel:
  def __init__(self, joueur1, joueur2, details="base", max_manche=100):
    self.num_manche = 1
    self.max_manche = max_manche
    self.joueur1 = joueur1
    self.joueur2 = joueur2
    self.end = False
    self.details = details

  def confrontation_not_null(self, score1, score2):
    return abs(score1 - score2)/min(score1, score2) >= 0.1

  def get_vainqueur(self):
    self.joueur2.score
    is_vainqueur_exist = self.confrontation_not_null(self.joueur1.score, self.joueur2.score)
    if self.joueur1.score > self.joueur2.score:
      vainqueur, looser = self.joueur1, self.joueur2
    else :
      vainqueur, looser = self.joueur2, self.joueur1
    return is_vainqueur_exist, vainqueur, looser

  def continue_manche(self):
    is_vainqueur_exist, vainqueur, looser = self.get_vainqueur()
    if not(is_vainqueur_exist):
      return False
    else :
      if looser.nb_atout > 0 and looser.num_manche_atout < self.num_manche:
        return True
      else :
        return False

  def run_resultat(self):
      is_vainqueur_exist, vainqueur, looser = self.get_vainqueur()
      difference = vainqueur.score - looser.score
      if difference / looser.score > 1.0:
          resultat = (0,0,1)
          resultat_str = "KO"
      elif difference / looser.score > 0.5:
          resultat = (0,1,0)
          resultat_str = "Blessé"
      elif difference / looser.score > 0.1:
          resultat = (1,0,0)
          resultat_str = "Légèrement blessé"
      else:
          resultat = (0,0,0)
          resultat_str = "Match nul"
      looser.update_state(resultat)
      vainqueur_atout = 'atout' if vainqueur.num_manche_atout == self.num_manche else ''
      looser_atout = 'atout' if looser.num_manche_atout == self.num_manche else ''
      resultat_sentence = ""
      if self.details == "transparent":
        resultat_sentence = "Manche {} : {} a {} {} ({} ({}, {})vs {} ({}, {}))".format(self.num_manche, vainqueur.name, resultat_str, looser.name,
                                    vainqueur.score, vainqueur.de, vainqueur_atout, looser.score, looser.de, looser_atout)
      if self.details == "base":
        resultat_sentence = "Manche {} : {} a {} {} ({} ({}, {})vs {} ({}, {}))".format(self.num_manche, vainqueur.name, resultat_str, looser.name,
                                    self.encoder_puissance(vainqueur.score), vainqueur.de, vainqueur_atout, self.encoder_puissance(looser.score), looser.de, looser_atout)
      if self.details == "public":
        resultat_sentence = "Manche {} : {} a {} {} ({} vs {})".format(self.num_manche, vainqueur.name, resultat_str, looser.name,
                                    vainqueur_atout, looser_atout)
      return resultat_sentence

  def resultat_duel(self):
    if self.joueur1.KO == 1:
      resultat_sentence_match = "{} a gagné (état : {}, {} atouts restants ({} manche)".format(
          self.joueur2.name, self.joueur2.state, self.joueur2.nb_atout, self.num_manche)
      self.joueur2.puissance_public = self.joueur1.puissance
    elif self.joueur2.KO == 1:
      resultat_sentence_match = "{} a gagné (état : {}, {} atouts restants) ({} manche)".format(
          self.joueur1.name, self.joueur1.state, self.joueur1.nb_atout, self.num_manche)
      self.joueur1.puissance_public = self.joueur2.puissance
    else:
      resultat_sentence_match_1 = "{} : {} ({} atouts restants)".format(self.joueur1.name, self.joueur1.state, self.joueur1.nb_atout)
      resultat_sentence_match_2 = "{} : {} ({} atouts restants)".format(self.joueur2.name, self.joueur2.state, self.joueur2.nb_atout)
      resultat_sentence_match = resultat_sentence_match_1 + "\n" + resultat_sentence_match_2
    return resultat_sentence_match

  def run_manche(self):
    puissance1 = self.joueur1.puissance
    puissance2 = self.joueur2.puissance
    self.joueur1.attack(atout=False, puissance_adverse=puissance2, num_manche=self.num_manche)
    self.joueur2.attack(atout=False, puissance_adverse=puissance1, num_manche=self.num_manche)
    if self.continue_manche():
      is_vainqueur_exist, vainqueur, looser = self.get_vainqueur()
      looser.attack(atout=True, puissance_adverse=vainqueur.puissance, num_manche=self.num_manche)
      if self.continue_manche():
        is_vainqueur_exist, vainqueur, looser = self.get_vainqueur()
        looser.attack(atout=True, puissance_adverse=vainqueur.puissance, num_manche=self.num_manche)
    is_vainqueur_exist, vainqueur, looser = self.get_vainqueur()
    resultat_sentence = self.run_resultat()
    print(resultat_sentence)
    if looser.KO == 1 or self.num_manche >= self.max_manche:
      self.end = True

  def run_match(self):
      while self.end == False:
        self.run_manche()
        self.num_manche += 1
      print(self.resultat_duel())

  def encoder_puissance(self, puissance):
    # Convertit la puissance en bytes, encode en base64, puis convertit en string pour l'affichage
    puissance_bytes = str(puissance).encode('utf-8')
    puissance_encodee = base64.b64encode(puissance_bytes)
    return puissance_encodee.decode('utf-8')

  def decoder_puissance(self, puissance_encodee):
    # Convertit la chaîne codée en base64 en bytes, décode de base64, puis convertit en string
    puissance_bytes = puissance_encodee.encode('utf-8')
    puissance_decodee = base64.b64decode(puissance_bytes)
    return int(puissance_decodee.decode('utf-8'))