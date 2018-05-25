from .provn import graph
from ..utils import unquote


@graph.prov("value")
def value(dot, vid, attrs=None, id_=None):
    return dot.node(attrs, "value", vid)


@graph.prov("accessed")
def accessed(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "accessed", eid, vid, "access\n{}".format(time or "-"))


@graph.prov("accessedPart")
def accessed_part(dot, eid=None, wid=None, key=None, pid=None, time=None, attrs=None, id_=None):
    key = unquote(key)
    return dot.arrow2(attrs, "accessedPart", eid, pid, "part\n{}[{}]\n{}".format(
        wid or "-", key or "-", time or "-"
    ))


@graph.prov("defined")
def defined(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "defined", eid, vid, "defined\n{}".format(time or "-"))


@graph.prov("wasDefinedBy")
def was_defined_by(dot, vid=None, eid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasDefinedBy", vid, eid, "def by\n{}".format(time or "-"))


@graph.prov("derivedByInsertion")
def derived_by_insertion(dot, eid=None, wid=None, changes=None, time=None, attrs=None, id_=None):
    result = []
    for pos, part in changes:
        pos = unquote(pos)
        result.append(dot.arrow2(
            attrs, "derivedByInsertion",
            wid, part, "der-ins-v\n[{}]\n{}".format(pos or "-", time or "-"),
            extra="0"
        ))
        result.append(dot.arrow2(
            attrs, "derivedByInsertion",
            part, eid, "der-ins-e\n[{}]\n{}".format(pos or "-", time or "-"),
            extra="1"
        ))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)


@graph.prov("derivedByRemoval")
def derived_by_removal(dot, eid=None, wid=None, positions=None, time=None, attrs=None, id_=None):
    result = []
    for pos in positions:
        pos = unquote(pos)
        result.append(dot.arrow2(
            attrs, "derivedByRemoval",
            wid, eid, "der-rem\n[{}]\n{}".format(pos or "-", time or "-")
        ))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)


def _main():
    """Main function"""
    graph.main()


if __name__ == "__main__":
    _main()

