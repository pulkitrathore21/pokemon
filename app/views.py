from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from .models import Pokemon, db

# from .utils import update_object
import json


pokemonapi = Blueprint("pokemon_api", __name__, url_prefix="/pokemon")


class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@pokemonapi.errorhandler(Exception)
def handle_exception(e):
    return {"success": False, "error": str(e)}, 400


def load_json():
    with open("pokemon_data.json") as f:
        data = json.load(f)
        check_in_db = Pokemon.query.all()
        if not check_in_db:
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
        raise PokemonException(f"Some data present in db", 400)


@pokemonapi.route("/load-json", methods=["POST"])
def load_into_db():
    res = load_json()
    return res


@pokemonapi.route("/delete-record", methods=["DELETE"])
def delete_all_rows():
    db.session.query(Pokemon).delete()
    db.session.commit()
    return {"success": True}


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
    # id=id or request.json.get("id")
    rank = rank or request.json.get("#")
    print(rank)
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
        print(pokemon_)
        db.session.add(pokemon_)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "data added successfully",
                    "data": pokemon_,
                }
            ),
            200,
        )

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": "this pokemon id  is already there "}),
            404,
        )


@pokemonapi.route("/", methods=["GET"])
@pokemonapi.route("/<pokemon_name>", methods=["GET"])
# @pokemonapi.route("/<legendary>",methods=["GET"])
def view(pokemon_name=None):
    search = None
    legendary = None
    generation = None
    # rank=None
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "desc")
    limit = 100
    page_num = request.args.get("page", 1, type=int)
    if search:
        search = request.args.get("search").capitalize()

    legendary = request.args.get("legendary")
    generation = request.args.get("generation")
    rank = request.args.get("rank")
    pokemon_ = view_pokemons(
        pokemon_name, rank, legendary, generation, sort, order, search
    )
    pokemon_ = pokemon_.paginate(page=page_num, per_page=limit, error_out=False)
    r = []
    for i in pokemon_:
        dict_ = {}
        dict_["rank"] = i.rank
        dict_["name"] = i.name
        dict_["type_1"] = i.type_1
        dict_["type_2"] = i.type_2
        dict_["HP"] = i.HP
        dict_["attack"] = i.attack
        dict_["sp_atk"] = i.sp_atk
        dict_["sp_def"] = i.sp_def
        dict_["speed"] = i.speed
        dict_["generation"] = i.generation
        dict_["legendary"] = i.legendary

        r.append(dict_)

    dict__ = {"x": r}
    return {
        "success": True,
        "pokemon": dict__,
        "currentPage": pokemon_.page,
        "totalPages": pokemon_.pages,
    }


@pokemonapi.route("/up-date/<pokemon_name>", methods=["PATCH"])
def pokemon_update(pokemon_name: dict, pokemons: list):
    """

    Payload:
        HP(str, Required),
        "Attack":
    #     "Defense
    #     "Sp. Atk
    #     "Sp. Def
    #     "Speed
    #     "Generatio
    #     "Legendary":True or False

    """

    payloads = request.json
    if type(payloads) == dict:
        result = update_pokemon(pokemon_name, payloads)
        return result
    if type(payloads) == list:
        pokemons = request.json
        model_name = "pokemons"
        upsert_status = upsert_do_update(model_name, pokemons)
        return {"success": True**upsert_status, "pokemons": pokemons}


@pokemonapi.route("/<string:name>", methods=["DELETE"])
def del_pokemon(name=None):
    print(name)
    matched_pokemon = Pokemon.query.filter_by(name=name.capitalize()).first()
    if not matched_pokemon:
        raise PokemonException(f"no record found in the {Pokemon.__tablename__} table")

    db.session.delete(matched_pokemon)
    db.session.commit()
    return {"success": True, "message": "deleted successfully"}


def update_pokemon(pokemon_name, payloads):
    if pokemon_name:
        match_pokemon = Pokemon.query.filter_by(name=pokemon_name).first()

        if not match_pokemon:
            raise PokemonException(
                f"pokemon id is not there in table {Pokemon.__tablename__}", 204
            )
        editable_columns = Pokemon().get_editable_fields()
        updated_pokemon = update_object(
            editable_keys=editable_columns,
            object_to_update=match_pokemon,
            params=payloads,
        )
        return {"success": True, "update_pokemon": updated_pokemon}, 200

    raise PokemonException(f"ID not given by user", 400)


def update_object(editable_keys, object_to_update, params):
    print(type(params))
    for key in params.keys():
        if key in editable_keys:
            setattr(object_to_update, key, params[key])
            # print(object_to_update)
    new_obj = add_object(object_to_update)
    return new_obj


def add_object(obj):
    updated_object = db.session.merge(obj)
    db.session.commit()
    return updated_object, 200

    # "HP": 45,
    #     "Attack": 49,
    #     "Defense": 49,
    #     "Sp. Atk": 65,
    #     "Sp. Def": 65,
    #     "Speed": 45,
    #     "Generation": 1,
    #     "Legendary": false


def view_pokemons(
    pokemon_name,
    rank,
    legendary,
    generation,
    sort=None,
    order=None,
    search=None,
):
    if pokemon_name:
        match_pokemon = Pokemon.query.filter_by(name=pokemon_name.capitalize())
        return match_pokemon

        if not match_data:
            raise PokemonException(
                f"Pokemon {pokemon_name} doesn't exist.",
                404,
            )
    if legendary:
        print(legendary)
        match_data = Pokemon.query.filter_by(legendary=legendary)
        # print(match_data)
        return match_data
    if rank:
        match_record = Pokemon.query.filter_by(rank=rank)
        # print(match_record)
        return match_record

    if generation:
        match_pokemon = Pokemon.query.filter_by(generation=generation)
        return match_pokemon

    pokemon = Pokemon.query
    pokemon = search_order_sort(
        pokemon,
        Pokemon,
        sort,
        order,
        search=search,
        search_field="name",
    )
    return pokemon

    # if pokemon_id:
    #     pokemon=Pokemon.query.filter(Pokemon.id==pokemon_id)
    # return pokemon


def search_order_sort(query_ob, model, sort, order, search=None, search_field=None):
    if search:
        search_query = f"%{search}%"
        search_attr = getattr(model, search_field)
        query_ob = query_ob.filter(search.attr.ilike(search_query))
    query_ob = query_ob.order_by(getattr(getattr(model, sort), order)())
    # print(query_ob)
    # print(type(query_ob))
    return query_ob


#  {
#         "#": 2,
#         "Name": "Ivysaur",
#         "Type 1": "Grass",
#         "Type 2": "Poison",
#         "Total": 405,
#         "HP": 60,
#         "Attack": 62,
#         "Defense": 63,
#         "Sp. Atk": 80,
#         "Sp. Def": 80,
#         "Speed": 60,
#         "Generation": 1,
#         "Legendary": false
#     },
