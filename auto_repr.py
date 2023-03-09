import inspect

from utility import typename


def auto_repr(cls):
    members = vars(cls)
        
    if "__repr__" in members:
        raise TypeError(f"{cls.__name__} already defines __repr__")
        
    if "__init__" not in members:
        raise TypeError(f"{cls.__name__} does not override __init__")
        
    sig = inspect.signature(cls.__init__)
    parameter_names = list(sig.parameters)[1:]          #0 parametr = first parametr is not needed, because it is self
       
    if not all(
        isinstance(members.get(name, None), property)
        for name in parameter_names
    ):
        raise TypeError(
            f"Cannot apply auto_repr to {cls.__name__} because not all "
            "__init__ parameters have matching properties"
        )
    
    def synthesized_repr(self):
        return "{typename}({args})".format(
            typename=typename(self),
            args=", ".join(
                "{name}={value!r}".format(
                    name=name,
                    value=getattr(self, name)
                ) for name in parameter_names
            )
        )
    
    setattr(cls, "__repr__", synthesized_repr)          #"__repr__" to atrybut klasy i metoda jednocześnie
    
    return cls
