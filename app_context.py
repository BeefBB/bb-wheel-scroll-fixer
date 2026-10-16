"""Defines the application context for the WheelScrollFixer application."""

class AppContext:
    """A class to hold the application context."""
    def __init__(self, settings, hook, update_tray_icon_callback):
        self.settings = settings
        self.hook = hook
        self.update_tray_icon_callback = update_tray_icon_callback
