# builder_pattern.py

class Character:
    """Complex object that is built step-by-step."""
    def __init__(self):
        self.name = None
        self.strength = 0
        self.agility = 0
        self.intelligence = 0

    def __str__(self):
        return f"{self.name} (Str: {self.strength}, Agi: {self.agility}, Int: {self.intelligence})"


class CharacterBuilder:
    """Abstract builder interface for building Character objects."""
    def __init__(self):
        self.character = Character()

    def set_name(self, name):
        self.character.name = name
        return self  # returning self allows chaining

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
        return self.character

    def build(self):
        built_character = self.character
        self.character = Character()  # re-initialize default vales for next usage
        return built_character


class CharacterDirector:
    """Optional director class orchestrates the building steps."""
    def __init__(self, builder):
        self.builder = builder

    def create_knight(self):
        return (self.builder
                .set_name("Knight")
                .set_strength(15)
                .set_agility(5)
                .set_intelligence(4)
                .build())

    def create_archer(self):
        return (self.builder
                .set_name("Archer")
                .set_strength(5)
                .set_agility(14)
                .set_intelligence(6)
                .build())

    def create_mage(self):
        return (self.builder
                .set_name("Mage")
                .set_strength(4)
                .set_agility(5)
                .set_intelligence(18)
                .build())


if __name__ == "__main__":
    builder = CharacterBuilder()
    director = CharacterDirector(builder)

    knight = director.create_knight()
    print(knight)  # Knight (Str: 15, Agi: 5, Int: 4)

    mage = director.create_mage()
    print(mage)    # Mage (Str: 4, Agi: 5, Int: 18)

    # Using the builder directly to create a custom character
    custom_builder = CharacterBuilder()
    alex = (custom_builder
            .set_name("Alex's Custom Character")
            .set_strength(1)
            .set_agility(2)
            .set_intelligence(3)
            .build())
    print(alex)

    nico = (builder
            .set_name("Nico's Custom Character")
            .set_strength(10)
            .set_agility(20)
            .build())
    print(nico)

