from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    name: str = None

    @property
    def aa(self):
        return 2

    def __getitem__(self, item):
        return getattr(self, item, None)

d = Data(None)
c = Data()
print(vars(d))
print(c)
