from enum import Enum
from pydantic import BaseModel, Field, conint
from typing import Dict

class ClasseType(str, Enum):
    C_minus = "C-"
    C = "C"
    C_plus = "C+"
    B_minus = "B-"
    B = "B"
    B_plus = "B+"
    A_minus = "A-"
    A = "A"
    A_plus = "A+"
    S_minus = "S-"
    S = "S"
    S_plus = "S+"

class InitType(str, Enum):
    new = "new"
    existing_encode = "existing encode"
    existing = "existing"

class JoueurInfo(BaseModel):
    classe: ClasseType = Field(
        ...,
        example="S",
        description="La classe du joueur, qui peut prendre des valeurs allant de C- à S+."
    )
    armee: conint(ge=1, le=10) = Field(
        ...,
        example=1,
        description="Le numéro de l'armée auquel appartient le joueur, doit être compris entre 1 et 10."
    )
    tour: conint(ge=0, le=100) = Field(
        ...,
        example=3,
        description="Le numéro du tour actuel, doit être compris entre 1 et 100."
    )
    bonus: conint(ge=0, le=10) = Field(
        ...,
        example=0,
        description="Le nombre de bonus du joueur, doit être compris entre 1 et 10."
    )
    puissance_base: int = Field(
        ...,
        example=350,
        description="La puissance de base du joueur, exprimée en entier."
    )

class InitInfo(BaseModel):
    info_init: Dict[str, JoueurInfo] = Field(
        ...,
        description="Un dictionnaire contenant les informations de chaque joueur."
    )
    init_type: InitType = Field(
        ...,
        example="new",
        description="Le type d'initialisation, peut être 'new', 'existing encode', ou 'existing'."
    )
