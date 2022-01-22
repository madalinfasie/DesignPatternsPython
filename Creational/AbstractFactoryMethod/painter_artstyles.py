"""
A painter learned how to make digital art and how to paint physical paintings.
He now wants to sell his artwork on his personal website.

Knowing that each client might like different art styles, he now offers
the option of choosing the art style of the artwork.

His art syles are: minimalism and surrealism

The clients will enter the website and send an order request for one
painting medium (physical or digital) and one art style
and the painter will draw it for them.
"""
import abc
import enum

#### Utilities ####
class OrderType(enum.Enum):
    PAINTING_ORDER = enum.auto()
    DIGITAL_ORDER = enum.auto()


class UnknownPaintingStyle(Exception):
    pass


#### Products ####
class PhysicalArt(abc.ABC):
    @abc.abstractmethod
    def display(self) -> None:
        pass


class DigitalArt(abc.ABC):
    @abc.abstractmethod
    def display(self) -> None:
        pass


class SurrealPhysicalArt(PhysicalArt):
    def display(self) -> None:
        print("Melted watches on a field on canvas")


class MinimalismPhysicalArt(PhysicalArt):
    def display(self) -> None:
        print("Single drop of water on canvas")


class SurrealDigitalArt(DigitalArt):
    def display(self) -> None:
        print("Weird looking animals with long legs as digital art")


class MinimalismDigitalArt(DigitalArt):
    def display(self) -> None:
        print("Single object in the middle of the screen as digital art")


#### Factories ####
class PainterFactory:
    def draw_digital(self) -> DigitalArt:
        pass

    def draw_physical(self) -> PhysicalArt:
        pass


class SurrealismPainterFactory(PainterFactory):
    def draw_digital(self) -> SurrealDigitalArt:
        return SurrealDigitalArt()

    def draw_physical(self) -> SurrealPhysicalArt:
        return SurrealPhysicalArt()


class MinimalismPainterFactory(PainterFactory):
    def draw_digital(self) -> MinimalismDigitalArt:
        return MinimalismDigitalArt()

    def draw_physical(self) -> MinimalismPhysicalArt:
        return MinimalismPhysicalArt()


#### Application ####
class Website:
    def __init__(self, painter: PainterFactory):
        self.painter = painter

    def submit_order(self, order_type: OrderType) -> None:
        if order_type == OrderType.DIGITAL_ORDER:
            art_piece = self.painter.draw_digital()
        elif order_type == OrderType.PAINTING_ORDER:
            art_piece = self.painter.draw_physical()
        else:
            raise UnknownPaintingStyle("Not a valid order type")

        art_piece.display()


if __name__ == "__main__":
    print("# User opens the page for Surrealism category")
    factory = SurrealismPainterFactory()
    website = Website(factory)
    website.submit_order(OrderType.PAINTING_ORDER)
    website.submit_order(OrderType.DIGITAL_ORDER)

    print()
    print("# User opens the page for Minimalism category")
    factory = MinimalismPainterFactory()
    website = Website(factory)
    website.submit_order(OrderType.PAINTING_ORDER)
    website.submit_order(OrderType.DIGITAL_ORDER)
