import pygame
import os


class MusicManager:
    def __init__(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Volume settings (0.0 to 1.0)
        self.music_volume = 0.7  # Default music volume
        self.sfx_volume = 0.7  # Default sound effects volume

        # Track current music
        self.current_music = None
        self.is_music_paused = False

    def play_music(self, music_path, loops=-1, fade_ms=500):
        """Play background music with optional looping and fade-in"""
        if not os.path.exists(music_path):
            print(f"Warning: Music file not found: {music_path}")
            return False

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = music_path
            self.is_music_paused = False
            return True
        except Exception as e:
            print(f"Error playing music: {e}")
            return False

    def stop_music(self, fade_ms=500):
        """Stop the currently playing music with optional fade-out"""
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None
        self.is_music_paused = False

    def pause_music(self):
        """Pause the currently playing music"""
        if self.is_playing():
            pygame.mixer.music.pause()
            self.is_music_paused = True

    def unpause_music(self):
        """Unpause the music if it's paused"""
        if self.is_music_paused:
            pygame.mixer.music.unpause()
            self.is_music_paused = False

    def is_playing(self):
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy()

    def get_volume(self):
        """Get the current music volume"""
        return self.music_volume

    def set_volume(self, volume):
        """Set the music volume (0.0 to 1.0)"""
        # Ensure volume is between 0 and 1
        volume = max(0.0, min(1.0, volume))
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_music_volume(self, volume):
        """Alias for set_volume for clarity"""
        self.set_volume(volume)

    def get_sfx_volume(self):
        """Get the current sound effects volume"""
        return self.sfx_volume

    def set_sfx_volume(self, volume):
        """Set the sound effects volume (0.0 to 1.0)"""
        # Ensure volume is between 0 and 1
        volume = max(0.0, min(1.0, volume))
        self.sfx_volume = volume

    def play_sound(self, sound, volume=None):
        """Play a sound effect with proper volume"""
        if sound:
            # Use specific volume if provided, otherwise use default sfx volume
            play_volume = volume if volume is not None else self.sfx_volume
            sound.set_volume(play_volume)
            sound.play()

    def load_sound(self, sound_path):
        """Load a sound file with error handling"""
        if not os.path.exists(sound_path):
            print(f"Warning: Sound file not found: {sound_path}")
            return None

        try:
            return pygame.mixer.Sound(sound_path)
        except Exception as e:
            print(f"Error loading sound: {e}")
            return None