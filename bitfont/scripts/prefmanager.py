#!/usr/bin/env python3

"""Classes for managing preferences, saving, loading, defaults, for the editor."""

import json
from pathlib import Path
from typing import Any

# Default preferences when json file is gone or corrupted.
DEFAULT_PREFERENCES = {
    "Version": "0.1",
    "Resolution": (800, 600),
    "Font": "CP437_12x12.png",
    "FPS": 0,
    "MenuBar": ("Bitfont", "File", "Edit", "Help")
}


class PreferenceManager:
    def __init__(self):
        # Get path to the preferences file.
        self.path = Path() / "preferences.json"
        # If the file does not exist, use the default preferences.
        if not self.path.exists():
            self.preferences = DEFAULT_PREFERENCES
        # Otherwise, load in the preferences from the file.
        else:
            with open(self.path) as pref_file:
                self.preferences = json.load(pref_file)

    def __getitem__(self, item: Any) -> Any:
        """Get a preference, if not found, give the default preference."""
        try:
            return self.preferences[item]
        except KeyError:
            return DEFAULT_PREFERENCES[item]

    def __setitem__(self, key: Any, value: Any):
        """Update preference to new value."""
        self.preferences[key] = value

    def save(self):
        """Save the current preferences to the json file."""
        with open(self.path, 'w') as pref_file:
            json.dump(self.preferences, pref_file)
