from .provn import prov
from .prov_dictionary import graph
from ..utils import unquote
from .. import utils

NAMESPACE = "https://dew-uff.github.io/versioned-prov/ns/intertwined#"

def intertwined(attrs, key, default="-"):
    try:
        return attrs[(key, "intertwined", NAMESPACE)]
    except KeyError:
        return default

def ns_intertwined(key):
    return {
        "intertwined:" + key,
        NAMESPACE + key,
        key
    }

@graph.prov("entity")
def entity(dot, eid, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_intertwined('Version'):
        return dot.node(attrs, "version", eid)
    return dot.node(attrs, "entity", eid)


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    if aid and gid and uid:
        dot.used_required[(aid, eused)] = (uid, attrs)
        dot.generated_required[(egenerated, aid)] = (gid, attrs)
    if prov(attrs, 'type') in ns_intertwined('Reference'):
        if intertwined(attrs, 'access', False):
            return dot.arrow3(
                attrs, "int_wasDerivedFrom",
                egenerated, intertwined(attrs, 'collection'), eused,
                "",
                "der ac-{}\n{}".format(
                    intertwined(attrs, 'access'),
                    intertwined(attrs, 'checkpoint')
                ),
                "[{}]".format(intertwined(attrs, 'key')),
            )
        return dot.arrow2(
            attrs, "int_wasDerivedFrom",
            egenerated, eused, "der ref\n{}".format(
                intertwined(attrs, 'checkpoint')
            ),
            extra="4"
        )
    return dot.arrow2(attrs, "wasDerivedFrom", egenerated, eused, "der")

if __name__ == "__main__":
    graph.main()


@graph.prov("used")
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    dot.used.add((aid, eid))
    checkpoint = intertwined(attrs, 'checkpoint', False)
    if checkpoint:
        return dot.arrow2(attrs, "int_used", aid, eid, "use\n{}".format(checkpoint))
    return dot.arrow2(attrs, "used", aid, eid, "use")

@graph.prov("wasGeneratedBy")
def was_generated_by(dot, aid, eid=None, time=None, attrs=None, id_=None):
    dot.used.add((aid, eid))
    checkpoint = intertwined(attrs, 'checkpoint', False)
    if checkpoint:
        return dot.arrow2(attrs, "int_wasGeneratedBy", aid, eid, "gen\n{}".format(checkpoint))
    return dot.arrow2(attrs, "wasGeneratedBy", aid, eid, "gen")


def _main():
    """Main function"""
    graph.main()


if __name__ == "__main__":
    _main()
