from threading import Thread
from sqlalchemy import orm
from datetime import datetime


def asynchronous(f):
    def wrapper(*args, **kwargs):
        def fn(*args, **kwargs):
            Thread(target=f, args=args, kwargs=kwargs).start()

        return fn

    return wrapper()


def convert_object_to_dict(obj, found=None):
    if found is None:
        found = set()

    mapper = orm.class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = (
        lambda c: (c, getattr(obj, c).isoformat())
        if isinstance(getattr(obj, c), datetime)
        else (c, getattr(obj, c))
    )
    out = dict(map(get_key_value, columns))

    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)

            if related_obj is not None:
                out[name] = (
                    [convert_object_to_dict(child, found) for child in related_obj]
                    if relation.uselist
                    else convert_object_to_dict(related_obj, found)
                )
    return out
