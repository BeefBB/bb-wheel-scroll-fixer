"""Settings dialog for the WheelScrollFixer application."""
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from localization import translator
from utils import get_foreground_process_name

class ModernSettingsDialog(QtWidgets.QDialog):
    """The main settings dialog for the application, redesigned."""

    def __init__(self, settings, hook, update_tray_icon_callback, configure_startup):
        super().__init__()
        self.settings = settings
        self.hook = hook
        self.update_tray_icon_callback = update_tray_icon_callback
        self.configure_startup = configure_startup
        
        self._init_ui()

    def _init_ui(self):
        """Initializes the user interface."""
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Scroll Lock Settings')
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "..", "mouse.ico")))
        
        # Load geometry or set default
        self.qt_settings = QtCore.QSettings("MetheTech", "WheelScrollFixer")
        if self.qt_settings.value("geometry"):
            self.restoreGeometry(self.qt_settings.value("geometry"))
            self.resize(min(self.width(), 700), max(self.height(), 900))
        else:
            self.resize(700, 900)

        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #ffffff; font-family: 'Microsoft JhengHei', sans-serif; font-size: 11pt; }
            QLabel { color: #e0e0e0; }
            QGroupBox { border: 1px solid #3d3d3d; border-radius: 6px; margin-top: 24px; background-color: #252525; padding-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; left: 10px; color: #f28c00; font-weight: bold; }
            
            /* Buttons */
            QPushButton { background-color: #3d3d3d; color: #ffffff; border: none; border-radius: 4px; padding: 8px 16px; font-weight: bold; font-size: 11pt; }
            QPushButton:hover { background-color: #4d4d4d; }
            QPushButton:pressed { background-color: #2d2d2d; }
            QPushButton#primary { background-color: #f28c00; }
            QPushButton#primary:hover { background-color: #e98200; }
            /* Inputs */
            QSpinBox, QDoubleSpinBox { background-color: #333; border: 1px solid #444; border-radius: 4px; padding: 6px; color: #fff; font-size: 11pt; min-height: 20px; }
            
            /* Checkbox */
            QCheckBox { spacing: 8px; color: #eee; font-size: 11pt; }
            QCheckBox::indicator { width: 20px; height: 20px; border: 1px solid #555; border-radius: 3px; background: #333; }
            QCheckBox::indicator:checked { background-color: #f28c00; border-color: #f28c00; }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(24, 20, 24, 20)
        self.content_layout.setSpacing(14)
        
        self.page_title = QtWidgets.QLabel("")
        self.page_title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #fff;")
        self.content_layout.addWidget(self.page_title)
        
        # Divider
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("background-color: #333;")
        self.content_layout.addWidget(line)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { background-color: #1e1e1e; }")
        self.scroll_area.viewport().setStyleSheet("background-color: #1e1e1e;")
        self.settings_content = QtWidgets.QWidget()
        self.settings_content.setStyleSheet("background-color: #1e1e1e;")
        self.settings_layout = QtWidgets.QVBoxLayout(self.settings_content)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_layout.setSpacing(16)
        self._create_settings_groups()
        self.settings_layout.addStretch()
        self.scroll_area.setWidget(self.settings_content)
        self.content_layout.addWidget(self.scroll_area, 1)

        # Footer
        self.footer_layout = QtWidgets.QHBoxLayout()
        
        self.defaults_btn = QtWidgets.QPushButton("")
        self.defaults_btn.clicked.connect(self.restore_defaults)
        self.defaults_btn.setMinimumHeight(40)
        
        self.save_btn = QtWidgets.QPushButton("")
        self.save_btn.setObjectName("primary")
        self.save_btn.clicked.connect(lambda: self.save(self.configure_startup))
        self.save_btn.setMinimumWidth(150)
        self.save_btn.setMinimumHeight(40)

        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")

        self.footer_layout.addWidget(self.defaults_btn)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.status_label)
        self.footer_layout.addSpacing(15)
        self.footer_layout.addWidget(self.save_btn)
        
        self.content_layout.addLayout(self.footer_layout)
        self.main_layout.addWidget(self.content_area)
        
        # Initial Translation
        self.retranslate_ui()

    def _create_settings_groups(self):
        grp_logic = QtWidgets.QGroupBox("")
        self.grp_logic = grp_logic
        form_logic = QtWidgets.QFormLayout()
        form_logic.setSpacing(15)
        form_logic.setContentsMargins(15, 25, 15, 15)
        
        self.interval_spin = QtWidgets.QDoubleSpinBox()
        self.interval_spin.setRange(0.05, 5.0)
        self.interval_spin.setValue(self.settings.get_interval())
        self.interval_lbl = QtWidgets.QLabel("")
        
        self.threshold_spin = QtWidgets.QSpinBox()
        self.threshold_spin.setRange(1, 10)
        self.threshold_spin.setValue(self.settings.get_direction_change_threshold())
        self.threshold_lbl = QtWidgets.QLabel("")
        
        self.reversal_spin = QtWidgets.QDoubleSpinBox()
        self.reversal_spin.setRange(0.01, 0.20)
        self.reversal_spin.setValue(self.settings.get_min_reversal_interval())
        self.reversal_lbl = QtWidgets.QLabel("")
        
        form_logic.addRow(self.interval_lbl, self.interval_spin)
        form_logic.addRow(self.threshold_lbl, self.threshold_spin)
        form_logic.addRow(self.reversal_lbl, self.reversal_spin)
        grp_logic.setLayout(form_logic)
        
        self.settings_layout.addWidget(grp_logic, alignment=QtCore.Qt.AlignTop)

        # Application Control Group
        grp_app = QtWidgets.QGroupBox("")
        self.grp_app = grp_app
        layout_grp_app = QtWidgets.QVBoxLayout()
        layout_grp_app.setContentsMargins(15, 25, 15, 15)

        # Blacklist
        self.lbl_bl = QtWidgets.QLabel("")
        self.bl_list = QtWidgets.QListWidget()
        self.bl_list.setStyleSheet(
            "QListWidget { background-color: #333333; color: #ffffff; "
            "border: 1px solid #555555; }"
            "QListWidget::item { color: #ffffff; }"
            "QListWidget::item:selected { background-color: #f28c00; color: #ffffff; }"
        )
        self.bl_list.addItems(self.settings.get_blacklist())
        self.bl_list.setFixedHeight(120)
        
        bl_btns = QtWidgets.QHBoxLayout()
        self.btn_bl_add = QtWidgets.QPushButton("")
        self.btn_bl_add.clicked.connect(self.add_current_app_to_blacklist)
        self.btn_bl_rem = QtWidgets.QPushButton("")
        self.btn_bl_rem.clicked.connect(self.remove_selected_from_blacklist)
        self.btn_bl_clr = QtWidgets.QPushButton("")
        self.btn_bl_clr.clicked.connect(self.clear_blacklist)
        for button in (self.btn_bl_add, self.btn_bl_rem, self.btn_bl_clr):
            button.setStyleSheet(
                "QPushButton { background-color: #f28c00; color: #ffffff; }"
                "QPushButton:hover { background-color: #e98200; }"
                "QPushButton:pressed { background-color: #cc6600; }"
            )
        bl_btns.addWidget(self.btn_bl_add)
        bl_btns.addWidget(self.btn_bl_rem)
        bl_btns.addWidget(self.btn_bl_clr)
        
        layout_grp_app.addWidget(self.lbl_bl)
        layout_grp_app.addWidget(self.bl_list)
        layout_grp_app.addLayout(bl_btns)
        
        grp_app.setLayout(layout_grp_app)
        self.settings_layout.addWidget(grp_app, alignment=QtCore.Qt.AlignTop)

        grp_sys = QtWidgets.QGroupBox("")
        self.grp_sys = grp_sys
        form_gen = QtWidgets.QVBoxLayout()
        form_gen.setContentsMargins(15, 25, 15, 15)
        form_gen.setSpacing(15)
        
        self.enabled_cb = QtWidgets.QCheckBox('')
        self.enabled_cb.setChecked(self.settings.get_enabled())
        
        self.start_cb = QtWidgets.QCheckBox("")
        self.start_cb.setChecked(self.settings.get_startup())
        
        form_gen.addWidget(self.enabled_cb)
        form_gen.addWidget(self.start_cb)
        grp_sys.setLayout(form_gen)
        
        self.settings_layout.addWidget(grp_sys, alignment=QtCore.Qt.AlignTop)

    def retranslate_ui(self):
        tr = translator.tr
        self.setWindowTitle(tr("window_title"))
        self.page_title.setText(tr("window_title"))

        # Sensitivity settings
        self.grp_logic.setTitle(tr("grp_blocking"))
        self.interval_lbl.setText(tr("lbl_interval"))
        self.interval_spin.setToolTip(tr("tip_interval"))
        self.threshold_lbl.setText(tr("lbl_threshold"))
        self.threshold_spin.setToolTip(tr("tip_threshold"))
        self.reversal_lbl.setText(tr("lbl_min_reversal"))
        self.reversal_spin.setToolTip(tr("tip_min_reversal"))
        
        # Blacklist settings
        self.grp_app.setTitle(tr("grp_app_control"))
        self.lbl_bl.setText(tr("lbl_blacklist"))
        self.btn_bl_add.setText(tr("btn_add_current"))
        self.btn_bl_rem.setText(tr("btn_remove_selected"))
        self.btn_bl_clr.setText(tr("btn_clear_all"))

        # General settings
        self.grp_sys.setTitle(tr("grp_system"))
        self.enabled_cb.setText(tr("chk_enable"))
        self.enabled_cb.setToolTip(tr("tip_enable"))
        self.start_cb.setText(tr("chk_start_boot"))
        self.start_cb.setToolTip(tr("tip_start_boot"))
        
        # Footer
        self.defaults_btn.setText(tr("btn_defaults"))
        self.save_btn.setText(tr("btn_save"))

    # --- Logic Methods ---
    def save(self, configure_startup):
        self.settings.set_interval(self.interval_spin.value())
        bl = [self.bl_list.item(i).text() for i in range(self.bl_list.count())]
        self.settings.set_blacklist(bl)
        self.settings.set_startup(self.start_cb.isChecked())
        configure_startup(self.start_cb.isChecked())
        self.settings.set_enabled(self.enabled_cb.isChecked())
        self.settings.set_direction_change_threshold(self.threshold_spin.value())
        self.settings.set_min_reversal_interval(self.reversal_spin.value())
        self.settings.sync()
        self.hook.reload_settings(self.update_tray_icon_callback)
        self.status_label.setText(translator.tr("status_saved"))
        QtCore.QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def restore_defaults(self):
        reply = QtWidgets.QMessageBox.question(self, translator.tr("msg_reset_title"), translator.tr("msg_reset_text"), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.interval_spin.setValue(0.05)
            self.threshold_spin.setValue(1)
            self.reversal_spin.setValue(0.05)
            self.enabled_cb.setChecked(True)
            self.resize(700, 900)
            self.save_btn.click()
            self.status_label.setText(translator.tr("status_restored"))

    def add_current_app_to_blacklist(self):
        self.hide()
        QtCore.QTimer.singleShot(120, self._get_and_add_foreground_app)

    def _get_and_add_foreground_app(self):
        proc_name = get_foreground_process_name()
        existing = [self.bl_list.item(i).text() for i in range(self.bl_list.count())]
        if proc_name and proc_name not in existing: self.bl_list.addItem(proc_name)
        self.show()

    def remove_selected_from_blacklist(self):
        for item in self.bl_list.selectedItems(): self.bl_list.takeItem(self.bl_list.row(item))

    def clear_blacklist(self):
        self.bl_list.clear()

    def closeEvent(self, event): 
        self.qt_settings.setValue("geometry", self.saveGeometry())
        self.hide()
        event.ignore()

# Aliasing for compatibility
SettingsDialog = ModernSettingsDialog
