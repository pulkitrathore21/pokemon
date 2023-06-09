from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from app import db, ma


@dataclass
class Pokemon(db.Model):
    __tablename__ = "pokemon_table"
    id: int = db.Column(db.Integer, primary_key=True)
    rank: int = db.Column(db.Integer,nullable=False)
    name: str = db.Column(db.String(100), unique=True,nullable=False)
    type_1: str = db.Column(db.String(100),nullable=False)
    type_2: str = db.Column(db.String(100),nullable=False)
    hp: int = db.Column(db.Integer,nullable=False)
    defense: int = db.Column(db.Integer,nullable=False)
    total: int = db.Column(db.Integer,nullable=False)
    attack: int = db.Column(db.Integer,nullable=False)
    sp_atk: int = db.Column(db.Integer,nullable=False)
    sp_def: int = db.Column(db.Integer)
    speed: int = db.Column(db.Integer,nullable=False)
    generation: int = db.Column(db.Integer)
    legendary: bool = db.Column(db.Boolean)

    def get_editable_fields(self):
        return (
            "hp",
            "defense",
            "attack",
            "sp_atk",
            "sp_def",
            "speed",
            "legendary",
            "total",
        )


class PokemonSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "rank",
            "name",
            "type_1",
            "type_2",
            "total",
            "hp",
            "attack",
            "defense",
            "sp_atk",
            "sp_def",
            "speed",
            "generation",
            "legendary",
        )


pokemon_schema = PokemonSchema()
pokemon_schema = PokemonSchema(many=True)

# def __init__(self, id, rank, name, type_1,
#             Defense, type_2, HP, total,attack,
#             sp_atk, sp_def, speed, generation,
#             legendary):

#     self.id=id
#     self.name = name
#     self.rank=rank,
#     self.Defense=Defense,
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
