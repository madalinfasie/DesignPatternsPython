"""
The technology advanced so much until year 2079 that
cloning inanimate objects is now possible.

A new restaurant tries to make a profit by cloning its dishes
instead of recreating them each time.
"""
import abc


class DishPrototype(abc.ABC):
    def clone(self) -> 'DishPrototype':
        pass


class PizzaProsciuttoFunghi(DishPrototype):
    def __init__(self, prototype: DishPrototype = None):
        self.size: int = None
        self.extra_mozzarella: bool = False

        if prototype:
            self.size = prototype.size
            self.extra_mozzarella = prototype.extra_mozzarella

    def plate(self) -> None:
        text = f'Serving a pizza prosciutto e fungi of size {self.size}'
        if self.extra_mozzarella:
            text += ' with extra mozzarella'

        print(text)

    def clone(self) -> DishPrototype:
        return PizzaProsciuttoFunghi(self)


class SpaghettiCarbonara(DishPrototype):
    def __init__(self, weight: int = 300, extra_parmigiano: bool = False):
        self.weight = weight
        self.extra_parmigiano = extra_parmigiano

    def plate(self) -> None:
        text = f'Serving a spagetti carbonara {self.weight}g'
        if self.extra_parmigiano:
            text += ' with extra parmigiano'

        print(text)

    def clone(self) -> DishPrototype:
        return SpaghettiCarbonara(
            weight=self.weight,
            extra_parmigiano=self.extra_parmigiano)


class Restaurant:
    def __init__(self):
        self.order = []

    def build_order(self) -> None:
        pizza = PizzaProsciuttoFunghi()
        pizza.size = 32
        pizza.extra_mozzarella = True

        self.order.append(pizza)
        self.order.append(pizza.clone())

        spaghetti = SpaghettiCarbonara(weight=400)
        self.order.append(spaghetti)
        self.order.append(spaghetti.clone())

    def serve(self) -> None:
        for dish in self.order:
            dish.plate()

        self.order = []


if __name__ == '__main__':
    restaurant = Restaurant()
    restaurant.build_order()
    restaurant.serve()