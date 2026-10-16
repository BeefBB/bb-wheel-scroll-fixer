# gui/help_dialog.py
"""The help dialog for the application."""
from PyQt5 import QtWidgets, QtGui, QtCore
import os
from localization import translator

class HelpDialog(QtWidgets.QDialog):
    """The help dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Microsoft JhengHei', sans-serif;
                font-size: 11pt;
            }
            QTextBrowser {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4d4d4d; }
            QPushButton:pressed { background-color: #2d2d2d; }
        """)
        self.setWindowTitle(translator.tr("help_window_title"))
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "..", "mouse.ico")))
        self.setMinimumSize(580, 460)

        layout = QtWidgets.QVBoxLayout(self)
        text_browser = QtWidgets.QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.document().setDefaultStyleSheet("""
            body { background-color: #1e1e1e; color: #e0e0e0; }
            h1, h2 { color: #f28c00; }
            code { color: #f0b35a; background-color: #333333; }
        """)

        text_browser.setHtml(translator.tr("help_content"))
        layout.addWidget(text_browser)

        close_button = QtWidgets.QPushButton(translator.tr("btn_close"))
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
