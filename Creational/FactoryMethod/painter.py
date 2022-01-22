"""
A painter learned how to make digital art and how to paint physical paintings.
He now wants to sell his artwork on his personal website.

The clients will enter the website and send an order request for one painting style
and the painter will draw it for them.
"""
import abc
import enum


class UnknownPaintingStyle(Exception):
    pass


class OrderType(enum.Enum):
    PAINTING_ORDER = enum.auto()
    DIGITAL_ORDER = enum.auto()
    POTTERY_ORDER = enum.auto()


class ArtPiece(abc.ABC):
    @abc.abstractmethod
    def display(self) -> None:
        pass


class DigitalArt(ArtPiece):
    def display(self) -> None:
        print("Beautiful digital art")


class PaintedArt(ArtPiece):
    def display(self) -> None:
        print("Beautiful painting in a frame")


class Painter:
    def draw(self, order_type: OrderType) -> ArtPiece:
        """The factory method for creating an ArtPiece based on an OrderType"""
        if order_type == OrderType.PAINTING_ORDER:
            return PaintedArt()
        elif order_type == OrderType.DIGITAL_ORDER:
            return DigitalArt()
        else:
            raise UnknownPaintingStyle(
                f"The painter does not master this art style {order_type.name}"
            )


class PaintersWebsite:
    def __init__(self):
        self.painter = Painter()

    def submit_order(self, order):
        art_piece = self.painter.draw(order)
        art_piece.display()


if __name__ == "__main__":
    website = PaintersWebsite()
    website.submit_order(OrderType.DIGITAL_ORDER)
    website.submit_order(OrderType.PAINTING_ORDER)

    try:
        website.submit_order(OrderType.POTTERY_ORDER)
    except UnknownPaintingStyle as e:
        print(str(e))  # This is handled like this just to make the output prettier
