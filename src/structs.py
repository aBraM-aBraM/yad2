import dataclasses
import os


@dataclasses.dataclass
class Details:
    title: str
    price: int
    link: str
    area: str

    def __repr__(self):
        return os.linesep.join([self.title, str(self.price), self.link, self.area])
