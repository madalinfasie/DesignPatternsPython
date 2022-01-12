"""
The technology advanced so much until year 2079 that
cloning inanimate objects is now possible.

A new restaurant tries to make a profit by cloning its dishes
instead of recreating them each time.

The restaurant has a menu that makes it easier for customers
to make their order
"""
import abc
import typing as t


class DishPrototype(abc.ABC):
    def clone(self) -> 'DishPrototype':
        pass


class Menu:
    """ Acts as a prototype registry """
    def __init__(self):
        self.items: t.Dict[str, DishPrototype] = {}

    def add(self, name: str, dish: DishPrototype) -> None:
        self.items[name] = dish

    def remove(self, name: str) -> None:
        if name in self.items:
            self.items.pop(name)

    def get_by_name(self, name: str) -> DishPrototype:
        return self.items[name].clone()

    def get_by_ingredient(self, ingredient: str) -> DishPrototype:
        for dish in self.items.values():
            if ingredient in dish.ingredients:
                return dish.clone()


class PizzaProsciuttoFunghi(DishPrototype):
    def __init__(self, size: int, extra_mozzarella: bool = False):
        self.size = size
        self.extra_mozzarella = extra_mozzarella
        self.ingredients = ['mozzarella', 'prosciutto', 'mushrooms']

    def plate(self) -> None:
        text = f'Serving a pizza prosciutto e fungi of size {self.size}'
        if self.extra_mozzarella:
            text += ' with extra mozzarella'

        print(text)

    def _clone(self, prototype: DishPrototype) -> DishPrototype:
        clone = PizzaProsciuttoFunghi(size=prototype.size)
        clone.extra_mozzarella = prototype.extra_mozzarella
        clone.ingredients = prototype.ingredients
        return clone

    def clone(self) -> DishPrototype:
        return self._clone(self)


class SpaghettiCarbonara(DishPrototype):
    def __init__(self, weight: int = 300, extra_parmigiano: bool = False):
        self.weight = weight
        self.extra_parmigiano = extra_parmigiano
        self.ingredients = ['spaghetti', 'egg', 'pancetta']

    def plate(self) -> None:
        text = f'Serving a spagetti carbonara {self.weight}g'
        if self.extra_parmigiano:
            text += ' with extra parmigiano'

        print(text)

    def _clone(self, prototype: DishPrototype) -> DishPrototype:
        clone = SpaghettiCarbonara(
            weight=self.weight,
            extra_parmigiano=self.extra_parmigiano)
        clone.ingredients = prototype.ingredients
        return clone

    def clone(self) -> DishPrototype:
        return self._clone(self)


class Restaurant:
    def __init__(self):
        self.order = []
        self.menu = Menu()

    def build_menu(self) -> None:
        pizza = PizzaProsciuttoFunghi(size=32, extra_mozzarella=True)
        spaghetti = SpaghettiCarbonara(weight=400)

        self.menu.add('Prosciutto e Funghi', pizza)
        self.menu.add('Spaghetti Carbonara', spaghetti)

    def build_order(self) -> None:
        self.order.append(self.menu.get_by_name('Prosciutto e Funghi'))
        self.order.append(self.menu.get_by_name('Spaghetti Carbonara'))
        self.order.append(self.menu.get_by_ingredient('mozzarella'))

    def serve(self) -> None:
        for dish in self.order:
            dish.plate()

        self.order = []


if __name__ == '__main__':
    restaurant = Restaurant()
    restaurant.build_menu()
    restaurant.build_order()
    restaurant.serve()