#!/usr/bin/env python3
"""
Here we provide the necessary imports.
The basic GUI widgets are located in QtWidgets module.
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

# Every PyQt application must create an application object.
# The application object is located in the QtWidgets module.
app = QApplication([])

# The QWidget widget is the base class of all user interface objects in PyQt.
# We provide the default constructor for QWidget. The default constructor has no parent.
# A widget with no parent is called a window.
window = QWidget()

window.resize(320, 240)  # The resize() method resizes the widget.
window.setWindowTitle("Hello, World!")  # Here we set the title for our window.
label = QLabel("Hello, world!", window)
button = QPushButton("Click me", window)
window.show()  # The show() method displays the widget on the screen.


sys.exit(app.exec())  # Finally, we enter the mainloop of the application.