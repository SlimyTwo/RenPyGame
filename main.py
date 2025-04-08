"""Main entry point for the game."""
from engine.game import Game
import sys

def main():
    """Initialize and run the game."""
    try:
        print("Entering main function...")
        print("Starting Fantasy Falls...")
        
        # Create and initialize game
        game = Game().initialize()
        
        # Run the main menu
        game.run_main_menu()
        
        # Clean up
        game.quit()
        print("Exiting main function...")
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        
        # Keep the window open on error for debugging
        input("Press Enter to close...")
        sys.exit(1)

if __name__ == "__main__":
    main()

#test