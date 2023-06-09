from flask import Blueprint, request, jsonify, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DataError
from sqlalchemy import desc, delete
from sqlalchemy.dialects.sqlite import insert

# custom imports
from app.models import Pokemon, db, pokemon_schema
from app import app
from app.utils import get_pagination, update_object

import urllib.request, json


pokemonapi = Blueprint("pokemon_api", __name__, url_prefix="/pokemons")


class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@pokemonapi.errorhandler(Exception)
def handle_exception(e):
    return {"success": False, "error": str(e)}, 400


class RecordNotFoundError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@pokemonapi.errorhandler(Exception)
def handle_record_exception(e):
    return {"success": False, "error": str(e)}


class FoundError(Exception):
    def __init__(self, message, code=200):
        self.message = message
        self.code = code


@pokemonapi.errorhandler(Exception)
def handle_record_exception(e):
    return {"success": False, "error": str(e)}


@pokemonapi.route("/", methods=["POST"])
def new_pokemon():
    rank = request.json.get("#")
    name = request.json.get("Name")
    if name:
        match_record = Pokemon.query.filter(Pokemon.name == name)
        if match_record:
            raise FoundError(
                f"record with this name is already present in the table", 200
            )

    type_1 = request.json.get("Type 1")
    type_2 = request.json.get("Type 2")
    total = request.json.get("Total")
    hp = request.json.get("HP")
    attack = request.json.get("Attack")
    defense = request.json.get("Defense")
    sp_atk = request.json.get("Sp. Atk")
    sp_def = request.json.get("Sp. Def")
    speed = request.json.get("Speed")
    generation = request.json.get("Generation")
    legendary = request.json.get("Legendary")
    pokemon_ = Pokemon(
            rank=rank,
            name=name,
            type_1=type_1,
            type_2=type_2,
            hp=hp,
            defense=defense,
            attack=attack,
            total=total,
            sp_atk=sp_atk,
            sp_def=sp_def,
            speed=speed,
            generation=generation,
            legendary=legendary,
        )
    try:

        db.session.add(pokemon_)
        db.session.commit()
        serialized_data = pokemon_schema.dump(pokemon_)
        return (
            {
                "success": True,
                "message": "data added successfully",
                "data": serialized_data,
            },
            200,
        )

    except IntegrityError as e:
        db.session.rollback()
        return {"success":"false","error":e},404


@pokemonapi.route("/", methods=["GET"])
@pokemonapi.route("/<int:id>", methods=["GET"])
def views(id=None):
    """if I provide the name of the pokemon and then it returns single
    match records other wise this function  fetched all the records with pagination
    of database
    query parameters:
    limit(int):records per page,
    sort(str):Column to sort on,
    order(str):desc/asc,
    page(int):fetch the requestd page,
    search(name):search str in pokemon name,
    legendary(bool):fetch pokemon based to legendary,
    type_1(str):fetch pokemon basd on type_1,
    type_2(str):fetch pokemon based on type_2,
    generation(int):fetch pokemon with generation,
    id(int,optional):id to retrieve pokemon

    """

    page = request.args.get("page", 1, type=int)
    order = request.args.get("order")  # order=asc
    limit = request.args.get("limit", app.config.get("PAGE_LIMIT"), type=int)
    page_num = request.args.get("page", 1, type=int)
    sort = request.args.get("sort", "rank")
    search = request.args.get("name")
    legendary = request.args.get("legendary")
    type_1 = request.args.get("type_1")
    type_2 = request.args.get("type_2")
    generation = request.args.get("generation", type=int)

    pokemon = Pokemon.query
    if id:
        pokemon = pokemon.filter(Pokemon.id == id)
        if not pokemon:
            raise RecordNotFoundError(
                f"Pokemon with id doesn't exist in {Pokemon.__tablename__} table.", 200
            )
    if type_1:
        pokemon = pokemon.filter(Pokemon.type_1 == type_1)
        if not pokemon:
            raise RecordNotFoundError(
                f"Pokemon with this type not exist in {Pokemon.__tablename__}", 200
            )

    if order == "asc":
        pokemon = pokemon.order_by(sort)
    else:
        pokemon = pokemon.order_by(desc(sort))

    if search:
        pokemon = pokemon.filter(Pokemon.name.ilike(f"%{search}%"))

    if type_1:
        pokemon = pokemon.filter(Pokemon.type_1 == type_1)

    if type_2:
        pokemon = pokemon.filter(Pokemon.type_2 == type_2)

    if legendary:
        pokemon = pokemon.filter(Pokemon.legendary == legendary)

    if generation:
        pokemon = pokemon.filter(Pokemon.generation == generation)

    pokemons = pokemon.paginate(page=page_num, per_page=limit, error_out=False)
    records = pokemons.items

    if len(records) == 0:
        raise RecordNotFoundError(f"No records found in the {Pokemon.__tablename__}", 204)
    if pokemons.has_next:
        next_url = url_for("pokemon_api.views", page=pokemons.next_num)
    else:
        next_url = None
    serialized = pokemon_schema.dump(pokemons)

    return {
        "success": True,
        "currentPage": pokemons.page,
        "totalPages": pokemons.pages,
        "next_page": next_url,
        "all_pokemon": serialized,
        "total": pokemons.total,
        "order": order,
        "sort": sort,
    }


@pokemonapi.route("/", methods=["PUT", "POST"])
def pokemon_update():
    """
    The API updates if the pokemon is already exist,
    if pokemon is not exist then it will insert new pokemon.

    Payload:
        id:id of pokemon
        HP(str, Required),
        "Attack":
        "Defense"
        "Sp. Atk'
        "Sp. Def"
        "Speed"
        "Generation"
        "Legendary":True or False

    """

    pokemon_data = request.json.get("items")
    if not pokemon_data:
        return {"error": "data no found"}, 404

    query = insert(Pokemon).values(pokemon_data)
    query = query.on_conflict_do_update(
        index_elements=[Pokemon.name],
        set_=dict(
            name=query.excluded.name,
            type_1=query.excluded.type_1,
            type_2=query.excluded.type_2,
            total=query.excluded.total,
            hp=query.excluded.hp,
            attack=query.excluded.attack,
            defense=query.excluded.defense,
            sp_atk=query.excluded.sp_atk,
            sp_def=query.excluded.sp_def,
            speed=query.excluded.speed,
            generation=query.excluded.generation,
            legendary=query.excluded.legendary,
        ),
    )
    try:
        db.session.execute(query)
        db.session.commit()
    except (SQLAlchemyError, DataError, IntegrityError) as e:
        return {"error": str(e)}, 404
    return {
        "success": True,
        "message": f"{len(pokemon_data)} Pokemons updated sucessfully.",
    }, 200


# API for deleting the record by id column name
@pokemonapi.route("/<pokemon_id>", methods=["DELETE"])
@pokemonapi.route("/more-pokemons", methods=["DELETE"])

def del_pokemon(pokemon_id=None,type_1=None):
    pokemon_query = Pokemon.query
    if pokemon_id:
        pokemon_ = (pokemon_id,)

    else:
        pokemon_ = request.json.get("pokemon_ids")
        for item in pokemon_:
            pokemons = pokemon_query.filter(Pokemon.id == item).first()
            if pokemons:
                db.session.delete(pokemons)
                db.session.commit()
                return {
                    "success": True,
                    "pokemon": pokemons,
                    "message": f"deleted successfully with{item}",
                }
            else:
                raise RecordNotFoundError(f"No record with this id", 400)


@pokemonapi.route("/load-json", methods=["GET"])
def load_into_db():
    res = load_json()
    return res


def load_json():
    url = "https://coralvanda.github.io/pokemon_data.json"

    response = urllib.request.urlopen(url)

    data = json.loads(response.read())

    for item in data:
        pokemon = Pokemon(
            rank=item.get("#"),
            name=item.get("Name"),
            type_1=item.get("Type 1"),
            type_2=item.get("Type 2"),
            total=item.get("Total"),
            hp=item.get("HP"),
            attack=item.get("Attack"),
            defense=item.get("Defense"),
            sp_atk=item.get("Sp. Atk"),
            sp_def=item.get("Sp. Def"),
            speed=item.get("Speed"),
            generation=item.get("Generation"),
            legendary=item.get("Legendary"),
        )

        db.session.add(pokemon)
        db.session.commit()
    return jsonify({"success": True, "message": "data inserted successfully"})
