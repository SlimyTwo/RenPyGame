import os
import json

class SettingsManager:
    """Handles saving and loading game settings"""
    
    def __init__(self, settings_file="game_settings.json"):
        """Initialize the settings manager with default values"""
        # Base directory for settings file (same directory as the script)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.settings_file = os.path.join(self.base_dir, settings_file)
        
        # Default settings
        self.default_settings = {
            "music_volume": 100,
            "sfx_volume": 100,
            "music_enabled": True,
            "fullscreen": False,
            "fps_display": False
        }
        
        # Current settings (will be loaded from file if it exists)
        self.settings = self.default_settings.copy()
        
        # Load settings from file if it exists
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file, or create with defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                    # Update settings with loaded values
                    self.settings.update(loaded_settings)
                    
                    print(f"Settings loaded from {self.settings_file}")
            else:
                # Create settings file with defaults if it doesn't exist
                self.save_settings()
                print(f"Created new settings file with defaults at {self.settings_file}")
        except Exception as e:
            print(f"Error loading settings: {e}")
            # If there's an error, use defaults and try to save them
            self.settings = self.default_settings.copy()
            try:
                self.save_settings()
            except:
                print("Could not save default settings")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                print(f"Settings saved to {self.settings_file}")
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """Get a setting value by key, with optional default"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Set a setting value and save to file"""
        self.settings[key] = value
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()
