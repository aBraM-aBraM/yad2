import dataclasses
import os


@dataclasses.dataclass
class Details:
    title: str
    area: str
    price: str

    def __repr__(self):
        return os.linesep.join([self.title, self.area, self.price])


@dataclasses.dataclass
class Product:
    details: Details
    phone: str

    def __repr__(self):
        return os.linesep.join([self.details.__repr__(), self.phone])
