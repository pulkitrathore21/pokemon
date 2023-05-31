from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from . import db



@dataclass
class Pokemon(db.Model):
    print("start db")
    __tablename__ = "pokemon_table"
    rank: int = db.Column(db.Integer, nullable=False)
    name: str = db.Column(db.String(100), primary_key=True, nullable=False)
    type_1: str = db.Column(db.String(100), nullable=False)
    type_2: str = db.Column(db.String(100), nullable=False)
    HP: int = db.Column(db.Integer, nullable=False)
    Defense: int = db.Column(db.Integer, nullable=False)
    total: int = db.Column(db.Integer, nullable=False)
    attack: int = db.Column(db.Integer, nullable=False)
    sp_atk: int = db.Column(db.Integer, nullable=False)
    sp_def: int = db.Column(db.Integer, nullable=False)
    speed: int = db.Column(db.Integer, nullable=False)
    generation: int = db.Column(db.Integer, nullable=False)
    legendary: bool = db.Column(db.Boolean, nullable=False)

    print("end database")
    # def __init__(self, name, type_1, type_2, HP, total,attack, sp_atk, sp_def, speed, generation, legendary):
    #     self.name = name
    #     self.type_1 = type_1
    #     self.type_2 = type_2
    #     self.HP = HP
    #     self.total=total
    #     self.attack = attack
    #     self.sp_atk = sp_atk
    #     self.sp_def = sp_def
    #     self.speed = speed
    #     self.generation = generation
    #     self.legendary = legendary

    def get_editable_fields(self):
        return ("HP", "total", "attack", "sp_atk", "sp_def", "speed", "legendary")
