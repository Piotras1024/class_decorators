import functools
import inspect

from auto_repr import auto_repr
from location import Location
from location import hong_kong, stockholm, cape_town, rotterdam, maracaibo


def postcondition(predicate):               #predicate is a function that return False or True and builds a decrator around it

    def function_decorator(f):

        @functools.wraps(f)                 #funkcja f to funckja pod którą znajduje się decorator.
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            if not predicate(self):
                raise RuntimeError(
                    f"Post-condition {predicate.__name__} not "
                    f"maintained for {self!r}"
                )
            return result

        return wrapper

    return function_decorator


def invariant(predicate):
    function_decorator = postcondition(predicate)

    def class_decorator(cls):
        members = list(vars(cls).items())       #w decorator_class(auto_repr) bez list, why ??
        for name, member in members:
            if inspect.isfunction(member):
                decorated_member = function_decorator(member)
                setattr(cls, name, decorated_member)
        return cls

    return class_decorator


def at_least_two_locations(itinerary):
    return len(itinerary._locations) >= 2               #dlaczego _locations a nie locations ???!!!
                                                        #to to znaczy protectem member _locations of class co to chroni


def no_duplicates(itinerary):
    already_seen = set()
    for location in itinerary._locations:
        if location in already_seen:
            return False
        already_seen.add(location)
    return True


@auto_repr
@invariant(no_duplicates)
@invariant(at_least_two_locations)
class Itinerary:

    @classmethod
    def from_locations(cls, *locations):
        return cls(locations)

    # @postcondition(at_least_two_locations)
    def __init__(self, locations):
        self._locations = list(locations)

    def __str__(self):
        return "\n".join(location.name for location in self._locations)

    @property
    def locations(self):
        return tuple(self._locations)

    @property
    def origin(self):
        return self._locations[0]

    @property
    def destination(self):
        return self._locations[-1]

    # @postcondition(at_least_two_locations)
    def add(self, location):
        self._locations.append(location)

    # @postcondition(at_least_two_locations)
    def remove(self, name):
        removal_indexes = [
            index for index, location in enumerate(self._locations)
            if location.name == name
        ]
        for index in reversed(removal_indexes):
            del self._locations[index]

    # @postcondition(at_least_two_locations)
    def truncate_at(self, name):
        stop = None
        for index, location in enumerate(self._locations):
            if location.name == name:
                stop = index + 1

        self._locations = self._locations[:stop]
