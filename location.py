# from auto_repr import auto_repr
from dataclasses import dataclass
from position import Position, EarthPosition
# @auto_repr


@dataclass(eq=True, frozen=True)
class Location:
    name: str
    position: Position

    def __post_init__(self):
        if self.name == "":
            raise ValueError("location name cannot be empty")

    # def __init__(self, name, position):
    #     self._name = name
    #     self._position = position
    #
    # @property
    # def name(self):
    #     return self._name
    #
    # @property
    # def position(self):
    #     return self._position
    #
    # def __str__(self):
    #     return self.name
    
'''
e = Location("Paris", EarthPosition(48.8, 2.3))
f = Location("Paris", EarthPosition(48.8, 2.3))
e == f
False

a = hong_kong
b = hong_kong
a is b
True

dlaczego krzako ?

'''
hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(59.33, 18.06))
cape_town = Location("Cape Town", EarthPosition(-33.93, 18.42))
rotterdam = Location("Rotterdam", EarthPosition(51.96, 4.47))
maracaibo = Location("Maracaibo", EarthPosition(10.65, -71.65))
