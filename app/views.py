from flask import Blueprint, request, jsonify, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, delete
from sqlalchemy.dialects.sqlite import insert

# custom imports
from app.models import Pokemon, db, pokemon_schema
from app import app
from .utils import get_pagination,update_object

import urllib.request, json


pokemonapi = Blueprint("pokemon_api", __name__, url_prefix="/pokemons")


class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


# @pokemonapi.errorhandler(Exception)
# def handle_exception(e):
#     return {"success": False, "error": str(e)}, 400


class RecordNotFoundError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

# @pokemonapi.errorhandler(Exception)
# def handle_record_exception(e):
#     return {"success":False,"error":str(e)}


@pokemonapi.route("/new", methods=["POST"])
def new_pokemon():
    rank = None
    name = None
    type_1 = None
    type_2 = None
    total = None
    hp = None
    attack = None
    defense = None
    sp_atk = None
    sp_def = None
    speed = None
    generation = None
    legendry = None
    rank = rank or request.json.get("#")
    name = name or request.json.get("Name")
    type_1 = type_1 or request.json.get("Type 1")
    type_2 = type_2 or request.json.get("Type 2")
    total = total or request.json.get("Total")
    hp = hp or request.json.get("HP")
    attack = attack or request.json.get("Attack")
    defense = defense or request.json.get("Defense")
    sp_atk = sp_atk or request.json.get("Sp. Atk")
    sp_def = sp_def or request.json.get("Sp. Def")
    speed = speed or request.json.get("Speed")
    generation = generation or request.json.get("Generation")
    legendary = legendry or request.json.get("Legendary")
    try:
        pokemon_ = Pokemon(
            rank=rank,
            name=name,
            type_1=type_1,
            type_2=type_2,
            HP=hp,
            attack=attack,
            total=total,
            sp_atk=sp_atk,
            sp_def=sp_def,
            speed=speed,
            generation=generation,
            legendary=legendary,
        )
        db.session.add(pokemon_)
        db.session.commit()
        return (
                {
                    "success": True,
                    "message": "data added successfully",
                    "data": pokemon_schema.dump(pokemon_),
                }
            ,
            200,
        )

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": "this pokemon id  is already there "}),
            404,
        )


@pokemonapi.route("/", methods=["GET"])
@pokemonapi.route("/<int:id>", methods=["GET"])
# @pokemonapi.route("/<string:type_1>",methods=["GET"])
def views(id=None,type_1=None):
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
    order=None
    page = request.args.get("page", 1, type=int)
    order = order or request.args.get("order") #order=asc
    limit = request.args.get("limit", app.config.get("PAGE_LIMIT"), type=int)
    page_num = request.args.get("page", 1, type=int)
    sort = request.args.get("sort", "rank")
    search = request.args.get("name")
    legendary = request.args.get("legendary")
    type_1 = request.args.get("type_1")
    type_2 = request.args.get("type_2")
    generation = request.args.get("generation", type=int)
    # rank = request.args.get("rank")
    pokemon = Pokemon.query
    if id:
        pokemon = pokemon.filter(Pokemon.id == id)
        if not pokemon:
            raise PokemonException(
                f"Pokemon with id doesn't exist in {Pokemon.__tablename__} table.", 200
            )
    print(type_1)
    if type_1:
        pokemon=pokemon.filter(Pokemon.type_1==type_1)
        if not pokemon:
            raise RecordNotFoundError(f"Pokemon with this type not exist in {Pokemon.__tablename__}",200)
        
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
        raise PokemonException(f"No records found in the {Pokemon.__tablename__}", 204)
    if pokemons.has_next:
        next_url = url_for("pokemon_api.views", page=pokemons.next_num)
    else:
        next_url = None
    result = get_pagination(pokemons)
    dict_ = {"Record with_pagination": result}

    return {
        "success": True,
        "all_pokemon": dict_,
        "total": pokemons.total,
        "order": order,
        "sort": sort,
        "currentPage": pokemons.page,
        "totalPages": pokemons.pages,
        "next_page": next_url,
    }


# @pokemonapi.route("/",methods=["PUT"])
@pokemonapi.route("/", methods=["PUT"])
@pokemonapi.route("/<pokemon_id>", methods=["PUT"])
def pokemon_update(pokemon_id=None):
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
    if pokemon_id:
        new_record = request.json
        match_record = Pokemon.query.get(pokemon_id)

        if not match_record:
            raise PokemonException(
                f"record with this pokemon id is not available in {Pokemon.__tablename__}",
                200,
            )
        editable_columns = Pokemon().get_editable_fields()
        updated_pokemon = update_object(
            pokemon_id, editable_columns, match_record, params=new_record
        )
        return {"success": True, "update_pokemon": updated_pokemon}, 200
    
    # writing upsert command 
    else:
        pokemon_data = request.json.get("items")
        if not pokemon_data:
            return {"error": "data no found"}, 404
        try:
            query = insert(Pokemon).values(pokemon_data)
            query = query.on_conflict_do_update(
                index_elements=[Pokemon.id],
                set_=dict(
                    name=query.excluded.name,
                    type_1=query.excluded.type_1,
                    type_2=query.excluded.type_2,
                    total=query.excluded.total,
                    HP=query.excluded.HP,
                    attack=query.excluded.attack,
                    Defense=query.excluded.Defense,
                    sp_atk=query.excluded.sp_atk,
                    sp_def=query.excluded.sp_def,
                    speed=query.excluded.speed,
                    generation=query.excluded.generation,
                    legendary=query.excluded.legendary,
                ),
            )

            db.session.execute(query)
            db.session.commit()
        except Exception as error:
            return {"error": str(error)}, 404
        return {
            "success": True,
            "message": f"{len(pokemon_data)} Pokemons updated sucessfully.",
        }, 200






# API for deleting the record by id column name
@pokemonapi.route("/<id>", methods=["DELETE"])
@pokemonapi.route("", methods=["DELETE"])
# @pokemonapi.route("/<string:name>", methods=["DELETE"])
def del_pokemon(id=None):
    pokemon_query=Pokemon.query
    if id :
        ids=(id,)
        
    else:
        ids=request.json.get("pokemon_ids")
        print(ids)
    for item in ids:
        print(item)
        pokemons=pokemon_query.filter(Pokemon.id==item).first()
        if pokemons:
            db.session.delete(pokemons)
            db.session.commit()
            return {"success":True,"Ppokemon":pokemons,"message":f"deleted successfully with{ids}"} 
        else:
            raise RecordNotFoundError(f"No record with this id",400)
    
    


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
            HP=item.get("HP"),
            attack=item.get("Attack"),
            Defense=item.get("Defense"),
            sp_atk=item.get("Sp. Atk"),
            sp_def=item.get("Sp. Def"),
            speed=item.get("Speed"),
            generation=item.get("Generation"),
            legendary=item.get("Legendary"),
        )

        db.session.add(pokemon)
        db.session.commit()
    return jsonify({"success": True, "message": "data inserted successfully"})


