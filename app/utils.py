# from . import db


# def update_object(
#         object_to_update,
#         editable_keys,
#         params):
#     # print(object_to_update,"hello pulkit")
#     for key in params:
#         if key in editable_keys:
#             setattr(object_to_update,key,params[key])
#     new_object=add_object(object_to_update)
#     return new_object


# def add_object(new_object):
#     updated_object=db.session.merge(new_object)
#     db.session.commit()

# return updated_object
