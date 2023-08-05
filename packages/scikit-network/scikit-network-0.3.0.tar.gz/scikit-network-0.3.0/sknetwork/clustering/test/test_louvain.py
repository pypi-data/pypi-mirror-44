#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for louvain.py"""


import unittest
from sknetwork.clustering import *
from sknetwork.toy_graphs import *
from scipy.sparse import identity


class TestLouvainClustering(unittest.TestCase):

    def setUp(self):
        self.louvain = Louvain()
        self.louvain_high_resolution = Louvain(GreedyModularity(engine='python', resolution=2))
        self.louvain_numba = Louvain(GreedyModularity(engine='numba'))
        self.karate_club_graph = karate_club_graph()

    def test_unknown_types(self):
        with self.assertRaises(TypeError):
            self.louvain.fit(identity(1))

        with self.assertRaises(TypeError):
            self.louvain.fit(identity(2, format='csr'), node_weights=1)

    def test_unknown_options(self):
        with self.assertRaises(ValueError):
            self.louvain.fit(identity(2, format='csr'), node_weights='unknown')

    def test_single_node_graph(self):
        self.assertEqual(self.louvain.fit(identity(1, format='csr')).labels_, [0])

    def test_karate_club_graph(self):
        labels = self.louvain.fit(self.karate_club_graph).labels_
        self.assertEqual(labels.shape, (34,))
        self.assertAlmostEqual(modularity(self.karate_club_graph, labels), 0.42, 2)
        labels = self.louvain_numba.fit(self.karate_club_graph).labels_
        self.assertEqual(labels.shape, (34,))
        self.assertAlmostEqual(modularity(self.karate_club_graph, labels), 0.42, 2)
        labels = self.louvain_high_resolution.fit(self.karate_club_graph).labels_
        self.assertEqual(labels.shape, (34,))
        self.assertAlmostEqual(modularity(self.karate_club_graph, labels), 0.34, 2)

