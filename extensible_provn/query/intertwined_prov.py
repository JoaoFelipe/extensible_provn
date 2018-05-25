"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.query.prov_dictionary import *
from tools.utils import parsetime, unquote

@querier.prov("entity", ["id", "checkpoint", "type", "text"])
def entity(querier, eid, attrs={}, id_=None):
    attrs = attrs or {}
    time = attrs.get("intertwined:checkpoint")
    type_ = attrs.get("type")
    return [
        eid, parsetime(time), unquote(type_),
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("wasDerivedFrom", ["generated", "used", "activity", "generation", "use", "type", "checkpoint", "collection", "key", "mode", "attrs", "text"])
def wasDerivedFrom(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        eid1, eid2, aid, gid, uid,
        unquote(attrs.get("type")), parsetime(attrs.get("intertwined:checkpoint")),
        unquote(attrs.get("intertwined:collection")), unquote(attrs.get("intertwined:key")), unquote(attrs.get("intertwined:access")),
        attrs, querier.text("wasDerivedFrom", [eid1, eid2, aid, gid, uid], attrs, id_)
    ]
