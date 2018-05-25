"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.query.provn import *

@querier.prov("derivedByInsertionFrom", ["generated", "used", "changes", "text"])
def derivedByInsertionFrom(dot, dgen=None, duse=None, changes=None, attrs=None, id_=None):
    return [
        dgen, duse, changes,
        querier.text("derivedByInsertionFrom", [dgen, duse, changes], attrs, id_)
    ]


@querier.prov("hadDictionaryMember", ["dict", "entity", "key", "text"])
def hadDictionaryMember(dot, did=None, eid=None, key=None, attrs=None, id_=None):
    return [
        did, eid, key,
        querier.text("hadDictionaryMember", [did, eid, key], attrs, id_)
    ]
