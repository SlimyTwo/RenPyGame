"""Module for managing game audio."""
import os
import json
import pygame
from typing import Dict, Any, Optional

class SettingsManager:
    """Manages persistent game settings."""

    def __init__(self, settings_path="settings.json"):
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings()

    def load_settings(self) -> None:
        """Load settings from file if it exists."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = {}  # Use defaults on error

    def save_settings(self) -> bool:
        """Save settings to file."""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value by key, with optional default."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> bool:
        """Set a setting value and save."""
        self.settings[key] = value
        return self.save_settings()

class MusicManager:
    """Manages background music and sound effects."""

    def __init__(self):
        # Ensure mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Volume settings (0.0 to 1.0)
        self.settings_manager = SettingsManager()
        self.music_volume = self.settings_manager.get_setting("music_volume", 0.5)
        self.sound_volume = self.settings_manager.get_setting("sound_volume", 0.7)
        self.current_music = None
        pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, music_path: str, loops: int = -1) -> None:
        """Play background music. Loops forever by default."""
        if not music_path or not os.path.exists(music_path):
            print(f"Music file not found: {music_path}")
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops)
            self.current_music = music_path
        except Exception as e:
            print(f"Error playing music: {e}")

    def stop_music(self) -> None:
        """Stop currently playing music."""
        pygame.mixer.music.stop()
        
    def pause_music(self) -> None:
        """Pause currently playing music."""
        pygame.mixer.music.pause()
        
    def resume_music(self) -> None:
        """Resume paused music."""
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0) and save to settings."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        self.settings_manager.set_setting("music_volume", self.music_volume)

    def set_sound_volume(self, volume: float) -> None:
        """Set sound effect volume (0.0 to 1.0) and save to settings."""
        self.sound_volume = max(0.0, min(1.0, volume))
        self.settings_manager.set_setting("sound_volume", self.sound_volume)

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        """Play a sound effect."""
        if sound:
            sound.set_volume(self.sound_volume)
            sound.play()
