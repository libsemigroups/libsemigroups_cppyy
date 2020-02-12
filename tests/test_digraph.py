import unittest, libsemigroups_cppyy
from libsemigroups_cppyy import ActionDigraph

class TestActionDigraph(unittest.TestCase):
    def test_action_digraph(self):
        D = ActionDigraph(4)
        D.add_to_out_degree(1)
        self.assertEqual(D.out_degree(), 1)
        self.assertEqual(D.nr_nodes(), 4)
        self.assertEqual(D.validate(), False)
        for i in range(4):
            D.add_edge(i, (i + 1) % 4, 0)
        self.assertEqual(D.validate(), True)
        self.assertEqual(D.nr_edges(), 4)
        self.assertEqual(D.nr_scc(), 1)
