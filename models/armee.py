# Importer la classe Joueur depuis le module approprié
from models import Joueur  # Remplacez 'your_module' par le nom correct du module où Joueur est défini


class Armee:
    def __init__(self, name):
        self.name = name
        self.dict_joueur = {}

    def add_joueur(self, joueur):
        self.dict_joueur[joueur.name] = joueur

    def display_state(self, details="base"):
      if details == "base":
        for name, joueur in self.dict_joueur.items():
          joueur.display_state(details=details)
      if details == "transparent":
        for name, joueur in self.dict_joueur.items():
          joueur.display_state(details=details)
      if details == "public":
        for name, joueur in self.dict_joueur.items():
          if joueur.deploye == False:
            print(f"{joueur.name} : non déployé")
          else :
            joueur.display_state(details=details)