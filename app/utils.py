from app import db

# from app.models import Pokemon
# from app.views import PokemonException


def get_pagination(pokemon):
    task_to_dict = []
    for item in pokemon:
        dict_ = {}
        dict_["id"] = item.id
        dict_["rank"] = item.rank
        dict_["name"] = item.name
        dict_["type_1"] = item.type_1
        dict_["type_2"] = item.type_2
        dict_["HP"] = item.HP
        dict_["attack"] = item.attack
        dict_["sp_atk"] = item.sp_atk
        dict_["sp_def"] = item.sp_def
        dict_["speed"] = item.speed
        dict_["generation"] = item.generation
        dict_["legendary"] = item.legendary

        task_to_dict.append(dict_)
    return task_to_dict


# writing function for update pokemon columns

# def update_pokemon(pokemon_name, payloads):
#     if pokemon_name:
#         match_pokemon = Pokemon.query.filter_by(name=pokemon_name).first()

#         if not match_pokemon:
#             raise PokemonException(
#                 f"pokemon id is not there in table {Pokemon.__tablename__}", 204
#             )
#         editable_columns = Pokemon().get_editable_fields()
#         # print(editable_columns)
#         updated_pokemon = update_object(
#             pokemon_name,
#             editable_columns,
#             match_pokemon,
#             params=payloads,
#         )
#         return {"success": True, "update_pokemon": updated_pokemon}, 200

#     raise PokemonException(f"ID not given by user", 400)


# def update_object(pokemon_name,editable_keys, object_to_update, params):
#     '''
#     get editable keys= ("HP", "total", "attack", "sp_atk", "sp_def", "speed", "legendary")
#     '''

#     print(params.keys(),editable_keys)
#     for key in params:
#         if key in editable_keys:
#             setattr(object_to_update, key,params.get(key))
#     new_obj = add_object(object_to_update)
#     return new_obj


def add_object(obj):
    updated_object = db.session.merge(obj)
    db.session.commit()
    return updated_object, 200


#written function for updating single object
def update_object(pokemon_id, editable_keys, object_to_update, params):
    params = params["items"][0]

    """
    get editable keys= ("HP", "total", "attack", "sp_atk", "sp_def", "speed", "legendary")
    """

    print(params.keys(), editable_keys)
    for key in params:
        if key in editable_keys:
            setattr(object_to_update, key, params.get(key))
    new_obj = add_object(object_to_update)
    return new_obj
