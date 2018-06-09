"""Parser for PROV-N.

It does not comply completely with PROV-N.
It was designed to support only the situations we use in this repository in an extensible way.
"""
import sys
from collections import namedtuple

from lark import Lark, Transformer
from lark.lexer import Token

from lark.tree import Tree

'''
def eq(self, other):
    print(type(self.children[0]))
    try:
        if self.data != other.data:
            return False
        if not isinstance(self.children, list) or not isinstance(other.children, list):
            return self.children == other.children
        if len(self.children) != len(other.children):
            return False
        todo = list(zip(self.children, other.children))
        while todo:
            sc, oc = todo.pop()
            if isinstance(sc, Tree) and isinstance(oc, Tree):
                if sc.data != oc.data:
                    return False
                todo.append((sc, oc))
            else:
                if sc != oc:
                    return False
        return True
    except AttributeError:
        return False

Tree.__eq__ = eq
'''
PARSER = Lark(u'''
    start: document

    document: "document" optional_declarations (expr)* (bundle)* "endDocument"

    ?optional_declarations: (namespace_declarations)?
    namespace_declarations: (default_namespace_declaration | namespace_declaration) (namespace_declaration)*
    namespace_declaration: "prefix" QUALIFIED_NAME IRI_REF
    default_namespace_declaration: "default" IRI_REF
    ?namespace: IRI_REF


    expr: QUALIFIED_NAME "(" optional_identifier arg ("," arg)* optional_attributes ")"

    optional_identifier: ( identifier_marker ";")?
    ?identifier_marker: identifier | "-"
    ?identifier: QUALIFIED_NAME

    arg: identifier_marker
       | literal
       | expr
       | tuple

    tuple: "{{" arg ("," arg )* "}}"
         | "(" arg ("," arg )* ")"


    ?optional_attributes: ( "," "[" attr_pairs "]")?
    attr_pairs: ( | attr_pair ("," attr_pair)* )
    attr_pair: attr "=" literal
    attr: QUALIFIED_NAME


    bundle: "bundle" identifier optional_declarations (expr)* "endBundle"

    ?literal: typed_literal
           | convenience_notation

    typed_literal: ESCAPED_STRING "%%" datatype
    ?datatype: QUALIFIED_NAME
    convenience_notation: ESCAPED_STRING (LANGTAG)?
                       | SIGNED_NUMBER
                       | QUALIFIED_NAME_LITERAL

    QUALIFIED_NAME: ( PN_PREFIX ":" )? PN_LOCAL
                  | PN_PREFIX ":"
    QUALIFIED_NAME_LITERAL: "'" QUALIFIED_NAME "'"
    LANGTAG: "@" LETTER+ ("-" (LETTER|DIGIT)+)*
    PN_PREFIX: PN_CHARS_BASE ((PN_CHARS | ".")* PN_CHARS)?
    PN_LOCAL: ( PN_CHARS_U | DIGIT | PN_CHARS_OTHERS ) ((PN_CHARS | "." | PN_CHARS_OTHERS )* (PN_CHARS | PN_CHARS_OTHERS ))?
    PN_CHARS_OTHERS: PN_CHARS_ESC | PERCENT | "@" | "~" | "&" | "+" | "*" | "?" | "#" | "$" | "!"
    PN_CHARS_ESC: "\\\\" ( "=" | "'" | "(" | ")" | "," | "-" | ":" | ";" | "[" | "]" | "." )
    PERCENT: "%" HEX HEX
    HEX: DIGIT
       | "A-F"
       | "a-f"
    PN_CHARS_BASE: LETTER
                 | "\u00C0".."\u00D6"
                 | "\u00D8".."\u00F6"
                 | "\u00F8".."\u02FF"
                 | "\u0370".."\u037D"
                 | "\u037F".."\u1FFF"
                 | "\u200C".."\u200D"
                 | "\u2070".."\u218F"
                 | "\u2C00".."\u2FEF"
                 | "\u3001".."\uD7FF"
                 | "\uF900".."\uFDCF"
                 | "\uFDF0".."\uFFFD"
                 {}
    PN_CHARS: PN_CHARS_U
            | "-"
            | ":"
            | DIGIT
            | "\u00B7"
            | "\u0300".."\u036F"
            | "\u203F".."\u2040"
    PN_CHARS_U: PN_CHARS_BASE | "_"
    IRI_REF: "<" /.*/ ">"

    COMMENT: /\/\/[^\\n]*/

    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.LETTER
    %import common.DIGIT
    %import common.WS
    %ignore COMMENT
    %ignore WS
'''.format(u'| "\U00010000".."\U000EFFFF"' if sys.version_info > (3, 0) else ""), lexer='standard')

# (\d{4}-\d\d-\d\d(T\d\d:\d\d(:\d\d)?(\.\d+)?(([+-]\d\d:\d\d)|Z)?)?)


class CallProvN(Transformer):

    def __init__(self, functions={}):
        self.functions = functions

    def start(self, elements):
        return elements[0]

    def document(self, elements):
        if "document" in self.functions:
            return self.functions["document"](elements[0], elements[1:])
        else:
            return [x for x in elements if x is not None]

    def optional_declarations(self, elements):
        if elements:
            return elements
        return []

    def namespace_declarations(self, elements):
        if "<namespaces>" in self.functions:
            return self.functions["<namespaces>"](elements)
        else:
            filtered = [x for x in elements if x is not None]
            if filtered:
                return filtered
            return None

    def default_namespace_declaration(self, elements):
        params = ["<default>", elements[0].value]
        if "prefix" in self.functions:
            return self.functions["prefix"](*params)
        return self.functions["<warning>"]("prefix", *params)

    def namespace_declaration(self, elements):
        params = [x.value for x in elements]
        if "prefix" in self.functions:
            return self.functions["prefix"](*params)
        return self.functions["<warning>"]("prefix", *params)

    def expr(self, elements):
        name = elements[0]
        id_ = elements[1]
        attrs = elements[-1]
        params = elements[2:-1]
        if name.startswith("prov:"):
            name = name[5:]
        if name in self.functions:
            return self.functions[name](*params, id_=id_, attrs=attrs)
        return self.functions["<warning>"](name, *params, id_=id_, attrs=attrs)

    def arg(self, elements):
        element = elements[0]
        if isinstance(element, Token):
            return element.value
        if isinstance(element, str):
            return element
        if isinstance(element, list):
            return element

    def tuple(self, elements):
        return elements

    def optional_identifier(self, elements):
        if elements:
            return elements[0].value
        return None

    def identifier_marker(self, elements):
        if elements:
            print("AAAAAAAAAAAAA")
        return None

    def optional_attributes(self, elements):
        if elements:
            return elements
        return None

    def attr_pairs(self, elements):
        return {k:v for k, v in elements}

    def attr_pair(self, elements):
        return elements

    def attr(self, elements):
        return elements[0].value

    def typed_literal(self, elements):
        return [x.value for x in elements]
        #return Typed(*[x.value for x in elements])

    def convenience_notation(self, elements):
        return elements[0].value

    def bundle(self, elements):
        name, declarations, expressions = elements[0], elements[1], elements[2:]
        name = name.value
        if "bundle" in self.functions:
            return self.functions["bundle"](name, declarations, expressions)
        return self.functions["<warning>"]("bundle", name, declarations, expressions)


def _warning(name, *args, **kwargs):
    id_ = kwargs.get("id_", None)
    attrs = kwargs.get("attrs", None)
    print("WARNING: '{}' is not defined!".format(name))

import re

def provn_structure(content):
    """Surround contend with provn header and footer"""
    content = content.strip()
    if not content.startswith("document"):
        content = "document\ndefault <http://example.org/>\n" + content
    if not content.endswith("endDocument"):
        content = content + "\nendDocument"
    return content


def build_parser(functions, ignore_unnamed=False, warning=_warning):
    funcs = {
        "<warning>": warning,
    }
    if isinstance(functions, dict):
        for name, func in functions.items():
            if hasattr(func, 'provname'):
                funcs[func.provname] = func
            elif not ignore_unnamed:
                funcs[name] = func
    else:
        for func in functions.items():
            if hasattr(func, 'provname'):
                funcs[func.provname] = func
            elif not ignore_unnamed:
                funcs[func.__name__] = func

    transformer = CallProvN(funcs)
    def parser(content):
        tree = PARSER.parse(provn_structure(content))
        return transformer.transform(tree)
    return parser


def prov(name):
    def dec(fn):
        fn.provname = name
        return fn
    return dec
