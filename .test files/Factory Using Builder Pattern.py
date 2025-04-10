# factory_with_builder.py

from abc import ABC, abstractmethod

class Car:
    def __init__(self):
        self.make = None
        self.model = None
        self.color = None
        self.features = []

    def __str__(self):
        return f"{self.color} {self.make} {self.model} with features: {', '.join(self.features)}"


class CarBuilder(ABC):
    """Abstract builder interface for constructing a Car."""
    def __init__(self):
        self.car = Car()

    @abstractmethod
    def set_make_and_model(self):
        pass

    def set_color(self, color):
        self.car.color = color
        return self

    def add_feature(self, feature):
        self.car.features.append(feature)
        return self

    def build(self):
        return self.car


class EconomyCarBuilder(CarBuilder):
    def set_make_and_model(self):
        self.car.make = "Econo Motors"
        self.car.model = "Basic"
        return self


class LuxuryCarBuilder(CarBuilder):
    def set_make_and_model(self):
        self.car.make = "Luxury Co."
        self.car.model = "Elite"
        return self


class CarBuilderFactory:
    """
    Factory that returns a CarBuilder instance.
    This allows us to pick a builder (Economy vs. Luxury) at runtime
    without exposing the client to the details of each builder type.
    """
    @staticmethod
    def get_car_builder(car_type: str) -> CarBuilder:
        if car_type == "economy":
            return EconomyCarBuilder()
        elif car_type == "luxury":
            return LuxuryCarBuilder()
        else:
            raise ValueError(f"Unknown car_type '{car_type}'")


if __name__ == "__main__":
    # Client code asks for a builder from the factory.
    eco_builder = CarBuilderFactory.get_car_builder("economy")
    # Then configures the car via the builder methods.
    eco_car = (eco_builder
               .set_make_and_model()
               .set_color("Blue")
               .add_feature("Air Conditioning")
               .build())
    print(eco_car)  # Blue Econo Motors Basic with features: Air Conditioning

    lux_builder = CarBuilderFactory.get_car_builder("luxury")
    lux_car = (lux_builder
               .set_make_and_model()
               .set_color("Gold")
               .add_feature("Leather Seats")
               .add_feature("Panoramic Sunroof")
               .build())
    print(lux_car)  # Gold Luxury Co. Elite with features: Leather Seats, Panoramic Sunroof
