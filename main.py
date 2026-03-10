import sys
from PySide6.QtWidgets import QApplication
from ui.tree_visualizer import AVLVisualizer


app = QApplication(sys.argv)

window = AVLVisualizer()
window.show()

sys.exit(app.exec())