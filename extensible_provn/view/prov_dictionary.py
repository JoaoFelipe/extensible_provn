from .provn import graph
from ..utils import unquote
from .. import utils

@graph.prov("hadDictionaryMember")
def had_dictionary_member(dot, did=None, eid=None, key=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "hadDictionaryMember", did, eid, "[{}]".format(unquote(key)))


@graph.prov("derivedByInsertionFrom")
def derived_by_insertion_from(dot, dgen=None, duse=None, changes=None, attrs=None, id_=None):
    if not dgen:
        return None
    statement = "derivedByInsertionFrom"
    gen_url = dot.prefix(dgen)
    point, result = dot.point(attrs, statement)
    result += "\n" + dot._arrow(gen_url, point, attrs=dot.style.arrow(attrs, statement, "der-ins", "1"))

    if duse:
        use_url = dot.prefix(duse)
        result += "\n" + dot._arrow(point, use_url, attrs=dot.style.arrow(attrs, statement, "der", "0"))

    for key, ent in changes:
        key = unquote(key)
        if ent:
            ent_url = dot.prefix(ent)
            result += "\n" + dot._arrow(point, ent_url, attrs=dot.style.arrow(attrs, statement, "[{}]".format(key), "2"))
    return result


@graph.prov("derivedByRemovalFrom")
def derived_by_removal_from(dot, dgen=None, duse=None, removals=None, attrs=None, id_=None):
    tremovals = ", ".join(
        "[{}]".format(unquote(x)) for x in removals if x
    )
    return dot.arrow2(attrs, "derivedByRemovalFrom", dgen, duse, "der-rem\n{}".format(tremovals))


def _main():
    """Main function"""
    graph.main()


if __name__ == "__main__":
    _main()
