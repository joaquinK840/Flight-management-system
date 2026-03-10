import sys
import matplotlib.pyplot as plt
import networkx as nx

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QLabel
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.structures.avl_tree.tree import AVL
from core.structures.node.node import Node


class AVLVisualizer(QWidget):

    def __init__(self):
        super().__init__()

        self.avl = AVL()

        self.setWindowTitle("AVL Tree Visualizer")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Insertar valor")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.button = QPushButton("Insertar")
        self.button.clicked.connect(self.insert_value)
        layout.addWidget(self.button)

        # Figura de matplotlib embebida
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def insert_value(self):

        try:
            value = int(self.input.text())
        except:
            return

        self.avl.insert(Node(value))
        self.input.clear()

        self.draw_tree()

    def draw_tree(self):

        root = self.avl.getRoot()

        self.figure.clear()

        if root is None:
            self.canvas.draw()
            return

        G = nx.DiGraph()
        pos = {}

        self.build_graph(G, pos, root, 0, 0, 1)

        ax = self.figure.add_subplot(111)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2000,
            node_color="lightblue",
            font_size=10,
            ax=ax
        )

        self.canvas.draw()

    def build_graph(self, G, pos, node, x, y, layer):

        if node is None:
            return

        value = node.getValue()

        G.add_node(value)
        pos[value] = (x, -y)

        if node.getLeftChild():

            left = node.getLeftChild().getValue()

            G.add_edge(value, left)

            self.build_graph(
                G,
                pos,
                node.getLeftChild(),
                x - 1 / layer,
                y + 1,
                layer + 1
            )

        if node.getRightChild():

            right = node.getRightChild().getValue()

            G.add_edge(value, right)

            self.build_graph(
                G,
                pos,
                node.getRightChild(),
                x + 1 / layer,
                y + 1,
                layer + 1
            )