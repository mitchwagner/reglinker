import io
import unittest

import RegLinkerIO as rlio

class TestRegLinkerIO(unittest.TestCase):


    def test_read_graph(self):

        infile = io.StringIO(
            "a\tb\tlabel1\t5\n"
            "b\tc\tlabel2\t6\n" 
            "c\td\tlabel1\t2"
            ) 

        G = rlio.read_graph(infile, label_col=2, weight_col=3)

        self.assertTrue(G.has_edge("a", "b"))
        self.assertTrue(G.has_edge("b", "c"))
        self.assertTrue(G.has_edge("c", "d"))

        self.assertTrue(G["a"]["b"]["l"] == "label1")
        self.assertTrue(G["b"]["c"]["l"] == "label2")
        self.assertTrue(G["c"]["d"]["l"] == "label1")

        self.assertTrue(G["a"]["b"]["w"] == float(5))
        self.assertTrue(G["b"]["c"]["w"] == float(6))
        self.assertTrue(G["c"]["d"]["w"] == float(2))


    def test_read_node_types(self):
        infile = io.StringIO( 
            "a\tsource\n"
            "b\treceptor\n"
            "c\ttargeto\n"
            "d\ttarget\n"
            "e\tno\n"
            "f\talso no"
            )

        sources, targets = rlio.read_node_types(
            infile, 
            source_kws=["source", "receptor"],
            target_kws=["target", "targeto"]
            )

        sources = list(sources)
        targets = list(targets)

        self.assertTrue("a" in sources)
        self.assertTrue("b" in sources)
        self.assertTrue("c" in targets)
        self.assertTrue("d" in targets)

        self.assertTrue("e" not in sources and "e" not in targets)
        self.assertTrue("f" not in sources and "f" not in targets)


if __name__ == '__main__':
    unittest.main()
