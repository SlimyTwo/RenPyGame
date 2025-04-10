import time

class GameState:
    """Base class for all states."""
    def run(self):
        raise NotImplementedError


class MainMenu(GameState):
    def run(self):
        print("Main Menu: [start] to begin, [settings] for settings, [quit] to exit")
        choice = input("> ").strip().lower()
        if choice == "start":
            return "gameplay"
        elif choice == "settings":
            return "settings"
        elif choice == "quit":
            return "exit"
        return "main_menu"


class SettingsMenu(GameState):
    def run(self):
        print("Settings Menu: [back] to return to main menu")
        input("> ")
        return "main_menu"


class Gameplay(GameState):
    def run(self):
        print("Playing the game... (pretend fun happens here)")
        time.sleep(1)
        print("Returning to main menu...")
        return "main_menu"


class GameStateManager:
    def __init__(self):
        self.states = {
            "main_menu": MainMenu(),
            "settings": SettingsMenu(),
            "gameplay": Gameplay()
        }
        self.current_state = "main_menu"

    def run(self):
        while self.current_state != "exit":
            state_obj = self.states[self.current_state]
            self.current_state = state_obj.run()


# Run the game state manager
if __name__ == "__main__":
    game = GameStateManager()
    game.run()
