import unittest

import RegLinker as rl
import networkx as nx

class TestRegLinker(unittest.TestCase):


    @staticmethod
    def __make_G():
        G = nx.DiGraph()

        G.add_edge(1, 2, l="a", w=1)
        G.add_edge(1, 3, l="b", w=2)
        G.add_edge(1, 4, l="c", w=3)

        G.add_edge(2, 5, l="a", w=1)
        G.add_edge(3, 6, l="a", w=2)
        G.add_edge(4, 7, l="b", w=3)

        G.add_edge(5, 8, l="a", w=1)
        G.add_edge(6, 8, l="b", w=2)
        G.add_edge(7, 8, l="b", w=3)
    
        return G


    @staticmethod
    def __make_dfa_one():
        '''
        a*
        '''
        H = nx.DiGraph()

        H.add_edge(0, 0, l="a")
        
        return H


    def __make_dfa_two():
        '''
        (a|b)*
        '''
        H = nx.DiGraph()

        H.add_edge(0, 0, l=("a", "b"))

        return H


    def __make_dfa_three():
        '''
        de
        '''
        H = nx.DiGraph()

        H.add_edge(0, 1, l="d")
        H.add_edge(1, 2, l="e")

        return H


    def setUp(self):
        self.G = TestRegLinker.__make_G()
        self.dfa1 = TestRegLinker.__make_dfa_one()
        self.dfa2 = TestRegLinker.__make_dfa_two()
        self.dfa3 = TestRegLinker.__make_dfa_three()
        
    
    def test_RegLinker(self):
        results = rl.RegLinker(self.G, self.dfa1, [1], [8], [0], [0])
        for result in results:
            print(result)

        print("----")
        results = rl.RegLinker(self.G, self.dfa2, [1], [8], [0], [0])
        for result in results:
            print(result)

        print("----")
        results = rl.RegLinker(self.G, self.dfa3, [1], [8], [0], [0])
        for result in results:
            print(result)


if __name__ == '__main__':
    unittest.main()
