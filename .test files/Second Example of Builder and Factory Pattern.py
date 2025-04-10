from abc import ABC, abstractmethod

class Character:
    """Complex object that is built step-by-step."""
    def __init__(self):
        self.name = None
        self.strength = 0
        self.agility = 0
        self.intelligence = 0

    def __str__(self):
        return f"{self.name} (Str: {self.strength}, Agi: {self.agility}, Int: {self.intelligence})\n"


class CharacterBuilder(ABC):
    """
    Abstract builder interface for building Character objects.
    In Python, you don't always need ABC, but let's do so here
    to show how you'd enforce subclass overrides if you wanted.
    """
    def __init__(self):
        self.character = Character()

    def set_name(self, name):
        self.character.name = name
        return self

    def set_strength(self, value):
        self.character.strength = value
        return self

    def set_agility(self, value):
        self.character.agility = value
        return self

    def set_intelligence(self, value):
        self.character.intelligence = value
        return self

    def build(self):
        """Build the character, then reset the internal state for next usage."""
        built_character = self.character
        self.character = Character()  # re-initialize for future builds
        return built_character

    @abstractmethod
    def apply_preset(self):
        """
        Optional: a specialized builder can override this to set default stats
        (like Knight, Archer, Mage). If not used, can remain abstract or do nothing.
        """
        pass


class KnightBuilder(CharacterBuilder):
    def apply_preset(self):
        # If you want to chain right away, do it in the method itself
        self.set_name("Knight")
        self.set_strength(15)
        self.set_agility(5)
        self.set_intelligence(4)
        return self


class ArcherBuilder(CharacterBuilder):
    def apply_preset(self):
        self.set_name("Archer")
        self.set_strength(5)
        self.set_agility(14)
        self.set_intelligence(6)
        return self


class MageBuilder(CharacterBuilder):
    def apply_preset(self):
        self.set_name("Mage")
        self.set_strength(4)
        self.set_agility(5)
        self.set_intelligence(18)
        return self


class GenericCharacterBuilder(CharacterBuilder):
    """
    This subclass can be used as a 'do-it-yourself' builder
    without a preset (or with an optional apply_preset).
    """
    def apply_preset(self):
        # In this example, do nothing by default
        return self


class CharacterBuilderFactory:
    """
    Factory that returns a specialized CharacterBuilder instance.
    This lets you pick the right builder at runtime, without exposing
    each builder subclass to the client.
    """
    @staticmethod
    def get_builder(builder_type: str) -> CharacterBuilder:
        if builder_type.lower() == "knight":
            return KnightBuilder()
        elif builder_type.lower() == "archer":
            return ArcherBuilder()
        elif builder_type.lower() == "mage":
            return MageBuilder()
        else:
            # Default or fallback: the user can do their own settings
            return GenericCharacterBuilder()


if __name__ == "__main__":
    # 1) Knight from factory
    knight_builder = CharacterBuilderFactory.get_builder("knight")
    knight = knight_builder.apply_preset().build()
    print(knight)
    # Output: Knight (Str: 15, Agi: 5, Int: 4)

    # 2) Archer from factory, with a name tweak
    archer_builder = CharacterBuilderFactory.get_builder("archer")
    archer = (archer_builder
              .apply_preset()
              .set_name("Elite Archer")
              .build())
    print(archer)
    # Output: Elite Archer (Str: 5, Agi: 14, Int: 6)

    # 3) Mage from factory, no changes
    mage_builder = CharacterBuilderFactory.get_builder("mage")
    mage = mage_builder.apply_preset().build()
    print(mage)
    # Output: Mage (Str: 4, Agi: 5, Int: 18)

    # 4) Use the "generic" builder for a custom character
    custom_builder = CharacterBuilderFactory.get_builder("custom")
    custom_char = (custom_builder
                   .set_name("Heroic Adventurer")
                   .set_strength(20)
                   .set_agility(10)
                   .set_intelligence(7)
                   .build())
    print(custom_char)
    # Output: Heroic Adventurer (Str: 20, Agi: 10, Int: 7)

    # 5) Build multiple characters from the same builder
    #    Because .build() resets the builder's character to a new instance each time.
    multi_builder = CharacterBuilderFactory.get_builder("knight")
    first_knight = multi_builder.apply_preset().build()
    second_knight = (multi_builder
                     .apply_preset()
                     .set_name("Champion Knight")
                     .build())
    print(first_knight)
    # Output: Knight (Str: 15, Agi: 5, Int: 4)
    print(second_knight)
    # Output: Champion Knight (Str: 15, Agi: 5, Int: 4)