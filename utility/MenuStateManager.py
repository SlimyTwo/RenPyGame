import enum

class MenuState(enum.Enum):
    """Enum defining all possible menu states in the game"""
    MAIN_MENU = 0
    SETTINGS = 1
    GAME = 2
    LOAD_GAME = 3
    CREDITS = 4
    QUIT = 5


class MenuStateManager:
    """Manages menu state transitions and stack-based navigation"""
    
    def __init__(self, initial_state=MenuState.MAIN_MENU):
        """Initialize the state manager with an initial state"""
        self.current_state = initial_state
        self.state_stack = [initial_state]  # Stack for navigation history
        self.transition_callbacks = {}
        
    def get_current_state(self):
        """Get the current menu state"""
        return self.current_state
    
    def change_state(self, new_state):
        """
        Change to a new menu state
        
        Args:
            new_state: The MenuState to transition to
        
        Returns:
            bool: True if state changed successfully
        """
        previous_state = self.current_state
        self.current_state = new_state
        self.state_stack.append(new_state)
        
        # Call transition callback if registered
        if (previous_state, new_state) in self.transition_callbacks:
            self.transition_callbacks[(previous_state, new_state)]()
            
        return True
    
    def go_back(self):
        """
        Return to the previous state in the navigation stack
        
        Returns:
            bool: True if successfully went back, False if at root state
        """
        # Cannot go back if we're at the root state or have only one state
        if len(self.state_stack) <= 1:
            return False
        
        # Remove current state
        self.state_stack.pop()
        
        # Set current state to the previous one
        previous_state = self.current_state
        self.current_state = self.state_stack[-1]
        
        # Call transition callback if registered
        if (previous_state, self.current_state) in self.transition_callbacks:
            self.transition_callbacks[(previous_state, self.current_state)]()
            
        return True
    
    def register_transition_callback(self, from_state, to_state, callback):
        """
        Register a callback function to be called on specific state transition
        
        Args:
            from_state: The origin MenuState
            to_state: The destination MenuState
            callback: Function to call when this transition occurs
        """
        self.transition_callbacks[(from_state, to_state)] = callback
    
    def clear_stack(self):
        """Reset navigation stack to only contain the current state"""
        self.state_stack = [self.current_state]
