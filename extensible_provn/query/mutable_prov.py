"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.query.provn import *
from tools.utils import parsetime


@querier.prov("value", ["id", "text"])
def value(dot, vid, attrs=None, id_=None):
    return [
        vid,
        querier.text("value", [vid], attrs, id_)
    ]


@querier.prov("accessed", ["entity", "value", "time", "text"])
def accessed(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, vid, ti,
        querier.text("accessed", [eid, vid, time], attrs, id_)
    ]


@querier.prov("accessedPart", ["entity", "collection", "key", "part", "time", "text"])
def accessedPart(dot, eid=None, wid=None, key=None, pid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, wid, key, pid, ti,
        querier.text("accessedPart", [eid, wid, key, pid, time], attrs, id_)
    ]


@querier.prov("defined", ["entity", "value", "time", "text"])
def defined(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, vid, ti,
        querier.text("defined", [eid, vid, time], attrs, id_)
    ]


@querier.prov("wasDefinedBy", ["value", "entity", "time", "text"])
def wasDefinedBy(dot, vid=None, eid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        vid, eid, ti,
        querier.text("wasDefinedBy", [vid, eid, time], attrs, id_)
    ]


@querier.prov("derivedByInsertion", ["entity", "collection", "changes", "time", "text"])
def derivedByInsertion(dot, eid=None, wid=None, changes=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, wid, changes, ti,
        querier.text("derivedByInsertion", [eid, wid, changes, time], attrs, id_)
    ]
