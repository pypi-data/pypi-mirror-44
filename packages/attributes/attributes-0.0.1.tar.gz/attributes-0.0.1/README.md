# attributes

a python version attribute like attribute of csharp.

## Usage

``` py
from attributes import Attribute

class Data(Attribute): # make your own attribute
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

@Data(1, 2) # use your attribute
class SomeClass:
    pass

data, = Attribute.get_attrs(SomeClass) # than load on runtime and use it.
```
