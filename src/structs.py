import dataclasses
import os
import hashlib


@dataclasses.dataclass
class Details:
    title: str
    price: int
    link: str
    picture: str
    area: str
    _id: str
    sent: bool

    def __init__(self, title: str, price: int, link: str, picture: str, area: str):
        self.title = title
        self.price = price
        self.link = link
        self.picture = picture
        self.area = area
        self._id = hashlib.md5("\n".join(self.__repr__().strip().splitlines()).encode()).hexdigest()
        self.sent = False

    def __repr__(self):
        return os.linesep.join([self.title, str(self.price), self.area])

    @property
    def item_id(self):
        return self._id
