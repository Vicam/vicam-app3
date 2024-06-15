import pandas as pd
from random import random
from models import Joueur

# Assurez-vous que les classes left_player et right_player sont définies ou importées si elles sont dans un autre module


class Field:
  def __init__(self, id, left_player, right_player):
    self.id = id
    self.pos = 0
    self.left_player = left_player
    self.right_player = right_player
    self.left_call = 'no'
    self.right_call = 'no'
    self.rule_dict = {
        'Type/position': ['No', 'B', 'Team A+B', 'Team A'],
        '0': ['80%', '18%', '2%', '0%'],
        '1': ['50%', '35%', '14%', '1%'],
        '2': ['20%', '35%', '35%', '10%'],
        '3': ['0%', '0%', '80%', '20%']
    }
    self.rule_df = pd.DataFrame(self.rule_dict).set_index('Type/position')
    self.turn = 0
    self.statut = 'nothing'


  def update_call(self):
    random_numbers = [random() for _ in range(2)]
    # print(f"Nombres aléatoires générés: {random_numbers}")
    categories = []
    if abs(self.pos) < 4:
      for random_number in random_numbers:
          cum_percentage = 0
          # print(self.rule_dict)
          # print(self.rule_df)
          for index, value in self.rule_df[str(abs(self.pos))].items():
                # Enlever le signe '%' et convertir en décimal
                percentage = float(value.strip('%')) / 100
                cum_percentage += percentage
                # Vérifier si le nombre aléatoire se trouve dans l'intervalle actuel
                # print(random_number, " <= ", cum_percentage)
                if random_number <= cum_percentage:
                    categories.append(index)
                    break  # Sortir de la boucle interne une fois la catégorie trouvée

      # print(categories)
      self.left_call = categories[0]
      self.right_call = categories[1]
    self.statut = 'call'

  def print_status(self, print_level):
    if print_level == "all":
      print(f"{self.id} (turn {self.turn}, {self.statut}) ({self.pos}) : {self.left_player} ({self.left_call}) / {self.right_player} ({self.right_call})")
    if print_level == "essentiel":
      if self.statut == 'battle':
        print(f"{self.id} ({self.pos}) : {self.left_player} ({self.left_call}) / {self.right_player} ({self.right_call})")

  def automatic_turn(self):
    self.statut = 'ok'
    self.turn += 1
    if self.left_call == 'No' and self.right_call == 'No':
      r = random()
      if r < 0.5:
        self.pos += -1
      if r > 0.5:
        self.pos += 1
    if self.left_call == 'No' and self.right_call != 'No':
      self.pos += -1
    if self.left_call != 'No' and self.right_call == 'No':
      self.pos += 1
    if self.left_call != 'No' and self.right_call != 'No':
      self.statut = 'battle'
      self.turn += -1

  def manual_turn(self, vainqueur):
    self.statut = 'ok'
    self.turn += 1
    if vainqueur == 'left':
      self.pos += 1
    if vainqueur == 'right':
      self.pos += -1
    else:
      self.pos += 0