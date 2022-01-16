"""
A graphic designer knows how to make digital art and how to
send it to the manager for approval via email.
A painter gets hired to the same company, but he can only
paint on canvas and show the result physically.

The Company wants to start a new ad campaign and both the graphic designer
and the painter have been asked to come up with ideas.
The company has some standard procedures in place to validate each idea
so it only accepts paintings in digital form via email.
"""
import abc


class WrongSubmissionType(Exception):
    pass


class Artwork(abc.ABC):
    """ This class (and its children) is not part of the pattern.

    Its purpose is to show how to handle different return types from
    the adapter and the adaptee
    """
    def __init__(self, message: str):
        self.message = message


class CompanyDesigner(abc.ABC):
    @abc.abstractmethod
    def draw(self) -> None:
        pass

    @abc.abstractmethod
    def send_email(self) -> Artwork:
        pass


class DigitalArt(Artwork):
    pass


class PaintingArt(Artwork):
    pass


class Painter:
    """ The painter knows how to draw PaintingArt
    and shows the results in person.

    This class can be seen as an external module that
    we cannot control.
    """
    def __init__(self):
        self.painting = None

    def draw(self) -> None:
        self.painting = PaintingArt('Strong message on canvas')

    def show_results(self) -> PaintingArt:
        return self.painting


class GraphicDesigner(CompanyDesigner):
    """ This acts as our class upon which all the other
    functionalities are based on.
    """
    def __init__(self):
        self.digital = None

    def draw(self) -> None:
        self.digital = DigitalArt('Motivational message in digital form')

    def send_email(self) -> DigitalArt:
        return self.digital


class PainterAdapter(CompanyDesigner):
    def __init__(self, painter: Painter):
        self.painter = painter
        self.digital = None

    def draw(self) -> None:
        """ Make the painter draw the pucture and extract the results
        into a DigitalArt object.

        This method shows how an adapter can handle different return types
        of the adaptee.
        """
        self.painter.draw()
        painting = self.painter.show_results()
        # Take a photo of the painting to make it digital
        self.digital = DigitalArt(painting.message)

    def send_email(self) -> DigitalArt:
        """ This method is named to match the CompanyDesigner interface.

        This method is meant to show how the adapter can handle
        different method names in the interface.

        It is also possible to combine multiple methods from painter
        into only one method inside the adapter if such case is needed.
        """
        return self.digital


class Company:
    def ask_for_submission(self, artist: CompanyDesigner) -> Artwork:
        artist.draw()
        return artist.send_email()

    def check_submission(self, submission: Artwork) -> None:
        if not isinstance(submission, DigitalArt):
            raise WrongSubmissionType('Wrong submission type! Only digital arts are accepted')

        print(f'Amazing art about: {submission.message}')


if __name__ == '__main__':
    painter = Painter()
    graphic_designer = GraphicDesigner()

    company = Company()

    # Graphic designer submission
    designer_submission = company.ask_for_submission(graphic_designer)
    company.check_submission(designer_submission)

    # Painter adapter submission
    painter_adapter = PainterAdapter(painter)
    painter_adapter_submission = company.ask_for_submission(painter_adapter)
    company.check_submission(painter_adapter_submission)

    # Wrong painter submissions
    try:
        # This will fail to run (no send_email method)
        painter_submission = company.ask_for_submission(painter)
        company.check_submission(painter_submission)
    except AttributeError as e:
        print(f'[FAILED] {e}')

    try:
        # This will raise Wrong submission type
        painting = painter.show_results()
        company.check_submission(painting)
    except WrongSubmissionType as e:
        print(f'[FAILED] {e}')