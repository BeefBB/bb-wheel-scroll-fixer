# gui/about_dialog.py
"""The about dialog for the application."""
from PySide6 import QtWidgets, QtCore, QtGui
import os
from localization import translator

class AboutDialog(QtWidgets.QDialog):
    """The about dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setStyleSheet(QtWidgets.QApplication.instance().styleSheet())
        self.setWindowTitle(translator.tr("about_window_title"))
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "..", "mouse.ico")))
        self.setFixedSize(340, 210)

        layout = QtWidgets.QVBoxLayout(self)

        # app_name_label = QtWidgets.QLabel("<b>WheelScrollFixer</b>")
        app_name_label = QtWidgets.QLabel(translator.tr("about_qlabel"))
        app_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name_label)

        version_label = QtWidgets.QLabel(translator.tr("about_version"))
        version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        author_label = QtWidgets.QLabel(translator.tr("about_author"))
        author_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        description_label = QtWidgets.QLabel(translator.tr("about_description"))
        description_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Optimized: Use QLabel with OpenExternalLinks instead of full QTextBrowser
        website_label = QtWidgets.QLabel('<a href="https://github.com/BeefBB/bb-wheel-scroll-fixer" style="color: #f28c00; text-decoration: none;">GitHub專案網址</a>')
        website_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        website_label.setOpenExternalLinks(True)
        website_label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        layout.addWidget(website_label)

        ok_button = QtWidgets.QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
