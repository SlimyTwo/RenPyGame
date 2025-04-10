# factory_pattern.py

from abc import ABC, abstractmethod

class Widget(ABC):
    """Abstract base class for different widget types."""
    @abstractmethod
    def render(self):
        pass


class Button(Widget):
    def render(self):
        print("Rendering a Button")


class Slider(Widget):
    def render(self):
        print("Rendering a Slider")


class WidgetFactory(ABC):
    """Abstract factory with a factory method."""
    @abstractmethod
    def create_widget(self) -> Widget:
        pass


class ButtonFactory(WidgetFactory):
    """Concrete factory for creating Button widgets."""
    def create_widget(self) -> Widget:
        return Button()


class SliderFactory(WidgetFactory):
    """Concrete factory for creating Slider widgets."""
    def create_widget(self) -> Widget:
        return Slider()


if __name__ == "__main__":
    # Example usage
    button_factory = ButtonFactory()
    slider_factory = SliderFactory()

    # The client uses factory objects to create widgets without specifying the exact class.
    btn = button_factory.create_widget()
    sld = slider_factory.create_widget()

    btn.render()  # "Rendering a Button"
    sld.render()  # "Rendering a Slider"
