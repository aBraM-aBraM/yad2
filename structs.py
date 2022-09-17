import dataclasses


@dataclasses.dataclass
class Details:
    title: str
    area: str
    price: str


@dataclasses.dataclass
class Product:
    details: Details
    phone: str
