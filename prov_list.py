# prov_list.py
"""
PROV-N with entlist(lid; e1, e2, ..., en) statement that is equivalent to:
entity(lid)
entity(e1)
hadMember(lid, e1)
entity(e2)
hadMember(lid, e2)
...
entity(en)
hadMember(lid, en)
"""

from extensible_provn.view import provn  # Use Plain PROV as base
from extensible_provn.view.dot import graph

@graph.prov("entlist")
def entlist(dot, *args, **kwargs):
    attrs = kwargs.get("attrs", None)
    id_ = kwargs.get("id_", None)
    lines = [dot.node(attrs, "entity", id_)]
    for entity_id in args:
        lines.append(dot.node(attrs, "entity", entity_id))
        lines.append(dot.arrow2(attrs, "hadMember", id_, entity_id))
    return "\n".join(lines)

if __name__ == "__main__":
    graph.main()