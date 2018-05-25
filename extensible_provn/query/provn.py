"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

import dateutil.parser
from tools.query.querier import querier, var, BLANK
from tools.utils import parsetime


@querier.prov("entity", ["id", "text"])
def entity(querier, eid, attrs={}, id_=None):
    return [
        eid,
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("activity", ["id", "start", "end", "text"])
def activity(dot, aid, start_time=None, end_time=None, attrs=None, id_=None):
    start = parsetime(start_time)
    end = parsetime(end_time)
    return [
        aid, start, end,
        querier.text("activity", [aid, start_time, end_time], attrs, id_)
    ]


@querier.prov("used", ["id", "activity", "entity", "time", "text"])
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        id_, aid, eid, ti,
        querier.text("used", [aid, eid, time], attrs, id_)
    ]


@querier.prov("wasDerivedFrom", ["generated", "used", "activity", "generation", "use", "attrs", "text"])
def wasDerivedFrom(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    return [
        egenerated, eused, aid, gid, uid,
        attrs or {}, querier.text(
            "wasDerivedFrom",
            [egenerated, eused, aid, gid, uid], attrs, id_
        )
    ]


@querier.prov("wasGeneratedBy", ["id", "entity", "activity", "time", "text"])
def wasGeneratedBy(dot, eid, aid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        id_, eid, aid, ti,
        querier.text("wasGeneratedBy", [eid, aid, time], attrs, id_)
    ]


@querier.prov("hadMember", ["collection", "entity", "text"])
def hadMember(dot, ecollection=None, eid=None, attrs=None, id_=None):
    return [
        ecollection, eid,
        querier.text("hadMember", [ecollection, eid], attrs, id_)
    ]


@querier.prov("specializationOf", ["specific", "general", "text"])
def specializationOf(dot, specific=None, general=None, attrs=None, id_=None):
    return [
        specific, general,
        querier.text("specializationOf", [specific, general], attrs, id_)
    ]
