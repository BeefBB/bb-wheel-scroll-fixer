"""Exercise wheel filtering without installing a system mouse hook."""
import ctypes
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from PySide6 import QtWidgets


PROJECT_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "wheel_scroll_fixer", PROJECT_ROOT / "bb-wheel-scroll-fixer.py"
)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)


class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = app_module.Settings.__new__(app_module.Settings)
        self.settings.data = {}
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.settings.json_path = str(Path(temp_dir.name) / "settings.json")


class SameDirectionFilterTests(SettingsTestCase):
    def setUp(self):
        super().setUp()
        self.user32 = Mock()
        self.user32.CallNextHookEx.return_value = 77
        self.user32.SetWindowsHookExA.return_value = 42
        self.user32.GetMessageA.return_value = 0
        kernel32 = Mock()
        kernel32.GetCurrentThreadId.return_value = 123
        with patch.object(
            app_module.ctypes,
            "windll",
            SimpleNamespace(user32=self.user32, kernel32=kernel32),
        ):
            self.hook = app_module.MouseHook(self.settings)
        self.hook._get_foreground_app_name = Mock(return_value="app.exe")
        self.hook.start()
        self.addCleanup(self.hook.stop)

    def emit(self, delta, timestamp):
        event = app_module.MSLLHOOKSTRUCT()
        event.mouseData = (delta & 0xFFFF) << 16
        with patch.object(app_module.time, "monotonic", return_value=timestamp):
            return self.hook.hook_cb(
                0, app_module.win32con.WM_MOUSEWHEEL, ctypes.addressof(event)
            )

    def test_short_same_direction_events_are_blocked_in_both_directions(self):
        for delta in (120, -120):
            with self.subTest(delta=delta):
                self.hook.last_dir = None
                self.assertEqual(self.emit(delta, 0.0), 77)
                self.assertEqual(self.emit(delta, 0.015), 1)

    def test_exact_minimum_interval_is_allowed(self):
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(120, 0.02), 77)

    def test_blocked_events_do_not_extend_the_wait(self):
        self.assertEqual(self.emit(120, 0.0), 77)
        for millisecond in range(1, 20):
            self.assertEqual(self.emit(120, millisecond / 1000), 1)
        self.assertEqual(self.emit(120, 0.02), 77)
        self.assertEqual(self.emit(120, 0.021), 1)
        self.assertEqual(self.emit(120, 0.04), 77)

    def test_zero_disables_same_direction_filtering(self):
        self.settings.set_min_same_direction_interval(0.0)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(120, 0.001), 77)

    def test_same_direction_interval_can_exceed_reversal_block_interval(self):
        self.settings.set_interval(0.05)
        self.settings.set_min_same_direction_interval(0.1)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(120, 0.06), 1)
        self.assertEqual(self.emit(120, 0.1), 77)

    def test_same_direction_interval_does_not_delay_reversals(self):
        self.settings.set_min_same_direction_interval(0.1)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(-120, 0.06), 77)

    def test_reversal_time_and_direction_change_threshold_still_apply(self):
        self.settings.set_direction_change_threshold(2)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(-120, 0.02), 1)
        self.assertEqual(self.emit(-120, 0.06), 1)
        self.assertEqual(self.emit(-120, 0.07), 77)
        self.assertEqual(self.emit(-120, 0.075), 1)
        self.assertEqual(self.emit(-120, 0.095), 77)

    def test_blocked_same_direction_event_interrupts_opposite_event_count(self):
        self.settings.set_min_same_direction_interval(0.1)
        self.settings.set_direction_change_threshold(2)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(-120, 0.06), 1)
        self.assertEqual(self.emit(120, 0.07), 1)
        self.assertEqual(self.emit(-120, 0.08), 1)
        self.assertEqual(self.emit(-120, 0.09), 77)

    def test_disabled_filter_and_blacklisted_apps_bypass_same_direction_block(self):
        self.assertEqual(self.emit(120, 0.0), 77)
        self.settings.set_enabled(False)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.001), 77)
        self.settings.set_enabled(True)
        self.settings.set_blacklist(["APP.EXE"])
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.002), 77)

    def test_reloaded_interval_takes_effect_without_restarting_hook(self):
        self.assertEqual(self.emit(120, 0.0), 77)
        self.assertEqual(self.emit(120, 0.015), 1)
        self.settings.set_min_same_direction_interval(0.01)
        self.hook.reload_settings()
        self.assertEqual(self.emit(120, 0.015), 77)
        self.user32.SetWindowsHookExA.assert_called_once()


class SameDirectionSettingsTests(SettingsTestCase):
    def test_existing_settings_use_default_and_new_value_survives_reload(self):
        self.assertEqual(self.settings.get_min_same_direction_interval(), 0.02)
        self.settings.set_min_same_direction_interval(0.03)
        self.settings.sync()
        self.settings.data = {}
        self.settings._load_settings()
        self.assertEqual(self.settings.get_min_same_direction_interval(), 0.03)


class SameDirectionDialogTests(SettingsTestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def setUp(self):
        super().setUp()
        self.hook = Mock()
        self.dialog = app_module.SettingsDialog(
            self.settings, self.hook, Mock(), Mock(return_value=True), lambda: False
        )
        self.addCleanup(self.dialog.deleteLater)

    def test_dialog_saves_ten_millisecond_precision_and_zero(self):
        self.assertEqual(self.dialog.same_direction_spin.value(), 0.02)
        self.dialog.same_direction_spin.stepUp()
        self.assertEqual(self.dialog.same_direction_spin.value(), 0.03)
        self.dialog.same_direction_spin.stepDown()
        self.assertEqual(self.dialog.same_direction_spin.value(), 0.02)
        for entered, expected in ((0.03, 0.03), (0.034, 0.03), (0.0, 0.0)):
            with self.subTest(entered=entered):
                self.dialog.same_direction_spin.setValue(entered)
                self.dialog.save(self.dialog.configure_startup)
                self.settings.data = {}
                self.settings._load_settings()
                self.assertEqual(self.settings.get_min_same_direction_interval(), expected)
        self.assertEqual(self.hook.reload_settings.call_count, 3)

    def test_restore_defaults_restores_same_direction_interval(self):
        self.dialog.same_direction_spin.setValue(0.1)
        with patch.object(
            QtWidgets.QMessageBox,
            "exec",
            return_value=QtWidgets.QMessageBox.StandardButton.Yes,
        ):
            self.dialog.restore_defaults()
        self.settings.data = {}
        self.settings._load_settings()
        self.assertEqual(self.dialog.same_direction_spin.value(), 0.02)
        self.assertEqual(self.settings.get_min_same_direction_interval(), 0.02)
        self.hook.reload_settings.assert_called_once()


if __name__ == "__main__":
    unittest.main()
