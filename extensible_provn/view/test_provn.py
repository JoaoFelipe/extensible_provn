import unittest
import textwrap

from .provn import graph

graph.set_style("provtoolbox")

class TestProvN(unittest.TestCase):

    def test_entity(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        }""")
        result = graph.generate('entity(e1)')
        self.assertEqual(expected, result)

    def test_entity_with_attr(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "-attrs0" [color="gray",shape="note",fontsize="10",fontcolor="black",label=<<TABLE cellpadding="0" border="0">
        \t<TR>
        \t    <TD align="left">type:</TD>
        \t    <TD align="left">x</TD>
        \t</TR>
        </TABLE>>]
        "-attrs0" -> "http://example.org/e1" [color="gray",style="dashed",arrowhead="none"]
        }""")
        result = graph.generate('entity(e1, [type="x"])')
        self.assertEqual(expected, result)

    def test_activity(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        }""")
        result = graph.generate('activity(a1)')
        self.assertEqual(expected, result)

    def test_activity_with_attr(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "-attrs0" [color="gray",shape="note",fontsize="10",fontcolor="black",label=<<TABLE cellpadding="0" border="0">
        \t<TR>
        \t    <TD align="left">type:</TD>
        \t    <TD align="left">x</TD>
        \t</TR>
        </TABLE>>]
        "-attrs0" -> "http://example.org/a1" [color="gray",style="dashed",arrowhead="none"]
        }""")
        result = graph.generate('activity(a1, [type="x"])')
        self.assertEqual(expected, result)

    def test_agent(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        }""")
        result = graph.generate('agent(ag1)')
        self.assertEqual(expected, result)

    def test_agent_with_attr(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "-attrs0" [color="gray",shape="note",fontsize="10",fontcolor="black",label=<<TABLE cellpadding="0" border="0">
        \t<TR>
        \t    <TD align="left">type:</TD>
        \t    <TD align="left">x</TD>
        \t</TR>
        </TABLE>>]
        "-attrs0" -> "http://example.org/ag1" [color="gray",style="dashed",arrowhead="none"]
        }""")
        result = graph.generate('agent(ag1, [type="x"])')
        self.assertEqual(expected, result)

    def test_was_generated_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/e1" -> "http://example.org/a1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="gen"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasGeneratedBy(e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_generated_by_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasGeneratedBy(e1, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasGeneratedBy(-, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_used(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a1" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="use"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            used(a1, e1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_used_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            used(a1, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            used(-, e1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_informed_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "http://example.org/a2" -> "http://example.org/a1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="inf"]
        }""")
        result = graph.generate("""
            activity(a1)
            activity(a2)
            wasInformedBy(a2, a1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_informed_by_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        }""")
        result = graph.generate("""
            activity(a1)
            activity(a2)
            wasInformedBy(a2, -, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            activity(a1)
            activity(a2)
            wasInformedBy(-, a1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_started_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "bn0" [shape="point",label=""]
        "http://example.org/a2" -> "bn0" [arrowhead="none",dir="back",arrowtail="oinv"]
        "bn0" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="start"]
        "bn0" -> "http://example.org/a1"
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(a2, e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_started_by_incomplete_1(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "bn0" [shape="point",label=""]
        "bn0" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="start"]
        "bn0" -> "http://example.org/a1"
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(-, e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_started_by_incomplete_2(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "http://example.org/a2" -> "http://example.org/a1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="start",dir="back",arrowtail="oinv"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(a2, -, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_started_by_incomplete_3(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "http://example.org/a2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="start",dir="back",arrowtail="oinv"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(a2, e1, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_started_by_incomplete_12_23_13_123(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(-, -, a1, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(a2, -, -, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(-, e1, -, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasStartedBy(-, -, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_ended_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "bn0" [shape="point",label=""]
        "http://example.org/a2" -> "bn0" [arrowhead="none",dir="back",arrowtail="odiamond"]
        "bn0" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="end"]
        "bn0" -> "http://example.org/a1"
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(a2, e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_ended_by_incomplete_1(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "bn0" [shape="point",label=""]
        "bn0" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="end"]
        "bn0" -> "http://example.org/a1"
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(-, e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_ended_by_incomplete_2(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "http://example.org/a2" -> "http://example.org/a1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="end",dir="back",arrowtail="odiamond"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(a2, -, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_ended_by_incomplete_3(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        "http://example.org/a2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="end",dir="back",arrowtail="odiamond"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(a2, e1, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_ended_by_incomplete_12_23_13_123(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/a2" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a2",URL="http://example.org/a2"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(-, -, a1, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(a2, -, -, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(-, e1, -, -, [type="x"])
        """)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            activity(a2)
            wasEndedBy(-, -, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_invalidated_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/e1" -> "http://example.org/a1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="inv",dir="both",arrowtail="odiamond"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasInvalidatedBy(e1, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_invalidated_by_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        }""")
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasInvalidatedBy(-, a1, -, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            activity(a1)
            wasInvalidatedBy(e1, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_derived_from(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        "http://example.org/e2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="der"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasDerivedFrom(e2, e1, -, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_derived_from_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasDerivedFrom(-, e1, -, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasDerivedFrom(e2, -, -, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_attributed_to(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="att"]
        }""")
        result = graph.generate("""
            entity(e1)
            agent(ag1)
            wasAttributedTo(e1, ag1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_attributed_to_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        }""")
        result = graph.generate("""
            entity(e1)
            agent(ag1)
            wasAttributedTo(-, ag1, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            agent(ag1)
            wasAttributedTo(e1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_associated_with(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "bn0" [shape="point",label=""]
        "http://example.org/a1" -> "bn0" [arrowhead="none"]
        "bn0" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="assoc"]
        "bn0" -> "http://example.org/e1"
        }""")
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(a1, ag1, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_associated_with_incomplete_1(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "bn0" [shape="point",label=""]
        "bn0" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="assoc"]
        "bn0" -> "http://example.org/e1"
        }""")
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(-, ag1, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_associated_with_incomplete_2(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="assoc"]
        }""")
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(a1, -, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_associated_with_incomplete_3(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/a1" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="assoc"]
        }""")
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(a1, ag1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_associated_with_12_23_13_123(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/a1" [fillcolor="#9FB1FC",color="#0000FF",shape="polygon",sides="4",style="filled",label="a1",URL="http://example.org/a1"]
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        }""")
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(-, -, e1, [type="x"])
        """)
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(a1, -, -, [type="x"])
        """)
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(-, ag1, -, [type="x"])
        """)
        result = graph.generate("""
            activity(a1)
            agent(ag1)
            entity(e1)
            wasAssociatedWith(-, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_acted_on_behalf_of(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/ag2" [fillcolor="#FDB266",shape="house",style="filled",label="ag2",URL="http://example.org/ag2"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "bn0" [shape="point",label=""]
        "http://example.org/ag2" -> "bn0" [arrowhead="none"]
        "bn0" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="del"]
        "bn0" -> "http://example.org/e1"
        }""")
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(ag2, ag1, e1, [type="x"])
        """)
        self.maxDiff = None
        self.assertEqual(expected, result)

    def test_acted_on_behalf_of_incomplete_1(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/ag2" [fillcolor="#FDB266",shape="house",style="filled",label="ag2",URL="http://example.org/ag2"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "bn0" [shape="point",label=""]
        "bn0" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="del"]
        "bn0" -> "http://example.org/e1"
        }""")
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(-, ag1, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_acted_on_behalf_of_incomplete_2(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/ag2" [fillcolor="#FDB266",shape="house",style="filled",label="ag2",URL="http://example.org/ag2"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/ag2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="del"]
        }""")
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(ag2, -, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_acted_on_behalf_of_incomplete_3(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/ag2" [fillcolor="#FDB266",shape="house",style="filled",label="ag2",URL="http://example.org/ag2"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/ag2" -> "http://example.org/ag1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="del"]
        }""")
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(ag2, ag1, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_acted_on_behalf_of_12_23_13_123(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/ag1" [fillcolor="#FDB266",shape="house",style="filled",label="ag1",URL="http://example.org/ag1"]
        "http://example.org/ag2" [fillcolor="#FDB266",shape="house",style="filled",label="ag2",URL="http://example.org/ag2"]
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        }""")
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(-, -, e1, [type="x"])
        """)
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(a1, -, -, [type="x"])
        """)
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(-, ag1, -, [type="x"])
        """)
        result = graph.generate("""
            agent(ag1)
            agent(ag2)
            entity(e1)
            actedOnBehalfOf(-, -, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_influenced_by(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        "http://example.org/e2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="inf"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasInfluencedBy(e2, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_was_influenced_by_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasInfluencedBy(-, e1, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            entity(e2)
            wasInfluencedBy(e2, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_alternate_of(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        "http://example.org/e2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="alt"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            alternateOf(e2, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_alternate_of_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            alternateOf(-, e1, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            entity(e2)
            alternateOf(e2, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_specialization_of(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        "http://example.org/e2" -> "http://example.org/e1" [labelfontsize="8",labeldistance="1.5",labelangle="60.0",rotation="20",taillabel="spe"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            specializationOf(e2, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_specialization_of_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            specializationOf(-, e1, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            entity(e2)
            specializationOf(e2, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_had_member(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        "http://example.org/e2" -> "http://example.org/e1"
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            hadMember(e2, e1, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_had_member_incomplete(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }""")
        result = graph.generate("""
            entity(e1)
            entity(e2)
            hadMember(-, e1, [type="x"])
        """)
        self.assertEqual(expected, result)
        result = graph.generate("""
            entity(e1)
            entity(e2)
            hadMember(e2, -, [type="x"])
        """)
        self.assertEqual(expected, result)

    def test_bundle(self):
        expected = textwrap.dedent("""\
        digraph "PROV" { size="16,12"; rankdir="BT";
        "http://example.org/e1" [fillcolor="#FFFC87",color="#808080",style="filled",label="e1",URL="http://example.org/e1"]
        subgraph "clusterhttp://example.org/e3" {
          label="e3";
          URL="http://example.org/e3";
        "http://example.org/e2" [fillcolor="#FFFC87",color="#808080",style="filled",label="e2",URL="http://example.org/e2"]
        }
        }""")
        result = graph.generate("""
            entity(e1)
            bundle e3
                entity(e2)
            endBundle
        """)
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()