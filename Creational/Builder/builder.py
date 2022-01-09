"""
The pandemic is over and with it all the travel restrictions.

A tourist agency is ready to offer a wide range of travel plans to everyone.
The agency offers a set of traveling options and for an aditional price, they can also
provide a blog post with all the travel details.

The program will have two builders: the travel plan builder and the travel blog builder.
The agency will act as the director, building some predefined offers.
"""
import abc
from datetime import datetime


class TravelDetails:
    def __init__(self):
        self.destination: str = None
        self.depart_date: datetime = None
        self.return_date: datetime = None
        self.accomodation: str = None

    def __str__(self) -> str:
        return ', '.join([
            self.destination or '',
            self.depart_date.strftime('%Y-%m-%d %H:%M') or '',
            self.return_date.strftime('%Y-%m-%d %H:%M') or '',
            self.accomodation or ''
        ])


class TravelBlogPost:
    def __init__(self):
        self.destination: str = None
        self.depart_date: str = None
        self.return_date: str = None
        self.accomodation: str = None

    def article(self) -> str:
        return '.\n'.join([
            self.destination or '',
            self.depart_date or '',
            self.return_date or '',
            self.accomodation or ''
        ])


class TravelBuilder(abc.ABC):
    def build_destination(self, destination: str) -> None:
        pass

    def build_flight(self, depart_date: datetime, return_date: datetime) -> None:
        pass

    def build_accomodation(self, hotel_name: str, street: str, number: int) -> None:
        pass

    def reset(self) -> None:
        pass


class TravelPlanBuilder(TravelBuilder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._travel = TravelDetails()

    def build_destination(self, destination: str) -> None:
        self._travel.destination = destination

    def build_flight(self, depart_date: datetime, return_date: datetime) -> None:
        self._travel.depart_date = depart_date
        self._travel.return_date = return_date

    def build_accomodation(self, hotel_name: str, street: str, number: int) -> None:
        address = f'{hotel_name} - Str. {street} No. {number}'
        self._travel.accomodation = address

    def get_result(self) -> TravelDetails:
        travel = self._travel
        self.reset()
        return travel


class TravelBlogBuilder(TravelBuilder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._travel_post = TravelBlogPost()

    def build_destination(self, destination: str) -> None:
        self._travel_post.destination = f'An adventure in {destination}'

    def build_flight(self, depart_date: datetime, return_date: datetime) -> None:
        formatted_depart = depart_date.strftime('%A %d %B %H:%M')
        formatted_return = return_date.strftime('%A %d %B %H:%M')
        self._travel_post.depart_date = f'The departure was on {formatted_depart}'
        self._travel_post.return_date = f'No matter how much we loved it, we had to go back on {formatted_return}'

    def build_accomodation(self, hotel_name: str, street: str, number: int) -> None:
        self._travel_post.accomodation = f'We had an amazing stay at {hotel_name} ' \
            f'located on {street} street number {number}'

    def get_result(self) -> TravelBlogPost:
        travel_post = self._travel_post
        self.reset()
        return travel_post


class TravelAgency:
    def travel_to_budapest_in_summer(self, builder: TravelBuilder) -> None:
        builder.reset()
        builder.build_destination('Budapest')
        builder.build_flight(
            depart_date=datetime(2022, 7, 2, 5, 10),
            return_date=datetime(2022, 7, 7, 7, 0)
        )
        builder.build_accomodation(hotel_name='Ibis', street='Szalloda', number=41)

    def travel_to_athens(self, builder: TravelBuilder) -> None:
        builder.reset()
        builder.build_destination('Athens')
        builder.build_flight(
            depart_date=datetime(2022, 2, 2, 12, 30),
            return_date=datetime(2022, 2, 5, 3, 15)
        )


if __name__ == '__main__':
    agency = TravelAgency()

    # Travel to Budapest
    travel_builder = TravelPlanBuilder()
    agency.travel_to_budapest_in_summer(travel_builder)
    travel = travel_builder.get_result()

    blog_builder = TravelBlogBuilder()
    agency.travel_to_budapest_in_summer(blog_builder)
    travel_blog = blog_builder.get_result()

    print('Travel details:', travel)
    print('Travel blog:', travel_blog.article())

    # Travel to Athens
    agency.travel_to_athens(travel_builder)
    travel = travel_builder.get_result()

    agency.travel_to_athens(blog_builder)
    travel_blog = blog_builder.get_result()

    print('Travel details:', travel)
    print('Travel blog:', travel_blog.article())
