"""
A painter learned how to make digital art and how to paint physical paintings.
He now wants to sell his artwork on his personal website.

The clients will enter the website and send an order request for one painting style
and the painter will draw it for them.

For the physical paintings, the client can choose to order the painting with or without
a frame.
"""
import abc
import typing as t
import enum


class UnknownPaintingStyle(Exception):
    pass


class OrderType(enum.Enum):
    UNFRAMED_PAINTING_ORDER = enum.auto()
    FRAMED_PAINTING_ORDER = enum.auto()
    DIGITAL_ORDER = enum.auto()
    POTTERY_ORDER = enum.auto()


class Frame(abc.ABC):
    @abc.abstractmethod
    def hold(self, painting: t.Any) -> t.Any:
        pass


class ArtPiece(abc.ABC):
    @abc.abstractmethod
    def display(self) -> None:
        pass


class StringFrame(Frame):
    def hold(self, painting: str) -> str:
        top_bot_frame = "-" * (len(painting) + 4)
        return "{top}\n| {painting} |\n{bottom}".format(
            top=top_bot_frame, painting=painting, bottom=top_bot_frame
        )


class DigitalArt(ArtPiece):
    def display(self) -> None:
        print("Beautiful digital art")


class PaintedArt(ArtPiece):
    def __init__(self, frame: Frame = None):
        self.frame = frame

    def display(self) -> None:
        painting = "Beautiful painting"
        print(self.frame.hold(painting) if self.frame else painting)


class Painter:
    def draw(self, order_type: OrderType) -> ArtPiece:
        if order_type == OrderType.FRAMED_PAINTING_ORDER:
            frame = StringFrame()
            return PaintedArt(frame=frame)
        elif order_type == OrderType.UNFRAMED_PAINTING_ORDER:
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

    def submit_order(self, order: OrderType) -> None:
        art_piece = self.painter.draw(order)
        art_piece.display()


if __name__ == "__main__":
    website = PaintersWebsite()
    website.submit_order(OrderType.DIGITAL_ORDER)
    website.submit_order(OrderType.UNFRAMED_PAINTING_ORDER)
    website.submit_order(OrderType.FRAMED_PAINTING_ORDER)

    try:
        website.submit_order(OrderType.POTTERY_ORDER)
    except UnknownPaintingStyle as e:
        print(str(e))  # This is handled like this just to make the output prettier
