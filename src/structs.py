import dataclasses
import os


@dataclasses.dataclass
class Details:
    LINK_INDEX = 2

    title: str
    price: int
    link: str
    area: str
    picture: str

    def __repr__(self):
        return os.linesep.join([self.title, str(self.price), self.link, self.area])

    def __hash__(self):
        return hash(os.linesep.join([str(self.__dict__[key]) for key in self.__dict__]))
