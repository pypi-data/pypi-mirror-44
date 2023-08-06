# Python Counter Dictionary

e.g.)

```
>>> from pycountdict import CounterDictionary
>>> cd = CounterDictionary()
>>> cd['a'] = 1
>>> print(cd)
a: 1
>>> cd['b'] = 1
>>> print(cd)
a: 1, b: 1
>>> cd['A'] = 1
>>> print(cd)
a: 1, A: 1, b: 1
>>> cd['a'] = 1
>>> print(cd)
a: 2, A: 1, b: 1
```
